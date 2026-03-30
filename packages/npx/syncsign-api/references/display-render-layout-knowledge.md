# Display Render Layout Knowledge Base

This document summarizes the official SyncSign Hub SDK references that matter when the user asks for custom Display rendering, especially custom layouts and calendar-aware templates.

Primary sources:
- Render Layout Template: <https://dev.sync-sign.com/hubsdk/guides/render_layout.html>
- Template for Calendars: <https://dev.sync-sign.com/hubsdk/references/calendar_template_editing.html>

## 1. Two Similar but Different JSON Shapes

There are two related layout formats in SyncSign:

### A. Direct Web API render payload used by this repository

Single-node render:

```json
{
  "layout": {
    "background": {},
    "items": [],
    "options": {}
  }
}
```

Batch render:

```json
[
  {
    "nodeId": "0008d1f9...",
    "layout": {
      "background": {},
      "items": [],
      "options": {}
    }
  }
]
```

This is the shape used by `examples/render-single.json`, `examples/render-batch.json`, and the Web API routes in this skill.

### B. Calendar template JSON pasted into SyncSign Cloud / SOPS

```json
{
  "layout": [
    {
      "status": "BUSY",
      "items": []
    },
    {
      "status": "FREE",
      "items": []
    }
  ]
}
```

The calendar template format is not a direct one-shot render. It is a template set. SyncSign chooses the matching block by `status`, then replaces some `TEXT` values according to the special `id` fields documented below.

## 2. Coordinate System and Screen Sizes

- Origin is the upper-left corner.
- `x` increases left to right.
- `y` increases top to bottom.
- Most `items[*].data.block` coordinates are absolute pixels.
- `background.rectangle.block` uses percentages instead of pixels.

Repository-validated canvas sizes for this project:

| Display size | Max width | Max height |
| --- | ---: | ---: |
| 2.9 inch | 296 | 128 |
| 4.2 inch | 400 | 300 |
| 7.5 inch | 800 | 480 |

Maintainer note:
- Older official Hub SDK examples may still show `7.5` inch as `880 x 528`.
- For current sellable Displays in this project, use `800 x 480` unless the maintainer explicitly says otherwise.

Implication for generation:
- If the user asks for a table, dashboard, or card layout, first infer the target display size.
- Then divide the canvas into blocks and place `TEXT`, `RECTANGLE`, `LINE`, `IMAGE`, or `QRCODE` items explicitly.
- SyncSign does not provide a native "table" widget. A table is assembled from drawing primitives plus text blocks.

## 3. Layout Sections and Their Meanings

### `background`

Used for full-screen or large-area background styling.

Important fields:
- `bgColor`: full-screen background color. Default is `WHITE`.
- `enableButtonZone`: whether the display button area is reserved.
- `rectangle`: one optional background rectangle with border/fill settings.
- `rectangle.strokeThickness`: border width.
- `rectangle.strokeColor`: border color.
- `rectangle.fillColor`: fill color.
- `rectangle.block.x_percent`, `y_percent`, `w_percent`, `h_percent`: rectangle position and size as percentages of total screen width/height.

Versioned fields:
- `transparentColor`, `rectangle.strokePattern`, and `rectangle.fillPattern` require Display support from `v1.25`.

### `items`

This is the main content array. Every visible element is an item.

Per maintainer guidance for this project, do not use `BOTTOM_CUSTOM_BUTTONS` or `PERIPHERAL_CONTROL` for button-triggered screen interactions. Treat them as out of scope for new templates and agent proposals unless the maintainer explicitly asks for them.

Common item types:

| Type | Purpose | Key fields |
| --- | --- | --- |
| `TEXT` | Render text or icons | `text`, `id`, `font`, `textColor`, `backgroundColor`, `textAlign`, `lineSpace`, `block`, `offset` |
| `RECTANGLE` | Draw filled or bordered boxes | `fillColor`, `strokeColor`, `strokeThickness`, `block` |
| `IMAGE` | Place the built-in organization logo image | `source`, `name`, `block` |
| `BITMAP_URI` | Fetch and render a bitmap by URL; preferred for custom images | `uri`, `foregroundColor`, `backgroundColor`, `block` |
| `QRCODE` | Draw a QR code | `text`, `position`, `scale`, `version`, `eccLevel` |
| `LINE` | Draw a line | `lineColor`, `linePattern`, `block.x0`, `y0`, `x1`, `y1` |
| `CIRCLE` | Draw a circle | `radius`, `center`, `fillColor`, `strokeColor` |

### `options`

Officially documented options:
- `pollRate`: deprecated. Milliseconds between polling attempts.
- `refreshScreen`: whether to refresh after rendering. Default is `true`.

Important note:
- The Hub SDK guide documents `pollRate` under `options`.
- The Swagger example and this repository's sample JSONs currently show a `POLL_RATE` item with `data.rate`.
- When authoring new custom layouts, prefer keeping the repository's currently working API wrapper shape, but be aware that the official guide describes polling as an `options.pollRate` concern.

## 4. Item Field Semantics

### `TEXT`

Use `TEXT` for labels, values, icons, placeholders, and calendar-bound content.

Important fields:
- `data.text`: literal text, or icon unicode.
- `data.id`: stable logical identifier for the block. In calendar templates, this is also the placeholder selector.
- `data.textColor`: font color.
- `data.backgroundColor`: background behind the text.
- `data.font`: font family and size.
- `data.textAlign`: `LEFT`, `CENTER`, or `RIGHT`.
- `data.lineSpace`: line spacing.
- `data.block`: the text bounding box with `x`, `y`, `w`, `h`.
- `data.offset`: pixel offset applied inside the block.

Useful rules:
- At least one of `TEXT.data.block.y` or `TEXT.data.block.h` must be a multiple of `8`.
- Text escape placeholders `<SN>` and `<NODE_ID>` are supported by Hubs above `v0.5.0`.
- Official Hub SDK docs use `textAlign`, while current repository sample payloads use `text-align`. Keep this mismatch in mind when comparing examples.
- If `id` matches a reserved calendar placeholder, SyncSign will replace `text` automatically during calendar rendering.
- `lineSpace` ranges from `0` to the display's max height. Default is `2`.
- `offset.x` and `offset.y` are fine-tuning tools for positioning inside the text block. Default is `0`.

### Supported font families and sizes

Do not invent font names. Use only documented font families and sizes from the official Hub SDK.

Common English font families:
- `DDIN`: `16`, `24`, `32`, `48`, `64`, `128`
- `DDIN_CONDENSED`: `16`, `24`, `32`, `48`, `64`
- `CHARRIOT`: `10`
- `APRILSANS`: `10`, `16`, `24`
- `ROBOTO_CONDENSED`: `24`, `48`
- `ROBOTO_SLAB`: `24`, `48`
- `YANONE_KAFFEESATZ`: `24_B`, `44_B`
- `KAUSHAN_SCRIPT`: `20`, `32`
- `SRIRACHA`: `24`
- `DORSA`: `32`
- `LONDRINA_OUTLINE`: `36`
- `BUNGEE_SHADE`: `36`

Chinese-capable fonts from the official guide:
- `NOTO_SERIF_16`
- `NOTO_SANS_24`
- `NOTO_SANS_40`

Important notes:
- The official guide says Chinese fonts are supported only on `4MB Flash Display` models.
- For icon rendering, use `TEXT` with `font` set to `ICON_WEATHER`, `ICON_FA_SOLID`, or `ICON_FA_BRANDS`, and provide the icon unicode in `text`.
- If the unicode is wrong for an icon font, the display may show an unintended icon.

Practical font selection guidance:
- Dense tables or cell values: prefer `DDIN_CONDENSED_16`, `DDIN_CONDENSED_24`, or `ROBOTO_CONDENSED_24`.
- Large KPI or numeric emphasis: prefer `DDIN_48`, `DDIN_64`, or `DDIN_128`.
- Calendar titles and prominent headings: `YANONE_KAFFEESATZ_44_B` is a safe default.
- Handwritten or decorative fonts such as `KAUSHAN_SCRIPT`, `SRIRACHA`, `LONDRINA_OUTLINE`, and `BUNGEE_SHADE` are better for short headings than for dense data tables.

### `RECTANGLE`

Use `RECTANGLE` for borders, dividers, cards, table cells, and filled areas.

Important fields:
- `fillColor`
- `strokeColor`
- `strokeThickness`
- `block.x`, `block.y`, `block.w`, `block.h`

Useful rules:
- `block.x` and `block.w` must be multiples of `8`.
- `strokePattern`, `fillPattern`, and `transparentColor` require Display support from `v1.25`.

Generation tip:
- For tables and dashboards, `RECTANGLE` is the safest primitive because it avoids the version requirement of `LINE`.

### `IMAGE`

Use `IMAGE` only for the built-in organization logo image in this project.

Important fields:
- `source`: use `BUILD_IN`
- `name`: file name
- `block`: position and size

Project-maintained rules:
- Treat `CUSTOM` as out of scope. It is not a recommended path for this project and should not be proposed to users unless the maintainer explicitly asks for it.
- For `BUILD_IN`, use `name: logo.bin`.
- For `BUILD_IN`, `block.w` and `block.h` must be `96` and `96`.
- The underlying bitmap is the organization's uploaded logo image from the SyncSign client path `Settings -> Organization`.
- The logo image should be a `96 x 96` monochrome `.bmp` with `1-bit` depth.

### `BITMAP_URI`

Use `BITMAP_URI` when the layout should download a bitmap from a URL.
In this project, this is the preferred way to show user-provided custom images.

Important fields:
- `uri`
- `foregroundColor`
- `backgroundColor`
- `transparentColor`
- `block`

Project guidance:
- If the user wants a custom image, prefer `BITMAP_URI` rather than `IMAGE`.
- Keep the bitmap size within the target Display's maximum canvas size.
- For `7.5` inch Displays in this project, cap the render area at `800 x 480`.

Operational notes from the official guide:
- Some HTTPS URLs may fail unless the needed root certificates are installed on the Hub/Display.
- Wi-Fi Displays download directly. Other models rely on the Hub and ZigBee forwarding, which is slower.
- The URL is cached. Change the filename or add a query string such as `?v=2` when the image content changes.

High-level tri-color usage for black and red images:
- For a picture containing black and red, split it into two monochrome BMP files: one black layer and one red layer.
- Render them as two `BITMAP_URI` items with the same `block` so they overlap in the same position.
- Use `foregroundColor: BLACK` for the black layer and `foregroundColor: RED` for the red layer.
- Keep `backgroundColor: WHITE` for both layers unless the maintainer specifies another approach.
- This pattern comes from the official `How to update a picture containing black and red?` example.

### `QRCODE`

Use `QRCODE` for scan targets such as forms, URLs, and confirmation links.

Important fields:
- `text`
- `position.x`, `position.y`
- `scale`
- `version`
- `eccLevel`

Sizing formula from the official guide:
- QR width and height are both `(4 * version + 17) * scale`

Memory note:
- On 4.2-inch Displays, if the QR block area exceeds `25600`, it may fail to display.

### `LINE`

Use `LINE` for dividers and table rules when the target Display supports it.

Important fields:
- `backgroundColor`
- `lineColor`
- `linePattern`
- `transparentColor`
- `block.x0`, `y0`, `x1`, `y1`

Version note:
- Requires Display support from `v1.25`.

### `CIRCLE`

Use `CIRCLE` for badges, markers, status dots, or decorative elements.

Important fields:
- `radius`
- `center.x`, `center.y`
- `fillColor`, `fillPattern`
- `strokeColor`, `strokePattern`
- `backgroundColor`
- `transparentColor`

Version note:
- Requires Display support from `v1.25`.

## 4A. Item-by-Item Authoring Checklist

Use this section as the quickest decision guide when composing a layout.

### `TEXT` checklist

Recommended use:
- Labels, values, headings, placeholders, icons, and calendar-bound text.

Required core fields:
- `text`
- `font`
- `block`

Use it like this:
- Use `TEXT` for all human-readable content.
- Add `id` only when the block needs a stable identifier or a calendar placeholder.
- Use `textAlign`, `lineSpace`, and `offset` to refine layout inside the block.

Hard constraints:
- Do not invent font names.
- At least one of `block.y` or `block.h` must be a multiple of `8`.
- Calendar placeholder IDs belong only on `TEXT`.
- If `id` is a reserved calendar placeholder, SyncSign will overwrite `text`.

Project guidance:
- Dense tables: prefer `DDIN_CONDENSED_*` or `ROBOTO_CONDENSED_24`.
- Large KPI values: prefer `DDIN_48`, `DDIN_64`, or `DDIN_128`.
- Chinese text: use documented `NOTO_*` fonts and remember the documented `4MB Flash Display` limitation.
- Icons should use `ICON_WEATHER`, `ICON_FA_SOLID`, or `ICON_FA_BRANDS` with the correct unicode value in `text`.

### `IMAGE` checklist

Recommended use:
- The built-in organization logo only.

Required core fields:
- `source`
- `name`
- `block`

Use it like this:
- Use `source: BUILD_IN`.
- Use `name: logo.bin`.
- Place the image by setting `block.x`, `block.y`, `block.w`, and `block.h`.

Hard constraints:
- In this project, do not use `source: CUSTOM` unless the maintainer explicitly asks for it.
- For the built-in logo, `block.w` and `block.h` must be `96` and `96`.
- `IMAGE.data.block.w` must be a multiple of `8`.

Project guidance:
- The source image is the organization's uploaded logo from `SyncSign client -> Settings -> Organization`.
- The logo asset should be a `96 x 96`, monochrome, `1-bit` `.bmp`.
- If the user wants any non-logo custom image, use `BITMAP_URI` instead.

### `BITMAP_URI` checklist

Recommended use:
- User-provided custom images fetched from a URL.
- Layered monochrome images for tri-color black/red output.

Required core fields:
- `uri`
- `foregroundColor`
- `backgroundColor`
- `transparentColor`
- `block`

Use it like this:
- Point `uri` to a BMP resource.
- Set `block` to the final rendered area on screen.
- Use one `BITMAP_URI` per monochrome layer.

Hard constraints:
- Keep the rendered area within the target Display's maximum canvas size.
- For `7.5` inch Displays in this project, cap the render area at `800 x 480`.
- HTTPS may fail if the required root certificates are not installed on the Hub or Display.

Project guidance:
- Prefer `BITMAP_URI` over `IMAGE` for custom pictures.
- The URL is cached, so change the filename or append a query string like `?v=2` when the image changes.
- For black/red pictures, split the artwork into two monochrome BMP files, then stack two `BITMAP_URI` items with the same `block`. Use `foregroundColor: BLACK` for one and `foregroundColor: RED` for the other.

### `RECTANGLE` checklist

Recommended use:
- Borders, panels, dividers, table cells, and card backgrounds.

Required core fields:
- `block`
- Usually `fillColor`, `strokeColor`, and `strokeThickness`

Use it like this:
- Use `RECTANGLE` as the default structural primitive for tables and dashboard cards.
- Use thin filled rectangles as dividers when you want maximum compatibility.

Hard constraints:
- `block.x` must be a multiple of `8`.
- `block.w` must be a multiple of `8`.
- `strokePattern`, `fillPattern`, and `transparentColor` need Display support from `v1.25`.

Project guidance:
- Prefer `RECTANGLE` over `LINE` when compatibility matters.
- For solid cell dividers, a narrow `RECTANGLE` is often safer than a `LINE`.

### `QRCODE` checklist

Recommended use:
- URLs, forms, check-in links, or any scan target.

Required core fields:
- `text`
- `position`
- `scale`
- `version`
- `eccLevel`

Use it like this:
- Choose `version` and `scale` together based on the available screen area.
- Place the QR code explicitly with `position.x` and `position.y`.

Hard constraints:
- The rendered width and height are both `(4 * version + 17) * scale`.
- On `4.2` inch Displays, QR areas above `25600` square pixels may fail to display.

Project guidance:
- Compute the QR size first, then confirm it fits the block you want.
- Use `QRCODE` only when the user truly needs scannable content; it consumes a lot of screen area.

### `LINE` checklist

Recommended use:
- Thin dividers or rules when the target Display supports it.

Required core fields:
- `backgroundColor`
- `lineColor`
- `linePattern`
- `transparentColor`
- `block.x0`, `block.y0`, `block.x1`, `block.y1`

Use it like this:
- Use `LINE` for simple separators when `v1.25+` support is acceptable.
- Define the start and end points explicitly.

Hard constraints:
- `LINE` requires Display support from `v1.25`.

Project guidance:
- If compatibility is uncertain, use a thin `RECTANGLE` instead.
- Reserve patterned lines for cases where the visual distinction matters enough to justify the version dependency.

### `CIRCLE` checklist

Recommended use:
- Status dots, badges, markers, or decorative round elements.

Required core fields:
- `radius`
- `center`
- Typically `fillColor` and `strokeColor`

Use it like this:
- Use `CIRCLE` for small emphasis marks, not for major layout framing.
- Keep the circle size modest so it does not dominate the screen.

Hard constraints:
- `CIRCLE` requires Display support from `v1.25`.
- If `strokeColor` is not `WHITE`, `fillColor` must match `strokeColor` or the fill will follow `strokeColor`.

Project guidance:
- Use `CIRCLE` for compact status indicators.
- For larger filled areas, prefer `RECTANGLE` unless a circular shape is visually necessary.

## 5. Calendar Template Field Semantics

Calendar templates are special because SyncSign will replace the `TEXT.data.text` value when `TEXT.data.id` matches one of the reserved IDs below.

### Ongoing event placeholders

- `ONGOING_EVENT_SUMMARY`: current event title/summary
- `ONGOING_CREATOR`: current event creator name
- `ONGOING_CREATOR_EMAIL`: current event creator email
- `ONGOING_ATTENDEES`: current event attendee count or attendee summary
- `ONGOING_ATTENDEES_LIST`: current event attendee list
- `ONGOING_TIME`: current event time range
- `ONGOING_TIME_WITH_YEAR`: old variant, marked obsolete

### Upcoming event placeholders

- `UPCOMING`: full forthcoming event list
- `UPCOMING_N_SUMMARY`: summary for the Nth upcoming event
- `UPCOMING_N_TIME`: time for the Nth upcoming event
- `UPCOMING_N_CREATOR`: creator for the Nth upcoming event
- `UPCOMING_N_CREATOR_EMAIL`: creator email for the Nth upcoming event
- `UPCOMING_N_ATTENDEES`: attendee summary for the Nth upcoming event
- `UPCOMING_N_ATTENDEES_LIST`: attendee list for the Nth upcoming event

Notes:
- Replace `N` with `1`, `2`, `3`, and so on.
- These reserved IDs affect only `TEXT` items whose `id` matches the documented placeholder name.

### Room and note placeholders

- `NOTE_AVAILABLE`: free/busy or availability note
- `NOTE_UNTIL`: note with end time
- `NOTE_UNTIL_WITH_YEAR`: old variant, marked obsolete
- `ROOM_NAME`: display room name
- `BOTTOM_BUTTONS`: system-controlled bottom buttons block

### Calendar block selection

Template selection is based on `status`:
- `BUSY`: SyncSign uses this block when an event is ongoing now.
- `FREE`: SyncSign uses this block when the first event is upcoming rather than ongoing.
- `ANY`: used for non-calendar data sources.

Authoring rules:
- Calendar templates pasted into SyncSign Cloud or SOPS should contain two template blocks under `layout`: one for `BUSY`, one for `FREE`.
- Non-calendar templates typically use a single `ANY` block.
- In calendar templates, `status` is not optional. It determines which visual block SyncSign picks at runtime.
- Reserved calendar placeholder IDs should be used only on `TEXT` items. They are not general-purpose IDs.
- If a `TEXT.id` uses a reserved placeholder name, any literal `text` value in that block should be treated as placeholder content that SyncSign will overwrite.

## 6. Practical Generation Rules for AI

When the user asks for a custom render:

1. Determine whether this is a direct render or a reusable calendar template.
2. Determine the display size, because all coordinates depend on it.
3. Build the page with explicit primitives.
4. Use `TEXT` for all labels and values.
5. Use `RECTANGLE` or `LINE` for table rules, borders, and cards.
6. Use reserved `TEXT.data.id` values only when the content should be filled by SyncSign automatically.
7. Keep within the documented pixel limits and version constraints.
8. Pick fonts only from the documented font list in this file.
9. If the user wants Chinese text, prefer the documented `NOTO_*` fonts and note the `4MB Flash Display` constraint when relevant.
10. If the request involves calendar templates, treat reserved `TEXT.id` values as data-binding hooks, not free-form labels.
11. Per maintainer guidance, do not propose `BOTTOM_CUSTOM_BUTTONS` or `PERIPHERAL_CONTROL` as interaction solutions unless the maintainer explicitly asks for them.

Heuristics that work well:
- Table or spreadsheet-like layout: `RECTANGLE` dividers plus centered `TEXT` blocks.
- Dashboard or KPI card layout: outer `RECTANGLE` cards plus large-font `TEXT`.
- Calendar template: two blocks, `BUSY` and `FREE`, with the same visual skeleton but different reserved IDs.


## 6A. Client-Editable Template Fields

For reusable templates pushed from the SyncSign client, a `TEXT` item can expose an input box in `Draw on Screen` when `data.property` is present.

Example shape:

```json
{
  "type": "TEXT",
  "data": {
    "text": "",
    "id": "LEFT_CELL",
    "font": "DDIN_CONDENSED_24",
    "textAlign": "CENTER",
    "block": { "x": 96, "y": 92, "w": 288, "h": 24 },
    "property": {
      "caption": "Left Cell",
      "control": "TEXTAREA",
      "minLength": 0,
      "maxLength": 64,
      "regex": "*"
    }
  }
}
```

What this means in practice:
- `property.caption` becomes the title shown above the input box in the SyncSign client.
- `property.control` determines the editor type. `TEXTAREA` is appropriate for general text entry.
- `minLength`, `maxLength`, and `regex` constrain what the user can enter in the client.

Editable-field authoring guidance:
- Use short, human-readable `caption` values because they become UI labels in the client.
- Keep `maxLength` realistic for the block size and selected font. Large values are allowed by JSON but can overflow visually.
- Treat `regex` as a validation rule for the editor. Use restrictive patterns only when the user truly needs them.
- Keep `text` empty or make it an intentional default value. The client editor will supply the actual final content.

Important binding rule learned from this project:
- Do not reuse the same `property.caption` across multiple editable fields that should hold different values.
- If multiple fields share the same caption, the client may treat them as one input and the last entered value can overwrite all of them.

Therefore:
- `id` should remain unique for the rendered item.
- `property.caption` should also be unique for each separately editable field.

Good examples:
- `Room Number`
- `Training Date Start`
- `Training Date End`
- `Trainee 1 Left`
- `Trainee 1 Right`
- `Training ID Line 1`
- `Instructor 2`

Use this pattern when the user wants:
- a table or card layout that is fixed structurally but editable in the SyncSign client
- a reusable template that non-technical users can fill before pushing to a Display
- client-side data entry without changing the JSON structure every time

See also:
- `examples/template-editable-table.json`
## 7. Ready-to-Adapt 4x4 Table Example

The example below targets a `4.2` inch Display (`400x300` canvas). It draws a 4x4 table using `RECTANGLE` dividers plus one centered `TEXT` item per cell.

Design choices:
- Outer margin: `20`
- Grid width: `360`
- Grid height: `240`
- Cell width: `90`
- Cell height: `60`
- Divider thickness: `2`

```json
{
  "layout": {
    "background": {
      "bgColor": "WHITE",
      "enableButtonZone": false
    },
    "items": [
      {
        "type": "RECTANGLE",
        "data": {
          "fillColor": "WHITE",
          "strokeColor": "BLACK",
          "strokeThickness": 2,
          "block": { "x": 16, "y": 28, "w": 368, "h": 244 }
        }
      },
      {
        "type": "RECTANGLE",
        "data": {
          "fillColor": "BLACK",
          "strokeThickness": 0,
          "block": { "x": 104, "y": 28, "w": 8, "h": 244 }
        }
      },
      {
        "type": "RECTANGLE",
        "data": {
          "fillColor": "BLACK",
          "strokeThickness": 0,
          "block": { "x": 192, "y": 28, "w": 8, "h": 244 }
        }
      },
      {
        "type": "RECTANGLE",
        "data": {
          "fillColor": "BLACK",
          "strokeThickness": 0,
          "block": { "x": 280, "y": 28, "w": 8, "h": 244 }
        }
      },
      {
        "type": "RECTANGLE",
        "data": {
          "fillColor": "BLACK",
          "strokeThickness": 0,
          "block": { "x": 16, "y": 88, "w": 368, "h": 4 }
        }
      },
      {
        "type": "RECTANGLE",
        "data": {
          "fillColor": "BLACK",
          "strokeThickness": 0,
          "block": { "x": 16, "y": 148, "w": 368, "h": 4 }
        }
      },
      {
        "type": "RECTANGLE",
        "data": {
          "fillColor": "BLACK",
          "strokeThickness": 0,
          "block": { "x": 16, "y": 208, "w": 368, "h": 4 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "A1",
          "id": "CELL_A1",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 20, "y": 36, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "A2",
          "id": "CELL_A2",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 108, "y": 36, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "A3",
          "id": "CELL_A3",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 196, "y": 36, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "A4",
          "id": "CELL_A4",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 284, "y": 36, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "B1",
          "id": "CELL_B1",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 20, "y": 96, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "B2",
          "id": "CELL_B2",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 108, "y": 96, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "B3",
          "id": "CELL_B3",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 196, "y": 96, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "B4",
          "id": "CELL_B4",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 284, "y": 96, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "C1",
          "id": "CELL_C1",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 20, "y": 156, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "C2",
          "id": "CELL_C2",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 108, "y": 156, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "C3",
          "id": "CELL_C3",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 196, "y": 156, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "C4",
          "id": "CELL_C4",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 284, "y": 156, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "D1",
          "id": "CELL_D1",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 20, "y": 216, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "D2",
          "id": "CELL_D2",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 108, "y": 216, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "D3",
          "id": "CELL_D3",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 196, "y": 216, "w": 84, "h": 48 }
        }
      },
      {
        "type": "TEXT",
        "data": {
          "text": "D4",
          "id": "CELL_D4",
          "font": "ROBOTO_CONDENSED_24",
          "textAlign": "CENTER",
          "block": { "x": 284, "y": 216, "w": 84, "h": 48 }
        }
      }
    ],
    "options": {
      "refreshScreen": true
    }
  }
}
```

How to adapt it:
- Replace `A1` to `D4` with real labels or values.
- If the user wants headers, dedicate the first row or first column to header styling.
- If the target is `2.9` inch or `7.5` inch, recalculate the cell widths and heights using that screen's max width and height.
- If the table comes from calendar data, keep the grid skeleton but replace selected cell `TEXT.id` values with SyncSign calendar placeholder IDs.

## 8. Important Constraints and Gotchas

- Prefer white text on red background, not black text on red background.
- A single block may be too large to display.
- On 2.9-inch Displays, when drawing the `background`, if one of `fillColor` and `bgColor` is `RED`, the other must also be `RED`.
- In `BACKGROUND`, `fillColor: WHITE` with `fillPattern: SOLID` can produce an all-black effect. Use `WHITE` with `NONE` to keep the interior white.
- In `CIRCLE`, if `strokeColor` is not `WHITE`, `fillColor` must match `strokeColor` or the fill will follow `strokeColor`.
- `background.rectangle.block` uses percentages, but most item blocks use pixels. Do not mix these mentally.
- `RECTANGLE.data.block.x` and `RECTANGLE.data.block.w` must be multiples of `8`.
- `IMAGE.data.block.w` must be a multiple of `8`.
- `BITMAP_URI` image areas should stay within the target Display's maximum canvas size.
- `TEXT.data.block.y` or `TEXT.data.block.h` must have at least one value that is a multiple of `8`.
- `QRCODE` size is `(4 * version + 17) * scale`, so check that square against the available canvas area before placing it.
- On `4.2` inch Displays, oversized QR blocks above `25600` square pixels may fail to render.
- `options.pollRate` is documented but deprecated. Prefer leaving it alone unless the user explicitly needs polling behavior.
- `options.refreshScreen` defaults to `true`. Setting it to `false` can reduce full refreshes but may leave e-ink ghosting or messy partial updates.
- If you include a `background` section, SyncSign will do a refresh of the screen. If the user wants to update only a portion with less blink, consider omitting `background`.
- For `BITMAP_URI`, HTTPS may fail unless the needed root certificates are installed on the Hub or Display.
- `BITMAP_URI` content is cached. To force an updated download, change the URL or append a version query such as `?v=2`.

## 9. Decision Shortcut

When the user says:
- "Render a 4x4 table": build a direct Web API `layout` using `RECTANGLE` plus `TEXT`.
- "Show room schedule": build a calendar template with `BUSY` and `FREE` blocks plus reserved `TEXT.id` placeholders.
- "Put a QR code on the lower right": use `QRCODE` with explicit `position`, `scale`, and `version`.
- "Show an uploaded logo": use `IMAGE`.
- "Show a remote bitmap": use `BITMAP_URI`.







