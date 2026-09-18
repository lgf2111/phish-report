# Offline tests for ai_manager.
# These test the parts that do NOT need the internet: building the prompt,
# reading the AI's JSON reply, and checking it has the right shape.
# We never call the real Groq API here.

import ai_manager
import pytest


def test_build_prompt_includes_the_message():
    prompt = ai_manager.build_prompt({"message": "click here to win"})
    assert "click here to win" in prompt
    # it should also ask for JSON with our three keys
    assert "credential_request" in prompt
    assert "suspicious" in prompt
    assert "insufficient_context" in prompt


def test_parse_response_plain_json():
    raw = '{"credential_request": true, "suspicious": false, "insufficient_context": false}'
    data = ai_manager.parse_response(raw)
    assert data["credential_request"] is True
    assert data["suspicious"] is False


def test_parse_response_strips_code_fence():
    # models sometimes wrap the JSON in ```json ... ```
    inner = '{"credential_request": false, "suspicious": true, "insufficient_context": false}'
    raw = "```json\n" + inner + "\n```"
    data = ai_manager.parse_response(raw)
    assert data["suspicious"] is True


def test_validate_response_accepts_good_data():
    good = {"credential_request": True, "suspicious": False, "insufficient_context": False}
    # should return the same dict without raising
    assert ai_manager.validate_response(good) == good


def test_validate_response_rejects_missing_key():
    bad = {"credential_request": True, "suspicious": False}  # no insufficient_context
    with pytest.raises(ValueError):
        ai_manager.validate_response(bad)


def test_validate_response_rejects_wrong_type():
    bad = {"credential_request": "yes", "suspicious": False, "insufficient_context": False}
    with pytest.raises(ValueError):
        ai_manager.validate_response(bad)
