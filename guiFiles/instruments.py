from os import stat
import tkinter as tk
from tkinter import StringVar, ttk
from guiFiles.configmgr import ConfigMgr

#region UI Imports
from guiFiles.ui_keithley import KeithleyUI
from guiFiles.ui_vcc import VCCUI
from guiFiles.ui_flircam import FlirCamUI
from guiFiles.ui_scope import ScopeUI
from guiFiles.ui_load import LoadUI
from guiFiles.ui_therm import ThermUI
from guiFiles.ui_vin import VinUI
from guiFiles.ui_fgen import FgenUI
from guiFiles.ui_dongle import DongleUI
from guiFiles.ui_polboards import PolBoards
from guiFiles.ui_buttons import Buttons
from guiFiles.ui_biasps import BIASPSUI
from guiFiles.ui_enps import ENPSUI
from guiFiles.ui_customps import CustomPSUI
from guiFiles.ui_bode100 import Bode100
from guiFiles.ui_psboards import PsBoards
#endregion


class Instruments(ttk.Frame):

    def __init__(self, root, gui):
        super(Instruments, self).__init__(root)

        instrLblFrame = tk.LabelFrame(self, text='Instruments')
        instrLblFrame.grid(row=0, column=0, padx=10, pady=5)

        self.scanInstrLbl = tk.Text(self, font=('Sans Serif Bold', 12), width=100, height=1, state='disabled')
        self.scanInstrLbl.grid(row=1, column=0)

        #region OSCILLOSCOPE
        self.scopeFrame = ScopeUI(instrLblFrame)
        self.scopeFrame.grid(row=0, column=0, rowspan=8, columnspan=3, padx=5, pady=5, sticky='new')
        #endregion

        # VERTICAL LINE
        self.verticalLine = ttk.Separator(instrLblFrame, orient='vertical')
        self.verticalLine.grid(column=3, row=0, rowspan=8, sticky='ns', padx=5)
        
        #region LOAD
        self.loadFrame = LoadUI(instrLblFrame)
        self.loadFrame.grid(row=0, column=4, padx=5, pady=5, sticky='new')
        #endregion

        # HORIZONTAL LINE
        self.verticalLine = ttk.Separator(instrLblFrame, orient='horizontal')
        self.verticalLine.grid(row=1, column=4, sticky='we', pady=5)

        #region THERMAL CHAMBER
        self.thermFrame = ThermUI(instrLblFrame)
        self.thermFrame.grid(row=2, column=4, padx=5, pady=5, sticky='new')
        #endregion

        # HORIZONTAL LINE
        self.verticalLine = ttk.Separator(instrLblFrame, orient='horizontal')
        self.verticalLine.grid(row=3, column=4, sticky='we', pady=5)

        # region KEITHLEY
        self.keithleyFrame = KeithleyUI(instrLblFrame)
        self.keithleyFrame.grid(row=4, column=4, padx=5, pady=5, sticky='new')
        # endregion

        # VERTICAL LINE
        self.verticalLine = ttk.Separator(instrLblFrame, orient='vertical')
        self.verticalLine.grid(row=0, column=5, rowspan=8, sticky='ns', padx=5)

        # region VCC PS
        self.vccFrame = VCCUI(instrLblFrame)
        self.vccFrame.grid(row=0, column=6, padx=5, pady=5, sticky='new')
        # endregion

        # HORIZONTAL LINE
        self.verticalLine = ttk.Separator(instrLblFrame, orient='horizontal')
        self.verticalLine.grid(row=1, column=6, pady=5, sticky='we')
        
        #region VIN PS
        self.vinFrame = VinUI(instrLblFrame)
        self.vinFrame.grid(row=2, column=6, padx=5, pady=5, sticky='w')
        #endregion

        # HORIZONTAL LINE
        self.verticalLine = ttk.Separator(instrLblFrame, orient='horizontal')
        self.verticalLine.grid(row=3, column=6, sticky='we', pady=5)

        #region BIAS PS
        self.biasFrame = BIASPSUI(instrLblFrame)
        self.biasFrame.grid(row=4, column=6, padx=5, pady=5, sticky='w')
        #endregion

        # VERTICAL LINE
        self.verticalLine = ttk.Separator(instrLblFrame, orient='vertical')
        self.verticalLine.grid(column=7, row=0, rowspan=8, sticky='ns', padx=5)

        #region FLIR CAMERA
        self.camFrame = FlirCamUI(instrLblFrame)
        self.camFrame.grid(row=0, column=8, padx=5, pady=5, sticky='w')
        #endregion

        # HORIZONTAL LINE
        self.verticalLine = ttk.Separator(instrLblFrame, orient='horizontal')
        self.verticalLine.grid(row=1, column=8, sticky='we', pady=5)

        #region USB Dongle
        self.polBoardsFrame = PolBoards(instrLblFrame)
        self.polBoardsFrame.grid(row=2, column=8, rowspan=3, padx=5, pady=5)

        # HORIZONTAL LINE
        horLine = ttk.Separator(instrLblFrame, orient='horizontal')
        horLine.grid(row=5, column=8, columnspan=1, sticky='ew')

        self.dongleFrame = DongleUI(instrLblFrame)
        self.dongleFrame.grid(row=6, column=8, padx=5, pady=5)
        #endregion

        # HORIZONTAL LINE
        horLine = ttk.Separator(instrLblFrame, orient='horizontal')
        horLine.grid(row=9, column=0, columnspan=9, sticky='ew')

        #region BODE100
        self.bodeFrame = Bode100(instrLblFrame)
        self.bodeFrame.grid(row=10, column=0, rowspan=3, pady=5)
        #endregion

        # VERTICAL LINE
        vertLine = ttk.Separator(instrLblFrame, orient='vertical')
        vertLine.grid(row=10, column=1, rowspan=3, pady=2, padx=5, sticky='ns')

        # region FGEN
        self.fgenFrame = FgenUI(instrLblFrame)
        self.fgenFrame.grid(row=10, column=2, padx=5, pady=5, sticky='nw')
        # endregion

        # VERTICAL LINE
        vertLine = ttk.Separator(instrLblFrame, orient='vertical')
        vertLine.grid(row=10, column=3, rowspan=3, pady=2, padx=5, sticky='ns')

        # VERTICAL LINE
        vertLine = ttk.Separator(instrLblFrame, orient='vertical')
        vertLine.grid(row=10, column=5, rowspan=3, pady=2, padx=5, sticky='ns')

        # region EN PS
        self.enFrame = ENPSUI(instrLblFrame)
        self.enFrame.grid(row=10, column=6, padx=5, pady=5, sticky='nw')
        # endregion

        # HORIZONTAL LINE BUTTONS
        horLine = ttk.Separator(instrLblFrame, orient='horizontal')
        horLine.grid(row=11, column=6, sticky='ew')

        # region Custom PS
        self.customFrame = CustomPSUI(instrLblFrame)
        self.customFrame.grid(row=12, column=6, padx=5, pady=5, sticky='nw')
        # endregion

        # VERTICAL LINE
        vertLine = ttk.Separator(instrLblFrame, orient='vertical')
        vertLine.grid(row=10, column=7, rowspan=3, pady=2, padx=5, sticky='ns')

        # region PS Part
        self.psPart = PsBoards(instrLblFrame)
        self.psPart.grid(row=10, column=8, rowspan=3, pady=5, padx=5, sticky='n')
        # endregion

        # HORIZONTAL LINE BUTTONS
        horLine = ttk.Separator(instrLblFrame, orient='horizontal')
        horLine.grid(row=13, column=0, columnspan=9, sticky='ew')

        #region BUTTONS
        buttons = Buttons(instrLblFrame, self.scanInstrLbl)
        buttons.grid(row=14, column=0, columnspan=9, sticky='e')
        #endregion

        self.master.update_idletasks()
        self.master.configure(scrollregion=self.bbox('all'))


if __name__ == '__main__':
    root = tk.Tk()
    config = ConfigMgr()
    instruments = Instruments(root)
    instruments.grid(row=0, column=0, padx=10, pady=10)
    root.mainloop()