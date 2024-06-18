import tkinter as tk
from tkinter import ttk, StringVar
from guiFiles.configmgr import ConfigMgr
import guiFiles.guihelperfunc as make

class PsBoards(ttk.Frame):

    polFamilies = [
        'Custom',
    ]

    dipolModel = [
        'TDA3883',
        'TDA3885',
    ]

    aresModel = [
        'TDA38527',
        'TDA38540',
        'IR3888A',
        'IR3888B',
    ]

    atlanticModel = [
        'IR3447A',
        'IR3823A',
        'IR3846A',
        'IR3899A',
    ]

    aurovilleModel = [
        'TDA38806',
        'TDA38807',
    ]

    baileysModel = [
        'TDA38812',
        'TDA38813',
    ]

    coronadoModel = [
        'TDA38825',
        'TDA38826',
    ]

    eastonModel = [
        'TDA38540',
    ]

    horseneckModel = [
        'TDA38643',
    ]

    malibuModel = [
        'TDA38640',
        'TDA38641',
        'TDA38642',
        'TDA38725',
        'TDA38740',
        'TDA38741',
    ]

    miramarModel = [
        'TDA38301',
    ]

    newportModel = [
        'IR3887',
        'IR3888',
        'IR3889',
    ]

    redondoModel = [
        'TDA38820',
    ]

    customModel = [
        'customModel',
    ]

    modelDict = {
        'Custom': customModel,
    }

    varPolBoardFamily = None
    varPolBoardModel = None
    varSiliconRev = None
    modelList = list()

    def __init__(self, parent):
        super(PsBoards, self).__init__(parent)
        self.varPolBoardFamilyCustom = StringVar()
        self.varPolBoardModelCustom = StringVar()
        lbl = tk.Label(
            self,
            text='PS Part',
            font=("Arial Bold", 10)
        )
        lbl.grid(row=0, column=0)
        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=0, column=6, columnspan=199, padx=(5, 2), sticky='e')
        helpMsg = '''Help - PS Board (family, model).'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion
        lbl2 = tk.Label(
            self,
            text='Family',
            font=("Arial Bold", 8)
        )
        lbl2.grid(row=1, column=0, pady=2)
        PsBoards.varPolBoardFamily = StringVar()
        self.familyDropMenu = ttk.OptionMenu(
            self,
            self.varPolBoardFamily,
            self.polFamilies[0],
            *self.polFamilies,
            command=self.pol_board_family,
        )
        self.varPolBoardFamily.set(ConfigMgr.instr['psBoardFamily'])
        self.modelList = self.modelDict[self.varPolBoardFamily.get()]
        self.familyDropMenu.grid(row=2, column=0)
        self.modelLbl = tk.Label(
            self,
            text='Model',
            font=("Arial Bold", 8)
        )
        self.modelLbl.grid(row=3, column=0, pady=2)
        PsBoards.varPolBoardModel = StringVar()
        self.modelDropMenu = ttk.OptionMenu(
            self,
            self.varPolBoardModel,
            self.modelList[0],
            *self.modelList,
            command=self.pol_board_model,
        )
        self.varPolBoardModel.set(ConfigMgr.instr['psBoardModel'])
        self.modelDropMenu.grid(row=4, column=0)
        self.silRevLbl = tk.Label(
            self,
            text='Silicon Rev.',
            font=('Arial Bold', 8)
        )
        self.silRevLbl.grid(row=6, column=0)
        PsBoards.varSiliconRev = StringVar()
        entry = ttk.Entry(
            self,
            textvariable=self.varSiliconRev,
            validate='focusout',
            validatecommand=self.silicon_rev,
            width=6,
        )
        entry.grid(row=7, column=0)
        PsBoards.varSiliconRev.set(ConfigMgr.instr['psBoardSilicRev'])

        #region CUSTOM FAMILY / MODEL
        self.varPolBoardFamilyCustom.set('Family')
        self.entryFamily = tk.Entry(
            self,
            textvariable=self.varPolBoardFamilyCustom,
            validate='focusout',
            validatecommand=self.custom_pol_board_family,
            width=10,
        )
        self.entryFamily.grid(row=3, column=0, pady=2)
        self.varPolBoardModelCustom.set('Model')
        self.entryModel = tk.Entry(
            self,
            textvariable=self.varPolBoardModelCustom,
            validate='focusout',
            validatecommand=self.custom_pol_board_model,
            width=10,
        )
        self.entryFamily.grid(row=4, column=0, pady=2)
        self.entryFamily.grid_remove()
        self.entryModel.grid_remove()
        #endregion
        self.pol_board_family(content=None)

    def pol_board_family(self, content):
        if self.varPolBoardFamily.get() == 'Custom':
            self.modelDropMenu.grid_remove()
            self.modelLbl.grid_remove()
            self.varPolBoardFamilyCustom.set('Family')
            self.varPolBoardModelCustom.set('Model')
            self.entryFamily.grid(row=3, column=0, pady=3)
            self.entryModel.grid(row=4, column=0, pady=3)
            pass
        else:
            self.entryFamily.grid_remove()
            self.entryModel.grid_remove()
            ConfigMgr.instr['psBoardFamily'] = self.varPolBoardFamily.get()
            self.modelList = self.modelDict[self.varPolBoardFamily.get()]
            self.modelDropMenu.grid_remove()
            self.modelDropMenu = ttk.OptionMenu(
                self,
                self.varPolBoardModel,
                self.modelList[0],
                *self.modelList,
                command=self.pol_board_model,
            )
            self.varPolBoardModel.set(self.modelList[0])
            self.modelDropMenu.grid(row=4, column=0)
            self.modelLbl.grid()
        return True

    def pol_board_model(self, content):
        ConfigMgr.instr['psBoardModel'] = self.varPolBoardModel.get()
        return True

    def silicon_rev(self):
        ConfigMgr.instr['psBoardSilicRev'] = self.varSiliconRev.get()
        return True

    def custom_pol_board_family(self):
        ConfigMgr.instr['psBoardFamily'] = self.varPolBoardFamilyCustom.get()
        return True

    def custom_pol_board_model(self):
        ConfigMgr.instr['psBoardModel'] = self.varPolBoardModelCustom.get()
        return True

    @classmethod
    def update_variables(cls):
        # deactivated because custom is using same variable to avoid having to change the code on every test to adapt the folder name
        # The code is commented here in case we want to change that in the future.
        #
        # cls.varPolBoardFamily.set(ConfigMgr.instr['polBoardFamily'])
        # cls.varSiliconRev.set(ConfigMgr.instr['polBoardSilicRev'])
        # cls.varPolBoardModel.set(ConfigMgr.instr['polBoardModel'])
        pass

