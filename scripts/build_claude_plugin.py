import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "plugins" / "syncsign-api"
IGNORE_PATTERNS = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")
PACKAGE_NOTICE = """# Generated Package

This directory is a generated Claude marketplace package.

Do not edit files in this directory directly. Update the canonical source files in the repository root and regenerate this package with:

```bash
python scripts/build_claude_plugin.py
```
"""

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

DIRECTORY_COPIES = [
    ("common", "common"),
    ("scripts", "scripts"),
]

FILE_COPIES = [
    ("requirements.txt", "requirements.txt"),
    ("LICENSE", "LICENSE"),
    ("AGENTS.md", "AGENTS.md"),
    ("GEMINI.md", "GEMINI.md"),
    (".claude-plugin/syncsign-swagger.json", "syncsign-swagger.json"),
]

REQUIRED_OUTPUTS = [
    ".claude-plugin/plugin.json",
    "skills/syncsign-api/SKILL.md",
    "scripts/syncsign_get_user_info.py",
    "common/syncsign_auth.py",
    "common/syncsign_client.py",
    "syncsign-swagger.json",
    "README.generated.md",
    "AGENTS.md",
    "GEMINI.md",
]


def ensure_exists(path):
    if not path.exists():
        raise FileNotFoundError(f"Required source path is missing: {path}")


def copy_tree(src_rel, dst_rel):
    src = REPO_ROOT / src_rel
    dst = PACKAGE_ROOT / dst_rel
    ensure_exists(src)
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, ignore=IGNORE_PATTERNS)


def copy_file(src_rel, dst_rel):
    src = REPO_ROOT / src_rel
    dst = PACKAGE_ROOT / dst_rel
    ensure_exists(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_plugin_manifest():
    manifest_path = PACKAGE_ROOT / ".claude-plugin" / "plugin.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(PLUGIN_MANIFEST, indent=2) + "\n", encoding="utf-8")


def write_skill():
    src = REPO_ROOT / "SKILL.md"
    dst = PACKAGE_ROOT / "skills" / "syncsign-api" / "SKILL.md"
    ensure_exists(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_package_notice():
    notice_path = PACKAGE_ROOT / "README.generated.md"
    notice_path.write_text(PACKAGE_NOTICE, encoding="utf-8")


def prune_generated_artifacts():
    for pycache_dir in PACKAGE_ROOT.rglob("__pycache__"):
        shutil.rmtree(pycache_dir)
    for compiled_file in list(PACKAGE_ROOT.rglob("*.pyc")) + list(PACKAGE_ROOT.rglob("*.pyo")):
        compiled_file.unlink()


def validate_package():
    missing = [path for path in REQUIRED_OUTPUTS if not (PACKAGE_ROOT / path).exists()]
    if missing:
        raise FileNotFoundError("Generated package is missing required files: " + ", ".join(missing))

    pycache_entries = list(PACKAGE_ROOT.rglob("__pycache__"))
    if pycache_entries:
        raise RuntimeError(
            "Generated package contains __pycache__ directories: "
            + ", ".join(str(path.relative_to(PACKAGE_ROOT)) for path in pycache_entries)
        )

    pyc_entries = list(PACKAGE_ROOT.rglob("*.pyc"))
    if pyc_entries:
        raise RuntimeError(
            "Generated package contains compiled Python files: "
            + ", ".join(str(path.relative_to(PACKAGE_ROOT)) for path in pyc_entries)
        )


def main():
    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)

    for src_rel, dst_rel in DIRECTORY_COPIES:
        copy_tree(src_rel, dst_rel)

    for src_rel, dst_rel in FILE_COPIES:
        copy_file(src_rel, dst_rel)

    write_plugin_manifest()
    write_skill()
    write_package_notice()
    prune_generated_artifacts()
    validate_package()
    print(f"Generated Claude plugin package at {PACKAGE_ROOT}")


if __name__ == "__main__":
    main()
