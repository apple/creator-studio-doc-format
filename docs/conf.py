# Copyright © 2026 Apple Inc.
#
# Licensed under Apache License v2.0. For more information, see LICENSE.
# SPDX-License-Identifier: Apache-2.0


from importlib.metadata import version as _installed_version

from docutils import nodes
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

_DIST = "creator-studio-doc-format"

project = "Creator Studio Document Format"
copyright = "2026, Apple Inc."
author = "Apple Inc."
release = _installed_version(_DIST)
_FORMAT_DOCS = "https://developer.apple.com/documentation/"
_PYDANTIC_DOCS = "https://docs.pydantic.dev/2.11/"
# A substitution, because a link's own text can't be code font.
rst_epilog = f"""
.. _Keynote Interchange Format: {_FORMAT_DOCS}keynoteinterchangeformat
.. _Creator Studio Document Exporting API: {_FORMAT_DOCS}creatorstudiodocumentexportingapi
.. _Pydantic model: {_PYDANTIC_DOCS}concepts/models/
.. |pydantic_error| replace:: ``pydantic.ValidationError``
.. _pydantic_error: {_PYDANTIC_DOCS}errors/errors/
"""
language = "en"
default_role = "literal"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.extlinks",
]

extlinks = {
    "authoring": (
        (
            f"{_FORMAT_DOCS}keynoteinterchangeformat/"
            "understanding-authoring-requirements-for-keynote-interchange-format#%s"
        ),
        None,
    ),
    "structure": (
        (
            f"{_FORMAT_DOCS}keynoteinterchangeformat/"
            "understanding-keynote-interchange-format-structure#%s"
        ),
        None,
    ),
    "formatref": (f"{_FORMAT_DOCS}keynoteinterchangeformat/%s", None),
}

autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_validator_summary = False
autodoc_pydantic_model_show_validator_members = False
autodoc_pydantic_model_show_field_summary = False
autodoc_pydantic_field_list_validators = False
autodoc_pydantic_field_show_constraints = True
autodoc_pydantic_model_member_order = "bysource"
autodoc_pydantic_model_hide_paramlist = False
autodoc_pydantic_model_signature_prefix = "class"

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_attr_annotations = False

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "exclude-members": "model_config,model_post_init",
}
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
toc_object_entries = False

nitpicky = True
nitpick_ignore = [
    ("py:class", "os.PathLike"),
    ("py:class", "enum.Enum"),
    ("py:class", "collections.abc.Iterator"),
    ("py:class", "collections.abc.Iterable"),
    ("py:class", "collections.abc.Mapping"),
    ("py:class", "collections.abc.MutableMapping"),
    ("py:class", "collections.abc.Callable"),
    ("py:class", "BaseModel"),
    ("py:class", "pydantic.main.BaseModel"),
    ("py:class", "ConfigDict"),
    ("py:class", "Strict"),
    ("py:class", "creator_studio_doc_format.core.package.PayloadT"),
    ("py:obj", "creator_studio_doc_format.core.package.PayloadT"),
    ("py:class", "PayloadT"),
    ("py:obj", "creator_studio_doc_format.core._wire._OT"),
    ("py:class", "creator_studio_doc_format.core._wire._E"),
    ("py:class", "_OT"),
    ("py:class", "_E"),
    ("py:class", "creator_studio_doc_format.core._wire._OverrideState"),
    ("py:meth", "Package.save"),
]

copybutton_prompt_text = r">>> |\.\.\. |\$ |% "
copybutton_prompt_is_regexp = True

_UNLINKED_EXTERNAL = frozenset({"pydantic.ValidationError"})


def _code_font(
    app: Sphinx,
    env: BuildEnvironment,
    node: addnodes.pending_xref,
    contnode: nodes.Element,
) -> nodes.Node | None:
    if node["reftarget"] in _UNLINKED_EXTERNAL:
        return nodes.literal(text=node["reftarget"])
    return None


def setup(app: Sphinx) -> None:
    """Connects the handler."""
    app.connect("missing-reference", _code_font)
