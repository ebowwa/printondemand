# context_menus.py - Context Menu Actions

import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext  # Add this line to import scrolledtext

def show_entry_context_menu(menu, event, widget):
    # Implementation adjusted to use the widget if needed
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()


def show_text_context_menu(text_context_menu, event):
    try:
        text_context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        text_context_menu.grab_release()

def copy(master, results_display):
    try:
        master.clipboard_clear()
        text = results_display.get("sel.first", "sel.last")
        master.clipboard_append(text)
    except tk.TclError:
        pass  # Handle case where no text is selected

def paste(master):
    try:
        widget = master.focus_get()
        print(f"Debug: Focused widget type is {type(widget)}")  # Helps in debugging
        if isinstance(widget, (tk.Entry, ttk.Entry, tk.Text, scrolledtext.ScrolledText)):
            try:
                clipboard_content = master.clipboard_get()
                widget.insert(tk.INSERT, clipboard_content)
            except tk.TclError:
                print("Clipboard is empty or contains non-text data.")
        else:
            print("The focused widget does not support pasting.")
    except tk.TclError as e:
        print(f"General Error accessing clipboard: {e}")
  
  
