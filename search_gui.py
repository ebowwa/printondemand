# search_gui.py - GUI Layout and Widgets

import tkinter as tk
from tkinter import ttk, scrolledtext, Menu
from search_gui.search_interface import SearchInterface  # Update this import according to your project structure
# Ensure correct module name is used. Assuming the correct file name is context_menu.py
from search_gui.context_menu import show_entry_context_menu, show_text_context_menu, copy, paste  # Update import path as needed

class SearchGUI:
    def __init__(self, master):
        self.master = master
        master.title("Search Viewer")

        self.search_interface = SearchInterface("data_2024-02-20_06-52-02/uuid_data.csv", "data_2024-02-20_06-52-02/prompt_data.csv", "response")

        self.entry_context_menu = Menu(master, tearoff=0)
        self.entry_context_menu.add_command(label="Paste", command=lambda: paste(self.master))

        self.text_context_menu = Menu(master, tearoff=0)
        self.text_context_menu.add_command(label="Copy", command=lambda: copy(self.master, self.results_display))

        self.uuid_label = ttk.Label(master, text="UUID:")
        self.uuid_label.grid(row=0, column=0, sticky=tk.W)
        self.uuid_entry = ttk.Entry(master)
        self.uuid_entry.grid(row=0, column=1, sticky=(tk.W + tk.E))
        self.uuid_entry.bind("<Button-3>", lambda event: show_entry_context_menu(self.entry_context_menu, event, self.uuid_entry))

        self.search_button = ttk.Button(master, text="Search", command=self.perform_search)
        self.search_button.grid(row=1, column=0, columnspan=2)

        self.results_display = scrolledtext.ScrolledText(master, height=10, wrap=tk.WORD)
        self.results_display.grid(row=2, column=0, columnspan=2, sticky=(tk.W + tk.E))
        self.results_display.bind("<Button-3>", lambda event: show_text_context_menu(self.text_context_menu, event, self.results_display))

    def perform_search(self):
        self.results_display.delete('1.0', tk.END)

        uuid = self.uuid_entry.get()
        if uuid:
            search_results = self.search_interface.search_by_uuid(uuid)

            self.results_display.insert(tk.INSERT, "Search Results for UUID '{}':\n".format(uuid))
            self.results_display.insert(tk.INSERT, "UUID Records:\n{}\n\n".format(search_results['uuid_records']))
            self.results_display.insert(tk.INSERT, "Prompts:\n{}\n\n".format(search_results['prompts']))
            self.results_display.insert(tk.INSERT, "Responses:\n{}\n\n".format(search_results['responses']))
            self.results_display.insert(tk.INSERT, "PNG Files:\n{}\n".format(search_results['png_files']))
        else:
            self.results_display.insert(tk.INSERT, "Please enter a UUID to search.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SearchGUI(root)
    root.mainloop()
