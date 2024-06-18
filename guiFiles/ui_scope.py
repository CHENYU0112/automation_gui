import tkinter as tk
from tkinter import ttk, StringVar
from guiFiles.configmgr import ConfigMgr
import guiFiles.guihelperfunc as make

class ScopeUI(ttk.Frame):
    # Scope variables
    scopeLabel = None
    varScopeBox = None
    scopeBox = None
    scope_list = [
        "DPO7104",
        "DPO7104C",
        "MSO58",
        "MSO58B",
        "MSO58LP",
        "MSO56",
        "MSO54",
        "MSO5204",
        "MSO5204B",
        "TDS5104B",
        "MSO4104",
        "MDO3104",
    ]
    varScopeM = None
    drop_menu_scope = None
    txt_GPIBscope = None
    varScopeAddr = None
    scopeAddrComm = None
    varVertScaleCh1 = None
    varVertScaleCh2 = None
    varVertScaleCh3 = None
    varVertScaleCh4 = None
    varVertScaleCh5 = None
    varVertScaleCh6 = None
    varVertScaleCh7 = None
    varVertScaleCh8 = None
    varTerminationCh1 = None
    varTerminationCh2 = None
    varTerminationCh3 = None
    varTerminationCh4 = None
    varTerminationCh5 = None
    varTerminationCh6 = None
    varTerminationCh7 = None
    varTerminationCh8 = None
    varVertPosCh1 = None
    varVertPosCh2 = None
    varVertPosCh3 = None
    varVertPosCh4 = None
    varVertPosCh5 = None
    varVertPosCh6 = None
    varVertPosCh7 = None
    varVertPosCh8 = None
    varAttnCh1 = None
    varAttnCh2 = None
    varAttnCh3 = None
    varAttnCh4 = None
    varAttnCh5 = None
    varAttnCh6 = None
    varAttnCh7 = None
    varAttnCh8 = None
    varHorScale = None
    varUpdateModel = None

    def __init__(self, parent):
        super(ScopeUI, self).__init__(parent)
        self.testing()
        self.t_r = 0
        ScopeUI.varScopeBox = StringVar()
        self.varScopeBox.set(ConfigMgr.instr['scopeOnOff'])
        self.scopeBox = ttk.Checkbutton(
            self,
            text='On/Off',
            variable=self.varScopeBox,
            command=lambda: self.display_scope(self.varScopeBox.get())
        )
        self.scopeBox.grid(row=self.t_r, column=0, padx=5, pady=5)
        self.scopeLabel = tk.Label(
            self, text='Oscilloscope',
            font=("Arial Bold", 10)
        )
        self.scopeLabel.grid(row=self.t_r, column=1)
        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=self.t_r, column=7, columnspan=199, padx=(0, 2), sticky='e')
        helpMsg = '''Help - Most tests will get the vertical position, vertical scale, termination and attenuation values from here.'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion
        self.t_r += 1
        ScopeUI.varScopeM = StringVar()
        self.drop_menu_scope = ttk.OptionMenu(
            self,
            self.varScopeM,
            self.scope_list[0],
            *self.scope_list,
            command=self.scope_model_option,
        )
        self.drop_menu_scope.configure(width=15)
        self.drop_menu_scope.grid(row=self.t_r, column=0)
        self.varScopeM.set(ConfigMgr.instr['scopeModel'])
        self.t_r += 1
        self.lbl1 = ttk.Label(self, text="Address")
        self.lbl1.grid(row=self.t_r, column=0)
        self.scopeAddrComm = self.register(self.scope_addr_command)
        ScopeUI.varScopeAddr = StringVar()
        self.varScopeAddr.set(ConfigMgr.instr['scopeAddr'])
        self.txt_GPIBscope = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(self.scopeAddrComm, '%P'),
            textvariable=self.varScopeAddr,
            width=15
        )
        self.txt_GPIBscope.grid(row=self.t_r, column=1)

        #region CH1
        ScopeUI.varVertScaleCh1 = StringVar()
        self.varVertScaleCh1.set(ConfigMgr.instr['scopeVertScaleCh1'])
        varVertScaleCommCh1 = self.register(self.validate_vert_scale_ch1)
        vertScale = ttk.Label(self, text='V. Scale:', font=('Arial Bold', 10), padding=5)
        vertScale.grid(row=3, column=0, padx=5, pady=2)
        vertScaleCh1 = ttk.Label(self, text='CH1', font=('Arial', 10), padding=5)
        vertScaleCh1.grid(row=4, column=0, padx=5, pady=2, sticky='w')
        vertScaleEntryCh1 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertScaleCommCh1, '%P'),
            textvariable=self.varVertScaleCh1,
            width=5
        )
        vertScaleEntryCh1.configure(width=4)
        vertScaleEntryCh1.grid(row=4, column=0, padx=5, pady=2, sticky='e')
        ScopeUI.varTerminationCh1 = StringVar()
        self.varTerminationCh1.set(ConfigMgr.instr['scopeTermCh1'])
        termination = ttk.Label(self, text='Termination:', font=('Arial Bold', 10), padding=5)
        termination.grid(row=3, column=1, padx=5, pady=2)
        terminationEntryCh150 = ttk.Radiobutton(
            self,
            text='50\u03A9',
            variable=self.varTerminationCh1,
            value='50.0e+0',
            command=lambda: self.validate_term_ch1(self.varTerminationCh1.get())
        )
        terminationEntryCh150.grid(row=4, column=1, padx=2, pady=2, sticky='w')
        terminationEntryCh11 = ttk.Radiobutton(
            self,
            text='1M\u03A9',
            variable=self.varTerminationCh1,
            value='1.0e+6',
            command=lambda: self.validate_term_ch1(self.varTerminationCh1.get())
        )
        terminationEntryCh11.configure(width=4)
        terminationEntryCh11.grid(row=4, column=1, padx=2, pady=2, sticky='e')
        ScopeUI.varVertPosCh1 = StringVar()
        self.varVertPosCh1.set(ConfigMgr.instr['scopeVertPosCh1'])
        varVertPosCommCh1 = self.register(self.validate_vert_pos_ch1)
        vertPos = ttk.Label(self, text='V. Pos:', font=('Arial Bold', 10), padding=5)
        vertPos.grid(row=3, column=2, padx=5, pady=2)
        vertPosEntryCh1 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertPosCommCh1, '%P'),
            textvariable=self.varVertPosCh1,
            width=5
        )
        vertPosEntryCh1.configure(width=4)
        vertPosEntryCh1.grid(row=4, column=2, padx=5, pady=2)
        ScopeUI.varAttnCh1 = StringVar()
        self.varAttnCh1.set(ConfigMgr.instr['scopeAttnCh1'])
        attnLbl = ttk.Label(self, text='Attn.:', font=('Arial Bold', 10), padding=5)
        attnLbl.grid(row=3, column=3, padx=2, pady=2)
        attnEntryCh1 = ttk.Entry(
            self,
            textvariable=self.varAttnCh1,
            validate='focusout',
            validatecommand=self.validate_attn,
            width=4,
        )
        attnEntryCh1.grid(row=4, column=3, padx=2, pady=2)
        #endregion

        #region CH2
        ScopeUI.varVertScaleCh2 = StringVar()
        self.varVertScaleCh2.set(ConfigMgr.instr['scopeVertScaleCh2'])
        varVertScaleCommCh2 = self.register(self.validate_vert_scale_ch2)
        vertScaleCh2 = ttk.Label(self, text='CH2', font=('Arial', 10), padding=5)
        vertScaleCh2.grid(row=5, column=0, padx=5, pady=2, sticky='w')
        vertScaleEntryCh2 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertScaleCommCh2, '%P'),
            textvariable=self.varVertScaleCh2,
            width=5
        )
        vertScaleEntryCh2.configure(width=4)
        vertScaleEntryCh2.grid(row=5, column=0, padx=5, pady=2, sticky='e')
        ScopeUI.varTerminationCh2 = StringVar()
        self.varTerminationCh2.set(ConfigMgr.instr['scopeTermCh2'])
        terminationEntryCh250 = ttk.Radiobutton(
            self,
            text='50\u03A9',
            variable=self.varTerminationCh2,
            value='50.0e+0',
            command=lambda: self.validate_term_ch2(self.varTerminationCh2.get())
        )
        terminationEntryCh250.grid(row=5, column=1, padx=2, pady=2, sticky='w')
        terminationEntryCh21 = ttk.Radiobutton(
            self,
            text='1M\u03A9',
            variable=self.varTerminationCh2,
            value='1.0e+6',
            command=lambda: self.validate_term_ch2(self.varTerminationCh2.get())
        )
        terminationEntryCh21.configure(width=4)
        terminationEntryCh21.grid(row=5, column=1, padx=2, pady=2, sticky='e')
        ScopeUI.varVertPosCh2 = StringVar()
        self.varVertPosCh2.set(ConfigMgr.instr['scopeVertPosCh2'])
        varVertPosCommCh2 = self.register(self.validate_vert_pos_ch2)
        vertPosEntryCh2 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertPosCommCh2, '%P'),
            textvariable=self.varVertPosCh2,
            width=5
        )
        vertPosEntryCh2.configure(width=4)
        vertPosEntryCh2.grid(row=5, column=2, padx=5, pady=2)
        ScopeUI.varAttnCh2 = StringVar()
        self.varAttnCh2.set(ConfigMgr.instr['scopeAttnCh2'])
        attnEntryCh2 = ttk.Entry(
            self,
            textvariable=self.varAttnCh2,
            validate='focusout',
            validatecommand=self.validate_attn,
            width=4,
        )
        attnEntryCh2.grid(row=5, column=3, padx=2, pady=2)
        #endregion

        #region CH3
        ScopeUI.varVertScaleCh3 = StringVar()
        self.varVertScaleCh3.set(ConfigMgr.instr['scopeVertScaleCh3'])
        varVertScaleCommCh3 = self.register(self.validate_vert_scale_ch3)
        vertScaleCh3 = ttk.Label(self, text='CH3', font=('Arial', 10), padding=5)
        vertScaleCh3.grid(row=6, column=0, padx=5, pady=2, sticky='w')
        vertScaleEntryCh3 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertScaleCommCh3, '%P'),
            textvariable=self.varVertScaleCh3,
            width=5
        )
        vertScaleEntryCh3.configure(width=4)
        vertScaleEntryCh3.grid(row=6, column=0, padx=5, pady=2, sticky='e')
        ScopeUI.varTerminationCh3 = StringVar()
        self.varTerminationCh3.set(ConfigMgr.instr['scopeTermCh3'])
        terminationEntryCh350 = ttk.Radiobutton(
            self,
            text='50\u03A9',
            variable=self.varTerminationCh3,
            value='50.0e+0',
            command=lambda: self.validate_term_ch3(self.varTerminationCh3.get())
        )
        terminationEntryCh350.grid(row=6, column=1, padx=2, pady=2, sticky='w')
        terminationEntryCh31 = ttk.Radiobutton(
            self,
            text='1M\u03A9',
            variable=self.varTerminationCh3,
            value='1.0e+6',
            command=lambda: self.validate_term_ch3(self.varTerminationCh3.get())
        )
        terminationEntryCh31.configure(width=4)
        terminationEntryCh31.grid(row=6, column=1, padx=2, pady=2, sticky='e')
        ScopeUI.varVertPosCh3 = StringVar()
        self.varVertPosCh3.set(ConfigMgr.instr['scopeVertPosCh3'])
        varVertPosCommCh3 = self.register(self.validate_vert_pos_ch3)
        vertPosEntryCh3 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertPosCommCh3, '%P'),
            textvariable=self.varVertPosCh3,
            width=5
        )
        vertPosEntryCh3.configure(width=4)
        vertPosEntryCh3.grid(row=6, column=2, padx=5, pady=2)
        ScopeUI.varAttnCh3 = StringVar()
        self.varAttnCh3.set(ConfigMgr.instr['scopeAttnCh3'])
        attnEntryCh3 = ttk.Entry(
            self,
            textvariable=self.varAttnCh3,
            validate='focusout',
            validatecommand=self.validate_attn,
            width=4,
        )
        attnEntryCh3.grid(row=6, column=3, padx=2, pady=2)
        #endregion

        #region CH4
        ScopeUI.varVertScaleCh4 = StringVar()
        self.varVertScaleCh4.set(ConfigMgr.instr['scopeVertScaleCh4'])
        varVertScaleCommCh4 = self.register(self.validate_vert_scale_ch4)
        vertScaleCh4 = ttk.Label(self, text='CH4', font=('Arial', 10), padding=5)
        vertScaleCh4.grid(row=7, column=0, columnspan=4, padx=5, pady=2, sticky='w')
        vertScaleEntryCh4 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertScaleCommCh4, '%P'),
            textvariable=self.varVertScaleCh4,
            width=5
        )
        vertScaleEntryCh4.configure(width=4)
        vertScaleEntryCh4.grid(row=7, column=0, padx=5, pady=2, sticky='e')
        ScopeUI.varTerminationCh4 = StringVar()
        self.varTerminationCh4.set(ConfigMgr.instr['scopeTermCh4'])
        terminationEntryCh450 = ttk.Radiobutton(
            self,
            text='50\u03A9',
            variable=self.varTerminationCh4,
            value='50.0e+0',
            command=lambda: self.validate_term_ch4(self.varTerminationCh4.get())
        )
        terminationEntryCh450.grid(row=7, column=1, padx=2, pady=2, sticky='w')
        terminationEntryCh41 = ttk.Radiobutton(
            self,
            text='1M\u03A9',
            variable=self.varTerminationCh4,
            value='1.0e+6',
            command=lambda: self.validate_term_ch4(self.varTerminationCh4.get())
        )
        terminationEntryCh41.configure(width=4)
        terminationEntryCh41.grid(row=7, column=1, padx=2, pady=2, sticky='e')
        ScopeUI.varVertPosCh4 = StringVar()
        self.varVertPosCh4.set(ConfigMgr.instr['scopeVertPosCh4'])
        varVertPosCommCh4 = self.register(self.validate_vert_pos_ch4)
        vertPosEntryCh4 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertPosCommCh4, '%P'),
            textvariable=self.varVertPosCh4,
            width=5
        )
        vertPosEntryCh4.configure(width=4)
        vertPosEntryCh4.grid(row=7, column=2, padx=5, pady=2)
        ScopeUI.varAttnCh4 = StringVar()
        self.varAttnCh4.set(ConfigMgr.instr['scopeAttnCh4'])
        attnEntryCh4 = ttk.Entry(
            self,
            textvariable=self.varAttnCh4,
            validate='focusout',
            validatecommand=self.validate_attn,
            width=4,
        )
        attnEntryCh4.grid(row=7, column=3, padx=2, pady=2)
        #endregion

        #region CH5
        ScopeUI.varVertScaleCh5 = StringVar()
        self.varVertScaleCh5.set(ConfigMgr.instr['scopeVertScaleCh5'])
        varVertScaleCommCh5 = self.register(self.validate_vert_scale_ch5)
        self.vertScaleCh5 = ttk.Label(self, text='CH5', font=('Arial', 10), padding=5)
        self.vertScaleCh5.grid(row=8, column=0, columnspan=4, padx=5, pady=2, sticky='w')
        self.vertScaleEntryCh5 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertScaleCommCh5, '%P'),
            textvariable=self.varVertScaleCh5,
            width=5
        )
        self.vertScaleEntryCh5.configure(width=4)
        self.vertScaleEntryCh5.grid(row=8, column=0, padx=5, pady=2, sticky='e')
        ScopeUI.varTerminationCh5 = StringVar()
        self.varTerminationCh5.set(ConfigMgr.instr['scopeTermCh5'])
        self.terminationEntryCh550 = ttk.Radiobutton(
            self,
            text='50\u03A9',
            variable=self.varTerminationCh5,
            value='50.0e+0',
            command=lambda: self.validate_term_ch5(self.varTerminationCh5.get())
        )
        self.terminationEntryCh550.grid(row=8, column=1, padx=2, pady=2, sticky='w')
        self.terminationEntryCh51 = ttk.Radiobutton(
            self,
            text='1M\u03A9',
            variable=self.varTerminationCh5,
            value='1.0e+6',
            command=lambda: self.validate_term_ch5(self.varTerminationCh5.get())
        )
        self.terminationEntryCh51.configure(width=4)
        self.terminationEntryCh51.grid(row=8, column=1, padx=2, pady=2, sticky='e')
        ScopeUI.varVertPosCh5 = StringVar()
        self.varVertPosCh5.set(ConfigMgr.instr['scopeVertPosCh5'])
        varVertPosCommCh5 = self.register(self.validate_vert_pos_ch5)
        self.vertPosEntryCh5 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertPosCommCh5, '%P'),
            textvariable=self.varVertPosCh5,
            width=5
        )
        self.vertPosEntryCh5.configure(width=4)
        self.vertPosEntryCh5.grid(row=8, column=2, padx=5, pady=2)
        ScopeUI.varAttnCh5 = StringVar()
        self.varAttnCh5.set(ConfigMgr.instr['scopeAttnCh2'])
        self.attnEntryCh5 = ttk.Entry(
            self,
            textvariable=self.varAttnCh5,
            validate='focusout',
            validatecommand=self.validate_attn,
            width=4,
        )
        self.attnEntryCh5.grid(row=8, column=3, padx=2, pady=2)
        #endregion

        # region CH6
        ScopeUI.varVertScaleCh6 = StringVar()
        self.varVertScaleCh6.set(ConfigMgr.instr['scopeVertScaleCh6'])
        varVertScaleCommCh6 = self.register(self.validate_vert_scale_ch6)
        self.vertScaleCh6 = ttk.Label(self, text='CH6', font=('Arial', 10), padding=5)
        self.vertScaleCh6.grid(row=9, column=0, columnspan=4, padx=5, pady=2, sticky='w')
        self.vertScaleEntryCh6 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertScaleCommCh6, '%P'),
            textvariable=self.varVertScaleCh6,
            width=5
        )
        self.vertScaleEntryCh6.configure(width=4)
        self.vertScaleEntryCh6.grid(row=9, column=0, padx=5, pady=2, sticky='e')
        ScopeUI.varTerminationCh6 = StringVar()
        self.varTerminationCh6.set(ConfigMgr.instr['scopeTermCh6'])
        self.terminationEntryCh650 = ttk.Radiobutton(
            self,
            text='50\u03A9',
            variable=self.varTerminationCh6,
            value='50.0e+0',
            command=lambda: self.validate_term_ch6(self.varTerminationCh6.get())
        )
        self.terminationEntryCh650.grid(row=9, column=1, padx=2, pady=2, sticky='w')
        self.terminationEntryCh61 = ttk.Radiobutton(
            self,
            text='1M\u03A9',
            variable=self.varTerminationCh6,
            value='1.0e+6',
            command=lambda: self.validate_term_ch6(self.varTerminationCh6.get())
        )
        self.terminationEntryCh61.configure(width=4)
        self.terminationEntryCh61.grid(row=9, column=1, padx=2, pady=2, sticky='e')
        ScopeUI.varVertPosCh6 = StringVar()
        self.varVertPosCh6.set(ConfigMgr.instr['scopeVertPosCh6'])
        varVertPosCommCh6 = self.register(self.validate_vert_pos_ch6)
        self.vertPosEntryCh6 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertPosCommCh6, '%P'),
            textvariable=self.varVertPosCh6,
            width=5
        )
        self.vertPosEntryCh6.configure(width=4)
        self.vertPosEntryCh6.grid(row=9, column=2, padx=5, pady=2)
        ScopeUI.varAttnCh6 = StringVar()
        self.varAttnCh6.set(ConfigMgr.instr['scopeAttnCh6'])
        self.attnEntryCh6 = ttk.Entry(
            self,
            textvariable=self.varAttnCh6,
            validate='focusout',
            validatecommand=self.validate_attn,
            width=4,
        )
        self.attnEntryCh6.grid(row=9, column=3, padx=2, pady=2)
        # endregion

        # region CH7
        ScopeUI.varVertScaleCh7 = StringVar()
        self.varVertScaleCh7.set(ConfigMgr.instr['scopeVertScaleCh7'])
        varVertScaleCommCh7 = self.register(self.validate_vert_scale_ch7)
        self.vertScaleCh7 = ttk.Label(self, text='CH7', font=('Arial', 10), padding=5)
        self.vertScaleCh7.grid(row=10, column=0, columnspan=4, padx=5, pady=2, sticky='w')
        self.vertScaleEntryCh7 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertScaleCommCh7, '%P'),
            textvariable=self.varVertScaleCh7,
            width=5
        )
        self.vertScaleEntryCh7.configure(width=4)
        self.vertScaleEntryCh7.grid(row=10, column=0, padx=5, pady=2, sticky='e')
        ScopeUI.varTerminationCh7 = StringVar()
        self.varTerminationCh7.set(ConfigMgr.instr['scopeTermCh7'])
        self.terminationEntryCh750 = ttk.Radiobutton(
            self,
            text='50\u03A9',
            variable=self.varTerminationCh7,
            value='50.0e+0',
            command=lambda: self.validate_term_ch7(self.varTerminationCh7.get())
        )
        self.terminationEntryCh750.grid(row=10, column=1, padx=2, pady=2, sticky='w')
        self.terminationEntryCh71 = ttk.Radiobutton(
            self,
            text='1M\u03A9',
            variable=self.varTerminationCh7,
            value='1.0e+6',
            command=lambda: self.validate_term_ch7(self.varTerminationCh7.get())
        )
        self.terminationEntryCh71.configure(width=4)
        self.terminationEntryCh71.grid(row=10, column=1, padx=2, pady=2, sticky='e')
        ScopeUI.varVertPosCh7 = StringVar()
        self.varVertPosCh7.set(ConfigMgr.instr['scopeVertPosCh7'])
        varVertPosCommCh7 = self.register(self.validate_vert_pos_ch7)
        self.vertPosEntryCh7 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertPosCommCh7, '%P'),
            textvariable=self.varVertPosCh7,
            width=5
        )
        self.vertPosEntryCh7.configure(width=4)
        self.vertPosEntryCh7.grid(row=10, column=2, padx=5, pady=2)
        ScopeUI.varAttnCh7 = StringVar()
        self.varAttnCh7.set(ConfigMgr.instr['scopeAttnCh7'])
        self.attnEntryCh7 = ttk.Entry(
            self,
            textvariable=self.varAttnCh7,
            validate='focusout',
            validatecommand=self.validate_attn,
            width=4,
        )
        self.attnEntryCh7.grid(row=10, column=3, padx=2, pady=2)
        # endregion

        # region CH8
        ScopeUI.varVertScaleCh8 = StringVar()
        self.varVertScaleCh8.set(ConfigMgr.instr['scopeVertScaleCh8'])
        varVertScaleCommCh8 = self.register(self.validate_vert_scale_ch8)
        self.vertScaleCh8 = ttk.Label(self, text='CH8', font=('Arial', 10), padding=5)
        self.vertScaleCh8.grid(row=11, column=0, columnspan=4, padx=5, pady=2, sticky='w')
        self.vertScaleEntryCh8 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertScaleCommCh8, '%P'),
            textvariable=self.varVertScaleCh8,
            width=5
        )
        self.vertScaleEntryCh8.configure(width=4)
        self.vertScaleEntryCh8.grid(row=11, column=0, padx=5, pady=2, sticky='e')
        ScopeUI.varTerminationCh8 = StringVar()
        self.varTerminationCh8.set(ConfigMgr.instr['scopeTermCh8'])
        self.terminationEntryCh850 = ttk.Radiobutton(
            self,
            text='50\u03A9',
            variable=self.varTerminationCh8,
            value='50.0e+0',
            command=lambda: self.validate_term_ch8(self.varTerminationCh8.get())
        )
        self.terminationEntryCh850.grid(row=11, column=1, padx=2, pady=2, sticky='w')
        self.terminationEntryCh81 = ttk.Radiobutton(
            self,
            text='1M\u03A9',
            variable=self.varTerminationCh8,
            value='1.0e+6',
            command=lambda: self.validate_term_ch8(self.varTerminationCh8.get())
        )
        self.terminationEntryCh81.configure(width=4)
        self.terminationEntryCh81.grid(row=11, column=1, padx=2, pady=2, sticky='e')
        ScopeUI.varVertPosCh8 = StringVar()
        self.varVertPosCh8.set(ConfigMgr.instr['scopeVertPosCh8'])
        varVertPosCommCh8 = self.register(self.validate_vert_pos_ch8)
        self.vertPosEntryCh8 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varVertPosCommCh8, '%P'),
            textvariable=self.varVertPosCh8,
            width=5
        )
        self.vertPosEntryCh8.configure(width=4)
        self.vertPosEntryCh8.grid(row=11, column=2, padx=5, pady=2)
        ScopeUI.varAttnCh8 = StringVar()
        self.varAttnCh8.set(ConfigMgr.instr['scopeAttnCh8'])
        self.attnEntryCh8 = ttk.Entry(
            self,
            textvariable=self.varAttnCh8,
            validate='focusout',
            validatecommand=self.validate_attn,
            width=4,
        )
        self.attnEntryCh8.grid(row=11, column=3, padx=2, pady=2)
        # endregion

        #region HORIZONTAL SCALE
        ScopeUI.varHorScale = StringVar()
        self.varHorScale.set(ConfigMgr.instr['scopeHorScale'])
        varHorScaleCommCh1 = self.register(self.validate_hor_scale)
        HorScale = ttk.Label(self, text='Hor. Scale:', font=('Arial Bold', 10), padding=5)
        HorScale.grid(row=1, column=2, padx=5, pady=2)
        HorScaleEntryCh1 = ttk.Entry(
            self,
            validate='focusout',
            validatecommand=(varHorScaleCommCh1, '%P'),
            textvariable=self.varHorScale,
            width=5
        )
        HorScaleEntryCh1.configure(width=7)
        HorScaleEntryCh1.grid(row=2, column=2, padx=5, pady=2)
        #endregion
        self._adjust_scope_view()

    #region VALIDATE FUNCTIONS
    def display_scope(self, option):
        ConfigMgr.instr['scopeOnOff'] = str(option)
        return True

    def scope_addr_command(self, content):
        ConfigMgr.instr['scopeAddr'] = str(content)
        return True

    def scope_model_option(self, content):
        ConfigMgr.instr['scopeModel'] = str(content)
        self._adjust_scope_view(content)
        return True

    def validate_vert_scale_ch1(self, content):
        ConfigMgr.instr['scopeVertScaleCh1'] = str(content)
        return True

    def validate_vert_scale_ch2(self, content):
        ConfigMgr.instr['scopeVertScaleCh2'] = str(content)
        return True

    def validate_vert_scale_ch3(self, content):
        ConfigMgr.instr['scopeVertScaleCh3'] = str(content)
        return True

    def validate_vert_scale_ch4(self, content):
        ConfigMgr.instr['scopeVertScaleCh4'] = str(content)
        return True

    def validate_vert_scale_ch5(self, content):
        ConfigMgr.instr['scopeVertScaleCh5'] = str(content)
        return True

    def validate_vert_scale_ch6(self, content):
        ConfigMgr.instr['scopeVertScaleCh6'] = str(content)
        return True

    def validate_vert_scale_ch7(self, content):
        ConfigMgr.instr['scopeVertScaleCh7'] = str(content)
        return True

    def validate_vert_scale_ch8(self, content):
        ConfigMgr.instr['scopeVertScaleCh8'] = str(content)
        return True

    def validate_term_ch1(self, content):
        ConfigMgr.instr['scopeTermCh1'] = str(content)
        return True

    def validate_term_ch2(self, content):
        ConfigMgr.instr['scopeTermCh2'] = str(content)
        return True

    def validate_term_ch3(self, content):
        ConfigMgr.instr['scopeTermCh3'] = str(content)
        return True

    def validate_term_ch4(self, content):
        ConfigMgr.instr['scopeTermCh4'] = str(content)
        return True

    def validate_term_ch5(self, content):
        ConfigMgr.instr['scopeTermCh5'] = str(content)
        return True

    def validate_term_ch6(self, content):
        ConfigMgr.instr['scopeTermCh6'] = str(content)
        return True

    def validate_term_ch7(self, content):
        ConfigMgr.instr['scopeTermCh7'] = str(content)
        return True

    def validate_term_ch8(self, content):
        ConfigMgr.instr['scopeTermCh8'] = str(content)
        return True

    def validate_vert_pos_ch1(self, content):
        ConfigMgr.instr['scopeVertPosCh1'] = str(content)
        return True

    def validate_vert_pos_ch2(self, content):
        ConfigMgr.instr['scopeVertPosCh2'] = str(content)
        return True

    def validate_vert_pos_ch3(self, content):
        ConfigMgr.instr['scopeVertPosCh3'] = str(content)
        return True

    def validate_vert_pos_ch4(self, content):
        ConfigMgr.instr['scopeVertPosCh4'] = str(content)
        return True

    def validate_vert_pos_ch5(self, content):
        ConfigMgr.instr['scopeVertPosCh5'] = str(content)
        return True

    def validate_vert_pos_ch6(self, content):
        ConfigMgr.instr['scopeVertPosCh6'] = str(content)
        return True

    def validate_vert_pos_ch7(self, content):
        ConfigMgr.instr['scopeVertPosCh7'] = str(content)
        return True

    def validate_vert_pos_ch8(self, content):
        ConfigMgr.instr['scopeVertPosCh8'] = str(content)
        return True

    def validate_hor_scale(self, content):
        ConfigMgr.instr['scopeHorScale'] = str(content)
        return True

    def validate_attn(self):
        ConfigMgr.instr['scopeAttnCh1'] = self.varAttnCh1.get()
        ConfigMgr.instr['scopeAttnCh2'] = self.varAttnCh2.get()
        ConfigMgr.instr['scopeAttnCh3'] = self.varAttnCh3.get()
        ConfigMgr.instr['scopeAttnCh4'] = self.varAttnCh4.get()
        ConfigMgr.instr['scopeAttnCh5'] = self.varAttnCh5.get()
        ConfigMgr.instr['scopeAttnCh6'] = self.varAttnCh6.get()
        ConfigMgr.instr['scopeAttnCh7'] = self.varAttnCh7.get()
        ConfigMgr.instr['scopeAttnCh8'] = self.varAttnCh8.get()
        return True
    #endregion

    #region Update Variables
    @classmethod
    def update_variables(cls):
        cls.varScopeBox.set(ConfigMgr.instr['scopeOnOff'])
        cls.varScopeM.set(ConfigMgr.instr['scopeModel'])
        cls.varScopeAddr.set(ConfigMgr.instr['scopeAddr'])
        cls.varVertScaleCh1.set(ConfigMgr.instr['scopeVertScaleCh1'])
        cls.varVertScaleCh2.set(ConfigMgr.instr['scopeVertScaleCh2'])
        cls.varVertScaleCh3.set(ConfigMgr.instr['scopeVertScaleCh3'])
        cls.varVertScaleCh4.set(ConfigMgr.instr['scopeVertScaleCh4'])
        cls.varVertScaleCh5.set(ConfigMgr.instr['scopeVertScaleCh5'])
        cls.varVertScaleCh6.set(ConfigMgr.instr['scopeVertScaleCh6'])
        cls.varVertScaleCh7.set(ConfigMgr.instr['scopeVertScaleCh7'])
        cls.varVertScaleCh8.set(ConfigMgr.instr['scopeVertScaleCh8'])
        cls.varTerminationCh1.set(ConfigMgr.instr['scopeTermCh1'])
        cls.varTerminationCh2.set(ConfigMgr.instr['scopeTermCh2'])
        cls.varTerminationCh3.set(ConfigMgr.instr['scopeTermCh3'])
        cls.varTerminationCh4.set(ConfigMgr.instr['scopeTermCh4'])
        cls.varTerminationCh5.set(ConfigMgr.instr['scopeTermCh5'])
        cls.varTerminationCh6.set(ConfigMgr.instr['scopeTermCh6'])
        cls.varTerminationCh7.set(ConfigMgr.instr['scopeTermCh7'])
        cls.varTerminationCh8.set(ConfigMgr.instr['scopeTermCh8'])
        cls.varVertPosCh1.set(ConfigMgr.instr['scopeVertPosCh1'])
        cls.varVertPosCh2.set(ConfigMgr.instr['scopeVertPosCh2'])
        cls.varVertPosCh3.set(ConfigMgr.instr['scopeVertPosCh3'])
        cls.varVertPosCh4.set(ConfigMgr.instr['scopeVertPosCh4'])
        cls.varVertPosCh5.set(ConfigMgr.instr['scopeVertPosCh5'])
        cls.varVertPosCh6.set(ConfigMgr.instr['scopeVertPosCh6'])
        cls.varVertPosCh7.set(ConfigMgr.instr['scopeVertPosCh7'])
        cls.varVertPosCh8.set(ConfigMgr.instr['scopeVertPosCh8'])
        cls.varAttnCh1.set(ConfigMgr.instr['scopeAttnCh1'])
        cls.varAttnCh2.set(ConfigMgr.instr['scopeAttnCh2'])
        cls.varAttnCh3.set(ConfigMgr.instr['scopeAttnCh3'])
        cls.varAttnCh4.set(ConfigMgr.instr['scopeAttnCh4'])
        cls.varAttnCh5.set(ConfigMgr.instr['scopeAttnCh5'])
        cls.varAttnCh6.set(ConfigMgr.instr['scopeAttnCh6'])
        cls.varAttnCh7.set(ConfigMgr.instr['scopeAttnCh7'])
        cls.varAttnCh8.set(ConfigMgr.instr['scopeAttnCh8'])
        cls.varHorScale.set(ConfigMgr.instr['scopeHorScale'])
        cls.varUpdateModel = 1
    #endregion

    #region HELPER FUNCTIONS
    def _adjust_scope_view(self, model=None):
        if model is None:
            model = ConfigMgr.instr['scopeModel']
        self._ch5_state('normal')
        self._ch6_state('normal')
        self._ch7_state('normal')
        self._ch8_state('normal')
        if model in ['MSO56']:
            self._ch7_state('disabled')
            self._ch8_state('disabled')
        if model in ['MSO4104', 'TDS5104B', 'DPO7104', 'DPO7104C', 'MSO54', 'MSO5204', 'MDO3104']:
            self._ch5_state('disabled')
            self._ch6_state('disabled')
            self._ch7_state('disabled')
            self._ch8_state('disabled')

    def testing(self):
        if self.varUpdateModel:
            self._adjust_scope_view()
            ScopeUI.varUpdateModel = None
        self.after(1000, self.testing)

    def _ch5_state(self, state):
        self.vertScaleCh5['state'] = state
        self.vertScaleEntryCh5['state'] = state
        self.terminationEntryCh550['state'] = state
        self.terminationEntryCh51['state'] = state
        self.vertPosEntryCh5['state'] = state
        self.attnEntryCh5['state'] = state

    def _ch6_state(self, state):
        self.vertScaleCh6['state'] = state
        self.vertScaleEntryCh6['state'] = state
        self.terminationEntryCh650['state'] = state
        self.terminationEntryCh61['state'] = state
        self.vertPosEntryCh6['state'] = state
        self.attnEntryCh6['state'] = state

    def _ch7_state(self, state):
        self.vertScaleCh7['state'] = state
        self.vertScaleEntryCh7['state'] = state
        self.terminationEntryCh750['state'] = state
        self.terminationEntryCh71['state'] = state
        self.vertPosEntryCh7['state'] = state
        self.attnEntryCh7['state'] = state

    def _ch8_state(self, state):
        self.vertScaleCh8['state'] = state
        self.vertScaleEntryCh8['state'] = state
        self.terminationEntryCh850['state'] = state
        self.terminationEntryCh81['state'] = state
        self.vertPosEntryCh8['state'] = state
        self.attnEntryCh8['state'] = state
    #endregion