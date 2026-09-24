"""Check real request construction using a mocked HTTP transport only."""

import json
import urllib.error
from unittest.mock import MagicMock, Mock

import ai_manager
import data_manager
import main
import pytest


def test_http_flow(monkeypatch, tmp_path, capsys):
    """Run both real API request functions through the application without a network."""
    # Isolate storage and replace only HTTP responses with synthetic envelopes.
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setattr("builtins.input", Mock(return_value="Call 12345678."))
    details = {"emails": [], "phone_numbers": ["12345678"], "ip_addresses": []}
    response = "Email: , Phone Number: 12345678, IP Address: "
    stream = Mock()
    stream.read.side_effect = [
        json.dumps({"choices": [{"message": {"content": json.dumps(payload)}}]}).encode()
        for payload in (details, {"response": response})
    ]
    transport = MagicMock()
    transport.return_value.__enter__.return_value = stream
    monkeypatch.setattr(ai_manager.urllib.request, "urlopen", transport)

    main.check_message()

    # Both requests must use the configured endpoint and the JSON response mode.
    assert transport.call_count == 2
    for request_call in transport.call_args_list:
        request = request_call.args[0]
        body = json.loads(request.data)
        assert request.full_url == ai_manager.URL
        assert request.get_header("Authorization") == "Bearer test-key"
        assert body["model"] == ai_manager.MODEL
        assert body["response_format"] == {"type": "json_object"}
        assert request_call.kwargs["timeout"] == 30
    assert data_manager.load()[0]["response"] == response
    assert capsys.readouterr().out == "\n" + response + "\n"


def test_missing_key(monkeypatch):
    """Require an API key before attempting a network request."""
    # No request or substitute AI answer should be possible without credentials.
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    transport = Mock()
    monkeypatch.setattr(ai_manager.urllib.request, "urlopen", transport)
    with pytest.raises(RuntimeError, match="GROQ_API_KEY"):
        ai_manager.call_api("Synthetic prompt")
    transport.assert_not_called()


@pytest.mark.parametrize("error", [urllib.error.URLError("offline"), TimeoutError("timeout")])
def test_network_error(monkeypatch, error):
    """Report network failures without retrying or generating an AI result."""
    # The transport error must propagate as the API client's RuntimeError.
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    transport = Mock(side_effect=error)
    monkeypatch.setattr(ai_manager.urllib.request, "urlopen", transport)
    with pytest.raises(RuntimeError, match="Could not reach the AI"):
        ai_manager.call_api("Synthetic prompt")
    transport.assert_called_once()
