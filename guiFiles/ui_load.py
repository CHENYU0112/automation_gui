import tkinter as tk
from tkinter import ttk, StringVar
from guiFiles.configmgr import ConfigMgr
import guiFiles.guihelperfunc as make

class LoadUI(ttk.Frame):
    # Load variables
    loadLabel = None
    varLoadBox = None
    loadBox = None
    load_list = [
        'Chroma 6312/14',
        'Chroma 63600',
        'XBL Series',
        'AMETEK PLA800',
    ]
    load_ch_list = [
        'CH1',
        'CH2',
        'CH3',
        'CH4',
        'CH5',
        'CH6',
        'CH7',
        'CH8',
    ]
    varLoadM = None
    varLoadCh = None
    drop_menu_load = None
    drop_menu_load_ch = None
    txt_GPIBload = None
    varLoadAddr = None
    loadAddrComm = None

    def __init__(self, parent):
        super(LoadUI, self).__init__(parent)
        self.t_r = 0
        LoadUI.varLoadBox = StringVar()
        self.varLoadBox.set(ConfigMgr.instr['loadOnOff'])
        self.loadBox = ttk.Checkbutton(self, text='On/Off', \
                                       variable=self.varLoadBox, command=lambda: \
                self.display_load(self.varLoadBox.get()))
        self.loadBox.grid(row=self.t_r, column=4, padx=5, pady=5)
        self.loadLabel = tk.Label(self, text='LOAD', \
                                  font=("Arial Bold", 10))
        self.loadLabel.grid(row=self.t_r, column=5)
        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=self.t_r, column=6, columnspan=199, padx=(0, 2), sticky='e')
        helpMsg = '''Help - Electronic Load Model, channel and address. Essential to most tests to sweep load current.'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion
        self.t_r += 1
        LoadUI.varLoadM = StringVar()
        self.drop_menu_load = ttk.OptionMenu(
            self,
            self.varLoadM,
            self.load_list[0],
            *self.load_list,
            command=self.load_model_option,
        )
        self.varLoadM.set(ConfigMgr.instr['loadModel'])
        self.drop_menu_load.configure(width=15)
        self.drop_menu_load.grid(row=self.t_r, column=4)
        LoadUI.varLoadCh = StringVar()
        self.drop_menu_load_ch = ttk.OptionMenu(
            self,
            self.varLoadCh,
            self.load_ch_list[0],
            *self.load_ch_list,
            command=self.load_channel,
        )
        self.drop_menu_load_ch.configure(width=5)
        self.drop_menu_load_ch.grid(row=self.t_r, column=5)
        self.varLoadCh.set(ConfigMgr.instr['loadChannel'])
        self.t_r += 1
        self.lbl2 = ttk.Label(self, text="Address")
        self.lbl2.grid(row=self.t_r, column=4)
        self.loadAddrComm = self.register(self.load_addr_command)
        LoadUI.varLoadAddr = StringVar()
        self.varLoadAddr.set(ConfigMgr.instr['loadAddr'])
        self.txt_GPIBload = ttk.Entry(self, validate='focusout', \
                                      validatecommand=(self.loadAddrComm, '%P'), \
                                      textvariable=self.varLoadAddr, width=15)
        self.txt_GPIBload.grid(row=self.t_r, column=5)

    def display_load(self, option):
        ConfigMgr.instr['loadOnOff'] = str(option)
        return True

    def load_addr_command(self, content):
        ConfigMgr.instr['loadAddr'] = str(content)
        return True

    def load_model_option(self, content):
        ConfigMgr.instr['loadModel'] = str(content)
        if str(content) == 'XBL Series':
            self.drop_menu_load_ch.grid_remove()
        else:
            self.drop_menu_load_ch.grid()
        return True

    def load_channel(self, content):
        ConfigMgr.instr['loadChannel'] = self.varLoadCh.get()
        return True

    @classmethod
    def update_variables(cls):
        cls.varLoadBox.set(ConfigMgr.instr['loadOnOff'])
        cls.varLoadM.set(ConfigMgr.instr['loadModel'])
        cls.varLoadCh.set(ConfigMgr.instr['loadChannel'])
        cls.varLoadAddr.set(ConfigMgr.instr['loadAddr'])




