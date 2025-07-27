import json
from datetime import datetime
import os
def display_menu():
    print("\n===== Notes App ======")
    print("1. View notes")
    print("2. Add note")
    print("3. Delete note")
    print("4. Exit")

def add_note():
    note = input("Enter your note: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note_entry = {"note": note, "timestamp": timestamp}
    notes = []

    if os.path.exists("notes.json"):
        with open("notes.json", "r") as file:
            notes = json.load(file)

    notes.append(note_entry)

    with open("notes.json", "w") as file:
        json.dump(notes, file, indent=2)
    print("Note added!")

def view_notes():
    if not os.path.exists("notes.json"):
        print("No notes file found. Add a note first.")
        return

    with open("notes.json", "r") as file:
        notes = json.load(file)

    if not notes:
        print("No notes found.")
    else:
        print("\nYour Notes:")
        for idx, entry in enumerate(notes, start=1):
            print(f"{idx}. [{entry['timestamp']}] {entry['note']}")

def delete_note():
    if not os.path.exists("notes.json"):
        print("No notes to delete.")
        return

    with open("notes.json", "r") as file:
        notes = json.load(file)

    view_notes()
    try:
        index = int(input("Enter the number of the note to delete: "))
        if 1 <= index <= len(notes):
            removed_note = notes.pop(index - 1)
            with open("notes.json", "w") as file:
                json.dump(notes, file, indent=2)
            print(f"Deleted note: {removed_note['note']}")
        else:
            print("Invalid index.")
    except ValueError:
        print("Invalid input.")

def main():
    while True:
        display_menu()
        choice = input("Choose an option (1-4): ")
        if choice == "1":
            view_notes()
        elif choice == "2":
            add_note()
        elif choice == "3":
            delete_note()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()