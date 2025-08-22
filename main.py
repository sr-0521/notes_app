import json
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# File where notes are stored in JSON format
NOTES_FILE = "notes.json"

# Loads notes from the file if it exists, returns empty list otherwise
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    return []

# Saves the current list of notes to the JSON file.
def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=2)

# Loads notes, clears the existing tree (table), and re-inserts each note
#  into the display.
def refresh_notes():
    notes = load_notes()
    for row in tree.get_children():
        tree.delete(row)
    for i, note in enumerate(notes):
        tree.insert('', 'end', iid=i, values=(i+1, note['note'], note['timestamp']))

# Receives text from input box, appends note and timestamp to notes list, saves,
#  and refreshes.
def add_note():
    note = note_entry.get().strip()
    if note:
        notes = load_notes()
        notes.append({
            "note": note,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_notes(notes)
        refresh_notes()
        note_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Note cannot be empty.")

# Removes selected note from the list, saves, and refreshes display.
def delete_note():
    selected = tree.focus()
    if selected:
        index = int(selected)
        notes = load_notes()
        deleted_note = notes.pop(index)
        save_notes(notes)
        refresh_notes()
        messagebox.showinfo("Deleted", f"Deleted note: {deleted_note['note']}")
    else:
        messagebox.showwarning("Selection Error", "Please select a note to delete.")

# Lets user edit a selected note from popup dialog, saves updated note with new
#  timestamp, and refreshes display.
def edit_note():
    selected = tree.focus()
    if selected:
        index = int(selected)
        notes = load_notes()
        new_text = simpledialog.askstring("Edit Note", "Enter the new note text:", initialvalue=notes[index]['note'])
        if new_text:
            notes[index]['note'] = new_text
            notes[index]['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_notes(notes)
            refresh_notes()
    else:
        messagebox.showwarning("Selection Error", "Please select a note to edit.")

# GUI Setup

# Creates the main window
root = tk.Tk()
root.title("Notes App")
root.geometry("1000x800")

# Frame holds the input box + button
frame = tk.Frame(root)
frame.pack(pady=50)

# Displays all notes with an ID, note text, and timestamp.
# Clicking on a row allows edit/delete.
note_entry = tk.Entry(frame, width=80)
note_entry.pack(side=tk.LEFT, padx=5)



# Displays all notes with an ID, note, text, and timestamp.
tree = ttk.Treeview(root, columns=('ID', 'Note', 'Timestamp'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Note', text='Note')
tree.heading('Timestamp', text='Timestamp')
tree.column('ID', width=30, anchor='center')
tree.column('Note', width=250)
tree.column('Timestamp', width=200)
tree.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

# Add button
# Styled label acting as a button
add_label = tk.Label(
    frame, text="Add Note", bg="blue", fg="white", font=("Arial", 15, "bold"), padx=10,
    pady=5, bd=3, relief="raised", cursor="hand2", width=15, height=2,wraplength=100,
    justify="center", 
)
# Make the label behave like a button
add_label.bind("<Button-1>", lambda event: add_note())

# Optional hover effect
add_label.bind("<Enter>", lambda e: add_label.config(bg="deepskyblue"))
add_label.bind("<Leave>", lambda e: add_label.config(bg="blue"))

add_label.pack(side=tk.LEFT, padx=5)
"""add_btn = tk.Button(frame, text="Add Note", command=add_note,
                    bd=2, cursor="hand2", fg="pink", font=("Arial", 15),
                    height=2, highlightbackground="pink",
                    highlightthickness=10, pady=10, wraplength=100)
add_btn.pack(side=tk.LEFT, padx=5)
"""


# Edit button (Label)
edit_label = tk.Label(
    btn_frame, text="Edit Selected", bg="blue", fg="white", font=("Arial", 15, "bold"),
    padx=10, pady=5, bd=3, relief="raised", cursor="hand2", width=15, height=2,
    wraplength=100, justify="center",
)
# Make the label behave like a button
edit_label.bind("<Button-1>", lambda event: edit_note())

# Optional hover effect
edit_label.bind("<Enter>", lambda e: edit_label.config(bg="deepskyblue"))
edit_label.bind("<Leave>", lambda e: edit_label.config(bg="blue"))

edit_label.pack(side=tk.LEFT, padx=10)

# Delete button (Label)
delete_label = tk.Label(
    btn_frame, text="Delete Selected", bg="blue", fg="white", font=("Arial", 15, "bold"),
    padx=10, pady=5, bd=3, relief="raised", cursor="hand2", width=15, height=2,
    wraplength=100, justify="center",
)
# Make the label behave like a button
delete_label.bind("<Button-1>", lambda event: delete_note())

# Optional hover effect
delete_label.bind("<Enter>", lambda e: delete_label.config(bg="deepskyblue"))
delete_label.bind("<Leave>", lambda e: delete_label.config(bg="blue"))

delete_label.pack(side=tk.LEFT, padx=10)

# Exit button (Label)
exit_label = tk.Label(
    btn_frame, text="Exit", bg="blue", fg="white", font=("Arial", 15, "bold"),
    padx=10, pady=5, bd=3, relief="raised", cursor="hand2", width=15, height=2,
    wraplength=100, justify="center",
)
# Make the label behave like a button
exit_label.bind("<Button-1>", lambda event: root.quit())

# Optional hover effect
exit_label.bind("<Enter>", lambda e: exit_label.config(bg="deepskyblue"))
exit_label.bind("<Leave>", lambda e: exit_label.config(bg="blue"))

exit_label.pack(side=tk.LEFT, padx=10)

# Fills in the note when the app starts.
# Starts the GUI event loop (keeps the window open)
refresh_notes()
root.mainloop()
