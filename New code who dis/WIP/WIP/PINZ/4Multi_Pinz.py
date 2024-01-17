import tkinter as tk
import tkinter.font as tkFont
import tkinter.simpledialog
from tkinter import messagebox 
from tkinter import ttk 
import sqlite3
import datetime
import webbrowser

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

        self.tree_rma = ttk.Treeview(root, columns=('Serial Number', 'Status', 'RMA Number', 'Ticket URL'), show="headings")
        self.tree_rma.heading('#1', text="Serial Number")
        self.tree_rma.heading('#2', text="Status")
        self.tree_rma.heading('#3', text="RMA Number")
        self.tree_rma.heading('#4', text="Ticket URL")
        self.tree_rma.place(x=750, y=40, width=261, height=281)

        self.tree.tag_configure("hyperlink", foreground="blue")
        self.tree_rma.bind("<Button-1>", self.on_treeview_rma_click)

        self.populate_treeviews()  # Populate treeviews when the program starts

        self.edit_form_open = False

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
                
             # Populate third Treeview (Out for RMA)
            cursor.execute("SELECT * FROM pinpads WHERE status = ?", ('Out for RMA',))
            records_rma = cursor.fetchall()
            for record in records_rma:
                # Assume that record[12] contains the ticket number
                ticket_number = record[12]
                ticket_url = "https://deskninja.com/issue/" + ticket_number
                self.tree_rma.insert('', tk.END, values=(record[1], record[2], record[12], ticket_url), tags=("hyperlink",))
                
            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")

    def on_treeview_rma_click(self, event):
        item = self.tree_rma.item(self.tree_rma.selection())
        if "hyperlink" in item["tags"]:
            url = item["values"][3]  # Assuming the URL is in the 4th column
            webbrowser.open(url)



    def new_entry_form(self):
        top = tk.Toplevel()
        top.title("New Pinpad Entry")

        labels = ["Serial Number", "Arrival From", "Condition Received","Processor Loaded", "Status" ]
        for i, label in enumerate(labels):
            tk.Label(top, text=label).grid(row=i, column=0)
            if label == "Processor Loaded":
                processor_options = ["First Data/Concord", "RBS/World Pay/5th3rd"]
                processor_combobox = ttk.Combobox(top, values=processor_options)
                processor_combobox.grid(row=i, column=1)
            elif label == "Status":
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
        
        # Automatically set date_entered
        form_values.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO pinpads (serial_number, arrival_from, condition_received, processor_loaded, status, date_entered)
            VALUES (?, ?, ?, ?, ?, ?)
            """, form_values)
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Duplicate Entry", "Serial number already exists. Please enter a unique serial number.")
        finally:
            conn.close()
            top.destroy()

    def ask_sending_status(self):
        status_window = tk.Toplevel()
        status_window.title("Sending Status")
        status_window.geometry("300x100")
    
        tk.Label(status_window, text="Is this being sent to a customer or sent out for RMA?").pack()
    
        status_var = tk.StringVar()
    
        def set_status_and_close(status):
            status_var.set(status)
            status_window.destroy()

        tk.Button(status_window, text="Sending to Customer", command=lambda: set_status_and_close("In the Field")).pack(side=tk.LEFT)
        tk.Button(status_window, text="Out for RMA", command=lambda: set_status_and_close("Out for RMA")).pack(side=tk.RIGHT)
    
        status_window.wait_window()
    
        return status_var.get()
    
    def edit_entry_form(self):
        if self.edit_form_open:
            return
        self.edit_form_open = True

        selected_serial_number = self.tree.item(self.tree.selection())["values"][0]
        sending_status = self.ask_sending_status()
    
        if not sending_status:
            self.edit_form_open = False
            return

        top = tk.Toplevel()
        top.title("Edit Pinpad Entry")
        
        selected_serial_number = self.tree.item(self.tree.selection())["values"][0]  # Get the selected serial number
        sending_status = self.ask_sending_status()  # New line to get the sending status
    
        if not sending_status:
            return  # Close the function if no status is selected
    
        top = tk.Toplevel()
        top.title("Edit Pinpad Entry")
        # Ask for sending status via a popup
        sending_status = tkinter.simpledialog.askstring("Sending Status", "Is this being sent to a customer or sent out for RMA?")

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

        submit_btn = tk.Button(top, text="Update", command=lambda: self.update_entry(top, record[0], sending_status))
        submit_btn.grid(row=len(labels), columnspan=2)

        top.protocol("WM_DELETE_WINDOW", self.on_closing_edit_form)  # Add this line

    def on_closing_edit_form(self):
        self.edit_form_open = False

    def update_entry(self, top, record_id, sending_status):
        form_values = [top.grid_slaves(row=i, column=1)[0].get() for i in range(4)]
        
        # Update date_changed
        form_values.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE pinpads SET
        serial_number = ?,
        arrival_from = ?,
        condition_received = ?,
        processor_loaded = ?,
        date_changed = ?,
        status = ?,  # Update the status here
        sent_to = ?
        WHERE id = ?
        """, form_values + [sending_status, sending_status, record_id])
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
