import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Fake credential used only by offline tests (never a real token).
TEST_TOKEN = "test-" + "channel-access-" + "token-value"


class FakeRuntime:
    def __init__(self, credentials):
        self.credentials = credentials


class FakeResponse:
    def __init__(self, status_code=200, body=None, headers=None):
        self.status_code = status_code
        self._body = body
        self.headers = headers or {}

    def json(self):
        if self._body is None:
            raise ValueError("no json body")
        return self._body


def make_tool(tool_cls, credentials):
    """Build a tool instance without the Dify plugin runtime."""
    tool = tool_cls.__new__(tool_cls)
    tool.runtime = FakeRuntime(credentials)
    tool.create_json_message = lambda payload: {"type": "json", "message": payload}
    return tool
