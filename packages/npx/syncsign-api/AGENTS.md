# Generic Agent Instructions

This repository is an agent-executed SyncSign skill.

Read `SKILL.md` before taking action.

Mandatory rules:
- Never read `.env`.
- Never inspect shell environment variables for SyncSign credentials.
- Never search the workspace, plugin folders, or memory files for API keys.
- Use only the atomic scripts in `scripts/`.
- If any SyncSign script returns `SYNCSIGN_API_KEY_MISSING` or exit code `2`, stop immediately and give the fixed setup guidance from `SKILL.md`.

