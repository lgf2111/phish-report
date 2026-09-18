# Offline tests for logic_manager.
# Uses fake AI answers (no real API), so it runs anywhere, including Docker.
# Run with:  pytest

import logic_manager


def make_record(ai, submitted=None, clicked=False, downloaded=False):
    return {
        "ai": ai,
        "submitted_category": submitted,
        "clicked": clicked,
        "downloaded": downloaded,
    }


def test_high_needs_both_credential_request_and_submitted_secret():
    record = make_record({"credential_request": True}, submitted="password")
    assert logic_manager.route(record) == "high"


def test_credential_request_alone_is_not_high():
    record = make_record({"credential_request": True})
    assert logic_manager.route(record) != "high"


def test_medium_when_suspicious_and_clicked():
    record = make_record({"suspicious": True}, clicked=True)
    assert logic_manager.route(record) == "medium"


def test_review_when_only_suspicious():
    record = make_record({"suspicious": True})
    assert logic_manager.route(record) == "review"


def test_insufficient_information():
    record = make_record({"insufficient_context": True})
    assert logic_manager.route(record) == "insufficient_information"


def test_no_clear_indicators():
    record = make_record({})
    assert logic_manager.route(record) == "no_clear_indicators"


def test_higher_priority_scores_more():
    high = make_record({"credential_request": True}, submitted="password")
    low = make_record({})
    assert logic_manager.score(high) > logic_manager.score(low)


def test_evaluate_gives_priority_score_and_checklist():
    record = make_record({"suspicious": True}, clicked=True)
    result = logic_manager.evaluate(record)
    assert result["priority"] == "medium"
    assert result["checklist"]  # not empty
