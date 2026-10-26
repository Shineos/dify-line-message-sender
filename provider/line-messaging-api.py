import json
from typing import Any

import httpx

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

API_BASE = "https://api.line.me"


class LineMessagingApiProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        token = (credentials or {}).get("channel_access_token") or ""
        if not token.strip():
            raise ToolProviderCredentialValidationError("Channel access token is empty.")

        try:
            response = httpx.get(
                f"{API_BASE}/v2/bot/info",
                headers={"Authorization": f"Bearer {token.strip()}"},
                timeout=15,
            )
        except httpx.RequestError as e:
            raise ToolProviderCredentialValidationError(f"Could not reach the LINE API: {e}") from e

        if response.status_code == 200:
            return

        detail = self._line_error_detail(response)
        if response.status_code == 401:
            detail = f"Authentication failed (invalid or expired channel access token). {detail}"
        raise ToolProviderCredentialValidationError(detail)

    @staticmethod
    def _line_error_detail(response: httpx.Response) -> str:
        try:
            body = response.json()
        except json.JSONDecodeError:
            return f"LINE API returned HTTP {response.status_code}."
        message = body.get("message") or ""
        details = body.get("details") or []
        extra = "; ".join(
            f"{d.get('property', '')}: {d.get('message', '')}" for d in details if isinstance(d, dict)
        )
        return f"LINE API error {response.status_code}: {message}{(' (' + extra + ')') if extra else ''}"
