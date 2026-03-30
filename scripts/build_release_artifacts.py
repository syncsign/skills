import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = REPO_ROOT / "packages" / "npx" / "syncsign-api"
CLAUDE_ROOT = REPO_ROOT / "plugins" / "syncsign-api"
IGNORE_PATTERNS = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")
ACTION_SCRIPT_GLOB = "syncsign_*.py"

PLUGIN_MANIFEST = {
    "name": "syncsign-api",
    "version": "1.0.0",
    "description": "SyncSign Web API assistant for account info, hubs, displays, node details, and rendering operations through the public API key routes.",
    "author": {
        "name": "SyncSign",
    },
    "license": "MIT",
    "keywords": [
        "syncsign",
        "display",
        "hub",
        "node",
        "render",
        "signage",
        "api key",
    ],
    "skills": "./skills/syncsign-api",
}

RUNTIME_README = """# Generated Runtime Package

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
"""

CLAUDE_NOTICE = """# Generated Package

This directory is a generated Claude marketplace package.

Do not edit files in this directory directly. Update the canonical source files in the repository root and regenerate this package with:

```bash
python scripts/build_release_artifacts.py
```

Custom layout guidance is bundled under:

`skills/syncsign-api/references/display-render-layout-knowledge.md`
"""

COMMON_FILE_COPIES = [
    ("requirements.txt", "requirements.txt"),
    ("LICENSE", "LICENSE"),
    (".env.example", ".env.example"),
    ("AGENTS.md", "AGENTS.md"),
    ("GEMINI.md", "GEMINI.md"),
]

REFERENCE_FILE_COPIES = [
    ("references/display-render-layout-knowledge.md", "references/display-render-layout-knowledge.md"),
]

EXAMPLE_FILE_COPIES = [
    ("examples/render-batch.json", "examples/render-batch.json"),
    ("examples/render-single.json", "examples/render-single.json"),
    ("examples/template-editable-table.json", "examples/template-editable-table.json"),
]

RUNTIME_FILE_COPIES = COMMON_FILE_COPIES + [
    (".claude-plugin/syncsign-swagger.json", "syncsign-swagger.json"),
] + REFERENCE_FILE_COPIES + EXAMPLE_FILE_COPIES

CLAUDE_FILE_COPIES = COMMON_FILE_COPIES + [
    (".claude-plugin/syncsign-swagger.json", "syncsign-swagger.json"),
    (
        "references/display-render-layout-knowledge.md",
        "skills/syncsign-api/references/display-render-layout-knowledge.md",
    ),
] + EXAMPLE_FILE_COPIES

RUNTIME_REQUIRED_OUTPUTS = [
    "SKILL.md",
    "README.md",
    "requirements.txt",
    ".env.example",
    "AGENTS.md",
    "GEMINI.md",
    "references/display-render-layout-knowledge.md",
    "common/syncsign_auth.py",
    "common/syncsign_client.py",
    "scripts/syncsign_get_user_info.py",
    "scripts/syncsign_list_devices.py",
    "examples/render-batch.json",
    "examples/render-single.json",
    "examples/template-editable-table.json",
    "syncsign-swagger.json",
]

CLAUDE_REQUIRED_OUTPUTS = [
    ".claude-plugin/plugin.json",
    "skills/syncsign-api/SKILL.md",
    "requirements.txt",
    ".env.example",
    "AGENTS.md",
    "GEMINI.md",
    "skills/syncsign-api/references/display-render-layout-knowledge.md",
    "common/syncsign_auth.py",
    "common/syncsign_client.py",
    "examples/template-editable-table.json",
    "scripts/syncsign_get_user_info.py",
    "scripts/syncsign_list_devices.py",
    "examples/render-batch.json",
    "examples/render-single.json",
    "syncsign-swagger.json",
    "README.generated.md",
]


def ensure_exists(path):
    if not path.exists():
        raise FileNotFoundError(f"Required source path is missing: {path}")


def reset_dir(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_file(src_rel, dst_root, dst_rel):
    src = REPO_ROOT / src_rel
    dst = dst_root / dst_rel
    ensure_exists(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_common_dir(dst_root):
    src = REPO_ROOT / "common"
    dst = dst_root / "common"
    ensure_exists(src)
    shutil.copytree(src, dst, ignore=IGNORE_PATTERNS)


def copy_action_scripts(dst_root):
    scripts_dir = dst_root / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    for src in sorted((REPO_ROOT / "scripts").glob(ACTION_SCRIPT_GLOB)):
        shutil.copy2(src, scripts_dir / src.name)


def write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_runtime_package():
    reset_dir(RUNTIME_ROOT)
    copy_common_dir(RUNTIME_ROOT)
    copy_action_scripts(RUNTIME_ROOT)
    for src_rel, dst_rel in RUNTIME_FILE_COPIES:
        copy_file(src_rel, RUNTIME_ROOT, dst_rel)
    copy_file("SKILL.md", RUNTIME_ROOT, "SKILL.md")
    write_text(RUNTIME_ROOT / "README.md", RUNTIME_README)
    validate_package(RUNTIME_ROOT, RUNTIME_REQUIRED_OUTPUTS)


def write_plugin_manifest():
    manifest_path = CLAUDE_ROOT / ".claude-plugin" / "plugin.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(PLUGIN_MANIFEST, indent=2) + "\n", encoding="utf-8")


def write_claude_package():
    reset_dir(CLAUDE_ROOT)
    copy_common_dir(CLAUDE_ROOT)
    copy_action_scripts(CLAUDE_ROOT)
    for src_rel, dst_rel in CLAUDE_FILE_COPIES:
        copy_file(src_rel, CLAUDE_ROOT, dst_rel)
    copy_file("SKILL.md", CLAUDE_ROOT, "skills/syncsign-api/SKILL.md")
    write_plugin_manifest()
    write_text(CLAUDE_ROOT / "README.generated.md", CLAUDE_NOTICE)
    validate_package(CLAUDE_ROOT, CLAUDE_REQUIRED_OUTPUTS)


def validate_package(root, required_outputs):
    missing = [path for path in required_outputs if not (root / path).exists()]
    if missing:
        raise FileNotFoundError(
            f"Generated package is missing required files under {root}: " + ", ".join(missing)
        )

    pycache_entries = list(root.rglob("__pycache__"))
    if pycache_entries:
        raise RuntimeError(
            "Generated package contains __pycache__ directories: "
            + ", ".join(str(path.relative_to(root)) for path in pycache_entries)
        )

    compiled_entries = list(root.rglob("*.pyc")) + list(root.rglob("*.pyo"))
    if compiled_entries:
        raise RuntimeError(
            "Generated package contains compiled Python files: "
            + ", ".join(str(path.relative_to(root)) for path in compiled_entries)
        )


def build_release_artifacts(include_runtime=True, include_claude=True):
    if include_runtime:
        write_runtime_package()
    if include_claude:
        write_claude_package()


if __name__ == "__main__":
    build_release_artifacts()
    print(f"Generated npx runtime package at {RUNTIME_ROOT}")
    print(f"Generated Claude plugin package at {CLAUDE_ROOT}")






