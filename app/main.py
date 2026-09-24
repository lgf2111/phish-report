# main.py
# Ties the four managers together:
#   input -> AI extraction -> Logic Manager -> AI response -> save and display

import os

import ai_manager
import data_manager
import io_manager
import logic_manager


def load_env():
    """Load project environment values without replacing existing settings."""
    # simple .env reader so you don't have to export the key by hand.
    # looks for a .env file in the current folder: KEY=value per line.
    if not os.path.exists(".env"):
        return
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


def check_message():
    """Run both AI requests and the Logic Manager handoff for one user message."""
    # Collect only the message needed for this extraction demonstration.
    record = io_manager.collect_input()

    try:
        # The first AI request supplies the details; validation preserves them.
        prompt = ai_manager.extract_prompt(record)
        raw = ai_manager.call_api(prompt)
        reply = ai_manager.parse_response(raw)
        details = ai_manager.validate_details(reply, record["message"])

        # Pass the Logic Manager's return value into the second AI request.
        details = logic_manager.hold_details(details)
        prompt = ai_manager.response_prompt(details)
        raw = ai_manager.call_api(prompt)
        reply = ai_manager.parse_response(raw)
        response = ai_manager.validate_reply(reply, details)
    except (RuntimeError, ValueError) as error:
        io_manager.show_message("Sorry, the check failed: " + str(error))
        return

    # Save and display only after both AI requests and validations succeed.
    record["details"] = details
    record["response"] = response
    data_manager.save(record)
    io_manager.display_result(response)


def view_reports():
    """Load saved reports and send them to the I/O Manager for display."""
    # The data layer keeps new records and previously saved records together.
    records = data_manager.load()
    io_manager.display_list(records)


def main():
    """Load settings and run the application's menu until the user quits."""
    # Dispatch each menu choice through the existing manager functions.
    load_env()
    while True:
        choice = io_manager.main_menu()
        if choice == "1":
            check_message()
        elif choice == "2":
            view_reports()
        elif choice == "3":
            io_manager.show_message("Bye!")
            break
        else:
            io_manager.show_message("Please choose 1, 2 or 3.")


if __name__ == "__main__":
    main()
