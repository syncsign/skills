# SyncSign Skills

Operate SyncSign Hubs and Displays from natural language through the public SyncSign Web API.

## Install

This repository now uses a single canonical source tree and two generated release artifacts.

**Option 1 - Claude Code plugin marketplace**

```bash
/plugin marketplace add syncsign/skills
```

Or install the specific plugin from that marketplace:

```bash
/plugin install syncsign-api@syncsign-marketplace
```

Claude uses the generated package at `plugins/syncsign-api`.

**Option 2 - npx (skills.sh)**

```bash
npx skills add syncsign/skills@syncsign-api
```

For repo-based `skills.sh` installs, the repository should expose the `syncsign-api` skill entry. The generated runtime artifact intended for `npx` distribution lives at `packages/npx/syncsign-api`.

Both methods install the same `syncsign-api` capability from different release artifacts.

## Build Artifacts

Canonical source files live at the repository root.

Generated outputs:
- `packages/npx/syncsign-api` for `skills.sh` runtime packaging
- `plugins/syncsign-api` for Claude marketplace packaging

Regenerate both packages with:

```bash
python scripts/build_release_artifacts.py
```

Or regenerate just one target:

```bash
python scripts/build_runtime_package.py
python scripts/build_claude_plugin.py
```

Do not edit files under `packages/npx/syncsign-api` or `plugins/syncsign-api` directly.

## Configuration

Run commands from the installed runtime root.

This project uses the public SyncSign API key routes only. Account email, account password, and login-token exchange are not part of this public skill bundle.

Create or edit the `.env` file in the current Skill runtime root with:

```env
SYNCSIGN_API_KEY=your_syncsign_api_key
```

If `.env` does not exist yet, create it or copy `.env.example` to `.env` first.

`SYNCSIGN_API_BASE_URL` is optional. Most users should leave it unset and use the built-in default API endpoint.

If you do not have an API key yet:

1. Open the SyncSign client.
2. Go to `Settings`.
3. Copy your API Key.
4. Paste it into the `.env` file in the current Skill runtime root.

`.env` is local-only and git-ignored.

## Core Capabilities

This skill currently supports:
- Account information lookup for the saved API key.
- Hub and device inventory lookup.
- Hub detail lookup by serial number.
- Display list and detail lookup by node ID or Hub serial number.
- Calendar binding and calendar subscription diagnosis for supported Display models `D75C-LEWI`, `D42C-LE`, and `D29C-LE`.
- Display sync troubleshooting based only on live API fields.
- Render submission to one Display or multiple Displays.
- Render status lookup by render ID.

## Rendering Knowledge Base

Custom Display rendering guidance now lives in `references/display-render-layout-knowledge.md`.

That reference summarizes:
- the official `layout` field semantics
- item and background field meanings
- calendar template placeholder IDs and `BUSY` / `FREE` block behavior
- generation rules for custom layouts such as `4x4` tables

Use it when the user asks for custom Display composition rather than a simple text-only render.

## Included Public API Endpoints

This project currently covers every route published in the SyncSign public Swagger document (`v2.0.0`):

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

Each route is implemented as an atomic Python script under `scripts/` in the canonical source tree and is copied into both generated artifacts.

## What You Can Ask

**User & Inventory**
> "Show my SyncSign account info."
> "List all Hubs under this API key."
> "Find all displays and tell me which are offline."

**Hub & Display Details**
> "Show details for hub SN ABCD1234."
> "List all displays attached to hub SN ABCD1234."
> "Get display details for node 123456."
> "Diagnose why display node 123456 is not syncing its calendar refresh."

**Rendering**
> "Render this layout to node 123456."
> "Push the same announcement to multiple displays."
> "Check whether render job abc-render-id has completed."

## Privacy

Credentials are stored only in the `.env` file in the current Skill runtime root, which is git-ignored. This public skill persists the API key and an optional base URL override only.

