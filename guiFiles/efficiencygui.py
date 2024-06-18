import tkinter as tk
from tkinter import ttk, StringVar

class EFFICIENCYGUI(tk.Tk):

    version = 'Version 1.5.2'

    def __init__(self):
        super().__init__()
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry(str(self.width-10) + 'x' + str(self.height-80) + '+0' + '+0')
        self.iconbitmap('guiFiles/infineon.ico')
        self.title(f'Efficiency GUI - {self.version}')

if __name__ == '__main__':
    root = EFFICIENCYGUI()