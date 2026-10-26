import pytest

from conftest import TEST_TOKEN, make_tool
from tools.get_bot_info import GetBotInfoTool
from tools.get_profile import GetProfileTool


class FakeHttpResponse:
    def __init__(self, status_code=200, content="{}"):
        self.status_code = status_code
        self._content = content
        self.headers = {}

    def json(self):
        import json as _json

        return _json.loads(self._content)


def test_bot_info_returns_profile(monkeypatch):
    captured = {}

    def fake_get(url, headers=None, timeout=None):
        captured["url"] = url
        captured["headers"] = headers
        return FakeHttpResponse(200, '{"displayName":"shineos-saas-starter","basicId":"@459uqdub"}')

    monkeypatch.setattr("tools.get_bot_info.httpx.get", fake_get)

    tool = make_tool(GetBotInfoTool, {"channel_access_token": TEST_TOKEN})
    outputs = list(GetBotInfoTool._invoke(tool, {}))

    assert captured["url"] == "https://api.line.me/v2/bot/info"
    assert captured["headers"]["Authorization"] == "Bearer " + TEST_TOKEN
    assert outputs == [{"type": "json", "message": {"displayName": "shineos-saas-starter", "basicId": "@459uqdub"}}]


def test_profile_returns_user(monkeypatch):
    captured = {}

    def fake_get(url, headers=None, timeout=None):
        captured["url"] = url
        return FakeHttpResponse(200, '{"displayName":"Taro","userId":"U123"}')

    monkeypatch.setattr("tools.get_profile.httpx.get", fake_get)

    tool = make_tool(GetProfileTool, {"channel_access_token": TEST_TOKEN})
    outputs = list(GetProfileTool._invoke(tool, {"user_id": "U123"}))

    assert captured["url"] == "https://api.line.me/v2/bot/profile/U123"
    assert outputs == [{"type": "json", "message": {"displayName": "Taro", "userId": "U123"}}]


def test_profile_requires_user_id():
    tool = make_tool(GetProfileTool, {"channel_access_token": TEST_TOKEN})
    with pytest.raises(Exception, match="'user_id' is required"):
        list(GetProfileTool._invoke(tool, {}))
