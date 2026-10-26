import json
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

API_BASE = "https://api.line.me"


class SendPushMessageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        token = (self.runtime.credentials or {}).get("channel_access_token") or ""
        to = str(tool_parameters.get("to") or "").strip()
        text = str(tool_parameters.get("message_text") or "")
        if not to:
            raise Exception("Parameter 'to' is required: a LINE user ID (U...), group ID (C...), or room ID (R...).")
        if not text:
            raise Exception("Parameter 'message_text' is required.")
        if len(text) > 5000:
            raise Exception("LINE text messages are limited to 5,000 characters.")

        payload: dict[str, Any] = {
            "to": to,
            "messages": [{"type": "text", "text": text}],
        }
        if tool_parameters.get("notification_disabled") is True:
            payload["notificationDisabled"] = True

        try:
            response = httpx.post(
                f"{API_BASE}/v2/bot/message/push",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json=payload,
                timeout=30,
            )
        except httpx.RequestError as e:
            raise Exception(f"Could not reach the LINE API: {e}") from e

        if response.status_code != 200:
            raise Exception(_line_error(response))

        yield self.create_json_message(
            {
                "status": "sent",
                "to": to,
                "request_id": response.headers.get("x-line-request-id", ""),
            }
        )


def _line_error(response: httpx.Response) -> str:
    try:
        body = response.json()
    except json.JSONDecodeError:
        return f"LINE API returned HTTP {response.status_code}."
    message = body.get("message") or ""
    details = body.get("details") or []
    extra = "; ".join(f"{d.get('property', '')}: {d.get('message', '')}" for d in details if isinstance(d, dict))
    return f"LINE API error {response.status_code}: {message}{(' (' + extra + ')') if extra else ''}"
