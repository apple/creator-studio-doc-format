# Creator Studio Document Format

A Python library for reading, creating, and editing Apple Creator Studio documents, starting with Keynote.

## Overview

This library works with Keynote presentations in [Keynote Interchange Format](https://developer.apple.com/documentation/keynoteinterchangeformat) (`.keyx`).
You can use it to:

- Read the slides, text, images, tables, charts, styles, and more in a `.keyx` file exported from Keynote.
- Create a presentation from scratch, or from a theme's slide layouts and styles.
- Edit a presentation, and check it against the format's rules before you save it.

The library reads and writes `.keyx` files itself, so it doesn't need Keynote, an Apple device, or a network connection.
To preview a presentation, open it in Keynote on an Apple device.
In other places, use the [Creator Studio Document Exporting API](https://developer.apple.com/documentation/creatorstudiodocumentexportingapi) to convert to other formats like PDF.

## Getting started

### Installation

The library needs Python 3.13 or later. Install the package with pip:

```bash
% pip install creator-studio-doc-format
```

### Quick start

Build a `Presentation` with a slide that holds a text box, wrap it in a `KeyxDocument`, and save
it as `hello.keyx`, which you can open in Keynote:

```python
# The star import keeps this short. In your own code, import only the names you use.
from creator_studio_doc_format.core import *

title = Textbox(
    geometry=Geometry(
        position=Position(x=160, y=440), size=Size(width=1600, height=200)
    ),
    stroke=Stroke(empty=True),
    layout_properties=LayoutProperties(vertical_alignment="center"),
    paragraph_properties=ParagraphProperties(
        alignment="center",
        character_properties=CharacterProperties(font_size=96),
    ),
    text=Text(string="Hello, Keynote"),
)
slide = Slide(contents=[SlideObject(object=CanvasObject(textbox=title))])

doc = KeyxDocument(
    Presentation(
        theme=KeynoteTheme(name="White", locale="en_US"),
        slide_size=Size(width=1920, height=1080),
        slides=[slide],
    )
)

doc.save("hello.keyx")
```

## Documentation

Three resources document the library:

- [Guide](https://apple.github.io/creator-studio-doc-format/#guide):
  Follow the tasks, from creating your first presentation to validating and navigating a
  document.
- [API reference](https://apple.github.io/creator-studio-doc-format/#api-reference):
  Look up every public symbol in the library, one page per topic.
- [Examples](https://github.com/apple/creator-studio-doc-format/tree/main/src/creator_studio_doc_format/examples): Browse a runnable script for each kind
  of slide content.

### Agent skill

The `creator-studio-doc-format` skill teaches a coding agent to use the library. Install it
from the latest release, which matches the latest library on PyPI:

```bash
% gh skill install apple/creator-studio-doc-format creator-studio-doc-format
```

Any agent that reads `SKILL.md` folders can also use a copy of
[the skill's folder](https://github.com/apple/creator-studio-doc-format/tree/main/skills/creator-studio-doc-format). The skill needs the library installed.

## Contributing

We actively want your feedback. GitHub Issues are open for problem reports and feature requests. Use the [Issue Template](https://github.com/apple/creator-studio-doc-format/issues/new/choose) to get started. This project isn't open for code or documentation contributions at this time.

- Before opening an issue:
  - Search existing issues to avoid duplicates.
  - Write a clear, concise title and detailed description.
  - Include precise steps to reproduce, expected behavior, and actual behavior.
  - Specify your environment and version information.
  - Explain the severity and impact of the problem.

## Code of conduct

This project follows the [Apple Open Source Code of Conduct](https://github.com/apple/.github/blob/main/CODE_OF_CONDUCT.md).

## Support

- [GitHub Issues](https://github.com/apple/creator-studio-doc-format/issues)

## Security

If you discover a security vulnerability, follow the [security policy](https://github.com/apple/.github/blob/main/SECURITY.md). Don't open a public issue.

## License

This project and the files in this repository are licensed under [Apache License v2.0](https://github.com/apple/creator-studio-doc-format/blob/main/LICENSE)
unless otherwise noted.
