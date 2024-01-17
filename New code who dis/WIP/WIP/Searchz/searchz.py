import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, Listbox, MULTIPLE
import threading
import queue

# Initialize the search_thread variable
search_thread = None
selected_files = []  # Store selected files

def search_text_in_file(file_path, search_terms):
    results = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, 1):
                for term in search_terms:
                    if term.lower() in line.lower():
                        start_line = max(1, line_number - 1)  # Capture the line above
                        end_line = min(len(lines), line_number + 1)  # Capture the line below

                        context_lines = [lines[i].strip() for i in range(start_line - 1, end_line)]

                        results.append({
                            "file": os.path.basename(file_path),
                            "line_number": line_number,
                            "search_term": term,
                            "context": context_lines
                        })

    except (OSError, IOError) as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    return results

def bold_search_term(result_text, search_term):
    text = result_text.get(1.0, tk.END)
    start = "1.0"
    while start:
        start = result_text.search(search_term, start, stopindex=tk.END, regexp=True)
        if start:
            end = f"{start}+{len(search_term)}c"
            result_text.tag_add("bold", start, end)
            start = end

def run_search(files_to_search, search_terms):
    all_results = []

    try:
        for file_path in files_to_search:
            search_results = search_text_in_file(file_path, search_terms)
            all_results.extend(search_results)

        if all_results:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Search results:\n")
            for result in all_results:
                result_text.insert(tk.END, f"In file '{result['file']}' at line {result['line_number']} ")
                result_text.insert(tk.END, f"for search term '{result['search_term']}':\n")
                for context_line in result['context']:
                    bold_search_term(result_text, result['search_term'])  # Bold the search term
                    result_text.insert(tk.END, context_line + "\n")
            result_text.config(state=tk.DISABLED)
        else:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "No results found or an error occurred.")
            result_text.config(state=tk.DISABLED)
    except queue.Empty:
        pass  # Queue was empty, meaning the search was stopped

    # Re-enable the search button when the search is finished
    search_button.config(state=tk.NORMAL)

def start_search(files_to_search, search_terms):
    global search_thread
    search_thread = threading.Thread(target=run_search, args=(files_to_search, search_terms))
    search_thread.start()

def choose_files():
    global selected_files
    selected_files = filedialog.askopenfilenames(
        filetypes=[("Text Files", "*.txt")],
        title="Choose Files to Search",
        multiple=True  # Allow multiple file selection
    )
    
    # Update the list of selected files in the listbox
    file_listbox.delete(0, tk.END)
    for file_path in selected_files:
        file_listbox.insert(tk.END, file_path)

def search_button_clicked():
    search_text = text_entry.get()
    search_terms = search_text.split(',')

    if not selected_files:
        messagebox.showwarning("Warning", "No files selected. Please choose files to search.")
        return

    # Disable the search button while the search is running
    search_button.config(state=tk.DISABLED)

    start_search(selected_files, search_terms)
    check_search_status()

def check_search_status():
    if search_thread and search_thread.is_alive():
        # Continue checking the search status after 500 milliseconds
        window.after(500, check_search_status)
    else:
        # Re-enable the search button when the search is finished
        search_button.config(state=tk.NORMAL)

def stop_search():
    global search_thread
    if search_thread and search_thread.is_alive():
        messagebox.showinfo("Info", "Stopping the current search...")
        search_thread.join()  # Wait for the current search to finish

def save_results_button_clicked():
    save_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if save_file_path:
        with open(save_file_path, 'w') as save_file:
            save_file.write(result_text.get(1.0, tk.END))


# Create the main window
window = tk.Tk()
window.title("Text File Search")
window.geometry("1280x720")
            
# Create and pack GUI elements
text_label = tk.Label(window, text="Search Text (comma-separated):")
text_label.pack()
text_entry = tk.Entry(window, width=40)
text_entry.pack()

choose_files_button = tk.Button(window, text="Choose Files", command=choose_files)
choose_files_button.pack()

# Create a listbox to display selected files
file_listbox = Listbox(window, selectmode=MULTIPLE, width=80, height=10)
file_listbox.pack()

search_button = tk.Button(window, text="Search", command=search_button_clicked)
search_button.pack()

stop_button = tk.Button(window, text="Stop", command=stop_search)
stop_button.pack()

save_results_button = tk.Button(window, text="Save Results", command=save_results_button_clicked)
save_results_button.pack()


result_text = scrolledtext.ScrolledText(window, width=80, height=20, state=tk.DISABLED)
result_text.pack()

# Configure the bold tag
result_text.tag_configure("bold", font=("Helvetica", 10, "bold"))

# Start the GUI main loop
window.mainloop()
