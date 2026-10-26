import importlib.util
from pathlib import Path

import pytest

from conftest import TEST_TOKEN, make_tool
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def load_provider_module():
    spec = importlib.util.spec_from_file_location(
        "line_message_sender_provider", PLUGIN_ROOT / "provider" / "line-message-sender.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(provider_module, credentials):
    provider = provider_module.LineMessageSenderProvider.__new__(provider_module.LineMessageSenderProvider)
    provider._validate_credentials(credentials)


def test_empty_token_is_rejected():
    module = load_provider_module()
    with pytest.raises(ToolProviderCredentialValidationError, match="empty"):
        validate(module, {})


def test_invalid_token_reports_authentication_failure(monkeypatch):
    module = load_provider_module()
    sent = {}

    def fake_get(url, headers=None, timeout=None):
        sent["url"] = url
        sent["authorization"] = headers.get("Authorization")

        class Response:
            status_code = 401

            def json(self):
                return {"message": "Authentication failed"}

        return Response()

    monkeypatch.setattr(module.httpx, "get", fake_get)

    with pytest.raises(ToolProviderCredentialValidationError, match="Authentication failed"):
        validate(module, {"channel_access_token": TEST_TOKEN})

    assert sent["url"] == "https://api.line.me/v2/bot/info"
    assert sent["authorization"] == "Bearer " + TEST_TOKEN


def test_valid_token_calls_bot_info(monkeypatch):
    module = load_provider_module()
    calls = []

    def fake_get(url, headers=None, timeout=None):
        calls.append(url)

        class Response:
            status_code = 200

            def json(self):
                return {"displayName": "shineos-saas-starter"}

        return Response()

    monkeypatch.setattr(module.httpx, "get", fake_get)

    validate(module, {"channel_access_token": TEST_TOKEN})

    assert calls == ["https://api.line.me/v2/bot/info"]
