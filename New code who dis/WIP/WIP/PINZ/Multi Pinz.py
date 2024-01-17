import tkinter as tk
import tkinter.font as tkFont
import sqlite3 

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=1015
        height=385
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_69 = tk.Button(root)
        GButton_69["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_69["font"] = ft
        GButton_69["fg"] = "#000000"
        GButton_69["justify"] = "center"
        GButton_69["text"] = "New Entry"  # Changed text to "New Entry"
        GButton_69.place(x=20, y=350, width=70, height=25)
        GButton_69["command"] = self.new_entry_form  # Changed command to new_entry_form


        GButton_393 = tk.Button(root)
        GButton_393["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_393["font"] = ft
        GButton_393["fg"] = "#000000"
        GButton_393["justify"] = "center"
        GButton_393["text"] = "Edit Entry"  # Changed text to "Edit Entry"
        GButton_393.place(x=110, y=350, width=70, height=25)
        GButton_393["command"] = self.edit_entry_form  # Changed command to edit_entry_form


        GButton_573=tk.Button(root)
        GButton_573["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_573["font"] = ft
        GButton_573["fg"] = "#000000"
        GButton_573["justify"] = "center"
        GButton_573["text"] = "Button"
        GButton_573.place(x=200,y=350,width=70,height=25)
        GButton_573["command"] = self.GButton_573_command

        GButton_737=tk.Button(root)
        GButton_737["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_737["font"] = ft
        GButton_737["fg"] = "#000000"
        GButton_737["justify"] = "center"
        GButton_737["text"] = "Button"
        GButton_737.place(x=290,y=350,width=70,height=25)
        GButton_737["command"] = self.GButton_737_command

        GButton_358=tk.Button(root)
        GButton_358["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_358["font"] = ft
        GButton_358["fg"] = "#000000"
        GButton_358["justify"] = "center"
        GButton_358["text"] = "Button"
        GButton_358.place(x=380,y=350,width=70,height=25)
        GButton_358["command"] = self.GButton_358_command

        GButton_184=tk.Button(root)
        GButton_184["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_184["font"] = ft
        GButton_184["fg"] = "#000000"
        GButton_184["justify"] = "center"
        GButton_184["text"] = "Button"
        GButton_184.place(x=470,y=350,width=70,height=25)
        GButton_184["command"] = self.GButton_184_command

        GButton_177=tk.Button(root)
        GButton_177["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_177["font"] = ft
        GButton_177["fg"] = "#000000"
        GButton_177["justify"] = "center"
        GButton_177["text"] = "Button"
        GButton_177.place(x=560,y=350,width=70,height=25)
        GButton_177["command"] = self.GButton_177_command

        GButton_653=tk.Button(root)
        GButton_653["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_653["font"] = ft
        GButton_653["fg"] = "#000000"
        GButton_653["justify"] = "center"
        GButton_653["text"] = "Button"
        GButton_653.place(x=650,y=350,width=70,height=25)
        GButton_653["command"] = self.GButton_653_command

        GButton_926=tk.Button(root)
        GButton_926["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_926["font"] = ft
        GButton_926["fg"] = "#000000"
        GButton_926["justify"] = "center"
        GButton_926["text"] = "Button"
        GButton_926.place(x=740,y=350,width=70,height=25)
        GButton_926["command"] = self.GButton_926_command

        GButton_879=tk.Button(root)
        GButton_879["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_879["font"] = ft
        GButton_879["fg"] = "#000000"
        GButton_879["justify"] = "center"
        GButton_879["text"] = "Button"
        GButton_879.place(x=830,y=350,width=70,height=25)
        GButton_879["command"] = self.GButton_879_command

        GButton_666=tk.Button(root)
        GButton_666["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_666["font"] = ft
        GButton_666["fg"] = "#000000"
        GButton_666["justify"] = "center"
        GButton_666["text"] = "Button"
        GButton_666.place(x=920,y=350,width=70,height=25)
        GButton_666["command"] = self.GButton_666_command

        GLineEdit_114=tk.Entry(root)
        GLineEdit_114["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_114["font"] = ft
        GLineEdit_114["fg"] = "#333333"
        GLineEdit_114["justify"] = "center"
        GLineEdit_114["text"] = "Entry"
        GLineEdit_114.place(x=10,y=10,width=192,height=30)

        GRadio_619=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        GRadio_619["font"] = ft
        GRadio_619["fg"] = "#333333"
        GRadio_619["justify"] = "center"
        GRadio_619["text"] = "RadioButton"
        GRadio_619.place(x=10,y=70,width=85,height=25)
        GRadio_619["command"] = self.GRadio_619_command

        GRadio_326=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        GRadio_326["font"] = ft
        GRadio_326["fg"] = "#333333"
        GRadio_326["justify"] = "center"
        GRadio_326["text"] = "RadioButton"
        GRadio_326.place(x=10,y=100,width=85,height=25)
        GRadio_326["command"] = self.GRadio_326_command

        GRadio_710=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        GRadio_710["font"] = ft
        GRadio_710["fg"] = "#333333"
        GRadio_710["justify"] = "center"
        GRadio_710["text"] = "RadioButton"
        GRadio_710.place(x=10,y=130,width=85,height=25)
        GRadio_710["command"] = self.GRadio_710_command

        GRadio_928=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        GRadio_928["font"] = ft
        GRadio_928["fg"] = "#333333"
        GRadio_928["justify"] = "center"
        GRadio_928["text"] = "RadioButton"
        GRadio_928.place(x=10,y=160,width=85,height=25)
        GRadio_928["command"] = self.GRadio_928_command

        GListBox_805=tk.Listbox(root)
        GListBox_805["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_805["font"] = ft
        GListBox_805["fg"] = "#333333"
        GListBox_805["justify"] = "center"
        GListBox_805.place(x=210,y=40,width=261,height=281)

        GListBox_11=tk.Listbox(root)
        GListBox_11["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_11["font"] = ft
        GListBox_11["fg"] = "#333333"
        GListBox_11["justify"] = "center"
        GListBox_11.place(x=480,y=40,width=261,height=280)

        GListBox_102=tk.Listbox(root)
        GListBox_102["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_102["font"] = ft
        GListBox_102["fg"] = "#333333"
        GListBox_102["justify"] = "center"
        GListBox_102.place(x=750,y=40,width=251,height=281)

        GMessage_771=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_771["font"] = ft
        GMessage_771["fg"] = "#333333"
        GMessage_771["justify"] = "center"
        GMessage_771["text"] = "Message"
        GMessage_771.place(x=10,y=200,width=181,height=128)
        
        self.GListBox_805 = GListBox_805  # Save the listbox as an instance variable
        self.populate_list_boxes()  # Populate list boxes when the program starts

       

    def GButton_69_command(self):
        print("command")


    def GButton_393_command(self):
        print("command")


    def GButton_573_command(self):
        print("command")


    def GButton_737_command(self):
        print("command")


    def GButton_358_command(self):
        print("command")


    def GButton_184_command(self):
        print("command")


    def GButton_177_command(self):
        print("command")


    def GButton_653_command(self):
        print("command")


    def GButton_926_command(self):
        print("command")


    def GButton_879_command(self):
        print("command")


    def GButton_666_command(self):
        print("command")


    def GRadio_619_command(self):
        print("command")


    def GRadio_326_command(self):
        print("command")


    def GRadio_710_command(self):
        print("command")


    def GRadio_928_command(self):
        print("command")
        
    def populate_list_boxes(self):
        try:
            conn = sqlite3.connect("pinpads.db")
            cursor = conn.cursor()

        # Populate GListBox_805 with items 'In the Shop'
            cursor.execute("SELECT * FROM pinpads WHERE status = ?", ('In the Shop',))
            records = cursor.fetchall()
            for record in records:
                self.GListBox_805.insert(tk.END, record[1])  # Assuming 2nd column is the serial number

            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")

    
    def new_entry_form(self):
        # Create a new top-level window for the form
        top = tk.Toplevel()
        top.title("New Pinpad Entry")

        # Create labels and entry widgets for the form
        labels = ["Serial Number", "Arrival From", "Condition Received", "Processor Loaded"]
        for i, label in enumerate(labels):
            tk.Label(top, text=label).grid(row=i, column=0)
            tk.Entry(top).grid(row=i, column=1)

        # Submit button
        submit_btn = tk.Button(top, text="Submit", command=lambda: self.add_new_entry(top))
        submit_btn.grid(row=len(labels), columnspan=2)

    def add_new_entry(self, top):
        # Fetch the form values (assuming the form entries are in grid layout)
        form_values = [top.grid_slaves(row=i, column=1)[0].get() for i in range(4)]

        # Connect to the database
        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()

        # Insert a new record (for simplicity, assuming all form fields are filled)
        cursor.execute("""
        INSERT INTO pinpads (serial_number, arrival_from, condition_received, processor_loaded, date_entered)
        VALUES (?, ?, ?, ?, date('now'))
        """, form_values)

        # Commit and close
        conn.commit()
        conn.close()

        # Close the form window
        top.destroy()
        
    def edit_entry_form(self):
        # Fetch the selected item from the active list box (here we'll use GListBox_805 as an example)
        selected_serial_number = self.GListBox_805.get(tk.ACTIVE)
        
        # Create a new top-level window for the form
        top = tk.Toplevel()
        top.title("Edit Pinpad Entry")

        # Fetch an existing record from the database by its Serial Number
        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pinpads WHERE serial_number = ?", (selected_serial_number,))
        record = cursor.fetchone()
        conn.close()

        # Create labels and entry widgets for the form
        labels = ["Serial Number", "Arrival From", "Condition Received", "Processor Loaded"]
        for i, (label, value) in enumerate(zip(labels, record[1:5])):  # Adjust indices based on your table
            tk.Label(top, text=label).grid(row=i, column=0)
            entry = tk.Entry(top)
            if value is not None:  # Only insert if value is not None
                entry.insert(0, str(value))  # Convert value to string just to be safe
            entry.grid(row=i, column=1)

        # Submit button
        submit_btn = tk.Button(top, text="Update", command=lambda: self.update_entry(top, record[0]))
        submit_btn.grid(row=len(labels), columnspan=2)
        
    def update_entry(self, top, record_id):
    # Fetch the form values
        form_values = [top.grid_slaves(row=i, column=1)[0].get() for i in range(4)]

    # Connect to the database
        conn = sqlite3.connect("pinpads.db")
        cursor = conn.cursor()

    # Update the existing record
        cursor.execute("""
        UPDATE pinpads SET
            serial_number = ?,
            arrival_from = ?,
            condition_received = ?,
            processor_loaded = ?
        WHERE id = ?
        """, form_values + [record_id])

    # Commit and close
        conn.commit()
        conn.close()
    
    # Close the form window
        top.destroy()

        
def initialize_db():
    # Create a new SQLite database or connect to an existing one
    conn = sqlite3.connect("pinpads.db")
    cursor = conn.cursor()

    # Create table for pinpad records
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pinpads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        serial_number TEXT UNIQUE,
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

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
