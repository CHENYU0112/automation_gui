import tkinter as tk
from tkinter import ttk, StringVar
from guiFiles.configmgr import ConfigMgr
import guiFiles.guihelperfunc as make

class ThermUI(ttk.Frame):
    # Thermal Chamber variables
    therm_list = [
        'F4T',
    ]

    varThermBox = None
    varThermM = None
    varThermAddr = None

    def __init__(self, parent):
        super(ThermUI, self).__init__(parent)
        self.t_r = 0
        ThermUI.varThermBox = StringVar()
        self.thermBox = ttk.Checkbutton(
            self,
            text='On/Off',
            variable=self.varThermBox,
            command=lambda: self.display_therm(self.varThermBox.get())
        )
        self.varThermBox.set(ConfigMgr.instr['thermOnOff'])
        self.thermBox.grid(row=self.t_r, column=4, padx=5, pady=5)
        self.thermLabel = tk.Label(self, text='Thermal Chamber', \
                                   font=("Arial Bold", 10))
        self.thermLabel.grid(row=self.t_r, column=5)
        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=self.t_r, column=6, columnspan=199, padx=(0, 2), sticky='e')
        helpMsg = '''Help - Thermal Chamber Model and address. Used when controlling ambient temperature in tests.'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion
        self.t_r += 1
        ThermUI.varThermM = StringVar()
        self.drop_menu_Therm = ttk.OptionMenu(
            self,
            self.varThermM,
            self.therm_list[0],
            *self.therm_list,
            command=self.therm_model_option,
        )
        self.varThermM.set(ConfigMgr.instr['thermModel'])
        self.drop_menu_Therm.configure(width=15)
        self.drop_menu_Therm.grid(row=self.t_r, column=4)
        self.t_r += 1
        self.lbl2 = ttk.Label(self, text="Address")
        self.lbl2.grid(row=self.t_r, column=4)
        self.thermAddrComm = self.register(self.therm_addr_command)
        ThermUI.varThermAddr = StringVar()
        self.txt_GPIBTherm = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(self.thermAddrComm, '%P'),
            textvariable=self.varThermAddr,
            width=15
        )
        self.varThermAddr.set(ConfigMgr.instr['thermAddr'])
        self.txt_GPIBTherm.grid(row=self.t_r, column=5)

    def display_therm(self, option):
        ConfigMgr.instr['thermOnOff'] = str(option)
        return True

    def therm_addr_command(self, content):
        ConfigMgr.instr['thermAddr'] = str(content)
        return True

    def therm_model_option(self, content):
        ConfigMgr.instr['thermModel'] = str(content)
        return True

    @classmethod
    def update_variables(cls):
        cls.varThermBox.set(ConfigMgr.instr['thermOnOff'])
        cls.varThermM.set(ConfigMgr.instr['thermModel'])
        cls.varThermAddr.set(ConfigMgr.instr['thermAddr'])

