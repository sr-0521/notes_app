# 📝 Modern Desktop Notes App
A lightweight, dark-themed note-taking application built with Python.

This project is a desktop application designed to provide a clean, distraction-free environment for taking quick notes. Unlike standard Tkinter applications that often look dated, this app features a custom Dark Mode UI, a split-view layout, and persistent JSON storage.

# 📸 Preview
<img width="1095" height="675" alt="Screenshot 2025-12-17 at 10 46 52 PM" src="https://github.com/user-attachments/assets/195bb72e-f07d-4382-b31d-7dea4b874029" />


# 🚀 Features
Modern Dark UI: Custom color palette (#2d2d2d background) with generic Tkinter widgets styled to look flat and modern.

Persistent Storage: Notes are automatically saved to a local notes.json file, ensuring data persists between sessions.

Split-View Layout: Classic "Master-Detail" view allows users to browse notes on the left while editing on the right.

CRUD Operations: Full capability to Create, Read, Update, and Delete notes.

Dynamic Timestamps: Automatically tracks and updates the "Last Modified" time for every note.

# 🛠️ Tech Stack
Language: Python 3.x

GUI Framework: Tkinter & ttk (Themed Tkinter)

Data Storage: JSON (Flat file database)

# 💻 Code Highlights
The application is structured using Object-Oriented Programming (OOP) to maintain clean separation between the Layout, Styling, and Logic.

Custom UI Styling

Standard Tkinter buttons look outdated, so I implemented a helper method to generate flat, modern buttons with hover effects:

Python
def create_button(self, parent, text, command, bg):
    btn = tk.Button(parent, text=text, command=command, 
                    bg=bg, fg="black", bd=0, padx=15, pady=8)
    
    # Dynamic Hover Effects
    btn.bind("<Enter>", lambda e: btn.config(bg=lighter_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=original_color))
    return btn
JSON Data Persistence

Data is managed through a lightweight JSON handler that ensures state is saved instantly upon every edit:

Python
def save_note(self):
    # Logic to update existing note or append new one
    notes = self.load_notes_from_file()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    notes[self.current_note_index]['note'] = content
    notes[self.current_note_index]['timestamp'] = timestamp
    
    self.save_notes_to_file(notes)
# 🎮 How to Run
Clone the repository:

Bash
git clone https://github.com/yourusername/notes_app.git
Navigate to the folder:

Bash
cd modern-notes-app
Run the application:

Bash
python3 notes.py
(No external dependencies or pip install required!)

🔮 Future Improvements
Add a Search Bar to filter notes by text.

Implement Markdown rendering for the text editor.

Add cloud sync support (Google Drive API).
