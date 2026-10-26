import pytest

from conftest import TEST_TOKEN, make_tool
from tools.send_broadcast_message import SendBroadcastMessageTool


class FakeHttpResponse:
    def __init__(self, status_code=200, content="{}"):
        self.status_code = status_code
        self._content = content
        self.headers = {"x-line-request-id": "req-1"}

    def json(self):
        import json as _json

        return _json.loads(self._content)


def test_broadcast_sends_expected_payload(monkeypatch):
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        return FakeHttpResponse(200)

    monkeypatch.setattr("tools.send_broadcast_message.httpx.post", fake_post)

    tool = make_tool(SendBroadcastMessageTool, {"channel_access_token": TEST_TOKEN})
    outputs = list(SendBroadcastMessageTool._invoke(tool, {"message_text": "hello everyone"}))

    assert captured["url"] == "https://api.line.me/v2/bot/message/broadcast"
    assert captured["json"] == {"messages": [{"type": "text", "text": "hello everyone"}]}
    assert outputs == [{"type": "json", "message": {"status": "sent", "scope": "all_friends", "request_id": "req-1"}}]


def test_broadcast_requires_text():
    tool = make_tool(SendBroadcastMessageTool, {"channel_access_token": TEST_TOKEN})
    with pytest.raises(Exception, match="'message_text' is required"):
        list(SendBroadcastMessageTool._invoke(tool, {}))


def test_broadcast_maps_line_error(monkeypatch):
    tool = make_tool(SendBroadcastMessageTool, {"channel_access_token": TEST_TOKEN})

    def fake_post(url, headers=None, json=None, timeout=None):
        return FakeHttpResponse(429, '{"message":"rate limit"}')

    monkeypatch.setattr("tools.send_broadcast_message.httpx.post", fake_post)

    with pytest.raises(Exception, match="LINE API error 429: rate limit"):
        list(SendBroadcastMessageTool._invoke(tool, {"message_text": "hi"}))
