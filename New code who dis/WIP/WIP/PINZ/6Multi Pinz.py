import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox 
from tkinter import ttk 
import sqlite3

class App:
    def __init__(self, root):
        root.title("Pinpad Management")
        width, height = 1040, 385
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_69 = tk.Button(root, bg="#f0f0f0", text="New Entry", command=self.new_entry_form)
        GButton_69.place(x=210, y=350, width=70, height=25)

        GButton_393 = tk.Button(root, bg="#f0f0f0", text="Edit Entry", command=self.edit_or_rma_dialog)
        GButton_393.place(x=300, y=350, width=70, height=25)

        
        GButton_Delete = tk.Button(root, bg="#f0f0f0", text="Delete Entry", command=self.delete_entry_form)
        GButton_Delete.place(x=390, y=350, width=100, height=25)


        self.tree = ttk.Treeview(root, columns=("Serial Number", "Status"), show="headings")
        self.tree.heading("Serial Number", text="Serial Number")
        self.tree.heading("Status", text="Status")
        self.tree.place(x=220, y=40, width=261, height=281)
        
        self.tree_field = ttk.Treeview(root, columns=('Serial Number', 'Location', 'Status'), show="headings")
        self.tree_field.heading('Serial Number', text='Serial Number')
        self.tree_field.heading('Location', text="Location")
        self.tree_field.heading('Status', text='Status')
        self.tree_field.place(x=490, y=40, width=261, height=281)

        self.tree_rma = ttk.Treeview(root, columns=('Serial Number', 'Status', 'RMA Number'), show="headings")
        self.tree_rma.heading('#1', text="Serial Number")
        self.tree_rma.heading('#2', text="Status")
        self.tree_rma.heading('#3', text="RMA Number")
        self.tree_rma.place(x=760, y=40, width=261, height=281)

        self.populate_treeviews()  # Populate treeviews when the program starts
        
        self.side_panel = tk.Frame(root, bg="#f0f0f0", width=200, height=400)
        self.side_panel.place(x=10, y=40)
        
        self.tree.bind("<ButtonRelease-1>", self.update_side_panel)
        self.tree_field.bind("<ButtonRelease-1>", self.update_side_panel)
        self.tree_rma.bind("<ButtonRelease-1>", self.update_side_panel)
        
    def update_side_panel(self, event):
        # Unselect items in other Treeviews
        for tree in [self.tree, self.tree_field, self.tree_rma]:
            if tree is not event.widget:
                tree.selection_remove(tree.selection())
            # Clear existing widgets in the side panel
            for widget in self.side_panel.winfo_children():
                widget.destroy()

        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            selected_serial_number = tree.item(selected_item, "values")[0]
            conn = sqlite3.connect("pinpads.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pinpads WHERE serial_number = ?", (selected_serial_number,))
            record = cursor.fetchone()
            conn.close()

            if record:
                labels = ["Serial Number", "Status", "Date Received", "Received From", "Condition Received", "Processor Loaded", "Date Left", "Sent To","RMA Number",  "Reason for RMA"]
                for i, (label, value) in enumerate(zip(labels, (record[1], record[2], record[3], record[5], record[6], record[7], record[8], record[9], record[14],  record[16]))):
                    tk.Label(self.side_panel, text=f"{label}: {value if value else 'N/A'}").pack(anchor="w")

    def populate_treeviews(self):
        for tree in [self.tree, self.tree_field, self.tree_rma]:
            for row in tree.get_children():
                tree.delete(row)
        try:
            conn = sqlite3.connect("pinpads.db")
            cursor = conn.cursor()
            
        

            # Populate first Treeview (In the Shop)
            cursor.execute("SELECT * FROM pinpads WHERE status = ?", ('In the Shop',))
            records_shop = cursor.fetchall()
            for record in records_shop:
                self.tree.insert('', tk.END, values=(record[1], record[2]))

            # Populate second Treeview (In the Field)
            cursor.execute("SELECT * FROM pinpads WHERE status = ?", ('In the Field',))
            records_field = cursor.fetchall()
            for record in records_field:
                print("Record:", record)
                self.tree_field.insert('', tk.END, values=(record[1], record[9], record[2]))
                
             # Populate third Treeview (Out for RMA)
            cursor.execute("SELECT * FROM pinpads WHERE status = ?", ('Out for RMA',))
            records_rma = cursor.fetchall()
            for record in records_rma:
                self.tree_rma.insert('', tk.END, values=(record[1], record[2], record[14]))  # Assuming RMA number is at index 14


            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")
        

    def add_new_entry(self, top, entry_vars):
        form_values = [var.get() for var in entry_vars]
        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO pinpads (serial_number, arrival_from, condition_received, processor_loaded, status, date_entered)
            VALUES (?, ?, ?, ?, ?, date('now'))
            """, form_values)
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Duplicate Entry", "Serial number already exists. Please enter a unique serial number.")
        finally:
            conn.close()
            top.destroy()
            self.populate_treeviews()  # Refresh the Treeviews
        
    def new_entry_form(self):
        top = tk.Toplevel()
        top.title("New Pinpad Entry")

        entry_vars = []  # List to hold the StringVar objects for each field

        labels = ["Serial Number", "Arrival From", "Condition Received", "Processor Loaded", "Status"]
        first_entry = None
        for i, label in enumerate(labels):
            tk.Label(top, text=label).grid(row=i, column=0)

            entry_var = tk.StringVar()
            entry_vars.append(entry_var)

            if label == "Processor Loaded":
                processor_options = ["First Data/Concord", "RBS/World Pay"]
                processor_combobox = ttk.Combobox(top, values=processor_options, textvariable=entry_var)
                processor_combobox.grid(row=i, column=1)
            elif label == "Status":
                status_options = ["In the Shop", "In the Field", "Out for RMA"]
                status_combobox = ttk.Combobox(top, values=status_options, textvariable=entry_var)
                status_combobox.grid(row=i, column=1)
                status_combobox.current(0)  # Set default value
            else:
                if i == 0:  # This is the first entry
                    first_entry = tk.Entry(top, textvariable=entry_var)
                    first_entry.grid(row=i, column=1)
                else:
                    tk.Entry(top, textvariable=entry_var).grid(row=i, column=1)

        first_entry.focus_set()  # Set focus to the first Entry

        submit_btn = tk.Button(top, text="Submit", command=lambda: self.add_new_entry(top, entry_vars))
        submit_btn.grid(row=len(labels), columnspan=2)

        
    def edit_or_rma_dialog(self):
        top = tk.Toplevel()
        top.title("Edit or RMA")

        tk.Label(top, text="Is the pinpad being sent to a store or for RMA?").pack()

        tk.Button(top, text="Send to Store", command=lambda: [self.edit_entry_form(), top.destroy()]).pack(side="left")
        tk.Button(top, text="Send for RMA", command=lambda: [self.rma_update_form(), top.destroy()]).pack(side="right")

    def rma_update_form(self):
        selected_tree = None
        selected_item = None
        for tree in [self.tree, self.tree_field, self.tree_rma]:
            selected_item = tree.selection()
            if selected_item:
                selected_tree = tree
                break  # Exit loop once we find a selected item

        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an entry to edit.")
            return

        selected_serial_number = selected_tree.item(selected_item, "values")[0]

        # Fetch existing data from database for pre-filling the form fields
        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pinpads WHERE serial_number = ?", (selected_serial_number,))
        existing_data = cursor.fetchone()
        conn.close()

        top = tk.Toplevel()
        top.title(f"Edit Pinpad Entry for {selected_serial_number}")

        tk.Label(top, text=f"Serial Number: {selected_serial_number}").grid(row=0, column=0, columnspan=2)

        editable_fields = ["Status", "Sent To", "Processor Loaded When Left"]
        entry_vars = []

        def on_status_change(event):
            selected_status = status_var.get()
            if selected_status == 'Out for RMA':
                sent_to_var.set('VeriFone')

        # Assuming these are the correct indices for your database columns
        existing_values = [existing_data[2], existing_data[9], existing_data[11]]  
        status_var = tk.StringVar()
        sent_to_var = tk.StringVar()

        first_entry = None  # To hold the first entry widget
        for i, (field, existing_value) in enumerate(zip(editable_fields, existing_values), start=1):
            tk.Label(top, text=field).grid(row=i, column=0)

            entry_var = tk.StringVar()
            entry_var.set(existing_value)
            entry_vars.append(entry_var)

            if field == 'Status':
                status_options = ['In the Shop', 'In the Field', 'Out for RMA']
                status_combobox = ttk.Combobox(top, values=status_options, textvariable=entry_var)
                status_combobox.grid(row=i, column=1)
                status_combobox.bind('<<ComboboxSelected>>', on_status_change)
                status_var = entry_var
            elif field == 'Processor Loaded When Left':
                processor_options = ['First Data/Concord', 'RBS/World Pay/5th3rd']
                processor_combobox = ttk.Combobox(top, values=processor_options, textvariable=entry_var)
                processor_combobox.grid(row=i, column=1)
            else:
                sent_to_entry = tk.Entry(top, textvariable=entry_var)
                sent_to_entry.grid(row=i, column=1)
                sent_to_var = entry_var

        if first_entry:  # Check if first_entry is not None
            first_entry.focus_set()  # Set focus to the first editable field

        submit_btn = tk.Button(top, text="Update", command=lambda: self.update_entry(top, selected_serial_number, entry_vars))
        submit_btn.grid(row=len(editable_fields) + 1, columnspan=2)

    def edit_entry_form(self):
        selected_tree = None
        selected_item = None
        for tree in [self.tree, self.tree_field, self.tree_rma]:
            selected_item = tree.selection()
            if selected_item:
                selected_tree = tree
                break  # Exit loop once we find a selected item

        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an entry to edit.")
            return

        selected_serial_number = selected_tree.item(selected_item, "values")[0]

        # Fetch existing data from database for pre-filling the form fields
        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pinpads WHERE serial_number = ?", (selected_serial_number,))
        existing_data = cursor.fetchone()
        conn.close()

        top = tk.Toplevel()
        top.title(f"Edit Pinpad Entry for {selected_serial_number}")

        tk.Label(top, text=f"Serial Number: {selected_serial_number}").grid(row=0, column=0, columnspan=2)

        editable_fields = ["Status", "Sent To", "Processor Loaded When Left"]
        entry_vars = []

        def on_status_change(event):
            selected_status = status_var.get()
            if selected_status == 'Out for RMA':
                sent_to_var.set('VeriFone')

        # Assuming these are the correct indices for your database columns
        existing_values = [existing_data[2], existing_data[9], existing_data[11]]  
        status_var = tk.StringVar()
        sent_to_var = tk.StringVar()

        first_entry = None  # To hold the first entry widget
        for i, (field, existing_value) in enumerate(zip(editable_fields, existing_values), start=1):
            tk.Label(top, text=field).grid(row=i, column=0)

            entry_var = tk.StringVar()
            entry_var.set(existing_value)
            entry_vars.append(entry_var)

            if field == 'Status':
                status_options = ['In the Shop', 'In the Field', 'Out for RMA']
                status_combobox = ttk.Combobox(top, values=status_options, textvariable=entry_var)
                status_combobox.grid(row=i, column=1)
                status_combobox.bind('<<ComboboxSelected>>', on_status_change)
                status_var = entry_var
            elif field == 'Processor Loaded When Left':
                processor_options = ['First Data/Concord', 'RBS/World Pay/5th3rd']
                processor_combobox = ttk.Combobox(top, values=processor_options, textvariable=entry_var)
                processor_combobox.grid(row=i, column=1)
            else:
                sent_to_entry = tk.Entry(top, textvariable=entry_var)
                sent_to_entry.grid(row=i, column=1)
                sent_to_var = entry_var

        if first_entry:  # Check if first_entry is not None
            first_entry.focus_set()  # Set focus to the first editable field

        submit_btn = tk.Button(top, text="Update", command=lambda: self.update_entry(top, selected_serial_number, entry_vars))
        submit_btn.grid(row=len(editable_fields) + 1, columnspan=2)

        
    def update_entry(self, top, selected_serial_number, entry_vars):
        form_values = [var.get() for var in entry_vars]
        
        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE pinpads SET
            status = ?,
            sent_to = ?,
            processor_loaded_when_left = ?,
            date_left_office = datetime('now')
        WHERE serial_number = ?
        """, form_values + [selected_serial_number])
        conn.commit()
        conn.close()
        top.destroy()
        self.populate_treeviews()
        
    def delete_entry_form(self):
        selected_tree = None
        selected_item = None
        for tree in [self.tree, self.tree_field, self.tree_rma]:
            selected_item = tree.selection()
            if selected_item:
                selected_tree = tree
                break  # Exit loop once we find a selected item

        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an entry to delete.")
            return

        selected_serial_number = selected_tree.item(selected_item, "values")[0]

        confirm_delete = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the entry with Serial Number: {selected_serial_number}?")

        if confirm_delete:
            try:
                conn = sqlite3.connect("pinpads.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pinpads WHERE serial_number = ?", (selected_serial_number,))
                conn.commit()
                conn.close()

                print(f"Deleted serial number: {selected_serial_number}")

                # Remove the item from the Treeview as well
                selected_tree.delete(selected_item)

                # Refresh the Treeviews
                self.populate_treeviews()
            except Exception as e:
                print(f"An error occurred while deleting: {e}")

def initialize_db():
    conn = sqlite3.connect("pinpads.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pinpads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        serial_number TEXT UNIQUE,
        status TEXT,
        date_entered TEXT,
        date_changed TEXT,
        arrival_from TEXT,
        condition_received TEXT,
        processor_loaded TEXT,
        date_left_office TEXT,
        sent_to TEXT,
        condition_left TEXT,
        processor_loaded_when_left TEXT,
        ticket_number TEXT,
        rma_status TEXT,
        rma_number TEXT,
        date_left_for_rma TEXT,
        reason_for_rma TEXT,
        original_ticket_number TEXT,
        date_returned_from_rma TEXT
    )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
