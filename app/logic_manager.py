# logic_manager.py
# Holds extracted details for the AI-to-Logic-to-AI flow. OWNER: Pair B.
# The existing scoring functions remain until the new flow is connected.
#
# Rules (checked top to bottom, from the proposal):
#   1. high   - AI saw a credential request AND user submitted a password/OTP
#   2. medium - AI saw something suspicious AND user clicked or downloaded
#   3. review - suspicious, but nothing above matched
#   4. insufficient - AI could not tell
#   5. none   - nothing above (not a promise that it's safe)


def hold_details(details):
    """Hold the AI-extracted details for this request and return them unchanged.

    Args:
        details: A dictionary of emails, phone_numbers, and ip_addresses lists.

    Returns:
        The same dictionary, preserving its lists, order, and repeated values.
    """
    # Keep the supplied object locally for the handoff back to the AI Manager.
    held_details = details
    return held_details


def route(record):
    ai = record.get("ai", {})

    credential_request = ai.get("credential_request", False)
    suspicious = ai.get("suspicious", False)
    insufficient = ai.get("insufficient_context", False)

    submitted = record.get("submitted_category")
    clicked = record.get("clicked", False)
    downloaded = record.get("downloaded", False)

    # rule 1: needs two things at once (this is the multi-condition rule)
    if credential_request and submitted in ("password", "otp"):
        return "high"
    # rule 2
    if suspicious and (clicked or downloaded):
        return "medium"
    # rule 3
    if suspicious:
        return "review"
    # rule 4
    if insufficient:
        return "insufficient_information"
    # rule 5
    return "no_clear_indicators"


def score(record):
    # simple score so we can rank/threshold. higher = more urgent.
    points = {
        "high": 90,
        "medium": 70,
        "review": 50,
        "insufficient_information": 30,
        "no_clear_indicators": 10,
    }
    return points[route(record)]


def evaluate(record):
    priority = route(record)
    return {
        "priority": priority,
        "score": score(record),
        "checklist": checklist_for(priority),
    }


def checklist_for(priority):
    if priority == "high":
        return ["Recover your account through the official website.", "Tell IT."]
    if priority == "medium":
        return ["Stop replying to the message.", "Ask IT what to do."]
    if priority == "review":
        return ["Check the sender another way.", "Report the message."]
    if priority == "insufficient_information":
        return ["Give more details so it can be checked."]
    return ["No clear signs found. This does not mean it is safe."]
