"""Exercise the connected application with synthetic AI replies and temporary storage."""

import json
from unittest.mock import Mock

import ai_manager
import data_manager
import io_manager
import logic_manager
import main
import pytest


@pytest.fixture
def flow(monkeypatch, tmp_path):
    """Record manager calls while isolating API requests and saved reports."""
    # Keep real input, validation, storage, and display behavior under observation.
    monkeypatch.chdir(tmp_path)
    calls = Mock()
    api = Mock()
    calls.attach_mock(api, "api")
    monkeypatch.setattr(ai_manager, "call_api", api)
    for name, module, target in (
        ("hold", logic_manager, "hold_details"),
        ("prompt", ai_manager, "response_prompt"),
        ("save", data_manager, "save"),
        ("display", io_manager, "display_result"),
        ("notice", io_manager, "show_message"),
    ):
        observed = Mock(wraps=getattr(module, target))
        calls.attach_mock(observed, name)
        monkeypatch.setattr(module, target, observed)
    return calls


@pytest.mark.parametrize(
    ("details", "response"),
    [
        (
            {"emails": [], "phone_numbers": [], "ip_addresses": []},
            "Email: , Phone Number: , IP Address: ",
        ),
        (
            {"emails": ["a1@example.test"], "phone_numbers": [], "ip_addresses": []},
            "Email: a1@example.test, Phone Number: , IP Address: ",
        ),
        (
            {"emails": [], "phone_numbers": ["00123456"], "ip_addresses": []},
            "Email: , Phone Number: 00123456, IP Address: ",
        ),
        (
            {"emails": [], "phone_numbers": [], "ip_addresses": ["192.0.2.10", "2001:DB8::1"]},
            "Email: , Phone Number: , IP Address: 192.0.2.10, 2001:DB8::1",
        ),
        (
            {
                "emails": ["b2@example.test", "a1@example.test", "b2@example.test"],
                "phone_numbers": ["87654321", "12345678", "87654321"],
                "ip_addresses": ["2001:DB8::1", "192.0.2.10", "2001:DB8::1"],
            },
            "Email: b2@example.test, a1@example.test, b2@example.test, "
            "Phone Number: 87654321, 12345678, 87654321, "
            "IP Address: 2001:DB8::1, 192.0.2.10, 2001:DB8::1",
        ),
    ],
)
def test_scan(flow, monkeypatch, capsys, details, response):
    """Require both AI calls and the Logic Manager before saving and displaying."""
    # Send synthetic details through the actual parsing and validation functions.
    message = "Sample: " + "; ".join(value for items in details.values() for value in items)
    user_input = Mock(return_value=message)
    monkeypatch.setattr("builtins.input", user_input)
    flow.api.side_effect = [json.dumps(details), json.dumps({"response": response})]

    main.check_message()

    # Verify the complete sequence, the handoff object, and the actual saved record.
    assert [entry[0] for entry in flow.mock_calls] == [
        "api", "hold", "prompt", "api", "save", "display",
    ]
    assert flow.hold.call_args.args[0] is flow.prompt.call_args.args[0]
    first_prompt = flow.api.call_args_list[0].args[0]
    second_prompt = flow.api.call_args_list[1].args[0]
    assert json.loads(first_prompt.split("Message (JSON string):\n", 1)[1]) == message.strip()
    assert json.loads(second_prompt.split("Details (JSON object):\n", 1)[1]) == details
    record = {"message": message.strip(), "details": details, "response": response}
    flow.save.assert_called_once_with(record)
    assert data_manager.load() == [record]
    assert capsys.readouterr().out == "\n" + response + "\n"
    user_input.assert_called_once()


@pytest.mark.parametrize("reply", [RuntimeError("AI unavailable"), "not JSON", "{}"])
def test_first_error(flow, monkeypatch, tmp_path, capsys, reply):
    """Stop before the Logic Manager or second request when extraction fails."""
    # An API error or invalid extraction reply must not produce a saved result.
    monkeypatch.setattr("builtins.input", Mock(return_value="No details here."))
    flow.api.side_effect = [reply]
    main.check_message()
    assert [entry[0] for entry in flow.mock_calls] == ["api", "notice"]
    assert capsys.readouterr().out.startswith("Sorry, the check failed:")
    assert not (tmp_path / "reports.json").exists()


@pytest.mark.parametrize(
    "reply",
    [
        RuntimeError("AI unavailable"),
        "not JSON",
        "{}",
        '{"response": "Email: invented@example.test, Phone Number: , IP Address: "}',
    ],
)
def test_second_error(flow, monkeypatch, tmp_path, capsys, reply):
    """Require a valid second AI response before saving or showing any result."""
    # Even valid first-call details must not become a locally generated response.
    details = {"emails": [], "phone_numbers": [], "ip_addresses": []}
    monkeypatch.setattr("builtins.input", Mock(return_value="No details here."))
    flow.api.side_effect = [json.dumps(details), reply]
    main.check_message()
    assert [entry[0] for entry in flow.mock_calls] == [
        "api", "hold", "prompt", "api", "notice",
    ]
    assert capsys.readouterr().out.startswith("Sorry, the check failed:")
    assert not (tmp_path / "reports.json").exists()


def test_logic_return(flow, monkeypatch):
    """Use the Logic Manager's returned object for the second prompt and storage."""
    # A distinct test return value detects accidentally reusing the first AI object.
    extracted = {"emails": ["a1@example.test"], "phone_numbers": [], "ip_addresses": []}
    returned = {"emails": ["b2@example.test"], "phone_numbers": [], "ip_addresses": []}
    response = "Email: b2@example.test, Phone Number: , IP Address: "
    monkeypatch.setattr("builtins.input", Mock(return_value="a1@example.test b2@example.test"))
    flow.hold.return_value = returned
    flow.api.side_effect = [json.dumps(extracted), json.dumps({"response": response})]
    main.check_message()
    assert flow.prompt.call_args.args[0] is returned
    assert data_manager.load()[0]["details"] == returned


def test_menu(flow, monkeypatch, tmp_path, capsys):
    """Check a message, view mixed report history, and quit through the real menu."""
    # Preserve an existing scoring record while a new AI report is appended.
    legacy = {"message": "Earlier report", "result": {"priority": "review", "score": 50}}
    (tmp_path / "reports.json").write_text(json.dumps([legacy]), encoding="utf-8")
    details = {"emails": ["a1@example.test"], "phone_numbers": [], "ip_addresses": []}
    response = "Email: a1@example.test, Phone Number: , IP Address: "
    answers = Mock(side_effect=["1", "a1@example.test", "2", "3"])
    monkeypatch.setattr("builtins.input", answers)
    flow.api.side_effect = [json.dumps(details), json.dumps({"response": response})]

    main.main()

    # Both the new response and the previously stored priority remain readable.
    output = capsys.readouterr().out
    records = data_manager.load()
    assert records[0] == legacy
    assert records[1]["response"] == response
    assert len(records) == 2
    assert output.count(response) == 2
    assert "review - Earlier report" in output
    assert "Bye!" in output
    assert answers.call_count == 4
    assert flow.api.call_count == 2


def test_input(monkeypatch):
    """Repeat a blank message prompt without asking the old scoring questions."""
    # A third input request would fail this finite sequence.
    answers = Mock(side_effect=["   ", "  a1@example.test  "])
    monkeypatch.setattr("builtins.input", answers)
    assert io_manager.collect_input() == {"message": "a1@example.test"}
    assert answers.call_count == 2


def test_empty_history(capsys):
    """Display the existing empty-history message when no reports are saved."""
    # An empty report list must not be interpreted as a new scan result.
    io_manager.display_list([])
    assert capsys.readouterr().out == "No saved reports yet.\n"
