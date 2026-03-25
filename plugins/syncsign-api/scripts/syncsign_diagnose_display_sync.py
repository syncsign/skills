import argparse
import sys
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from common.syncsign_auth import load_saved_credentials_or_exit
from common.syncsign_client import SyncSignApiError, SyncSignTransportError, print_json, request_api
from common.syncsign_display_diagnostics import diagnose_display_sync


def unwrap_response(payload):
    if isinstance(payload, dict) and "data" in payload:
        return payload.get("data")
    return payload


def fetch_node(creds, node_id, timeout, sn=None):
    if sn:
        return unwrap_response(
            request_api(
                "GET",
                "/key/{api_key}/devices/{sn}/nodes/{node_id}",
                api_key=creds["api_key"],
                base_url=creds["base_url"],
                path_params={"sn": sn, "node_id": node_id},
                timeout=timeout,
            )
        )

    return unwrap_response(
        request_api(
            "GET",
            "/key/{api_key}/nodes/{node_id}",
            api_key=creds["api_key"],
            base_url=creds["base_url"],
            path_params={"node_id": node_id},
            timeout=timeout,
        )
    )


def fetch_hub_detail(creds, hub_sn, timeout):
    if not hub_sn:
        return None
    return unwrap_response(
        request_api(
            "GET",
            "/key/{api_key}/devices/{sn}",
            api_key=creds["api_key"],
            base_url=creds["base_url"],
            path_params={"sn": hub_sn},
            timeout=timeout,
        )
    )


def main():
    parser = argparse.ArgumentParser(
        description="Diagnose SyncSign display sync and calendar subscription status for supported calendar display models."
    )
    parser.add_argument("--node_id", required=True)
    parser.add_argument("--sn")
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    creds = load_saved_credentials_or_exit()

    try:
        node = fetch_node(creds, node_id=args.node_id, sn=args.sn, timeout=args.timeout)
        hub_detail = fetch_hub_detail(creds, hub_sn=node.get("thingName"), timeout=args.timeout)
    except (SyncSignApiError, SyncSignTransportError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    now_ms = int(time.time() * 1000)
    diagnosis = diagnose_display_sync(node=node, now_ms=now_ms, hub_detail=hub_detail)
    diagnosis["node_id"] = args.node_id
    if args.sn:
        diagnosis["requested_sn"] = args.sn
    diagnosis["evaluated_at_ms"] = now_ms
    print_json(diagnosis)


if __name__ == "__main__":
    main()

