import tkinter as tk
from tkinter import StringVar, ttk
from tkinter.constants import HIDDEN
from guiFiles.configmgr import ConfigMgr
from guiFiles.tk_tooltip import CreateToolTip
import guiFiles.guihelperfunc as make


class CustomPSUI(ttk.Frame):

    # VCC/VDRV variables
    vccLabel = None
    varVccBox = None
    vccBox = None
    vccps_list = [
        'Agilent E3631A',
        'Agilent E3642A',
        'BK Precision 9130B',
        'Keysight N6705C',
        'GW PST 3202',
        'PWS4000 Series',
    ]
    varVccpsM = None
    drop_menu_vcc = None
    txt_GPIBvcc = None
    varVccPSAddr = None
    vccVal1 = None
    vccVal2 = None
    vccModelFrame = None

    def __init__(self, parent):
        super(CustomPSUI, self).__init__(parent)
        CustomPSUI.vccVal1 = StringVar()
        self.vccVal1.set(ConfigMgr.instr['customPSCh'])
        # ROW 0
        self.t_r = 0
        # on off checkbutton
        CustomPSUI.varVccBox = StringVar()
        self.vccpsBox = ttk.Checkbutton(
            self,
            text='On/Off',
            variable=self.varVccBox,
            command=lambda: self.display_vccps(self.varVccBox.get())
        )
        self.varVccBox.set(ConfigMgr.instr['customPSOnOff'])
        self.vccpsBox.grid(row=self.t_r, column=0, padx=5, pady=5)
        # vcc/vdrv label
        self.vccpsLabel = tk.Label(
            self,
            text='Custom PS',
            font=("Arial Bold", 10)
        )
        self.vccpsLabel.grid(row=self.t_r, column=1)
        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=self.t_r, column=6, columnspan=199, padx=(5, 2), sticky='e')
        helpMsg = '''Help - Power Supply Model, channel and address that will control a Custom signal.'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion
        # ROW 1
        self.t_r += 1
        # drop down menu
        CustomPSUI.varVccpsM = StringVar()
        self.drop_menu_vccps = ttk.OptionMenu(
            self, self.varVccpsM,
            self.vccps_list[0],
            *self.vccps_list,
            command=self.vcc_model,
        )
        self.varVccpsM.set(ConfigMgr.instr['customPSModel'])
        self.drop_menu_vccps.configure(width=20)
        self.drop_menu_vccps.grid(row=self.t_r, column=0)
        self.vccModelFrame = ttk.Frame(self)
        self.vcc_model(self.varVccpsM.get())
        # ROW 2
        self.t_r += 1
        self.lbl3 = ttk.Label(self, text="Address")
        self.lbl3.grid(row=self.t_r, column=0)
        CustomPSUI.varVccpsAddr = StringVar()
        self.txt_GPIBVccps = ttk.Entry(
            self,
            validate='focusout',
            textvariable=self.varVccpsAddr,
            validatecommand=self.vccps_addr_command,
            width=15
        )
        self.varVccpsAddr.set(ConfigMgr.instr['customPSAddr'])
        self.txt_GPIBVccps.grid(row=self.t_r, column=1)

    def vccps_addr_command(self):
        ConfigMgr.instr['customPSAddr'] = self.varVccpsAddr.get()
        return True

    def display_vccps(self, content):
        ConfigMgr.instr['customPSOnOff'] = self.varVccBox.get()
        return True

    def vcc_model(self, arg1):
        ConfigMgr.instr['customPSModel'] = self.varVccpsM.get()
        if arg1 in ['BK Precision 9130B', 'Agilent E3631A', 'Keysight N6705C', 'GW PST 3202']:
            r = 0
            ch1Label = ttk.Label(self.vccModelFrame, text='Ch:')
            ch1Label.grid(row=r, column=2, padx=5)
            ch1Value = ttk.Entry(
                self.vccModelFrame,
                textvariable=self.vccVal1,
                validate='focusout',
                validatecommand=self.validate_vcc_chs,
                width=4
            )
            ch1Value.grid(row=r, column=3)
            CreateToolTip(ch1Value, 'Custom')

            self.vccModelFrame.grid(row=0, column=2, rowspan=2)
        elif arg1 in ['Agilent E3642A']:
            self.vccModelFrame.grid_remove()
        else:
            self.vccModelFrame.grid_remove()
        return True

    def validate_vcc_chs(self):
        ConfigMgr.instr['customPSCh'] = self.vccVal1.get()
        return True

    @classmethod
    def update_variables(cls):
        cls.vccVal1.set(ConfigMgr.instr['customPSCh'])
        cls.varVccBox.set(ConfigMgr.instr['customPSOnOff'])
        cls.varVccpsM.set(ConfigMgr.instr['customPSModel'])
        cls.varVccpsAddr.set(ConfigMgr.instr['customPSAddr'])


if __name__ == '__main__':
    root = tk.Tk()
    vcc = CustomPSUI(root)
    vcc.grid(row=0, column=0)
    root.mainloop()