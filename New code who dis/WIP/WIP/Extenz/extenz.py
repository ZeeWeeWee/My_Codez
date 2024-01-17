import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

# Database Functions

def initialize_db():
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                extension TEXT,
                desk_phone TEXT,
                cell_phone TEXT,
                branch TEXT
            )
        ''')
        conn.commit()

# Function to handle clicking a phone number
def open_in_webex(phone_number):
    os.system(f"start tel:{phone_number}")

def add_contact(name, extension, desk_phone, cell_phone, branch):
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts (name, extension, desk_phone, cell_phone, branch) VALUES (?, ?, ?, ?, ?)',
                       (name, extension, desk_phone, cell_phone, branch))
        conn.commit()

def list_contacts():
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, extension, desk_phone, cell_phone, branch FROM contacts ORDER BY name')
        return cursor.fetchall()

def edit_contact(old_name, new_name, new_extension, new_desk_phone, new_cell_phone, new_branch):
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE contacts 
            SET name = ?, extension = ?, desk_phone = ?, cell_phone = ?, branch = ?
            WHERE name = ?''', (new_name, new_extension, new_desk_phone, new_cell_phone, new_branch, old_name))
        conn.commit()

def delete_contact(name):
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE name = ?', (name,))
        conn.commit()

def search_contact(name):
    with sqlite3.connect('contacts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, extension, desk_phone, cell_phone, branch FROM contacts WHERE name LIKE ?', ('%' + name + '%',))
        return cursor.fetchall()


# GUI Functions

# Function to refresh the list of contacts
def refresh_list():
    contacts = list_contacts()
    contacts_list.delete(*contacts_list.get_children())
    for contact in contacts:
        contacts_list.insert("", "end", values=contact)

# Function to handle clicking an item in the Treeview
def on_tree_click(event):
    col = contacts_list.identify_column(event.x)
    item = contacts_list.identify_row(event.y)
    item_values = contacts_list.item(item, "values")
    
    print(f"Clicked column: {col}")  # Debugging line
    
    if col in ["#2", "#3", "#4"]:  # Extension, Desk Phone, and Cell Phone columns
        col_index = int(col.lstrip("#")) - 1  # Convert '#2' to 1, '#3' to 2, etc.
        print(f"Attempting to open Webex with phone number: {item_values[col_index]}")  # Debugging line
        open_in_webex(item_values[col_index])

def add_contact_gui():
    def save_contact():
        name = name_entry.get()
        extension = extension_entry.get()
        desk_phone = desk_phone_entry.get()
        cell_phone = cell_phone_entry.get()
        branch = branch_entry.get()
        if name:
            add_contact(name, extension, desk_phone, cell_phone, branch)
            add_window.destroy()
            refresh_list()
        else:
            messagebox.showerror("Error", "Name is required")

    add_window = tk.Toplevel(root)
    add_window.title("Add Contact")

    labels = ["Name", "Extension", "Desk Phone Number", "Cell Phone Number", "Branch"]
    for i, label in enumerate(labels):
        ttk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")

    name_entry = ttk.Entry(add_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    extension_entry = ttk.Entry(add_window)
    extension_entry.grid(row=1, column=1, padx=10, pady=5)

    desk_phone_entry = ttk.Entry(add_window)
    desk_phone_entry.grid(row=2, column=1, padx=10, pady=5)

    cell_phone_entry = ttk.Entry(add_window)
    cell_phone_entry.grid(row=3, column=1, padx=10, pady=5)

    branch_entry = ttk.Entry(add_window)
    branch_entry.grid(row=4, column=1, padx=10, pady=5)

    ttk.Button(add_window, text="Save", command=save_contact).grid(row=5, column=1, padx=10, pady=10, sticky="e")

def edit_contact_gui():
    selected_items = contacts_list.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select a contact to edit.")
        return
    old_contact = contacts_list.item(selected_items[0], "values")
    old_name = old_contact[0]

    def update_contact():
        new_name = name_entry.get()
        new_extension = extension_entry.get()
        new_desk_phone = desk_phone_entry.get()
        new_cell_phone = cell_phone_entry.get()
        new_branch = branch_entry.get()
        if new_name:
            edit_contact(old_name, new_name, new_extension, new_desk_phone, new_cell_phone, new_branch)
            edit_window.destroy()
            refresh_list()
        else:
            messagebox.showerror("Error", "Name is required")

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Contact")

    labels = ["Name", "Extension", "Desk Phone Number", "Cell Phone Number", "Branch"]
    for i, label in enumerate(labels):
        ttk.Label(edit_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")

    name_entry = ttk.Entry(edit_window)
    name_entry.insert(0, old_contact[0])
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    extension_entry = ttk.Entry(edit_window)
    extension_entry.insert(0, old_contact[1])
    extension_entry.grid(row=1, column=1, padx=10, pady=5)

    desk_phone_entry = ttk.Entry(edit_window)
    desk_phone_entry.insert(0, old_contact[2])
    desk_phone_entry.grid(row=2, column=1, padx=10, pady=5)

    cell_phone_entry = ttk.Entry(edit_window)
    cell_phone_entry.insert(0, old_contact[3])
    cell_phone_entry.grid(row=3, column=1, padx=10, pady=5)

    branch_entry = ttk.Entry(edit_window)
    branch_entry.insert(0, old_contact[4])
    branch_entry.grid(row=4, column=1, padx=10, pady=5)

    ttk.Button(edit_window, text="Update", command=update_contact).grid(row=5, column=1, padx=10, pady=10, sticky="e")

def delete_contact_gui():
    selected_items = contacts_list.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select a contact to delete.")
        return
    name = contacts_list.item(selected_items[0], "values")[0]
    answer = messagebox.askyesno("Confirmation", f"Do you really want to delete {name}?")
    if answer:
        delete_contact(name)
        refresh_list()

def search_contact_gui():
    name = search_entry.get()
    contacts = search_contact(name)
    contacts_list.delete(*contacts_list.get_children())
    for contact in contacts:
        contacts_list.insert("", "end", values=contact)


# Main GUI

root = tk.Tk()
root.title("extenz")
root.iconbitmap('c:\\buttonz\\extenz.ico')


frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

contacts_list = ttk.Treeview(frame, columns=("Name", "Extension", "Desk Phone", "Cell Phone", "Branch"), show="headings")
contacts_list.heading("Name", text="Name")
contacts_list.heading("Extension", text="Extension")
contacts_list.heading("Desk Phone", text="Desk Phone")
contacts_list.heading("Cell Phone", text="Cell Phone")
contacts_list.heading("Branch", text="Branch")
contacts_list.pack(fill="both", expand=True)

contacts_list.bind('<ButtonRelease-3>', on_tree_click)

button_frame = ttk.Frame(root)
button_frame.pack(padx=10, pady=10, fill="x")

search_entry = ttk.Entry(button_frame)
search_entry.pack(side="left", padx=5)
ttk.Button(button_frame, text="Search", command=search_contact_gui).pack(side="left", padx=5)
ttk.Button(button_frame, text="Edit", command=edit_contact_gui).pack(side="left", padx=5)
ttk.Button(button_frame, text="Delete", command=delete_contact_gui).pack(side="left", padx=5)


ttk.Button(button_frame, text="Add", command=add_contact_gui).pack(side="left", padx=5)
ttk.Button(button_frame, text="Refresh", command=refresh_list).pack(side="right", padx=5)

initialize_db()
refresh_list()
root.mainloop()
