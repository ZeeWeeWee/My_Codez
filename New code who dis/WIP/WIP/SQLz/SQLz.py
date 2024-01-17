import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import sqlite3

def is_sqlite3(filename):
    """Check if a file is a valid SQLite3 database."""
    with open(filename, 'rb') as f:
        header = f.read(16)
        return header == b'SQLite format 3\x00'

def open_db_file():
    file_path = filedialog.askopenfilename(title="Select a .db file", filetypes=[("db files", "*.db")])
    if not file_path:
        return

    # Check if the file is a valid SQLite database
    if not is_sqlite3(file_path):
        messagebox.showerror("Error", "The selected file is not a valid SQLite database.")
        return

    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = cursor.fetchone()[0]

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Clear the existing treeview content
        for row in tree.get_children():
            tree.delete(row)

        # Add new content
        for row in rows:
            tree.insert("", "end", values=row)

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

app = tk.Tk()
app.title("SQL .dat Viewer")

open_button = tk.Button(app, text="Open .db File", command=open_db_file)
open_button.pack(pady=20)

# Creating a treeview to display SQL data
tree = ttk.Treeview(app, columns=(1,2,3), show="headings", height=15)
tree.pack(pady=20)

app.mainloop()
