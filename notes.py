import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --- CONFIGURATION ---
NOTES_FILE = "notes.json"
# Dark Theme Colors
COLORS = {
    "bg": "#2d2d2d",           # Main Background (Dark Grey)
    "panel": "#333333",        # Side Panel (Slightly lighter)
    "fg": "#ffffff",           # Text Color (White)
    "accent": "#4a90e2",       # Blue Accent
    "accent_hover": "#357abd", # Darker Blue for hover
    "list_bg": "#252526",      # Treeview background
    "entry_bg": "#3c3c3c",     # Input fields background
}

class ModernNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Notes")
        self.root.geometry("1100x650")
        self.root.configure(bg=COLORS["bg"])

        # State variable to track if we are editing an existing note
        self.current_note_index = None

        # Load Styling
        self.setup_styles()
        
        # Build Layout
        self.create_layout()
        
        # Load Data
        self.refresh_notes()

    def setup_styles(self):
        """Configures the custom look and feel using ttk.Style"""
        style = ttk.Style()
        style.theme_use('clam') 

        # Scrollbar
        style.configure("Vertical.TScrollbar", gripcount=0,
                        background=COLORS["panel"], darkcolor=COLORS["bg"], 
                        lightcolor=COLORS["bg"], troughcolor=COLORS["bg"], bordercolor=COLORS["bg"], arrowcolor=COLORS["fg"])

        # Treeview (The List)
        style.configure("Treeview", 
                        background=COLORS["list_bg"],
                        foreground=COLORS["fg"], 
                        fieldbackground=COLORS["list_bg"],
                        font=("Segoe UI", 11),
                        rowheight=30,
                        borderwidth=0)
        
        style.map('Treeview', background=[('selected', COLORS["accent"])])

        # Treeview Heading
        style.configure("Treeview.Heading", 
                        background=COLORS["panel"], 
                        foreground=COLORS["fg"], 
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0)

    def create_layout(self):
        # --- MAIN CONTAINER (Split into Left and Right) ---
        main_paned = tk.PanedWindow(self.root, bg=COLORS["bg"], orient=tk.HORIZONTAL, sashwidth=4, sashrelief=tk.FLAT)
        main_paned.pack(fill=tk.BOTH, expand=True)

        # --- LEFT SIDE: SIDEBAR (List of Notes) ---
        sidebar = tk.Frame(main_paned, bg=COLORS["panel"], width=300)
        main_paned.add(sidebar)

        # Title for Sidebar
        tk.Label(sidebar, text="ALL NOTES", bg=COLORS["panel"], fg="#888888", 
                 font=("Segoe UI", 9, "bold"), anchor="w").pack(fill=tk.X, padx=15, pady=(15, 5))

        # Treeview
        columns = ('note_preview', 'timestamp')
        self.tree = ttk.Treeview(sidebar, columns=columns, show='', selectmode="browse")
        self.tree.column('note_preview', width=180)
        self.tree.column('timestamp', width=100, anchor='e')
        
        # Add scrollbar to tree
        scrollbar = ttk.Scrollbar(sidebar, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=10)
        
        # Bind click event
        self.tree.bind('<<TreeviewSelect>>', self.load_selected_note)

        # --- RIGHT SIDE: EDITOR ---
        editor_frame = tk.Frame(main_paned, bg=COLORS["bg"])
        main_paned.add(editor_frame)

        # Toolbar (Buttons)
        toolbar = tk.Frame(editor_frame, bg=COLORS["bg"])
        toolbar.pack(fill=tk.X, padx=20, pady=15)

        self.btn_new = self.create_button(toolbar, "+ New Note", self.clear_editor, bg=COLORS["accent"])
        self.btn_new.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_save = self.create_button(toolbar, "💾 Save", self.save_note, bg="#388e3c") # Green
        self.btn_save.pack(side=tk.LEFT)

        self.btn_delete = self.create_button(toolbar, "🗑 Delete", self.delete_note, bg="#d32f2f") # Red
        self.btn_delete.pack(side=tk.RIGHT)

        # Note Input Area
        self.note_text = tk.Text(editor_frame, bg=COLORS["entry_bg"], fg=COLORS["fg"], 
                                 font=("Consolas", 12), borderwidth=0, highlightthickness=0, 
                                 insertbackground="white", padx=15, pady=15)
        self.note_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    def create_button(self, parent, text, command, bg):
        """Helper to create a flat, modern button"""
        # --- UPDATE: fg and activeforeground changed to "black" ---
        btn = tk.Button(parent, text=text, command=command, 
                        bg=bg, fg="black", activebackground=bg, activeforeground="black",
                        font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=8, cursor="hand2")
        
        # Add hover effect
        def on_enter(e): btn.config(bg=self.adjust_color_brightness(bg, 1.1)) # Lighter
        def on_leave(e): btn.config(bg=bg) # Original

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def adjust_color_brightness(self, hex_color, factor):
        """Utility to make a hex color lighter/darker for hover effects"""
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    # --- LOGIC ---

    def load_notes_from_file(self):
        if os.path.exists(NOTES_FILE):
            try:
                with open(NOTES_FILE, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, ValueError):
                return []
        return []

    def save_notes_to_file(self, notes):
        with open(NOTES_FILE, "w") as file:
            json.dump(notes, file, indent=2)

    def refresh_notes(self):
        # clear list
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        notes = self.load_notes_from_file()
        for i, note in enumerate(notes):
            # Show first 30 chars as preview
            preview = note['note'][:30].replace("\n", " ") + "..." if len(note['note']) > 30 else note['note']
            # Format timestamp to look cleaner (e.g., "Oct 24 10:30")
            ts = note.get('timestamp', '')
            try:
                dt_obj = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                pretty_ts = dt_obj.strftime("%b %d, %H:%M")
            except:
                pretty_ts = ts
                
            self.tree.insert('', 'end', iid=i, values=(preview, pretty_ts))

    def load_selected_note(self, event):
        selected = self.tree.focus()
        if not selected: return
        
        index = int(selected)
        notes = self.load_notes_from_file()
        
        if 0 <= index < len(notes):
            self.current_note_index = index
            full_text = notes[index]['note']
            
            self.note_text.delete("1.0", tk.END)
            self.note_text.insert("1.0", full_text)

    def save_note(self):
        content = self.note_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Note cannot be empty")
            return

        notes = self.load_notes_from_file()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.current_note_index is not None:
            # Update existing
            notes[self.current_note_index]['note'] = content
            notes[self.current_note_index]['timestamp'] = timestamp
        else:
            # Create new
            notes.append({"note": content, "timestamp": timestamp})
        
        self.save_notes_to_file(notes)
        self.refresh_notes()
        
        # If we just created a new note, select it
        if self.current_note_index is None:
            new_index = len(notes) - 1
            self.current_note_index = new_index
            self.tree.selection_set(new_index)
            self.tree.focus(new_index)

    def delete_note(self):
        if self.current_note_index is None:
            messagebox.showwarning("Selection Error", "Please select a note to delete.")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?")
        if confirm:
            notes = self.load_notes_from_file()
            if 0 <= self.current_note_index < len(notes):
                notes.pop(self.current_note_index)
                self.save_notes_to_file(notes)
                self.clear_editor()
                self.refresh_notes()

    def clear_editor(self):
        self.note_text.delete("1.0", tk.END)
        self.current_note_index = None
        # Deselect tree
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

# --- RUN APP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernNotesApp(root)
    root.mainloop()