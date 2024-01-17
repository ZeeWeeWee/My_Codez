import sqlite3
import tkinter as tk
from tkinter import ttk

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

# Show entries from database with optional search query
def display_records(query=None):
    for row in tree.get_children():
        tree.delete(row)
        
    conn = sqlite3.connect("store_info.db")
    c = conn.cursor()
    
    if query:
        # Search by both 'store_name' and 'address'
        c.execute("SELECT * FROM stores WHERE store_name LIKE ? OR address LIKE ?", ('%' + query + '%', '%' + query + '%'))
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

# Run the main loop
root.mainloop()

