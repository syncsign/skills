import argparse
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from common.syncsign_auth import load_saved_credentials_or_exit
from common.syncsign_client import SyncSignApiError, SyncSignTransportError, print_json, request_api


def main():
    parser = argparse.ArgumentParser(description="Get a SyncSign render job result by render ID.")
    parser.add_argument("--render_id", required=True)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    creds = load_saved_credentials_or_exit()

    try:
        result = request_api(
            "GET",
            "/key/{api_key}/renders/{render_id}",
            api_key=creds["api_key"],
            base_url=creds["base_url"],
            path_params={"render_id": args.render_id},
            timeout=args.timeout,
        )
    except (SyncSignApiError, SyncSignTransportError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print_json(result)


if __name__ == "__main__":
    main()
