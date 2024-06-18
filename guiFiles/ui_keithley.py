import tkinter as tk
from tkinter import StringVar, ttk
from guiFiles.configmgr import ConfigMgr
import guiFiles.guihelperfunc as make

class KeithleyUI(ttk.Frame):

    keith_list = [
        'Keithley 2700',
        'Keithley DAQ6510',
        'Keithley 3706A',
        'Agilent 34970A',
    ]
    varKeithBox = None
    varKeithM = None
    varKeithAddr = None

    def __init__(self, parent):
        super(KeithleyUI, self).__init__(parent)
        self.t_r = 0
        KeithleyUI.varKeithBox = StringVar()
        self.keithBox = ttk.Checkbutton(
            self,
            text='On/Off',
            variable=self.varKeithBox,
            command=lambda: self.display_keith(self.varKeithBox.get())
        )
        self.varKeithBox.set(ConfigMgr.instr['keithOnOff'])
        self.keithBox.grid(row=self.t_r, column=7, padx=5, pady=5)
        self.keithLabel = tk.Label(self, text='Keithley',\
                        font=("Arial Bold", 10))
        self.keithLabel.grid(row=self.t_r, column=8)
        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=self.t_r, column=9, columnspan=199, padx=(0, 2), sticky='e')
        helpMsg = '''Help - Keithley (data acquisition) Model and address. Some tests use keithley to capture voltage and temperature readings.
        Tracked channels are informed in the test box.'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion
        self.t_r += 1
        KeithleyUI.varKeithM = StringVar()
        self.drop_menu_Keith = ttk.OptionMenu(
            self,
            self.varKeithM,
            self.keith_list[0],
            *self.keith_list,
            command=self.keith_model_option,
        )
        self.varKeithM.set(ConfigMgr.instr['keithModel'])
        self.drop_menu_Keith.configure(width=20)
        self.drop_menu_Keith.grid(row=self.t_r, column=7)
        self.t_r += 1
        self.lbl3 = ttk.Label(self, text="Address")
        self.lbl3.grid(row=self.t_r, column=7)
        self.keithAddrComm = self.register(self.keith_addr_command)
        KeithleyUI.varKeithAddr = StringVar()
        self.txt_GPIBKeith = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(self.keithAddrComm, '%P'),
            textvariable=self.varKeithAddr,
            width=15
        )
        self.varKeithAddr.set(ConfigMgr.instr['keithAddr'])
        self.txt_GPIBKeith.grid(row=self.t_r, column=8)

    def keith_addr_command(self, content):
        ConfigMgr.instr['keithAddr'] = str(content)
        return True

    def display_keith(self, content):
        ConfigMgr.instr['keithOnOff'] = str(content)
        return True

    def keith_model_option(self, content):
        ConfigMgr.instr['keithModel'] = str(content)
        return True

    @classmethod
    def update_variables(cls):
        cls.varKeithBox.set(ConfigMgr.instr['keithOnOff'])
        cls.varKeithM.set(ConfigMgr.instr['keithModel'])
        cls.varKeithAddr.set(ConfigMgr.instr['keithAddr'])


if __name__ == '__main__':
    config = ConfigMgr()
    config.read('config.ini')
    root = tk.Tk()
    kei = KeithleyUI(root, config)
    kei.grid(row=0, column=0)
    root.mainloop()