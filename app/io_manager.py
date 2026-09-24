# io_manager.py
# All input() and print() live here. OWNER: Lee Guan Feng.


def main_menu():
    """Display the available actions and return the user's menu choice."""
    # show the menu and return the user's choice
    print()
    print("=== PhishReport ===")
    print("1. Check a new message")
    print("2. View saved reports")
    print("3. Quit")
    return input("Choose 1-3: ").strip()


def collect_input():
    """Collect a nonempty message and return it in a new report record."""
    # Repeat the input question until there is text for the AI to examine.
    message = input("Paste the message: ").strip()
    while message == "":
        message = input("Message cannot be empty. Paste it again: ").strip()

    return {"message": message}


def display_result(response):
    """Display the validated final response supplied by the AI."""
    # Print the original response without composing or changing its contents.
    print()
    print(response)


def display_list(records):
    """Display saved AI responses and summaries of earlier scoring reports."""
    # Preserve the existing empty-history message.
    if not records:
        print("No saved reports yet.")
        return
    print()
    for i, record in enumerate(records, start=1):
        # Older records retain their stored priority; no new score is calculated.
        if "response" in record:
            summary = record["response"]
        else:
            summary = record.get("result", {}).get("priority", "?")
        print(i, "-", summary, "-", record.get("message", "")[:50])


def show_message(text):
    """Display a menu or error message supplied by the application."""
    # Keep terminal output in the I/O Manager.
    print(text)
