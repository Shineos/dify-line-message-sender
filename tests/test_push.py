import pytest

from conftest import TEST_TOKEN, make_tool
from tools.send_push_message import SendPushMessageTool


class FakeHttpResponse:
    def __init__(self, status_code=200, content="{}"):
        self.status_code = status_code
        self._content = content
        self.headers = {"x-line-request-id": "req-1"}

    def json(self):
        import json as _json

        return _json.loads(self._content)


def test_push_sends_expected_payload(monkeypatch):
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        return FakeHttpResponse(200)

    monkeypatch.setattr("tools.send_push_message.httpx.post", fake_post)

    tool = make_tool(SendPushMessageTool, {"channel_access_token": TEST_TOKEN})
    outputs = list(SendPushMessageTool._invoke(tool, {"to": "U123", "message_text": "hello"}))

    assert captured["url"] == "https://api.line.me/v2/bot/message/push"
    assert captured["headers"]["Authorization"] == "Bearer " + TEST_TOKEN
    assert captured["json"] == {"to": "U123", "messages": [{"type": "text", "text": "hello"}]}
    assert outputs == [{"type": "json", "message": {"status": "sent", "to": "U123", "request_id": "req-1"}}]


def test_push_rejects_missing_recipient():
    tool = make_tool(SendPushMessageTool, {"channel_access_token": TEST_TOKEN})
    with pytest.raises(Exception, match="'to' is required"):
        list(SendPushMessageTool._invoke(tool, {"message_text": "hi"}))


def test_push_rejects_over_5000_chars():
    tool = make_tool(SendPushMessageTool, {"channel_access_token": TEST_TOKEN})
    with pytest.raises(Exception, match="5,000"):
        list(SendPushMessageTool._invoke(tool, {"to": "U123", "message_text": "x" * 5001}))


def test_push_maps_line_error(monkeypatch):
    tool = make_tool(SendPushMessageTool, {"channel_access_token": TEST_TOKEN})

    def fake_post(url, headers=None, json=None, timeout=None):
        return FakeHttpResponse(400, '{"message":"invalid recipient","details":[{"property":"to","message":"Not a valid user ID"}]}')

    monkeypatch.setattr("tools.send_push_message.httpx.post", fake_post)

    with pytest.raises(Exception, match=r"LINE API error 400: invalid recipient \(to: Not a valid user ID\)"):
        list(SendPushMessageTool._invoke(tool, {"to": "BAD", "message_text": "hi"}))
