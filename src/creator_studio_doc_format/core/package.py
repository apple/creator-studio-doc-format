# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0

"""Document packages, and the class that reads and writes them.

A package is the container a document lives in. Keynote Interchange Format stores a
package as a ZIP archive, the ``.keyx`` file, and that's the only form this library
reads and writes. The archive holds these entries:

- ``main.json``: the payload, which is the document's root model, such as a
  presentation.
- ``manifest.json``: the manifest, which declares the package version.
- ``presets.json``: the presets that objects in the payload adopt.
- ``Data/``: the resources that the payload refers to, in one flat directory.

``Package`` keeps each entry in its own attribute: ``payload``, ``manifest``,
``presets``, and ``resources``. ``PayloadT`` names the payload's type, and
``KeyxDocument`` fixes it to ``Presentation``. Each preset's properties stay raw JSON
rather than models.
"""

from __future__ import annotations

import errno
import json
import lzma
import os
import stat
import sys
import unicodedata
import zipfile
import zlib
from collections.abc import (
    Callable,
    Generator,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
)
from contextlib import contextmanager
from types import TracebackType
from typing import Any, BinaryIO, ClassVar, Generic, Protocol, TypeVar, cast

from pydantic import ValidationError
from pydantic_core import PydanticSerializationError

from ._errors import (
    DocumentPackageError,
    DocumentPackageErrorKind,
    DocumentVersionError,
)
from ._preset import Preset, PresetRegistry
from ._wire import ObjectModel, Version

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

# The major version of the package format this library reads and writes. Saving always
# writes it with minor 0, and a package with a newer major is rejected on open.
SUPPORTED_PACKAGE_MAJOR = 1


@contextmanager
def _catching_zip_errors(hint: str = "") -> Generator[None, None, None]:
    try:
        yield
    except (
        zipfile.BadZipFile,
        zlib.error,
        lzma.LZMAError,
        NotImplementedError,
    ) as exc:
        raise DocumentPackageError(
            DocumentPackageErrorKind.MALFORMED_ARCHIVE, f"{exc}{hint}"
        ) from exc
    except RuntimeError as exc:
        msg = str(exc).lower()
        if "encrypt" in msg or "password" in msg:
            raise DocumentPackageError(
                DocumentPackageErrorKind.MALFORMED_ARCHIVE, f"{exc}{hint}"
            ) from exc
        raise
    except OSError as exc:
        # `zipfile` and bz2 report an error in the format, such as "Invalid data stream"
        # or a truncated end of central directory record, as a bare `OSError` with no
        # `errno`. A file system `OSError`, such as `EIO`, `ENOENT`, `EACCES`, or
        # `ENOSPC`, always carries an `errno`. The operator can act on that error, so it
        # must not be relabeled as corruption.
        if exc.errno is None:
            raise DocumentPackageError(
                DocumentPackageErrorKind.MALFORMED_ARCHIVE, f"{exc}{hint}"
            ) from exc
        raise


def _rezip_hint(names: Iterable[str], prefix: str) -> str:
    evidence = []
    if prefix:
        evidence.append(f"entries live under {prefix!r}, not at the archive root")
    if any(n.startswith(_MACOSX_PREFIX) for n in names):
        evidence.append("__MACOSX sidecars present")
    if not evidence:
        return ""
    return f" (archive was re-zipped: {' and '.join(evidence)})"


def _coerce_version_str(raw: Any) -> str | None:
    if raw is None or isinstance(raw, bool):
        return None
    if isinstance(raw, str):
        return raw
    if isinstance(raw, (int, float)):
        return str(raw)
    if isinstance(raw, dict):
        found = Version.parse(raw)
        return str(found) if found is not None else None
    return None


class Manifest:
    """The package manifest, which records the version of the package format.

    Saving writes the package format version this library supports, whatever
    ``package_version`` holds, so the attribute reports the version that was read, and a
    round trip doesn't preserve it.

    Args:
        package_version: The package format version, in ``major.minor`` form.

    Raises:
        ValueError: ``package_version`` has a newer major version than this library
            supports.
    """

    __slots__ = ("package_version",)

    def __init__(self, package_version: str | None = None) -> None:
        if package_version is not None:
            found = Version.parse(package_version)
            if found is not None and found.major > SUPPORTED_PACKAGE_MAJOR:
                raise ValueError(
                    f"`package_version` {package_version!r} (major {found.major}) exceeds "
                    f"supported major {SUPPORTED_PACKAGE_MAJOR}"
                )
        self.package_version = package_version

    @classmethod
    def parse(cls, data: object) -> Manifest:
        """Creates a manifest from the decoded contents of a manifest file.

        ``parse`` reads a ``package_version`` written as a JSON number, such as ``1.0``,
        or as a ``{"major": ..., "minor": ...}`` object as the ``"major.minor"`` string
        it spells, and checks it the same way.

        Args:
            data: The decoded ``manifest.json`` value, which can be ``None`` or
                malformed.

        Returns:
            Manifest: The parsed manifest, or a default one when ``data`` is missing, is
            malformed, or has no ``package_version``.

        Raises:
            DocumentVersionError: the ``package_version`` in ``data`` has a newer major
                version than this library supports.
        """
        if not isinstance(data, dict):
            return cls()
        version = _coerce_version_str(data.get("package_version"))
        try:
            return cls(version)
        except ValueError as exc:
            raise DocumentVersionError(
                f"{exc}. Update this library to a newer version to read it.",
            ) from exc

    def to_dict(self) -> dict[str, str]:
        """Returns the manifest in the form that the manifest file stores.

        Returns:
            dict[str, str]: The ``manifest.json`` object, with the package format
            version that this library writes.
        """
        return {"package_version": f"{SUPPORTED_PACKAGE_MAJOR}.0"}


def _ascii_skeleton(name: str) -> str:
    return "".join(c for c in name if ord(c) < 128)


def _is_valid_flat_name(name: str) -> bool:
    return bool(
        name
        and name not in (".", "..")
        and "/" not in name
        and "\\" not in name
        and not os.path.isabs(name)
    )


def _validate_resource_filename(name: str) -> None:
    if not isinstance(name, str) or not _is_valid_flat_name(name):
        raise ValueError(
            f"invalid resource filename {name!r}: expected a flat filename "
            "(nonempty, no '/', '\\', or '..')"
        )


class _ResourceKeyError(KeyError):
    def __str__(self) -> str:
        message: str = self.args[0]
        return message


class ResourceStore(MutableMapping[str, bytes]):
    r"""The package's resources, as a map from filename to bytes.

    Saving writes exactly these entries to ``Data/``. A resource that the JSON embeds,
    such as a ``Base64EncodedResource``, is never in the store. Any method that adds a
    key raises ``ValueError`` unless the key is a flat filename: nonempty, not ``.`` or
    ``..``, and without ``/`` or ``\``.

    A store from ``Package.open_lazy`` knows every name up front but reads each resource
    from the archive on first access, so ``len``, iteration, and ``in`` read nothing.
    Reading isn't safe across threads.

    Args:
        initial: The resources to start with, as a map from filename to bytes.

    Keys match exactly, as in any mapping, so storing under a name that's taken replaces
    that resource. ``unique_filename`` picks a free name instead:

    >>> from creator_studio_doc_format.core import ResourceStore
    >>> store = ResourceStore({"logo.png": b"old"})
    >>> name = store.unique_filename("logo.png")
    >>> store[name] = b"new"
    >>> sorted(store)
    ['logo 2.png', 'logo.png']

    The payload refers to a file from an ``IndirectResource``, by its ``identifier`` or,
    when that's absent, its ``filename``. That name's spelling can differ from the
    key's, such as a name that a zip tool stored decomposed. Indexing and ``in`` miss
    it, and ``can_resolve`` and ``bytes_for`` find it:

    >>> import unicodedata
    >>> store = ResourceStore({unicodedata.normalize("NFD", "café.png"): b"png bytes"})
    >>> "café.png" in store
    False
    >>> store.bytes_for("café.png")
    b'png bytes'
    """

    def __init__(self, initial: Mapping[str, bytes] | None = None) -> None:
        self._backend: _ResourceBackend | None = None
        self._backend_keys: frozenset[str] = frozenset()
        self._nfc_index: tuple[frozenset[str], dict[str, str]] | None = None
        self._data: dict[str, bytes] = {}
        self._tombstones: set[str] = set()
        if isinstance(initial, ResourceStore) and initial._backend is not None:
            self._backend = initial._backend
            self._backend_keys = initial._backend_keys
            self._data = dict(initial._data)
            self._tombstones = set(initial._tombstones)
            initial._backend = None
            initial._backend_keys = frozenset()
            initial._tombstones = set()
            return
        if initial:
            for key, value in initial.items():
                self[key] = value

    @classmethod
    def _lazy(cls, backend: _ResourceBackend) -> ResourceStore:
        store = cls()
        store._backend = backend
        store._backend_keys = frozenset(backend.names())
        return store

    def _effective_keys(self) -> frozenset[str]:
        return (self._backend_keys - self._tombstones) | set(self._data)

    def __getitem__(self, key: str) -> bytes:
        if key in self._data:
            return self._data[key]
        if (
            self._backend is not None
            and key in self._backend_keys
            and key not in self._tombstones
        ):
            data = self._backend.read(key)
            self._data[key] = data
            return data
        raise KeyError(key)

    def __setitem__(self, key: str, value: bytes) -> None:
        _validate_resource_filename(key)
        self._data[key] = value
        self._tombstones.discard(key)

    def __delitem__(self, key: str) -> None:
        # A key can be a backend key and also cached in the overlay, so deletion
        # tombstones it and drops it from the overlay independently. Unless both go, a
        # later read resurrects the key and `clear` or `popitem` never converges.
        present = False
        if key in self._data:
            del self._data[key]
            present = True
        if key in self._backend_keys and key not in self._tombstones:
            self._tombstones.add(key)
            present = True
        if not present:
            raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        return iter(self._effective_keys())

    def __len__(self) -> int:
        return len(self._effective_keys())

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False
        return (
            key in self._backend_keys and key not in self._tombstones
        ) or key in self._data

    def close(self) -> None:
        """Releases the backing archive and keeps only the resources already read.

        Calling ``close`` again does nothing, and so does calling it on a store that
        isn't lazy.
        """
        if self._backend is not None:
            self._backend.close()
            self._backend = None
            self._backend_keys = frozenset()
            self._tombstones = set()

    def _resolve_key(self, identifier: str) -> str | None:
        keys = self._effective_keys()
        if identifier in keys:
            return identifier
        if self._nfc_index is None or self._nfc_index[0] != keys:
            index: dict[str, str] = {}
            for k in sorted(keys):
                index.setdefault(unicodedata.normalize("NFC", k), k)
            self._nfc_index = (keys, index)
        if (
            key := self._nfc_index[1].get(unicodedata.normalize("NFC", identifier))
        ) is not None:
            return key
        target = _ascii_skeleton(identifier)
        matches = [k for k in keys if _ascii_skeleton(k) == target]
        return matches[0] if len(matches) == 1 else None

    def bytes_for(self, identifier: str) -> bytes:
        """Returns the bytes for an indirect resource's identifier or filename.

        Matching tries these in order:

        - The exact key.
        - A canonically equivalent key, so NFC and NFD spellings match.
        - The only key with the same ASCII characters as the identifier, which tolerates
          mojibake in zip names.

        The ASCII match can return a different file: ``é.png`` resolves to ``è.png``
        when that's the only key with the same ASCII characters. The resource check in
        ``Package.save`` accepts the same match.

        Args:
            identifier: An indirect resource's ``identifier`` or ``filename``.

        Returns:
            bytes: The bytes of the first key that matches.

        Raises:
            KeyError: no key matches, or the ASCII match is ambiguous.
            DocumentPackageError: a lazy store reads a corrupt member.
        """  # noqa: DOC502, DOC503 -- `_ResourceKeyError` is the `KeyError`, and the lazy read raises `DocumentPackageError`
        key = self._resolve_key(identifier)
        if key is None:
            raise _ResourceKeyError(
                f"no Data/ bytes for indirect resource {identifier!r}"
            )
        return self[key]

    def can_resolve(self, identifier: str) -> bool:
        """Returns a Boolean value that indicates whether a resource matches a name.

        ``can_resolve`` matches names the way ``bytes_for`` does, and never reads bytes.

        Args:
            identifier: An indirect resource's ``identifier`` or ``filename``.

        Returns:
            bool: ``True`` if ``bytes_for`` finds a resource for ``identifier``, or
            ``False`` if it doesn't.
        """
        return self._resolve_key(identifier) is not None

    def unique_filename(self, preferred: str) -> str:
        """Returns a filename that no resource uses, based on a preferred name.

        Reading and saving never rename a resource, so this is only for a caller adding
        one. The number goes before the last ``.``, so ``a.tar.gz`` becomes
        ``a.tar 2.gz`` and ``.hidden`` becomes ``" 2.hidden"``.

        Args:
            preferred: The filename to use if no entry has it.

        Returns:
            str: ``preferred`` if no entry has it, or else the first free numbered
            variant, such as ``name 2.ext``.
        """
        keys = self._effective_keys()
        if preferred not in keys:
            return preferred
        stem, dot, ext = preferred.rpartition(".")
        base = stem if dot else preferred
        suffix = f".{ext}" if dot else ""
        n = 2
        while f"{base} {n}{suffix}" in keys:
            n += 1
        return f"{base} {n}{suffix}"


#: The type of a package's payload, the document's root model. It's bound to
#: `ObjectModel`.
PayloadT = TypeVar("PayloadT", bound=ObjectModel)

_MAIN = "main.json"
_MANIFEST = "manifest.json"
_PRESETS = "presets.json"
_DATA = "Data"
_DATA_PREFIX = _DATA + "/"
_INDIRECT_TYPE_ID = "com.apple.apps.content-language.resource.indirect-resource"


class _ResourceBackend(Protocol):
    def names(self) -> Iterable[str]: ...

    def read(self, name: str) -> bytes: ...

    def close(self) -> None: ...


class _ZipBackend:
    def __init__(self, fh: BinaryIO) -> None:
        if not fh.seekable():
            raise ValueError("`source` must be a seekable stream")
        self._fh = fh
        with _catching_zip_errors():
            self._zip = zipfile.ZipFile(fh)
        self._closed = False
        self._members = _zip_members(self._zip)
        self._prefix = _detect_root_prefix(self._members)
        self._hint = _rezip_hint(self._members, self._prefix)
        data_prefix = self._prefix + _DATA_PREFIX
        self._map: dict[str, zipfile.ZipInfo] = {}
        for member, info in self._members.items():
            if member.startswith(_MACOSX_PREFIX) or not member.startswith(data_prefix):
                continue
            flat = member[len(data_prefix) :]
            if _is_valid_flat_name(flat):
                self._map[flat] = info

    def names(self) -> Iterable[str]:
        return self._map.keys()

    def read(self, name: str) -> bytes:
        with _catching_zip_errors(self._hint):
            return self._zip.read(self._map[name])

    def member(self, name: str) -> bytes | None:
        if (info := self._members.get(self._prefix + name)) is None:
            return None
        with _catching_zip_errors(self._hint):
            return self._zip.read(info)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._zip.close()
        self._fh.close()


def _iter_indirect_identifiers(
    value: Any,
    registry: PresetRegistry,
    adopting: frozenset[str] = frozenset(),
    memo: dict[tuple[str, str, frozenset[str]], list[tuple[str, str]]] | None = None,
) -> Iterator[tuple[str, str]]:
    if memo is None:
        memo = {}
    if isinstance(value, dict):
        props: dict[str, Any] | None = None
        within = adopting
        pid: str = p if isinstance(p := value.get("preset_identifier"), str) else ""
        if pid:
            props = registry.resolved_properties(pid)
            within = adopting | {pid}
        if value.get("type_identifier") == _INDIRECT_TYPE_ID:
            node = value
            if props is not None:
                node = {
                    k: props[k]
                    for k in ("identifier", "filename")
                    if isinstance(props.get(k), str)
                } | value
            field = "identifier" if node.get("identifier") is not None else "filename"
            if isinstance(name := node.get(field), str):
                yield field, name
        for v in value.values():
            yield from _iter_indirect_identifiers(v, registry, adopting, memo)
        if props is not None and pid not in adopting:
            for k, v in props.items():
                if k not in value:
                    if (key := (pid, k, adopting)) not in memo:
                        memo[key] = list(
                            _iter_indirect_identifiers(v, registry, within, memo)
                        )
                    yield from memo[key]
    elif isinstance(value, list):
        for v in value:
            yield from _iter_indirect_identifiers(v, registry, adopting, memo)


class Package(Generic[PayloadT]):
    """A document package in memory, with its payload, presets, manifest, and resources.

    Args:
        payload: The document's root model, written to ``main.json``.
        presets: The presets, written to ``presets.json``.
        manifest: The manifest, written to ``manifest.json``.
        resources: The ``Data/`` resources, as a map from filename to bytes.

    Attributes:
        payload_model: The model class that ``open`` and ``open_lazy`` validate
            ``main.json`` against by default. Each subclass sets it. ``Package`` sets
            none, so opening one directly needs ``payload_model=``.
    """

    payload_model: ClassVar[type[ObjectModel]]

    def __init__(
        self,
        payload: PayloadT,
        *,
        presets: list[Preset] | None = None,
        manifest: Manifest | None = None,
        resources: Mapping[str, bytes] | None = None,
    ) -> None:
        self.payload = payload
        self.presets = presets if presets is not None else []
        self.manifest = manifest if manifest is not None else Manifest()
        self.resources = ResourceStore(resources)

    @classmethod
    def open(
        cls,
        source: str | os.PathLike[str] | BinaryIO,
        *,
        payload_model: type[PayloadT] | None = None,
    ) -> Self:
        """Opens a package from a ZIP archive or a readable stream.

        The method doesn't accept an unzipped package directory. Zip it with
        ``main.json`` at the root of the archive.

        Args:
            source: A path to a ZIP package, or an open, seekable binary stream.
            payload_model: The model class that validates the payload in ``main.json``.
                Defaults to the class's ``payload_model``.

        Returns:
            Self: The package, with every resource already read.

        Raises:
            DocumentPackageError: ``source`` isn't a valid package, and ``kind`` names
                the defect.
            DocumentVersionError: ``source`` declares a package or object version this
                library doesn't implement.
            pydantic.ValidationError: ``main.json`` doesn't match ``payload_model``.
            ValueError: ``source`` is a stream that can't seek.
            OSError: ``source`` can't be read, such as a path that doesn't exist.
            TypeError: neither ``payload_model`` nor the class's ``payload_model`` is
                set.
        """  # noqa: DOC502, DOC503 -- raised by `_resolve_payload_model`, `_probe_archive`, `_read_probed_stream`, and `_decode_json_parts`, not here
        payload_model = cls._resolve_payload_model(payload_model)
        if hasattr(source, "read"):
            return cls._from_entries(
                _read_probed_stream(source),  # type: ignore[arg-type]
                payload_model=payload_model,
            )
        path = os.fspath(source)
        # The file is opened before the probe because `is_zipfile(path)` swallows every
        # `OSError` and returns `False`. A mistyped or unreadable path would then fail
        # as `NOT_A_PACKAGE`.
        with _open_package_file(path) as fh:
            _probe_archive(fh, repr(path))
            return cls._from_entries(
                _read_zip_stream(fh), payload_model=payload_model, source=path
            )

    @classmethod
    def open_lazy(
        cls,
        source: str | os.PathLike[str] | BinaryIO,
        *,
        payload_model: type[PayloadT] | None = None,
    ) -> Self:
        """Opens a package and reads each resource only on first access.

        ``pkg.resources`` is a lazy ``ResourceStore``, and the JSON parts are read up
        front. ``dict(pkg.resources)``, ``items()``, and ``save()`` read every resource,
        so laziness pays off only when a caller reads a subset, such as just the payload
        of a document with large media.

        The package holds a file handle until ``close()`` runs, so open it in a ``with``
        block. The method reads a stream eagerly, because its lifetime belongs to the
        caller.

        Args:
            source: A path to a ZIP package, or an open, seekable binary stream.
            payload_model: The model class that validates the payload in ``main.json``.
                Defaults to the class's ``payload_model``.

        Returns:
            Self: The package, with its resources still unread.

        Raises:
            DocumentPackageError: ``source`` isn't a valid package, as for ``open``.
            DocumentVersionError: ``source`` declares a package or object version this
                library doesn't implement.
            pydantic.ValidationError: ``main.json`` doesn't match ``payload_model``.
            ValueError: ``source`` is a stream that can't seek.
            OSError: ``source`` can't be read, such as a path that doesn't exist.
            TypeError: neither ``payload_model`` nor the class's ``payload_model`` is
                set.
        """  # noqa: DOC503 -- raised by `_resolve_payload_model`, `_probe_archive`, `_read_probed_stream`, and `_decode_json_parts`, not here
        payload_model = cls._resolve_payload_model(payload_model)
        if hasattr(source, "read"):
            return cls._from_entries(
                _read_probed_stream(source),  # type: ignore[arg-type]
                payload_model=payload_model,
            )
        path = os.fspath(source)
        fh = _open_package_file(path)
        try:
            _probe_archive(fh, repr(path))
            backend = _ZipBackend(fh)
        except BaseException:
            fh.close()
            raise
        try:
            payload, manifest, presets = _decode_json_parts(
                backend.member(_MAIN),
                backend.member(_MANIFEST),
                backend.member(_PRESETS),
                payload_model,
                source=path,
            )
        except BaseException:
            backend.close()
            raise
        return cls(
            payload,
            presets=presets,
            manifest=manifest,
            resources=ResourceStore._lazy(backend),
        )

    @classmethod
    def _resolve_payload_model(
        cls, payload_model: type[PayloadT] | None
    ) -> type[PayloadT]:
        if payload_model is not None:
            return payload_model
        if (default := getattr(cls, "payload_model", None)) is None:
            raise TypeError(
                f"{cls.__name__} has no payload model: pass `payload_model=`, or open through "
                "a subclass that sets `payload_model`"
            )
        return cast("type[PayloadT]", default)

    @classmethod
    def _from_entries(
        cls,
        entries: dict[str, bytes],
        *,
        payload_model: type[PayloadT],
        source: str | None = None,
    ) -> Self:
        payload, manifest, presets = _decode_json_parts(
            entries.get(_MAIN),
            entries.get(_MANIFEST),
            entries.get(_PRESETS),
            payload_model,
            source=source,
        )
        resources: dict[str, bytes] = {}
        for name, data in entries.items():
            if not name.startswith(_DATA_PREFIX):
                continue
            filename = name[len(_DATA_PREFIX) :]
            if _is_valid_flat_name(filename):
                resources[filename] = data
        return cls(payload, presets=presets, manifest=manifest, resources=resources)

    def _to_main_json(self) -> dict[str, Any]:
        context: dict[str, Any] = {
            "wire_presets": PresetRegistry(self.presets),
            "_wire_version_error": None,
        }
        try:
            return self.payload.model_dump(mode="json", context=context)
        except PydanticSerializationError:
            if (too_new := context.get("_wire_version_error")) is not None:
                raise too_new from None
            raise

    def _to_entries(self) -> dict[str, bytes]:
        return self._entries_from_main(self._to_main_json())

    def _entries_from_main(self, main: dict[str, Any]) -> dict[str, bytes]:
        entries: dict[str, bytes] = {
            _MAIN: _dumps(main),
            _MANIFEST: _dumps(self.manifest.to_dict()),
            _PRESETS: _dumps([p.to_dict() for p in self.presets]),
        }
        for filename, data in self.resources.items():
            entries[f"{_DATA_PREFIX}{filename}"] = data
        return entries

    def save(
        self,
        destination: str | os.PathLike[str],
        *,
        validate_resources: bool = True,
        pre_save_hooks: Iterable[
            Callable[[Package[PayloadT], dict[str, Any]], None]
        ] = (),
    ) -> None:
        """Writes the package to a path as a ZIP archive.

        ``save`` calls each hook as ``hook(self, main)``, where ``main`` is the exact
        value it writes to ``main.json``. A hook is the only supported way to reach that
        value, and it must not mutate it.

        A saved package doesn't match the one it came from, or an earlier save, byte for
        byte, but it's semantically the same. ``same_json`` compares two JSON
        values while ignoring key order and number spelling, such as ``1`` and ``1.0``.

        Args:
            destination: The destination path.
            validate_resources: If ``True``, ``save`` checks that every indirect
                resource the payload references resolves in ``self.resources`` before
                writing anything.
            pre_save_hooks: The functions to call, in order, before the write. A hook
                that raises stops the save and leaves ``destination`` untouched.

        Raises:
            ValueError: ``validate_resources`` is set and the payload references an
                indirect resource missing from ``self.resources``, or the presets'
                ``parent_identifier`` chain has a cycle.
            IsADirectoryError: ``destination`` is an existing directory. ``save`` checks
                this before calling any hook, and leaves the directory in place.
            DocumentPackageError: a lazily opened package has a corrupt resource.
            DocumentVersionError: a union's only case comes from a preset value too new
                for this library to read.
            OSError: ``destination`` can't be written, such as a missing parent
                directory.

        Any exception a hook raises propagates unchanged.
        """  # noqa: DOC503 -- the `ValueError` for a cycle, `DocumentPackageError`, `DocumentVersionError`, and `OSError` come from the dump and the write, not here
        path = os.fspath(destination)
        if os.path.isdir(path):
            raise IsADirectoryError(
                errno.EISDIR, "can't save a package over a directory", path
            )
        main = self._to_main_json()
        for hook in pre_save_hooks:
            hook(self, main)
        if validate_resources:
            missing: dict[str, set[str]] = {}
            registry = PresetRegistry(self.presets)
            for field, name in set(_iter_indirect_identifiers(main, registry)):
                if not self.resources.can_resolve(name):
                    missing.setdefault(name, set()).add(field)
            if missing:
                listed = ", ".join(
                    f"{name!r} (looked up by {' and '.join(sorted(fields))})"
                    for name, fields in sorted(missing.items())
                )
                raise ValueError(f"indirect resources missing from Data/: {listed}")
        _write_zip(path, self._entries_from_main(main))

    def close(self) -> None:
        """Releases the file handle that a lazily opened package holds.

        Calling ``close`` again does nothing, and so does calling it on an eagerly
        opened package, so ``with Package.open(...) as pkg:`` is always safe. A lazily
        opened package keeps only the resources already read, so a later ``save`` drops
        the rest or, with ``validate_resources``, raises for one the payload references.
        Save before closing, or read every resource first with ``dict(pkg.resources)``.
        """
        self.resources.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


def _decode_json_parts(
    main: bytes | None,
    manifest: bytes | None,
    presets: bytes | None,
    payload_model: type[PayloadT],
    *,
    source: str | None = None,
) -> tuple[PayloadT, Manifest, list[Preset]]:
    where = f"{source!r}: " if source is not None else ""
    if main is None:
        raise DocumentPackageError(
            DocumentPackageErrorKind.MISSING_MAIN_FILE, f"{where}{_MAIN} is required"
        )
    try:
        manifest_obj = Manifest.parse(_maybe_json(manifest))
    except DocumentVersionError as exc:
        raise DocumentVersionError(f"{where}{exc}") from exc.__cause__
    preset_list: list[Preset] = []
    if presets is not None:
        try:
            presets_raw = json.loads(presets)
        except ValueError as exc:
            raise DocumentPackageError(
                DocumentPackageErrorKind.MALFORMED_PRESETS, f"{where}{_PRESETS}: {exc}"
            ) from exc
        if not isinstance(presets_raw, list):
            raise DocumentPackageError(
                DocumentPackageErrorKind.MALFORMED_PRESETS,
                f"{where}{_PRESETS} isn't a JSON array",
            )
        entries = [
            e
            for e in presets_raw
            if isinstance(e, dict) and isinstance(e.get("identifier"), str)
        ]
        if missing := [e["identifier"] for e in entries if "properties" not in e]:
            raise DocumentPackageError(
                DocumentPackageErrorKind.MALFORMED_PRESETS,
                f"{where}{_PRESETS}: no `properties` in preset {missing[0]!r}",
            )
        preset_list = [Preset.from_dict(e) for e in entries]
    registry = PresetRegistry(preset_list)
    try:
        main_obj = json.loads(main)
    except ValueError as exc:
        raise DocumentPackageError(
            DocumentPackageErrorKind.MALFORMED_JSON, f"{where}{_MAIN}: {exc}"
        ) from exc
    try:
        payload = payload_model.model_validate(
            main_obj, context={"wire_presets": registry}
        )
    except ValueError as exc:
        if registry._cycle is not None:
            raise DocumentPackageError(
                DocumentPackageErrorKind.MALFORMED_PRESETS,
                f"{where}circular preset `parent_identifier` chain at {registry._cycle!r}, "
                f"so payload validation failed: {exc}",
            ) from exc
        if isinstance(exc, ValidationError) and any(
            e.get("type") == "recursion_loop" for e in exc.errors()
        ):
            raise DocumentPackageError(
                DocumentPackageErrorKind.MALFORMED_PRESETS,
                f"{where}a preset property value reaches its own preset, "
                f"so payload validation failed: {exc}",
            ) from exc
        raise
    if registry._cycle is not None:
        raise DocumentPackageError(
            DocumentPackageErrorKind.MALFORMED_PRESETS,
            f"{where}circular preset `parent_identifier` chain at {registry._cycle!r}",
        )
    return payload, manifest_obj, preset_list


def _open_package_file(path: str) -> BinaryIO:
    # Classified by stat, not by the error from `open`: opening a directory raises
    # `PermissionError` on Windows or when it is unreadable, and opening a named pipe
    # blocks. Either would escape the `except DocumentPackageError` a batch uses to skip
    # a file.
    mode = os.stat(path).st_mode
    if not stat.S_ISREG(mode):
        what = "a directory" if stat.S_ISDIR(mode) else "not a regular file"
        raise DocumentPackageError(
            DocumentPackageErrorKind.NOT_A_PACKAGE,
            f"{path!r} is {what}, not a ZIP package",
        )
    return open(path, "rb")


_ZIP_LOCAL_HEADER = b"PK\x03\x04"


def _probe_archive(fh: BinaryIO, name: str) -> None:
    # `is_zipfile` finds an archive by its end of central directory record, which
    # truncation cuts off, so input that still starts with a local file header is a
    # corrupt archive rather than some other format.
    is_zip = zipfile.is_zipfile(fh)
    fh.seek(0)
    if is_zip:
        return
    if fh.read(len(_ZIP_LOCAL_HEADER)) == _ZIP_LOCAL_HEADER:
        raise DocumentPackageError(
            DocumentPackageErrorKind.MALFORMED_ARCHIVE,
            f"{name} has no ZIP central directory, so it's truncated",
        )
    raise DocumentPackageError(
        DocumentPackageErrorKind.NOT_A_PACKAGE, f"{name} isn't a ZIP package"
    )


def _read_probed_stream(fh: BinaryIO) -> dict[str, bytes]:
    if not fh.seekable():
        raise ValueError("`source` must be a seekable stream")
    _probe_archive(fh, "the stream")
    return _read_zip_stream(fh)


def _dumps(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _write_zip(path: str, entries: dict[str, bytes]) -> None:
    tmp = f"{path}.tmp-{os.getpid()}"
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
            for name, data in entries.items():
                zf.writestr(name, data)
        try:
            os.replace(tmp, path)
        except IsADirectoryError:
            raise IsADirectoryError(
                errno.EISDIR, "can't save a package over a directory", path
            ) from None
    except OSError as exc:
        if exc.filename != tmp or exc.errno is None:
            raise
        raise type(exc)(exc.errno, exc.strerror, path) from None
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _maybe_json(data: bytes | None) -> Any:
    if data is None:
        return None
    try:
        return json.loads(data)
    except ValueError:
        return None


_MACOSX_PREFIX = "__MACOSX/"


def _detect_root_prefix(names: Iterable[str]) -> str:
    entries = [
        n for n in names if not n.endswith("/") and not n.startswith(_MACOSX_PREFIX)
    ]
    if not entries:
        return ""
    dotslash = "./" if all(n.startswith("./") for n in entries) else ""
    if dotslash:
        entries = [n[len(dotslash) :] for n in entries]
    tops = {n.split("/", 1)[0] for n in entries if "/" in n}
    roots_at_top = {n for n in entries if "/" not in n}
    if len(tops) == 1 and not roots_at_top:
        return dotslash + next(iter(tops)) + "/"
    return dotslash


_ZIP_UTF8_FLAG = 0x800


def _zip_members(zf: zipfile.ZipFile) -> dict[str, zipfile.ZipInfo]:
    members: dict[str, zipfile.ZipInfo] = {}
    for info in zf.infolist():
        name = info.filename
        # A name that differs from `orig_filename` came from the Unicode Path extra
        # field (0x7075), which zipfile reads in Python 3.12 and later. That name is
        # already decoded, and decoding it again would mangle a name with cp437 bytes
        # that happen to be valid UTF-8.
        if not info.flag_bits & _ZIP_UTF8_FLAG and name == info.orig_filename:
            try:
                name = name.encode("cp437").decode("utf-8")
            except UnicodeError:
                pass
        if not name.endswith("/"):
            members[name] = info
    return members


def _read_zip_stream(fh: BinaryIO) -> dict[str, bytes]:
    with _catching_zip_errors(), zipfile.ZipFile(fh) as zf:
        members = _zip_members(zf)
        prefix = _detect_root_prefix(members)
        with _catching_zip_errors(_rezip_hint(members, prefix)):
            return {
                n[len(prefix) :]: zf.read(info)
                for n, info in members.items()
                if n.startswith(prefix) and not n.startswith(_MACOSX_PREFIX)
            }
