import json
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

API_BASE = "https://api.line.me"


class GetBotInfoTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        credentials = self.runtime.credentials or {}
        token = credentials.get("channel_access_token") or ""
        if not token:
            raise Exception(
                f"No channel_access_token in runtime credentials (keys={sorted(credentials.keys())}). "
                "Re-authorize the provider in Dify Tools settings."
            )

        try:
            response = httpx.get(
                f"{API_BASE}/v2/bot/info",
                headers={"Authorization": f"Bearer {token}"},
                timeout=30,
            )
        except httpx.RequestError as e:
            raise Exception(f"Could not reach the LINE API: {e}") from e

        if response.status_code != 200:
            raise Exception(_line_error(response))

        yield self.create_json_message(response.json())


def _line_error(response: httpx.Response) -> str:
    try:
        body = response.json()
    except json.JSONDecodeError:
        return f"LINE API returned HTTP {response.status_code}."
    message = body.get("message") or ""
    details = body.get("details") or []
    extra = "; ".join(f"{d.get('property', '')}: {d.get('message', '')}" for d in details if isinstance(d, dict))
    return f"LINE API error {response.status_code}: {message}{(' (' + extra + ')') if extra else ''}"
