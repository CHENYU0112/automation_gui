import tkinter as tk
from tkinter import ttk, StringVar
from guiFiles.configmgr import ConfigMgr
from guiFiles.tk_tooltip import CreateToolTip
import guiFiles.guihelperfunc as make

class VinUI(ttk.Frame):
    # Vin variables
    vinLabel = None
    varVinBox = None
    vinBox = None
    vin_list = [
        "BK Precision 9205",
        "BK Precision 9117",
        "BK Precision 9115",
        "Gw Instek PSU Series",
        'HP 603X',
        "Keithley 2260B",
        "Xantrex XHR 33-33",
        "Keysight N6705C",
        "TDK-Lambda",
    ]
    varVinM = None
    drop_menu_vin = None
    txt_GPIBvin = None
    varVinAddr = None
    vinAddrComm = None
    vinVal1 = None

    def __init__(self, parent):
        super(VinUI, self).__init__(parent)
        self.t_r = 0
        VinUI.vinVal1 = StringVar()
        VinUI.varVinBox = StringVar()
        self.vinBox = ttk.Checkbutton(
            self, text='On/Off',
            variable=self.varVinBox,
            command=lambda: self.display_vin(self.varVinBox.get())
        )
        self.varVinBox.set(ConfigMgr.instr['vinPSOnOff'])
        self.vinVal1.set(ConfigMgr.instr['vinCh'])
        self.vinBox.grid(row=self.t_r, column=0, padx=5, pady=5)
        self.vinLabel = tk.Label(self, text='VIN PS', \
                                 font=("Arial Bold", 10))
        self.vinLabel.grid(row=self.t_r, column=1)
        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=self.t_r, column=6, columnspan=199, padx=(5, 2), sticky='e')
        helpMsg = '''Help - Power Supply Model, channel and address that will control the VIN/PVIN signal.'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion
        self.t_r += 1
        VinUI.varVinM = StringVar()
        self.drop_menu_vin = ttk.OptionMenu(
            self,
            self.varVinM,
            self.vin_list[0],
            *self.vin_list,
            command=self.vin_model_option,
        )
        self.varVinM.set(ConfigMgr.instr['vinPSModel'])
        self.drop_menu_vin.configure(width=20)
        self.drop_menu_vin.grid(row=self.t_r, column=0)
        self.vinModelFrame = ttk.Frame(self)
        self.t_r += 1
        self.lbl3 = ttk.Label(self, text="Address")
        self.lbl3.grid(row=self.t_r, column=0)
        self.vinAddrComm = self.register(self.vin_addr_command)
        VinUI.varVinAddr = StringVar()
        self.txt_GPIBvin = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(self.vinAddrComm, '%P'),
            textvariable=self.varVinAddr,
            width=15
        )
        self.varVinAddr.set(ConfigMgr.instr['vinPSAddr'])
        self.txt_GPIBvin.grid(row=self.t_r, column=1)
        self.vin_model_option(self.varVinM.get())

    def display_vin(self, option):
        ConfigMgr.instr['vinPSOnOff'] = str(option)
        return True

    def vin_addr_command(self, content):
        ConfigMgr.instr['vinPSAddr'] = str(content)
        return True

    def vin_model_option(self, content):
        ConfigMgr.instr['vinPSModel'] = str(content)
        if content in ['Keysight N6705C']:
            r = 0
            ch1Label = ttk.Label(self.vinModelFrame, text='Vin Ch:')
            ch1Label.grid(row=r, column=2, padx=5)
            ch1Value = ttk.Entry(
                self.vinModelFrame,
                textvariable=self.vinVal1,
                validate='focusout',
                validatecommand=self.validate_vin_ch,
                width=4
            )
            ch1Value.grid(row=r, column=3)
            CreateToolTip(ch1Value, 'VIN')

            self.vinModelFrame.grid(row=0, column=2, rowspan=2)
        else:
            self.vinModelFrame.grid_remove()
        return True

    def validate_vin_ch(self):
        ConfigMgr.instr['vinCh'] = self.vinVal1.get()
        return True

    @classmethod
    def update_variables(cls):
        cls.vinVal1.set(ConfigMgr.instr['vinCh'])
        cls.varVinBox.set(ConfigMgr.instr['vinPSOnOff'])
        cls.varVinM.set(ConfigMgr.instr['vinPSModel'])
        cls.varVinAddr.set(ConfigMgr.instr['vinPSAddr'])

