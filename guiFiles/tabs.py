import tkinter as tk
from tkinter import ttk

class Tabs(ttk.Notebook):

    def __init__(self, master):
        super().__init__(master=master)
        self.pack(fill=tk.BOTH, expand=True)
        self.pressed_index = None
        self.bind("<<NotebookTabChanged>>", lambda e: self.tab_changed())

    def tab_changed(self):
        idx = self.index(self.select())
        canvas = self.winfo_children()[idx].winfo_children()[0]
        canvas.bind_all('<MouseWheel>', lambda e: self._on_mousewheel(e, canvas))

    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

if __name__ == '__main__':
    root = tk.Tk()
    tab = Tabs(root)
    root.mainloop()