import argparse
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from common.syncsign_auth import load_saved_credentials_or_exit
from common.syncsign_client import SyncSignApiError, SyncSignTransportError, load_json_body, print_json, request_api


def main():
    parser = argparse.ArgumentParser(description="Render content to a single SyncSign node.")
    parser.add_argument("--node_id", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body")
    group.add_argument("--body-file")
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    creds = load_saved_credentials_or_exit()

    try:
        body = load_json_body(body_text=args.body, body_file=args.body_file)
        result = request_api(
            "POST",
            "/key/{api_key}/nodes/{node_id}/renders",
            api_key=creds["api_key"],
            base_url=creds["base_url"],
            path_params={"node_id": args.node_id},
            body=body,
            timeout=args.timeout,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
    except (SyncSignApiError, SyncSignTransportError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print_json(result)


if __name__ == "__main__":
    main()
