import tkinter as tk
from tkinter import ttk
from ftplib import FTP
import sqlite3
import tkinter.messagebox as messagebox

# FTP credentials
ftp_username = None
ftp_password = None

def show_login_dialog():
    global ftp_username, ftp_password

    login_dialog = tk.Toplevel()
    login_dialog.title("FTP Login")

    tk.Label(login_dialog, text="Username:").pack(padx=10, pady=5)
    username_entry = tk.Entry(login_dialog)
    username_entry.pack(padx=10, pady=5)

    tk.Label(login_dialog, text="Password:").pack(padx=10, pady=5)
    password_entry = tk.Entry(login_dialog, show="*")
    password_entry.pack(padx=10, pady=5)

    def on_ok():
        global ftp_username, ftp_password
        ftp_username = username_entry.get()
        ftp_password = password_entry.get()
        login_dialog.destroy()

    def cancel_login():
        login_dialog.destroy()

    tk.Button(login_dialog, text="OK", command=on_ok).pack(padx=10, pady=5)
    tk.Button(login_dialog, text="Cancel", command=cancel_login).pack(padx=10, pady=5)

# FTP connection logic
def connect_to_ftp():
    global ftp_username, ftp_password

    while ftp_username is None or ftp_password is None:
        show_login_dialog()

    try:
        ftp = FTP('councilofheresy.com')
        ftp.login(user=ftp_username, passwd=ftp_password)
        return ftp
    except:
        messagebox.showerror("FTP Error", "Invalid username or password.")
        ftp_username = None
        ftp_password = None
        return None

# Downloading the database and handling the optional FTP connection
def download_db():
    ftp = connect_to_ftp()

    if ftp:  # If FTP connection is successful
        try:
            with open('store_info.db', 'wb') as localfile:
                ftp.retrbinary('RETR store_info.db', localfile.write, 1024)
            ftp.quit()
        except:
            messagebox.showerror("FTP Error", "Could not download database.")


def upload_db():
    ftp = connect_to_ftp()
    with open('store_info.db', 'rb') as localfile:
        ftp.storbinary('STOR store_info.db', localfile, 1024)
    ftp.quit()
# Database setup
def setup_database():
    # Moved Contract Type before Notes
    conn = sqlite3.connect("store_info.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS stores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT,
                main_contact TEXT,
                cell_phone TEXT,
                credit_processor TEXT,
                address TEXT,
                store_phone TEXT,
                contract_type TEXT,
                notes TEXT
                )""")
    conn.commit()
    conn.close()

# Add entry to database
def add_entry():
    # Moved Contract Type before Notes
    conn = sqlite3.connect("store_info.db")
    c = conn.cursor()
    c.execute("INSERT INTO stores (store_name, main_contact, cell_phone, credit_processor, address, store_phone, contract_type, notes) VALUES (:store_name, :main_contact, :cell_phone, :credit_processor, :address, :store_phone, :contract_type, :notes)",
              {'store_name': entries['Store Name'].get(),
               'main_contact': entries['Main Contact'].get(),
               'cell_phone': entries['Cell Phone'].get(),
               'credit_processor': credit_processor_var.get(),
               'address': entries['Address'].get(),
               'store_phone': entries['Store Phone'].get(),
               'contract_type': contract_type_var.get(),
               'notes': entries['Notes'].get("1.0", tk.END).strip()})
    conn.commit()
    conn.close()
    clear_fields()
    display_records()

    # Clear all entry fields after saving
    for field in fields:
        if field == 'Notes':
            entries[field].delete("1.0", tk.END)
        else:
            entries[field].delete(0, tk.END)

    # Refresh displayed records
    display_records()


# Show entries from database
# Show entries from database with optional search query
def display_records(query=None):
    for row in tree.get_children():
        tree.delete(row)
        
    conn = sqlite3.connect("store_info.db")
    c = conn.cursor()
    
    if query:
        # Assuming you want to search by 'store_name', modify this as needed
        c.execute("SELECT * FROM stores WHERE store_name LIKE ?", ('%' + query + '%',))
    else:
        c.execute("SELECT * FROM stores")
        
    records = c.fetchall()
    
    for record in records:
        tree.insert("", tk.END, values=record)
        
    conn.close()

# Function to perform search
def perform_search():
    query = search_var.get()
    display_records(query)

# Delete selected entry
def delete_entry():
    selected_items = tree.selection()
    if not selected_items:
        return

    selected_item = selected_items[0]
    selected_id = tree.item(selected_item, "values")[0]
    conn = sqlite3.connect("store_info.db")
    c = conn.cursor()
    c.execute("DELETE FROM stores WHERE id=?", (selected_id,))
    conn.commit()
    conn.close()

    # Refresh displayed records
    display_records()

# Populate the entry fields with selected data
def populate_fields(event):
    selected_item = tree.selection()[0]
    selected_values = tree.item(selected_item, "values")

    # Fields list should be in the same order as your database columns
    fields_in_order = ['Store Name', 'Main Contact', 'Cell Phone', 'Credit Processor', 'Address', 'Store Phone', 'Contract Type', 'Notes']

    for idx, field in enumerate(fields_in_order):
        if field == 'Notes':
            entries[field].delete("1.0", tk.END)
            entries[field].insert("1.0", selected_values[idx + 1])
        elif field == 'Contract Type':  # Update the ComboBox for Contract Type
            contract_type_var.set(selected_values[idx + 1])
        elif field == 'Credit Processor':  # Update the ComboBox for Credit Processor
            credit_processor_var.set(selected_values[idx + 1])
        else:
            entries[field].delete(0, tk.END)
            entries[field].insert(0, selected_values[idx + 1])

# Edit selected entry
def edit_entry():
    selected_items = tree.selection()
    if not selected_items:
        return

    selected_item = selected_items[0]
    selected_id = tree.item(selected_item, "values")[0]

    conn = sqlite3.connect("store_info.db")
    c = conn.cursor()

    c.execute("""UPDATE stores SET store_name=?, main_contact=?, cell_phone=?, credit_processor=?, address=?, store_phone=?, contract_type=?, notes=? WHERE id=?""",
              (entries['Store Name'].get(), entries['Main Contact'].get(), entries['Cell Phone'].get(),
               entries['Credit Processor'].get(), entries['Address'].get(), entries['Store Phone'].get(),
               contract_type_var.get(), entries['Notes'].get("1.0", tk.END).strip(), selected_id))

    conn.commit()
    conn.close()

    # Refresh displayed records
    display_records()

    # Clear all entry fields after editing
    for field in fields:
        if field == 'Notes':
            entries[field].delete("1.0", tk.END)
        else:
            entries[field].delete(0, tk.END)

def sort_by_column(tree, col, descending):
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    data.sort(reverse=descending)

    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)

    tree.heading(col,
                 command=lambda col=col: sort_by_column(tree, col, int(not descending)))

# Function to perform search
def perform_search():
    query = search_var.get()
    display_records(query)

# Create the main window
root = tk.Tk()
root.title("Store Information Database")
root.geometry('1000x600')

# Call this function to download the database when the program starts
root.after(0, lambda: download_db() if messagebox.askyesno("FTP", "Do you want to connect to FTP?") else None)


# Create a frame for the entry widgets
entry_frame = tk.Frame(root)
entry_frame.pack(pady=20)

# Replace 'Credit Processor' with 'Contract Type' in fields list
fields = ['Store Name', 'Main Contact', 'Cell Phone', 'Credit Processor', 'Address', 'Store Phone', 'Contract Type', 'Notes']
entries = {}
row_num = 0
col_num = 0

for field in fields[:-1]:  # Exclude the last field 'Notes'
    tk.Label(entry_frame, text=field, width=20, anchor='e').grid(row=row_num, column=col_num)
    
    # Add ComboBox for 'Credit Processor' and 'Contract Type'
    if field == 'Credit Processor':
        credit_processor_var = tk.StringVar()
        entries[field] = ttk.Combobox(entry_frame, textvariable=credit_processor_var, values=["RBS", "First Data", "See Notes"])
    elif field == 'Contract Type':
        contract_type_var = tk.StringVar()
        entries[field] = ttk.Combobox(entry_frame, textvariable=contract_type_var, values=["Full Contract", "Software Only", "Fee Only", "Billable", "COD", "Maintenance", "DNS"])
    else:
        entries[field] = tk.Entry(entry_frame, width=30)
        
    entries[field].grid(row=row_num, column=col_num + 1)
    col_num += 2

    if col_num > 2:
        col_num = 0
        row_num += 1

# Manually add 'Notes' at the end
tk.Label(entry_frame, text="Notes", width=20, anchor='e').grid(row=row_num, column=col_num)
entries['Notes'] = tk.Text(entry_frame, width=30, height=3)
entries['Notes'].grid(row=row_num, column=col_num + 1)
# Clear all entry fields
def clear_fields():
    for field in fields:
        if field == 'Notes':
            entries[field].delete("1.0", tk.END)
        else:
            entries[field].delete(0, tk.END)

# Create buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

ttk.Button(button_frame, text="Add Entry", command=add_entry).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Delete Entry", command=delete_entry).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="Edit Entry", command=edit_entry).grid(row=0, column=2, padx=10)
ttk.Button(button_frame, text="Refresh", command=display_records).grid(row=0, column=3, padx=10)
ttk.Button(button_frame, text="Clear", command=clear_fields).grid(row=0, column=4, padx=10)

# Create Treeview to display data
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=1)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Search Entry and Button
search_var = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_var, width=30)
search_entry.pack(side=tk.LEFT, padx=10, pady=10)
search_button = tk.Button(root, text="Search", command=perform_search)
search_button.pack(side=tk.LEFT, padx=10, pady=10)

# Adjusted columns to match the new database schema
tree = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings", yscrollcommand=tree_scroll.set)
tree.heading(1, text="ID")
tree.heading(2, text="Store Name")
tree.heading(3, text="Main Contact")  # Changed from Employee Name and Position
tree.heading(4, text="Cell Phone")
tree.heading(5, text="Credit Processor")
tree.heading(6, text="Address")
tree.heading(7, text="Store Phone")
tree.heading(8, text="Contract Type")
tree.heading(9, text="Notes")

tree.pack(fill=tk.BOTH, expand=1)

tree_scroll.config(command=tree.yview)

# Add commands for column headers to sort
for col in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
    tree.heading(col, text=tree.heading(col, "text"), command=lambda c=col: sort_by_column(tree, c, False))

# Initialize the database
setup_database()

# Bind the event here, after 'tree' has been defined
tree.bind("<ButtonRelease-1>", populate_fields)

# Initialize displayed records
display_records()

# Custom function to handle application closure
def on_closing():
    if ftp_username is not None and ftp_password is not None:
        upload_db()
    root.destroy()

# Hook the function to the WM_DELETE_WINDOW event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main loop
root.mainloop()