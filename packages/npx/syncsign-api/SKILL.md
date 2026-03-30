---
name: syncsign-api
description: SyncSign Web API skill for user info, hub or device inventory, display or node details, and render operations using the public SyncSign API key routes.
version: 1.0.0
tools: [ "run_shell_command" ]
---

# SyncSign API Skill

Use this skill whenever the user is asking about SyncSign account info, Hubs, Displays, nodes, render jobs, or screen rendering through the public SyncSign Web API.

## What This Skill Can Do

If the user asks what this skill can do, answer from the capability list below.

This skill can:
- Show SyncSign account information for the saved API key.
- List Hubs and other devices under the saved API key.
- List Displays globally or under a specific Hub.
- Get detailed Hub information by serial number.
- Get detailed Display information by node ID, or by Hub serial number plus node ID.
- Diagnose supported calendar Display sync issues for models `D75C-LEWI`, `D42C-LE`, and `D29C-LE` using live API data.
- Check whether a supported Display has a calendar bound.
- Check whether a supported Display calendar subscription is healthy by verifying `watchResourceId` and `watchExpiration`.
- Identify whether an offline supported Display is more likely affected by Hub status, low battery, or low signal, based only on fields returned by the API.
- Submit render jobs to one Display or multiple Displays.
- Check render job status by render ID.

Do not claim unsupported capabilities. Do not promise diagnosis beyond the fields actually returned by the API.

## Non-Negotiable Agent Rules

1. Use only the atomic scripts in `scripts/` for business actions.
2. Never read `.env`.
3. Never inspect `Env:` or shell environment variables for SyncSign credentials.
4. Never search the workspace, plugin folders, memory files, or history for API keys.
5. Never attempt login, password exchange, token recovery, or credential guessing.
6. If any SyncSign script exits with code `2` or stderr contains `SYNCSIGN_API_KEY_MISSING`, stop immediately.
7. After `SYNCSIGN_API_KEY_MISSING`, do not run any more diagnostic commands. Do not inspect `.env`. Do not continue exploring. Respond with the fixed setup message and end the turn.
8. Unless the user or maintainer explicitly asks, do not add extra docs, code, scripts, sample files, or other repository artifacts just to satisfy a one-off operational request. Prefer direct execution or inline JSON instead.

Forbidden examples after `SYNCSIGN_API_KEY_MISSING`:
- `Get-Content .env`
- `dir .env`
- `Get-ChildItem Env:`
- `Get-ChildItem -Recurse -Filter .env`
- searching for `SYNCSIGN_API_KEY`
- reading generated packages to hunt for credentials

## First-Time Setup

Do not proactively read or inspect the `.env` file. Credentials are checked automatically when the atomic scripts run. If any SyncSign script exits with code `2` and stderr contains `SYNCSIGN_API_KEY_MISSING`, output the following message verbatim, then stop and wait for the user to confirm setup is complete before taking any further action.

### API Key Missing - Fixed Response

---

SyncSign API key is not configured.
Open the SyncSign client and go to Settings.
Copy your API Key and add it to the `.env` file in the current Skill runtime root.
If the file does not exist yet, create it first.

```env
SYNCSIGN_API_KEY=your_api_key_here
```

Save the file and let me know when it is ready.

---

Never ask the user to send secrets in chat. Never guess credentials.

## Before Every Shell Command

Before running any script, always output one short sentence in plain language explaining what you are about to do and why. Keep it under 15 words.

Examples:
- Checking your saved SyncSign account info.
- Listing hubs under your API key.
- Rendering the requested layout to the selected display.

## Command Base Path

Run all commands from the generated runtime root shown below, not from the source repo root, unless you are explicitly maintaining this project locally.

- Generated `npx` runtime package: `python scripts/syncsign_list_nodes.py`
- Claude marketplace package: `python scripts/syncsign_list_nodes.py`
- Source repo for maintainers only: `python scripts/syncsign_list_nodes.py`

## Runtime Layout

Generated `npx` runtime package layout:

```text
runtime-root/
|- SKILL.md
|- README.md
|- requirements.txt
|- .env.example
|- examples/
|  |- render-batch.json
|  \- render-single.json
|- syncsign-swagger.json
|- scripts/
|  \- syncsign_*.py
\- common/
   |- syncsign_auth.py
   \- syncsign_client.py
```

Claude marketplace package layout:

```text
runtime-root/
|- .claude-plugin/
|  \- plugin.json
|- examples/
|  |- render-batch.json
|  \- render-single.json
|- requirements.txt
|- .env.example
|- syncsign-swagger.json
|- scripts/
|  \- syncsign_*.py
|- common/
|- skills/
|  \- syncsign-api/
|     \- SKILL.md
\- README.generated.md
```

Canonical source repo layout for maintainers:

```text
source-root/
|- common/
|- examples/
|  |- render-batch.json
|  \- render-single.json
|- references/
|- scripts/
|  |- build_release_artifacts.py
|  |- build_runtime_package.py
|  |- build_claude_plugin.py
|  \- syncsign_*.py
|- packages/
|  \- npx/
|     \- syncsign-api/
|- plugins/
|  \- syncsign-api/
|- README.md
\- SKILL.md
```

## Output Contract

- `stdout`: JSON data on success
- `stderr`: error messages only
- `exit code`: `0` success, `1` failure, `2` missing API key

## Core Workflow

1. Prefer the existing atomic scripts in `scripts/`. Do not replace them with ad hoc `curl` or one-off Python snippets unless you are patching the project itself.
2. Resolve identifiers before detail calls:
   - If `sn` is unknown, start with `syncsign_list_devices.py`
   - If `node_id` is unknown for a hub, start with `syncsign_list_device_nodes.py`
   - If `node_id` is unknown globally, start with `syncsign_list_nodes.py`
   - If `render_id` is unknown, only fetch it from the response of a prior render call
3. Treat render operations as side-effecting:
   - Make sure the target node or nodes are unambiguous
   - Use the user's requested layout exactly
   - Prefer `--body-file` for larger JSON payloads
   - After a render request, use `syncsign_get_render.py` when the user asks for final execution status or when you need to confirm delivery
4. The public routes in this skill authenticate only with the SyncSign API key saved in `.env`.

## Custom Rendering Reference

For custom Display composition, read the co-located `references/display-render-layout-knowledge.md`.

Use these repository-validated canvas sizes for layout coordinates in this project:
- `7.5 Inch`: `800 x 480`
- `4.2 Inch`: `400 x 300`
- `2.9 Inch`: `296 x 128`

If the official Hub SDK examples show different dimensions for `7.5 Inch`, prefer these repository-validated dimensions when rendering through this skill unless the user explicitly says otherwise.

Example request bodies are stored under `examples/`:
- `examples/render-single.json`: sample body for `syncsign_post_node_render.py` when rendering to one Display.
- `examples/render-batch.json`: sample body for `syncsign_post_nodes_render.py` when rendering the same or different layouts to multiple Displays.
- `examples/template-editable-table.json`: sample reusable template showing how `TEXT.data.property.caption` creates client-side input fields for custom table content.

Use that reference when the user asks for:
- custom `layout` JSON authoring
- tables, dashboards, cards, or mixed text-and-shape compositions
- calendar template customization with `BUSY` / `FREE` blocks
- calendar placeholder IDs such as `ONGOING_EVENT_SUMMARY` or `UPCOMING_1_TIME`
- SyncSign client editable templates where users should fill table cells or other text fields before pushing content to a Display

That knowledge base summarizes the official SyncSign rendering and calendar template docs and includes a ready-to-adapt `4x4` table example.

## Scripts

### User
- `python scripts/syncsign_get_user_info.py`

### Hubs / Devices
- `python scripts/syncsign_list_devices.py`
- `python scripts/syncsign_get_device_detail.py --sn <SN>`

### Displays / Nodes
- `python scripts/syncsign_list_device_nodes.py --sn <SN>`
- `python scripts/syncsign_get_device_node.py --sn <SN> --node_id <NODE_ID>`
- `python scripts/syncsign_list_nodes.py`
- `python scripts/syncsign_get_node.py --node_id <NODE_ID>`
- `python scripts/syncsign_diagnose_display_sync.py --node_id <NODE_ID>`
- `python scripts/syncsign_diagnose_display_sync.py --sn <SN> --node_id <NODE_ID>`

### Rendering
- `python scripts/syncsign_post_node_render.py --node_id <NODE_ID> --body-file <PATH>`
- `python scripts/syncsign_post_nodes_render.py --body-file <PATH>`
- `python scripts/syncsign_get_render.py --render_id <RENDER_ID>`

## Public API Coverage

The bundled `syncsign-swagger.json` mirrors the published SyncSign Swagger document at `https://dev.sync-sign.com/webapi/swagger.json?v=2.0.0`.

Covered routes:
- `GET /key/{api_key}`
- `GET /key/{api_key}/devices`
- `GET /key/{api_key}/devices/{sn}`
- `GET /key/{api_key}/devices/{sn}/nodes`
- `GET /key/{api_key}/devices/{sn}/nodes/{node_id}`
- `GET /key/{api_key}/nodes`
- `GET /key/{api_key}/nodes/{node_id}`
- `POST /key/{api_key}/nodes/{node_id}/renders`
- `POST /key/{api_key}/renders`
- `GET /key/{api_key}/renders/{render_id}`
## Display Sync Troubleshooting

Use this workflow when the user says a Display is not syncing or refreshing correctly.

This troubleshooting flow only applies to these Display models:
- `D75C-LEWI`
- `D42C-LE`
- `D29C-LE`

For any other Display model, say that this troubleshooting flow is not available for that model and refer the user to SyncSign Support.

### Evidence Rule

Only diagnose from fields that are actually returned by the API response. Do not guess or invent missing states.

If the API does not provide enough information for the next required decision, say exactly that there is not enough information from the API to continue the diagnosis. Then refer the user to SyncSign Support:
- `https://help.sync-sign.com`
- `help@sync-sign.com`

Never hallucinate Hub status, Display status, calendar status, battery cause, signal cause, or subscription status when the required API fields are missing.

### Required Concepts

- `Calendar bound`: the Display response includes a `calendar` object with calendar information.
- `Calendar subscription successful`: inside `calendar`, both `watchResourceId` and `watchExpiration` are present, and `watchExpiration` is still in the future and within the next 24 hours.
- `Calendar subscription failed`: `watchResourceId` is missing, `watchExpiration` is missing, or `watchExpiration` is already expired. Treat an expired subscription exactly the same as a missing subscription.

### Required Diagnostic Order

1. Check whether the Display is online.
2. If the Display is online:
   - Check whether a calendar is bound.
   - If a calendar is bound, check whether the calendar subscription is successful.
3. If the Display is offline:
   - Check whether the nearby Hub is online.
   - If the Hub is offline, prioritize restoring the Hub first.
   - If the Hub is online, inspect battery level and signal level from the Display detail.

### Preferred Command

Use the diagnosis script whenever possible:

```bash
python scripts/syncsign_diagnose_display_sync.py --node_id <NODE_ID>
python scripts/syncsign_diagnose_display_sync.py --sn <SN> --node_id <NODE_ID>
```

### Online Display Guidance

- If the Display is online and no calendar is bound, tell the user to bind the calendar from the Display configuration page in the SyncSign client.
- If the Display is online and the calendar is bound but the subscription fields are missing, tell the user the calendar subscription failed. Instruct them to unbind the calendar and bind it again, then check whether the Display can sync and refresh.
- If the Display is online and `watchExpiration` is expired, treat that as the same subscription failure and give the same unbind-and-rebind guidance.

### Offline Display Guidance

If the Display is offline, first explain that the battery and signal values returned by the API are the last values reported while the Display was still online.

For Displays paired with a Hub:

- If the Hub is offline, tell the user to restore the Hub first by power cycling it or re-adding it in the app.
- If the Hub is online, the likely causes to check are low battery and low signal.
- If the API does not provide enough information to confirm the nearby Hub status, do not guess. Tell the user there is not enough information from the API and refer them to SyncSign Support.

Thresholds:

- Battery below `15%` needs attention.
- Signal below `30%` needs attention.

Battery guidance by model:

- `D75C-LEWI` and `D42C-LE`: charge the Display with the matching power adapter and power cable.
- `D29C-LE`: replace the `AA 1.5V` batteries.

Signal guidance:

- Reposition the Hub and Display higher in the space when possible.
- Avoid obstacles and signal interference sources.
- Recommend keeping signal above `30%` for stable operation.

If the Display is offline, the Hub is online, and the returned API fields do not show a clear battery or signal issue, do not invent another cause. Say there is not enough information from the API and refer the user to SyncSign Support.

### Real Signal Check in the SyncSignr App

Tell the user they can check the real current Display signal like this:

1. Press the pinhole button on the Display for `1 second`.
2. Open the Display configuration page in the `SyncSignr` app.
3. Check whether `Last Seen` updates to the current time.
4. If `Last Seen` updates to the current time, the displayed signal level is the real current signal level at that position.



