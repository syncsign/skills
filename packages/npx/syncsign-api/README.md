# Generated Runtime Package

This directory is the generated SyncSign runtime package for `skills.sh` / `npx` distribution.

Do not edit files in this directory directly. Update the canonical source files in the repository root and regenerate this package with:

```bash
python scripts/build_release_artifacts.py
```

## First-Time Setup

1. Create `.env` in this directory, or copy `.env.example` to `.env`.
2. Add your SyncSign API key:

```env
SYNCSIGN_API_KEY=your_syncsign_api_key
```

3. Save the file, then rerun your request.

## Custom Rendering Reference

For custom layout and calendar-template authoring, see:

`references/display-render-layout-knowledge.md`
