import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, Listbox, MULTIPLE
import threading

class TextFileSearch(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text File Search")
        self.geometry("1280x720")

        self.search_thread = None
        self.stop_event = threading.Event()  # Event to signal the thread to stop
        self.selected_files = []

        self._build_ui()

    def _build_ui(self):
        self.text_label = tk.Label(self, text="Search Text (comma-separated):")
        self.text_label.pack()
        self.text_entry = tk.Entry(self, width=40)
        self.text_entry.pack()
        self.choose_files_button = tk.Button(self, text="Choose Files", command=self.choose_files)
        self.choose_files_button.pack()
        self.file_listbox = Listbox(self, selectmode=MULTIPLE, width=80, height=10)
        self.file_listbox.pack()
        self.search_button = tk.Button(self, text="Search", command=self.search_button_clicked)
        self.search_button.pack()
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_search)
        self.stop_button.pack()
        self.save_results_button = tk.Button(self, text="Save Results", command=self.save_results_button_clicked)
        self.save_results_button.pack()
        self.result_text = scrolledtext.ScrolledText(self, width=80, height=20, state=tk.DISABLED)
        self.result_text.pack()
        self.result_text.tag_configure("bold", font=("Helvetica", 10, "bold"))

    def search_text_in_file(self, file_path, search_terms):
        results = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                for line_number, line in enumerate(lines, 1):
                    if self.stop_event.is_set():
                        break
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

    def bold_search_term(self, search_term):
        start = "1.0"
        while start:
            start = self.result_text.search(search_term, start, stopindex=tk.END, regexp=True, nocase=True)
            if start:
                end = f"{start}+{len(search_term)}c"
                self.result_text.tag_add("bold", start, end)
                start = end


    def run_search(self, files_to_search, search_terms):
        all_results = []
        try:
            for file_path in files_to_search:
                if self.stop_event.is_set():
                    break
                search_results = self.search_text_in_file(file_path, search_terms)
                all_results.extend(search_results)
                
                # After each file search, check if stop has been requested
                if self.stop_event.is_set():
                    break
                
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)

            if all_results:
                self.result_text.insert(tk.END, "Search results:\n")
                for result in all_results:
                    self.result_text.insert(tk.END, f"In file '{result['file']}' at line {result['line_number']} ")
                    self.result_text.insert(tk.END, f"for search term '{result['search_term']}':\n")
                    for context_line in result['context']:
                        self.result_text.insert(tk.END, context_line + "\n")
                    self.bold_search_term(result['search_term'])  # Bold the search term
            else:
                self.result_text.insert(tk.END, "No results found or an error occurred.")
                
            self.result_text.config(state=tk.DISABLED)
        except:
            pass  # Do nothing if the search was stopped, just exit the function
        finally:
            self.search_button.config(state=tk.NORMAL)

    def start_search(self):
        self.stop_event.clear()  # Reset the stop event for a new search
        self.search_thread = threading.Thread(target=self.run_search, args=(self.selected_files, self.text_entry.get().split(',')))
        self.search_thread.start()
        self.check_search_status()
    def start_search(self):
        self.search_thread = threading.Thread(target=self.run_search, args=(self.selected_files, self.text_entry.get().split(',')))
        self.search_thread.start()
        self.check_search_status()

    def choose_files(self):
        self.selected_files = filedialog.askopenfilenames(
            filetypes=[("Text Files", "*.txt")],
            title="Choose Files to Search",
            multiple=True
        )
        self.file_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            self.file_listbox.insert(tk.END, file_path)

    def search_button_clicked(self):
        if not self.selected_files:
            messagebox.showwarning("Warning", "No files selected. Please choose files to search.")
            return
        self.search_button.config(state=tk.DISABLED)
        self.start_search()

    def check_search_status(self):
        if self.search_thread.is_alive():
            # Continue checking the search status after 500 milliseconds
            self.after(500, self.check_search_status)
        else:
            # Clear the stop event and re-enable the search button when the search is finished
            self.stop_event.clear()
            self.search_button.config(state=tk.NORMAL)

    def stop_search(self):
        if self.search_thread and self.search_thread.is_alive():
            self.stop_event.set()  # Signal the thread to stop
            # No need to wait for the search_thread here, it will be checked periodically in check_search_status

    def save_results_button_clicked(self):
        save_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_file_path:
            with open(save_file_path, 'w') as save_file:
                save_file.write(self.result_text.get(1.0, tk.END))

if __name__ == "__main__":
    app = TextFileSearch()
    app.mainloop()
