from datetime import datetime


def get_non_empty_text(prompt, field_name):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"Error: {field_name} cannot be empty.")


def get_positive_minutes(prompt):
    while True:
        try:
            minutes = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue

        if minutes <= 0:
            print("Minutes must be greater than 0.")
            continue

        return minutes


def get_valid_date(prompt):
    while True:
        date = input(prompt).strip()
        if not date:
            print("Error: Date cannot be empty.")
            continue

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError as error:
            print(f"Error: {error}")
            continue

        return date


def get_session_id(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid session ID.")


def get_menu_choice(prompt, valid_choices, error_message):
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(error_message)