from database import (
    add_session,
    connect_db,
    delete_session,
    initialize_database,
    get_or_create_subject,
    get_all_subjects,
    get_all_sessions,
    get_session_by_id,
    update_session_field,
    get_sessions_by_subject,
    get_sessions_by_area,
    get_sessions_by_date,
    get_sessions_oldest_first,
    get_sessions_newest_first,
    get_learning_totals,
    get_subject_statistics,
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


def select_subject_id(connection, allow_new=True):
    subjects = get_all_subjects(connection)
    for number, (_, name) in enumerate(subjects, start=1):
        print(f"{number}. {name}")

    if not subjects and not allow_new:
        print("No subjects available.")
        return None

    valid_choice_count = len(subjects)
    if allow_new:
        add_subject_choice = str(len(subjects) + 1)
        print(f"{add_subject_choice}. Add a new subject")
        valid_choice_count += 1

    valid_choices = tuple(
        str(number) for number in range(1, valid_choice_count + 1)
    )
    choice = get_menu_choice(
        "Choose a subject: ",
        valid_choices,
        f"Invalid choice. Enter a number from 1 to {valid_choice_count}.",
    )

    if allow_new and choice == add_subject_choice:
        name = get_non_empty_text("Enter the new subject name: ", "Subject")
        return get_or_create_subject(connection, name)

    return subjects[int(choice) - 1][0]


def add_session_flow(connection):
    area = get_non_empty_text("Enter the area of learning: ", "Area of learning")
    subject_id = select_subject_id(connection)
    topic = get_non_empty_text("Enter the topic: ", "Topic")
    minutes = get_positive_minutes("Enter the number of minutes spent: ")
    date = get_valid_date("Enter the date (YYYY-MM-DD): ")
    notes = input("Enter any notes: ").strip()

    add_session(connection, area, subject_id, topic, minutes, date, notes)
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
        value = select_subject_id(connection)
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


def filter_sessions_flow(connection):
    print("\nFilter/sort sessions")
    print("1. Filter by subject")
    print("2. Filter by area")
    print("3. Filter by date")
    print("4. Show newest sessions first")
    print("5. Show oldest sessions first")
    print("6. Back")

    choice = get_menu_choice(
        "Choose an option: ",
        ("1", "2", "3", "4", "5", "6"),
        "Invalid choice. Enter a number from 1 to 6.",
    )

    if choice == "6":
        return
    elif choice == "1":
        subject_id = select_subject_id(connection, allow_new=False)
        if subject_id is None:
            return
        sessions = get_sessions_by_subject(connection, subject_id)

        if sessions:
            for session in sessions:
                display_session(session)
        else:
            print("No sessions found for that subject.")
    elif choice == "2":
        area = get_non_empty_text("Enter an area to filter by: ", "Area")
        sessions = get_sessions_by_area(connection, area)

        if sessions:
            for session in sessions:
                display_session(session)
        else:
            print(f"No sessions found for area '{area}'.")
    elif choice == "3":
        date = get_valid_date("Enter a date to filter by (YYYY-MM-DD): ")
        sessions = get_sessions_by_date(connection, date)

        if sessions:
            for session in sessions:
                display_session(session)
        else:
            print(f"No sessions found for date '{date}'.")
    elif choice == "4":
        sessions = get_sessions_newest_first(connection)

        if sessions:
            for session in sessions:
                display_session(session)
        else:
            print("No sessions found.")
    elif choice == "5":
        sessions = get_sessions_oldest_first(connection)

        if sessions:
            for session in sessions:
                display_session(session)
        else:
            print("No sessions found.")


def statistics_flow(connection):
    totals = get_learning_totals(connection)
    session_count, total_minutes = totals
    hours = total_minutes // 60
    minutes = total_minutes % 60
    subject_stats = get_subject_statistics(connection)

    print(f"Total sessions: {session_count}")
    print(f"Total minutes: {total_minutes} ({hours} hours and {minutes} minutes)")
    print("\nSubject Statistics:")
    if subject_stats:
        print(f"Most studied subject: {subject_stats[0][0]}")
    for subject, subject_total_minutes, subject_session_count in subject_stats:
        subject_hours = subject_total_minutes // 60
        subject_minutes = subject_total_minutes % 60
        print(
            f"  {subject}: {subject_hours}h {subject_minutes}m "
            f"({subject_session_count} sessions)"
        )


def main():
    connection = connect_db()
    try:
        initialize_database(connection)

        while True:
            print("\nPersonal Learning Tracker")
            print("1. Add session")
            print("2. View sessions")
            print("3. Edit session")
            print("4. Delete session")
            print("5. Filter/sort sessions")
            print("6. Statistics")
            print("7. Exit")

            choice = get_menu_choice(
                "Choose an option: ",
                ("1", "2", "3", "4", "5", "6", "7"),
                "Invalid choice. Enter a number from 1 to 7.",
            )

            if choice == "1":
                add_session_flow(connection)
            elif choice == "2":
                view_sessions_flow(connection)
            elif choice == "3":
                edit_session_flow(connection)
            elif choice == "4":
                delete_session_flow(connection)
            elif choice == "5":
                filter_sessions_flow(connection)
            elif choice == "6":
                statistics_flow(connection)
            else:
                print("Goodbye!")
                break
    finally:
        connection.close()


if __name__ == "__main__":
    main()
