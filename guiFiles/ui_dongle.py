import tkinter as tk
from tkinter import ttk, StringVar
from guiFiles.configmgr import ConfigMgr
import guiFiles.guihelperfunc as make

class DongleUI(ttk.Frame):

    dongleList = [
        'Acadia',
        'McKinley',
        'Pollino',
        'Sequoia',
        'Sierra',
    ]

    def __init__(self, parent):
        super(DongleUI, self).__init__(parent)
        self.varDongleBox = StringVar()
        self.varDongleBox.set(ConfigMgr.instr['dongleOnOff'])
        self.dongleBox = ttk.Checkbutton(
            self,
            text='On/Off',
            variable=self.varDongleBox,
            command=lambda: self.display_dongle(self.varDongleBox.get())
        )
        self.dongleBox.grid(row=0, column=0)
        lbl = tk.Label(
            self,
            text='USB Dongle',
            font=("Arial Bold", 10)
        )
        lbl.grid(row=1, column=0)
        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=0, column=6, columnspan=199, padx=(5, 2), sticky='e')
        helpMsg = '''Help - Controller used on Power Stages. Used to set phase, frequency, vout, etc.'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion
        self.varDongleModel = StringVar()
        self.dropMenu = ttk.OptionMenu(
            self,
            self.varDongleModel,
            self.dongleList[0],
            *self.dongleList,
            command=self.dongle_model,
        )
        self.varDongleModel.set(ConfigMgr.instr['dongleModel'])
        self.dropMenu.grid(row=2, column=0)

    def display_dongle(self, content):
        ConfigMgr.instr['dongleOnOff'] = str(content)
        return True

    def dongle_model(self, content):
        ConfigMgr.instr['dongleModel'] = str(content)
        return True