import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Optional, Tuple


DEFAULT_HEADERS: Dict[str, str] = {
    # Some WAF/CDN setups block the default Python urllib user-agent.
    # Use a common, benign UA by default; callers may override.
    "User-Agent": "curl/8.5.0",
    "Accept": "*/*",
}


def post_form(
    url: str,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    data: Optional[Dict[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
) -> Tuple[int, str]:
    """POST form-encoded data to `url` using `urllib`.

    If `client_id` and `client_secret` are provided, adds a Basic
    Authorization header.

    Returns (status_code, response_text).
    """

    body = urllib.parse.urlencode(data or {}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")

    hdrs = dict(DEFAULT_HEADERS)
    hdrs.update(headers or {})
    hdrs.setdefault("Content-Type", "application/x-www-form-urlencoded")
    if client_id and client_secret:
        creds = f"{client_id}:{client_secret}".encode("utf-8")
        hdrs["Authorization"] = "Basic " + base64.b64encode(creds).decode("ascii")

    for k, v in hdrs.items():
        req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp_text = resp.read().decode("utf-8")
            return resp.getcode(), resp_text
    except urllib.error.HTTPError as e:
        try:
            text = e.read().decode("utf-8")
        except Exception:
            text = str(e)
        return e.code, text


def get(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
) -> Tuple[int, str]:
    """GET request to `url` using `urllib`.

    Returns (status_code, response_text).
    """

    req = urllib.request.Request(url, method="GET")

    hdrs = dict(DEFAULT_HEADERS)
    hdrs.update(headers or {})
    for k, v in hdrs.items():
        req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp_text = resp.read().decode("utf-8")
            return resp.getcode(), resp_text
    except urllib.error.HTTPError as e:
        try:
            text = e.read().decode("utf-8")
        except Exception:
            text = str(e)
        return e.code, text


def get_bytes(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 10,
) -> Tuple[int, bytes, str]:
    """GET request to `url` and return raw bytes.

    Returns (status_code, body_bytes, content_type).
    """

    req = urllib.request.Request(url, method="GET")

    hdrs = dict(DEFAULT_HEADERS)
    hdrs.update(headers or {})
    for k, v in hdrs.items():
        req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            content_type = resp.headers.get("Content-Type", "")
            return resp.getcode(), body, content_type
    except urllib.error.HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = str(e).encode("utf-8")
        content_type = ""
        try:
            content_type = e.headers.get("Content-Type", "")
        except Exception:
            pass
        return e.code, body, content_type


def parse_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None
