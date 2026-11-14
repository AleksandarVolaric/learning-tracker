from database import (
    add_session,
    connect_db,
    create_sessions_table,
    delete_session,
    get_all_sessions,
    get_session_by_id,
    update_session_field,
)
from validation import (
    get_menu_choice,
    get_non_empty_text,
    get_positive_minutes,
    get_session_id,
    get_valid_date,
)


def display_session(session):
    print(
        f"ID: {session[0]} | Area: {session[1]} | "
        f"Subject: {session[2]} | Topic: {session[3]} | "
        f"Minutes: {session[4]} | Date: {session[5]} | Notes: {session[6]}"
    )


def add_session_flow(connection):
    area = get_non_empty_text("Enter the area of learning: ", "Area of learning")
    subject = get_non_empty_text("Enter the subject: ", "Subject")
    topic = get_non_empty_text("Enter the topic: ", "Topic")
    minutes = get_positive_minutes("Enter the number of minutes spent: ")
    date = get_valid_date("Enter the date (YYYY-MM-DD): ")
    notes = input("Enter any notes: ").strip()

    add_session(connection, area, subject, topic, minutes, date, notes)
    print("Session saved successfully!")


def view_sessions_flow(connection):
    sessions = get_all_sessions(connection)
    if sessions:
        for session in sessions:
            display_session(session)
    else:
        print("No sessions found.")


def edit_session_flow(connection):
    session_id = get_session_id("Enter the ID of the session you want to edit: ")
    session = get_session_by_id(connection, session_id)

    if session is None:
        print(f"No session found with ID {session_id}.")
        return

    print("Found session:")
    display_session(session)

    print("1. Area")
    print("2. Subject")
    print("3. Topic")
    print("4. Minutes")
    print("5. Date")
    print("6. Notes")
    print("7. Cancel")
    choice = get_menu_choice(
        "Choose a field to edit: ",
        ("1", "2", "3", "4", "5", "6", "7"),
        "Invalid choice. Enter a number from 1 to 7.",
    )

    if choice == "7":
        print("Edit canceled.")
        return

    if choice == "1":
        field = "area"
        value = get_non_empty_text("Enter the new area: ", "Area")
    elif choice == "2":
        field = "subject"
        value = get_non_empty_text("Enter the new subject: ", "Subject")
    elif choice == "3":
        field = "topic"
        value = get_non_empty_text("Enter the new topic: ", "Topic")
    elif choice == "4":
        field = "minutes"
        value = get_positive_minutes("Enter the new number of minutes: ")
    elif choice == "5":
        field = "date"
        value = get_valid_date("Enter the new date (YYYY-MM-DD): ")
    else:
        field = "notes"
        value = input("Enter the updated notes: ").strip()

    update_session_field(connection, field, value, session_id)
    print(f"{field.title()} updated successfully!")


def delete_session_flow(connection):
    session_id = get_session_id("Enter the ID of the session you want to delete: ")
    session = get_session_by_id(connection, session_id)

    if session is None:
        print(f"No session found with ID {session_id}.")
        return

    print("Found session:")
    display_session(session)

    confirmation = get_menu_choice(
        "Delete this session? (y/n): ",
        ("y", "n"),
        "Please enter y or n.",
    )
    if confirmation == "y":
        delete_session(connection, session_id)
        print("Session deleted successfully!")
    else:
        print("Deletion canceled.")


def main():
    connection = connect_db()
    try:
        create_sessions_table(connection)

        while True:
            print("\nPersonal Learning Tracker")
            print("1. Add session")
            print("2. View sessions")
            print("3. Edit session")
            print("4. Delete session")
            print("5. Exit")

            choice = get_menu_choice(
                "Choose an option: ",
                ("1", "2", "3", "4", "5"),
                "Invalid choice. Enter a number from 1 to 5.",
            )

            if choice == "1":
                add_session_flow(connection)
            elif choice == "2":
                view_sessions_flow(connection)
            elif choice == "3":
                edit_session_flow(connection)
            elif choice == "4":
                delete_session_flow(connection)
            else:
                print("Goodbye!")
                break
    finally:
        connection.close()


if __name__ == "__main__":
    main()
