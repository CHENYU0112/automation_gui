import tkinter as tk
from tkinter import ttk, StringVar
from guiFiles.configmgr import ConfigMgr
import guiFiles.guihelperfunc as make

class FgenUI(ttk.Frame):
    # Fgen variables
    fgen_list = [
        'Agilent 33250A',
        'AFG 3022C',
    ]
    fgenChList = [
        'CH1',
        'CH2',
    ]
    varFgenBox = None
    varFgenM = None
    varFgCh = None
    varFgenAddr = None

    def __init__(self, parent):
        super(FgenUI, self).__init__(parent)
        self.t_r = 0
        FgenUI.varFgenBox = StringVar()
        self.fgenBox = ttk.Checkbutton(
            self,
            text='On/Off',
            variable=self.varFgenBox,
            command=lambda: self.display_fgen(self.varFgenBox.get())
        )
        self.varFgenBox.set(ConfigMgr.instr['fgenOnOff'])
        self.fgenBox.grid(row=self.t_r, column=7, padx=5, pady=5)
        self.fgenLabel = tk.Label(self, text='Func. Gen.', \
                                  font=("Arial Bold", 10))
        self.fgenLabel.grid(row=self.t_r, column=8)
        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=self.t_r, column=6, columnspan=199, padx=(5, 2), sticky='e')
        helpMsg = '''Help - Function Generator.'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion
        self.t_r += 1
        FgenUI.varFgenM = StringVar()
        self.drop_menu_fgen = ttk.OptionMenu(
            self,
            self.varFgenM,
            self.fgen_list[0],
            *self.fgen_list,
            command=self.fgen_model_option,
        )
        self.varFgenM.set(ConfigMgr.instr['fgenModel'])
        self.drop_menu_fgen.configure(width=20)
        self.drop_menu_fgen.grid(row=self.t_r, column=7)
        FgenUI.varFgCh = StringVar()
        self.fgCh = ttk.OptionMenu(
            self,
            self.varFgCh,
            self.fgenChList[0],
            *self.fgenChList,
            command=self.fgen_ch_option,
        )
        self.varFgCh.set(ConfigMgr.instr['fgenChannel'])
        self.fgCh.configure(width=4)
        self.fgCh.grid(row=self.t_r, column=8)
        self.fgCh.grid_remove()
        self.fgen_model_option(self.varFgenM.get())
        self.t_r += 1
        self.lbl3 = ttk.Label(self, text="Address")
        self.lbl3.grid(row=self.t_r, column=7)
        self.fgenAddrComm = self.register(self.fgen_addr_command)
        FgenUI.varFgenAddr = StringVar()
        self.txt_GPIBFgen = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(self.fgenAddrComm, '%P'),
            textvariable=self.varFgenAddr,
            width=15
        )
        self.varFgenAddr.set(ConfigMgr.instr['fgenAddr'])
        self.txt_GPIBFgen.grid(row=self.t_r, column=8)

    def display_fgen(self, option):
        ConfigMgr.instr['fgenOnOff'] = str(option)
        return True

    def fgen_addr_command(self, content):
        ConfigMgr.instr['fgenAddr'] = str(content)
        return True

    def fgen_model_option(self, content):
        ConfigMgr.instr['fgenModel'] = str(content)
        if(content == 'Agilent 33250A'):
            self.fgCh.grid_remove()
        elif(content == 'AFG 3022C'):
            self.fgCh.grid()
        return True

    def fgen_ch_option(self, content):
        ConfigMgr.instr['fgenChannel'] = str(content)
        return True

    @classmethod
    def update_variables(cls):
        cls.varFgCh.set(ConfigMgr.instr['fgenChannel'])
        cls.varFgenBox.set(ConfigMgr.instr['fgenOnOff'])
        cls.varFgenM.set(ConfigMgr.instr['fgenModel'])
        cls.varFgenAddr.set(ConfigMgr.instr['fgenAddr'])
