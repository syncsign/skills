# Gemini / Generic Agent Bridge

Read `SKILL.md` first and follow it as the primary runtime contract for this repository.

Hard rules:
- Never read `.env`.
- Never inspect environment variables for `SYNCSIGN_API_KEY`.
- Never search the workspace for credentials.
- Use only the atomic scripts in `scripts/` for SyncSign actions.
- If any SyncSign script prints `SYNCSIGN_API_KEY_MISSING` or exits with code `2`, stop immediately.
- After that signal, do not run any more commands. Tell the user to open SyncSign client `Settings`, copy the API Key, add it to `.env` in the current runtime root, then stop.

