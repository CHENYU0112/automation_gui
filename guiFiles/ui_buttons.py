import tkinter as tk
from tkinter import ttk, StringVar, filedialog
from guiFiles.configmgr import ConfigMgr
from guiFiles.ui_scope import ScopeUI
from guiFiles.ui_load import LoadUI
from guiFiles.ui_vcc import VCCUI
from guiFiles.ui_vin import VinUI
from guiFiles.ui_biasps import BIASPSUI
from guiFiles.ui_enps import ENPSUI
from guiFiles.ui_customps import CustomPSUI
from guiFiles.ui_therm import ThermUI
from guiFiles.ui_keithley import KeithleyUI
from guiFiles.ui_fgen import FgenUI
from guiFiles.ui_flircam import FlirCamUI
from guiFiles.ui_polboards import PolBoards
from guiFiles.ui_bode100 import Bode100
import pyvisa as visa
import threading as th
import sys

class Buttons(ttk.Frame):

    def __init__(self, parent, instrLbl):
        super(Buttons, self).__init__(parent)
        instrumentsBtn = ttk.Button(
            self,
            text='Scan Instruments',
            width=20,
            command=lambda: self.btn3(instrLbl),
        )
        instrumentsBtn.grid(row=0, column=0, padx=20, pady=5)
        saveConfigBtn = ttk.Button(
            self,
            text='Save Config',
            width=20,
            command=self.btn1,
        )
        saveConfigBtn.grid(row=0, column=1, padx=20, pady=5)
        loadConfigBtn = ttk.Button(
            self,
            text='Load Config',
            width=20,
            command=self.btn2,
        )
        loadConfigBtn.grid(row=0, column=2, padx=(20, 40), pady=5)
        # loadConfigBtn['state'] = 'disabled'

    def btn1(self):
        filePath = filedialog.asksaveasfilename(
            defaultextension='.ini',
            filetypes=(("Config files", "*.ini"),)
        )
        config = ConfigMgr()
        config.save_config(filePath)
        print('Saved')
        return

    def btn2(self):
        filePath = filedialog.askopenfilename(
            defaultextension='.ini',
            filetypes=(("Config files", "*.ini"),)
        )
        config = ConfigMgr()
        config.config.read(filePath)
        config.update_dict(
            inst=1,
            temp1=0,
            temp2=0,
            temp3=0,
            temp4=0,
            temp5=0,
            temp6=0,
            cond1=0,
            cond2=0,
            cond3=0,
            cond4=0,
            cond5=0,
            cond6=0,
            ini=0,
            pscond1=0,
        )
        CustomPSUI.update_variables()
        ScopeUI.update_variables()
        LoadUI.update_variables()
        VCCUI.update_variables()
        VinUI.update_variables()
        BIASPSUI.update_variables()
        ENPSUI.update_variables()
        ThermUI.update_variables()
        KeithleyUI.update_variables()
        FgenUI.update_variables()
        FlirCamUI.update_variables()
        PolBoards.update_variables()
        Bode100.update_variables()
        #@TODO need to update the tkinter variables
        print('Loaded')
        return

    def btn3(self, instrLbl):
        scan = th.Thread(target=self._btn3, args=(instrLbl,))
        scan.start()

    def _btn3(self, instrLbl):
        rm = visa.ResourceManager()
        resourceList = rm.list_resources()
        instrLbl['state'] = 'normal'
        instrLbl.delete(1.0, tk.END)
        count = 1
        for src in resourceList:
            try:
                dev = rm.open_resource(src)
                id = dev.query('*IDN?')
                if id.rstrip() == '':
                    raise Exception
                resourceText = src + ' - ' + id.rstrip() + '\n'
                dev.close()
                instrLbl.insert(eval(f'{count}.0'), resourceText)
            except:
                try:
                    dev = rm.open_resource(src)
                    id = dev.query('ID?')
                    resourceText = src + ' - ' + id.rstrip() + '\n'
                    dev.query('ERR?')
                    dev.write('REM 0')
                    dev.close()
                    instrLbl.insert(eval(f'{count}.0'), resourceText)
                except:
                    try:
                        dev.write('CONF:REM OFF')
                    except:
                        pass
                    dev.close()
                    resourceText = src + ' - Unable to ID this device\n'
                    instrLbl.insert(eval(f'{count}.0'), resourceText)
                    continue
            count += 1
        instrLbl.configure(height=count)
        instrLbl.bind('<Configure>', lambda e: self.master.master.master.configure(scrollregion=self.master.master.master.bbox('all')))
        instrLbl['state'] = 'disabled'
        sys.exit()
        return

if __name__ == '__main__':
    root = tk.Tk()
    config = ConfigMgr()
    mybuttons = Buttons(root)
    mybuttons.grid(row=0, column=0, padx=10, pady=5, sticky='nw')
    root.mainloop()