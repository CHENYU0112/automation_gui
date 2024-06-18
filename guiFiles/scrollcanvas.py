import tkinter as tk
from tkinter import ttk

class ScrollCanvas(tk.Canvas):

    counter = 0

    def __init__(self, master):
        super().__init__(master=master)
        ScrollCanvas.counter += 1
        self.scroll = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        self.configure(yscrollcommand=self.scroll.set)
        self.bind('<Configure>', lambda e: self.configure(scrollregion=self.bbox('all')))
        # self.bind('<MouseWheel>', self._on_mousewheel)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _on_mousewheel(self, event):
        self.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == '__main__':
    root = tk.Tk()
    canvas = ScrollCanvas(root)
    canvas.pack(fill=tk.BOTH)
    root.mainloop()