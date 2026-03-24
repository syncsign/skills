# SyncSign Skills

Operate SyncSign Hubs and Displays from natural language through the public SyncSign Web API.

## Install

**Option 1 - Claude Code plugin marketplace**

```bash
/plugin marketplace add syncsign/skills
```

Or install the specific plugin from that marketplace:

```bash
/plugin install syncsign-api@syncsign-marketplace
```

**Option 2 - npx (skills.sh)**

```bash
npx skills add syncsign/skills
```

Both methods install the single root skill `syncsign-api`.

## Configuration

Run commands from the installed runtime root.

This project uses the public SyncSign API key routes only. Account email, account password, and login-token exchange are not part of this public skill bundle.

Create or edit the `.env` file in the current Skill runtime root with:

```env
SYNCSIGN_API_KEY=your_syncsign_api_key
SYNCSIGN_API_BASE_URL=https://api.sync-sign.com/v2
```

If you do not have an API key yet:

1. Open the SyncSign client.
2. Go to `Settings`.
3. Copy your API Key.
4. Paste it into the `.env` file in the current Skill runtime root.

`.env` is local-only and git-ignored.

## Claude Packaging

The canonical source layout stays at the repository root so `npx skills add` and other agents can read the repo directly.

Claude marketplace publishing uses a generated, self-contained package at `plugins/syncsign-api`. Regenerate that package with:

```bash
python scripts/build_claude_plugin.py
```

Do not edit files under `plugins/syncsign-api` directly. Treat that directory as a generated release artifact.

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

Each route is implemented as an atomic Python script under `scripts/`.

## What You Can Ask

**User & Inventory**
> "Show my SyncSign account info."
> "List all Hubs under this API key."
> "Find all displays and tell me which are offline."

**Hub & Display Details**
> "Show details for hub SN ABCD1234."
> "List all displays attached to hub SN ABCD1234."
> "Get display details for node 123456."

**Rendering**
> "Render this layout to node 123456."
> "Push the same announcement to multiple displays."
> "Check whether render job abc-render-id has completed."

## Privacy

Credentials are stored only in the `.env` file in the current Skill runtime root, which is git-ignored. This public skill persists the API key and optional base URL only.
