import time
from typing import Optional

from al_quran_bot.constants import CLIENT_ID, CLIENT_SECRET, TOKEN_URL
from al_quran_bot.http_utils import get, parse_json, post_form


class QuranClient:
    """Simple OAuth2 client for https://oauth2.quran.foundation/token

    Automatically fetches and caches access token on init.
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        scope: str = "content",
        token_url: Optional[str] = None,
    ):
        self.client_id = client_id or CLIENT_ID
        self.client_secret = client_secret or CLIENT_SECRET
        if not self.client_id or not self.client_secret:
            raise RuntimeError("Missing CLIENT_ID/CLIENT_SECRET in .env or constructor")
        self.scope = scope
        self.token_url = token_url or TOKEN_URL
        self._access_token: Optional[str] = None
        self._expires_at: float = 0.0
        self.get_token()

    def get_token(self, force: bool = False) -> str:
        now = time.time()
        if self._access_token and not force and now < self._expires_at - 10:
            return self._access_token

        status, text = post_form(
            self.token_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            data={"grant_type": "client_credentials", "scope": self.scope},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10,
        )

        if status != 200:
            raise RuntimeError(f"Token request failed: {status} {text}")

        data = parse_json(text)
        if not data:
            raise RuntimeError(f"Invalid JSON response: {text}")

        token = data.get("access_token")
        if not token:
            raise RuntimeError(f"No access_token in response: {data}")

        expires_in = int(data.get("expires_in", 3600))
        self._access_token = token
        self._expires_at = now + expires_in
        return self._access_token

    def get_random_verse(self) -> dict:
        token = self.get_token()
        url = "https://apis.quran.foundation/content/api/v4/verses/random?translations=55&language=uz&fields=image_url,text_imlaei"
        headers = {
            "Accept": "application/json",
            "x-auth-token": token,
            "x-client-id": self.client_id,
        }
        status, text = get(url, headers=headers, timeout=10)
        if status != 200:
            raise RuntimeError(f"Random verse request failed: {status} {text}")
        data = parse_json(text)
        if not data:
            raise RuntimeError(f"Invalid JSON response: {text}")
        return data
