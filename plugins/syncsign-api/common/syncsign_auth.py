import sys
from pathlib import Path


DEFAULT_BASE_URL = "https://api.sync-sign.com/v2"
ENV_KEY_ORDER = [
    "SYNCSIGN_API_KEY",
    "SYNCSIGN_API_BASE_URL",
]


def resolve_runtime_root():
    repo_root = Path(__file__).resolve().parents[1]
    parent = repo_root.parent
    grandparent = parent.parent

    if parent.name == "plugins" and (grandparent / ".claude-plugin" / "marketplace.json").exists():
        return grandparent

    return repo_root


ROOT_DIR = resolve_runtime_root()
ENV_PATH = ROOT_DIR / ".env"


def read_env_map():
    data = {}
    if not ENV_PATH.exists():
        return data

    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        data[key] = value
    return data


def write_env_values(values):
    current = read_env_map()
    for key, value in values.items():
        if value is None:
            current.pop(key, None)
        else:
            current[key] = value

    rendered = []
    for key in ENV_KEY_ORDER:
        if key in current:
            rendered.append(f"{key}={current[key]}")

    remaining = sorted(key for key in current if key not in ENV_KEY_ORDER)
    rendered.extend(f"{key}={current[key]}" for key in remaining)
    ENV_PATH.write_text("\n".join(rendered) + "\n", encoding="utf-8")


def normalize_base_url(value):
    base_url = (value or DEFAULT_BASE_URL).strip()
    if not base_url:
        base_url = DEFAULT_BASE_URL
    return base_url.rstrip("/")


def load_saved_credentials():
    env = read_env_map()
    return {
        "api_key": env.get("SYNCSIGN_API_KEY"),
        "base_url": normalize_base_url(env.get("SYNCSIGN_API_BASE_URL")),
        "env_path": str(ENV_PATH),
    }


def print_credentials_missing_and_exit():
    print("SYNCSIGN_API_KEY_MISSING", file=sys.stderr)
    print("AGENT_MUST_STOP", file=sys.stderr)
    print("Do not read .env.", file=sys.stderr)
    print("Do not inspect environment variables.", file=sys.stderr)
    print("Do not search the workspace for API keys.", file=sys.stderr)
    print("SyncSign API key is not configured.", file=sys.stderr)
    print("Open the SyncSign client and go to Settings.", file=sys.stderr)
    print("Copy your API Key and add it to the .env file in the current Skill runtime root.", file=sys.stderr)
    print("Required:", file=sys.stderr)
    print("  SYNCSIGN_API_KEY=your_api_key_here", file=sys.stderr)
    print("Optional:", file=sys.stderr)
    print(f"  SYNCSIGN_API_BASE_URL={DEFAULT_BASE_URL}", file=sys.stderr)
    print("Save the file and rerun the command.", file=sys.stderr)
    sys.exit(2)


def load_saved_credentials_or_exit():
    credentials = load_saved_credentials()
    if not credentials.get("api_key"):
        print_credentials_missing_and_exit()
    return credentials
