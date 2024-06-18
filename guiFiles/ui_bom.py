import tkinter as tk
from tkinter import ttk, StringVar
from guiFiles.configmgr import ConfigMgr

class Bom(tk.Text):

    def __init__(self, parent):
        super(Bom, self).__init__(parent)
        self.config(width=37, height=13)
        self.bind('<KeyRelease>', self.get_text)

    def get_text(self, e):
        ConfigMgr.instr['bom'] = self.get('1.0', 'end')
