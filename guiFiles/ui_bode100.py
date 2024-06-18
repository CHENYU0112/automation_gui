import tkinter as tk
from tkinter import ttk, StringVar
from guiFiles.configmgr import ConfigMgr
import guiFiles.guihelperfunc as make

class Bode100(tk.Frame):

    varBodeBox = None
    varFreq1 = None
    varFreq2 = None
    varFreq3 = None
    varFreq4 = None
    varFreq5 = None
    varDbm1 = None
    varDbm2 = None
    varDbm3 = None
    varDbm4 = None
    varDbm5 = None

    def __init__(self, parent):
        super(Bode100, self).__init__(parent)
        self.t_r = 0
        Bode100.varBodeBox = StringVar()
        self.bodeBox = ttk.Checkbutton(
            self,
            text='On/Off',
            variable=self.varBodeBox,
            command=self.display_bode,
        )
        self.varBodeBox.set(ConfigMgr.instr['bodeOnOff'])
        self.bodeBox.grid(row=self.t_r, column=0, padx=5, pady=5)
        self.bodeBox['state'] = 'disabled'
        self.bodeLabel = tk.Label(
            self,
            text='BODE 100',
            font=("Arial Bold", 10)
        )
        self.bodeLabel.grid(row=self.t_r, column=1)

        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=self.t_r, column=6, columnspan=199, padx=(5, 2), sticky='e')
        helpMsg = '''Help - Bode100. For now always turned on for the test that uses it. The list of frequency and dBm under development (not functional yet).'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion

        self.t_r += 1

        lblFreq = tk.Label(self, text='Frequency (Hz)')
        lblFreq.grid(row=self.t_r, column=0, pady=2, padx=5)
        lblDbm = tk.Label(self, text='dBm')
        lblDbm.grid(row=self.t_r, column=1, pady=2, padx=5)

        self.t_r += 1

        Bode100.varFreq1 = StringVar()
        self.freqEntry1 = tk.Entry(
            self,
            textvariable=self.varFreq1,
            validate='focusout',
            validatecommand=self.validate_freq1,
            width=6,
        )
        self.freqEntry1.grid(row=self.t_r, column=0, padx=5, pady=2)
        self.varFreq1.set(ConfigMgr.instr['bodeFreq1'])
        Bode100.varDbm1 = StringVar()
        self.dbmEntry1 = tk.Entry(
            self,
            textvariable=self.varDbm1,
            validate='focusout',
            validatecommand=self.validate_dbm1,
            width=4,
        )
        self.dbmEntry1.grid(row=self.t_r, column=1, padx=5, pady=2)
        self.varDbm1.set(ConfigMgr.instr['bodeDbm1'])

        self.t_r += 1

        Bode100.varFreq2 = StringVar()
        self.freqEntry2 = tk.Entry(
            self,
            textvariable=self.varFreq2,
            validate='focusout',
            validatecommand=self.validate_freq2,
            width=6,
        )
        self.freqEntry2.grid(row=self.t_r, column=0, padx=5, pady=2)
        self.varFreq2.set(ConfigMgr.instr['bodeFreq2'])
        Bode100.varDbm2 = StringVar()
        dbmEntry2 = tk.Entry(
            self,
            textvariable=self.varDbm2,
            validate='focusout',
            validatecommand=self.validate_dbm2,
            width=4,
        )
        dbmEntry2.grid(row=self.t_r, column=1, padx=5, pady=2)
        self.varDbm2.set(ConfigMgr.instr['bodeDbm2'])

        self.t_r += 1

        Bode100.varFreq3 = StringVar()
        freqEntry3 = tk.Entry(
            self,
            textvariable=self.varFreq3,
            validate='focusout',
            validatecommand=self.validate_freq3,
            width=6,
        )
        freqEntry3.grid(row=self.t_r, column=0, padx=5, pady=2)
        self.varFreq3.set(ConfigMgr.instr['bodeFreq3'])
        Bode100.varDbm3 = StringVar()
        dbmEntry3 = tk.Entry(
            self,
            textvariable=self.varDbm3,
            validate='focusout',
            validatecommand=self.validate_dbm3,
            width=4,
        )
        dbmEntry3.grid(row=self.t_r, column=1, padx=5, pady=2)
        self.varDbm3.set(ConfigMgr.instr['bodeDbm3'])

        self.t_r += 1

        Bode100.varFreq4 = StringVar()
        freqEntry4 = tk.Entry(
            self,
            textvariable=self.varFreq4,
            validate='focusout',
            validatecommand=self.validate_freq4,
            width=6,
        )
        freqEntry4.grid(row=self.t_r, column=0, padx=5, pady=2)
        self.varFreq4.set(ConfigMgr.instr['bodeFreq4'])
        Bode100.varDbm4 = StringVar()
        dbmEntry4 = tk.Entry(
            self,
            textvariable=self.varDbm4,
            validate='focusout',
            validatecommand=self.validate_dbm4,
            width=4,
        )
        dbmEntry4.grid(row=self.t_r, column=1, padx=5, pady=2)
        self.varDbm4.set(ConfigMgr.instr['bodeDbm4'])

        self.t_r += 1

        Bode100.varFreq5 = StringVar()
        freqEntry5 = tk.Entry(
            self,
            textvariable=self.varFreq5,
            validate='focusout',
            validatecommand=self.validate_freq5,
            width=6,
        )
        freqEntry5.grid(row=self.t_r, column=0, padx=5, pady=2)
        self.varFreq5.set(ConfigMgr.instr['bodeFreq5'])
        Bode100.varDbm5 = StringVar()
        dbmEntry5 = tk.Entry(
            self,
            textvariable=self.varDbm5,
            validate='focusout',
            validatecommand=self.validate_dbm5,
            width=4,
        )
        dbmEntry5.grid(row=self.t_r, column=1, padx=5, pady=2)
        self.varDbm5.set(ConfigMgr.instr['bodeDbm5'])

    def display_bode(self):
        ConfigMgr.instr['bodeOnOff'] = self.varBodeBox.get()
        return True

    def validate_freq1(self):
        ConfigMgr.instr['bodeFreq1'] = self.varFreq1.get()
        return True

    def validate_dbm1(self):
        ConfigMgr.instr['bodeDbm1'] = self.varDbm1.get()
        return True

    def validate_freq2(self):
        ConfigMgr.instr['bodeFreq2'] = self.varFreq2.get()
        return True

    def validate_dbm2(self):
        ConfigMgr.instr['bodeDbm2'] = self.varDbm2.get()
        return True

    def validate_freq3(self):
        ConfigMgr.instr['bodeFreq3'] = self.varFreq3.get()
        return True

    def validate_dbm3(self):
        ConfigMgr.instr['bodeDbm3'] = self.varDbm3.get()
        return True

    def validate_freq4(self):
        ConfigMgr.instr['bodeFreq4'] = self.varFreq4.get()
        return True

    def validate_dbm4(self):
        ConfigMgr.instr['bodeDbm4'] = self.varDbm4.get()
        return True

    def validate_freq5(self):
        ConfigMgr.instr['bodeFreq5'] = self.varFreq5.get()
        return True

    def validate_dbm5(self):
        ConfigMgr.instr['bodeDbm5'] = self.varDbm5.get()
        return True

    @classmethod
    def update_variables(cls):
        cls.varBodeBox.set('bodeOnOff')
        cls.varDbm1.set(ConfigMgr.instr['bodeDbm1'])
        cls.varDbm2.set(ConfigMgr.instr['bodeDbm2'])
        cls.varDbm3.set(ConfigMgr.instr['bodeDbm3'])
        cls.varDbm4.set(ConfigMgr.instr['bodeDbm4'])
        cls.varDbm5.set(ConfigMgr.instr['bodeDbm5'])
        cls.varFreq1.set(ConfigMgr.instr['bodeFreq1'])
        cls.varFreq2.set(ConfigMgr.instr['bodeFreq2'])
        cls.varFreq3.set(ConfigMgr.instr['bodeFreq3'])
        cls.varFreq4.set(ConfigMgr.instr['bodeFreq4'])
        cls.varFreq5.set(ConfigMgr.instr['bodeFreq5'])
