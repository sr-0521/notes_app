import json
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

NOTES_FILE = "notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    return []

def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=2)

def refresh_notes():
    notes = load_notes()
    for row in tree.get_children():
        tree.delete(row)
    for i, note in enumerate(notes):
        tree.insert('', 'end', iid=i, values=(i+1, note['note'], note['timestamp']))

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
root = tk.Tk()
root.title("Notes App")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

note_entry = tk.Entry(frame, width=40)
note_entry.pack(side=tk.LEFT, padx=5)

add_btn = tk.Button(frame, text="Add Note", command=add_note)
add_btn.pack(side=tk.LEFT, padx=5)

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

edit_btn = tk.Button(btn_frame, text="Edit Selected", command=edit_note, width=15)
edit_btn.pack(side=tk.LEFT, padx=10)

delete_btn = tk.Button(btn_frame, text="Delete Selected", command=delete_note, width=15)
delete_btn.pack(side=tk.LEFT, padx=10)

exit_btn = tk.Button(btn_frame, text="Exit", command=root.quit, width=15)
exit_btn.pack(side=tk.LEFT, padx=10)

refresh_notes()
root.mainloop()