import json
import urllib.error
import urllib.parse
import urllib.request


CLIENT_VERSION = "1.0.0"
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "User-Agent": f"syncsign-skills/{CLIENT_VERSION}",
    "X-Client-Name": "syncsign-skills",
    "X-Client-Version": CLIENT_VERSION,
}


class SyncSignApiError(RuntimeError):
    def __init__(self, status_code, body, url):
        message = f"HTTP {status_code}"
        if body:
            message = f"{message} - {body}"
        super().__init__(message)
        self.status_code = status_code
        self.body = body
        self.url = url


class SyncSignTransportError(RuntimeError):
    pass


def build_path(path_template, api_key, path_params=None):
    params = {"api_key": api_key}
    params.update(path_params or {})

    rendered = path_template
    for key, value in params.items():
        rendered = rendered.replace("{" + key + "}", urllib.parse.quote(str(value), safe=""))
    return rendered


def request_api(method, path_template, api_key, base_url, path_params=None, body=None, timeout=30.0):
    path = build_path(path_template, api_key=api_key, path_params=path_params)
    url = f"{base_url}{path}"
    headers = dict(DEFAULT_HEADERS)
    data = None

    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"

    request = urllib.request.Request(
        url=url,
        data=data,
        headers=headers,
        method=method.upper(),
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise SyncSignApiError(exc.code, body_text, url) from exc
    except urllib.error.URLError as exc:
        raise SyncSignTransportError(str(exc.reason)) from exc

    if not raw.strip():
        return {}

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def validate_api_key(api_key, base_url, timeout=20.0):
    try:
        request_api(
            "GET",
            "/key/{api_key}",
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
        return True, None
    except SyncSignApiError as exc:
        return False, str(exc)
    except SyncSignTransportError as exc:
        return False, f"NETWORK_ERROR: {exc}"


def load_json_body(body_text=None, body_file=None):
    if bool(body_text) == bool(body_file):
        raise ValueError("Provide exactly one of --body or --body-file.")

    raw = body_text
    if body_file:
        with open(body_file, "r", encoding="utf-8") as handle:
            raw = handle.read()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON body: {exc}") from exc


def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))
