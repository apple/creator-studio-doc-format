# Example scripts

The package `creator_studio_doc_format` has four modules. A name that isn't in `core` is
probably in one of the others:

- `core`: Pydantic models that mirror the types in `main.json` one to one, and
  `KeyxDocument`, which represents a document. The root is `doc.presentation`, which
  holds `slides`, `slide_size`, and `theme`.
- `navigation`: `iterate_models`, which walks a model tree.
- `authoring`: `slide_from_layout` and its helpers, which build slides from a theme's
  layouts by placeholder name.
- `validation`: `validate_document`, which checks a document against the format's rules.

Models such as `Fill`, `Color`, and `Chart` are each a `TaggedUnionModel`, which holds one
of several variants, called cases. Such a class has one optional field per case, and a
value sets the field for the case it holds: `Fill(color=...)`, or `Stroke(empty=True)`
for a case with no payload. Read the `TaggedUnionModel` docstring before reading or
editing one, because a value can hold more than one case.

**Remove a default border with `Stroke(empty=True)`.** `Shape.stroke` and `Textbox.stroke` default to a
visible line, so a shape or text box you want borderless has to set it.

**Tracking is a fraction of the font's em, not points.** For `tracking`, `0.0` is the default
spacing, `0.05`–`0.2` gives subtle emphasis, and `1` or more adds a full em or more between letters. Validation doesn't flag
a value in points.

**Read a document in bounded pieces.** A real document can hold thousands of models, and every
model dumps its `type_identifier` and `version`, which buries the fields you want. Filter
`iterate_models(root)` for what you need and print only those fields, or print the top levels
with truncated output (`inspection.py` shows how).
Pass only those pieces to `print` or `model_dump*`, not a whole subtree. `model_dump` rejects field-filtering
options such as `exclude_unset` and `exclude_none`.

**Import only the `core` names you use.** `core` exports names like `Path` that shadow the standard library's after `import *`.

## Examples

The examples fall into three groups: content elements that you place on a slide, the
slide and document structure that holds them, and work on a document that already exists. Each entry below describes one example,
and each example runs standalone. Start with `basics.py`, which touches the most common
pieces of a slide. Then read the file that matches the task, not the whole directory.

### Content elements

- `charts.py`: Builds a mixed chart, a pie chart, and a scatter chart, one for each axis
  arrangement of `Chart`, and styles their title, caption, axis, and legend text.
- `hyperlinks.py`: Builds a `Hyperlink` to a URL, to another slide, to a file, and to a
  program action, and links to a slide by position with `SlideTarget`.
- `lists.py`: Builds bullet, numbered, and image lists through `ListProperties` and
  `ListLevelType`, nests list levels, and draws a paragraph border rule.
- `image_decoration.py`: Applies each `Image` decoration (`Mask`, frame `Stroke`,
  `Shadow`, opacity, and `Reflection`) and fills a `Shape` with an `ImageFill`.
- `shapes_and_lines.py`: Draws a rectangle, a rounded rectangle, an oval, a polygon, and a
  star as `Shape` paths, attaches a `ConnectionLine` to two of them, and sets `shadow` and
  `reflection`.
- `spreadsheets.py`: Builds a `Table` of financial data with a `CellFormat` for each
  column, a `SUM` formula that refers to cells by identifier, and a `CellRange` banner row.
- `tables.py`: Builds a `Table` of cells with header rows and alternating rows, and
  overrides the fill and text of single cells.

### Slide and document structure

- `basics.py`: Builds a typical content slide with presets, text, a shape, an image, a
  gradient overlay, a `Group` with a title and caption, and a presenter note.
- `authoring.py`: Makes slides from a themed document's layouts with placeholders set by
  name, and builds a slide by hand that takes its styles from the theme's stylesheet and
  `PresetRegistry.resolved_properties`.

### Existing documents

- `inspection.py`: Finds the text on each slide of a `.keyx` with
  `navigation.iterate_models`, prints it, and replaces the text of unlocked objects with
  lorem ipsum of the same length.

Run any script as a module with no arguments, for example
`python -m creator_studio_doc_format.examples.basics`. The script writes a `.keyx` under `tmp/`.

Sample files live in `fixtures/`, which is installed as package data. The files include `.png`
images and `.keyx` documents, such as `sample.keyx`, the default input of `inspection.py`.
