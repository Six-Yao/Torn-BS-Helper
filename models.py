import tkinter as tk
from tkinter import ttk

class CollapsiblePane(ttk.Frame):
    def __init__(self, parent, expanded_text, collapsed_text):
        ttk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.expanded_text = expanded_text
        self.collapsed_text = collapsed_text
        
        self.columnconfigure(0, weight=1)
        
        self.toggle_button = ttk.Button(self, text=self.collapsed_text, command=self.toggle, takefocus=0)
        self.toggle_button.grid(row=0, column=0, sticky="ew")
        
        self.content = ttk.Frame(self)
        self.content.grid(row=1, column=0, sticky="nsew")
        self.content.columnconfigure(0, weight=1)
        
        self.is_expanded = False
        self.content.grid_forget()
        
    def toggle(self):
        if self.is_expanded:
            self.content.grid_forget()
            self.toggle_button.configure(text=self.collapsed_text)
        else:
            self.content.grid(row=1, column=0, sticky="nsew")
            self.toggle_button.configure(text=self.expanded_text)
        
        self.is_expanded = not self.is_expanded