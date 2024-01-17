import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox 
from tkinter import ttk 
import sqlite3

class App:
    def __init__(self, root):
        root.title("Pinpad Management")
        width, height = 1015, 385
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_69 = tk.Button(root, bg="#f0f0f0", text="New Entry", command=self.new_entry_form)
        GButton_69.place(x=20, y=350, width=70, height=25)

        GButton_393 = tk.Button(root, bg="#f0f0f0", text="Edit Entry", command=self.edit_entry_form)
        GButton_393.place(x=110, y=350, width=70, height=25)

        self.tree = ttk.Treeview(root, columns=("Serial Number", "Status"), show="headings")
        self.tree.heading("Serial Number", text="Serial Number")
        self.tree.heading("Status", text="Status")
        self.tree.place(x=210, y=40, width=261, height=281)
        
        self.tree_field = ttk.Treeview(root, columns=('Location', 'Serial Number', 'Status'), show="headings")
        self.tree_field.heading('Location', text="Location")
        self.tree_field.heading('Serial Number', text='Serial Number')
        self.tree_field.heading('Status', text='Status')

        self.tree_field.place(x=480, y=40, width=261, height=281)


        self.populate_treeviews()  # Populate treeviews when the program starts

    def populate_treeviews(self):
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
                self.tree_field.insert('', tk.END, values=(record[9], record[1], record[2]))

            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")

    def new_entry_form(self):
        top = tk.Toplevel()
        top.title("New Pinpad Entry")

        labels = ["Serial Number", "Arrival From", "Condition Received", "Processor Loaded", "Status"]
        for i, label in enumerate(labels):
            tk.Label(top, text=label).grid(row=i, column=0)
            if label == "Status":
                # Create a Combobox for the 'Status' field
                status_options = ["In the Shop", "In the Field", "Out for RMA"]
                status_combobox = ttk.Combobox(top, values=status_options)
                status_combobox.grid(row=i, column=1)
            else:
                tk.Entry(top).grid(row=i, column=1)

        submit_btn = tk.Button(top, text="Submit", command=lambda: self.add_new_entry(top))
        submit_btn.grid(row=len(labels), columnspan=2)
    
    def add_new_entry(self, top):
        form_values = []
        for i in range(5):  # Change the range to match the number of fields including the Combobox
            widget = top.grid_slaves(row=i, column=1)[0]
            if isinstance(widget, ttk.Combobox):
                form_values.append(widget.get())
            else:
                form_values.append(widget.get())
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

    def edit_entry_form(self):
        selected_serial_number = self.GListBox_805.get(tk.ACTIVE)
        top = tk.Toplevel()
        top.title("Edit Pinpad Entry")

        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pinpads WHERE serial_number = ?", (selected_serial_number,))
        record = cursor.fetchone()
        conn.close()

        labels = ["Serial Number", "Arrival From", "Condition Received", "Processor Loaded"]
        for i, (label, value) in enumerate(zip(labels, record[1:5])):
            tk.Label(top, text=label).grid(row=i, column=0)
            entry = tk.Entry(top)
            if value is not None:
                entry.insert(0, str(value))
            entry.grid(row=i, column=1)

        submit_btn = tk.Button(top, text="Update", command=lambda: self.update_entry(top, record[0]))
        submit_btn.grid(row=len(labels), columnspan=2)

    def update_entry(self, top, record_id):
        form_values = [top.grid_slaves(row=i, column=1)[0].get() for i in range(4)]
        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE pinpads SET
            serial_number = ?,
            arrival_from = ?,
            condition_received = ?,
            processor_loaded = ?
        WHERE id = ?
        """, form_values + [record_id])
        conn.commit()
        conn.close()
        top.destroy()

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
