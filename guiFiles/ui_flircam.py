import tkinter as tk
from tkinter import ttk, StringVar
from pygrabber.dshow_graph import FilterGraph
from guiFiles.configmgr import ConfigMgr
import guiFiles.guihelperfunc as make

class FlirCamUI(ttk.Frame):

    varCamBox = None
    varCamModel = None

    def __init__(self, parent):
        super(FlirCamUI, self).__init__(parent)
        self.camList = self.list_cams()
        FlirCamUI.varCamBox = StringVar()
        self.camBox = ttk.Checkbutton(
            self,
            text='On/Off',
            variable=self.varCamBox,
            command=lambda: self.display_cam(self.varCamBox.get())
        )
        self.varCamBox.set(ConfigMgr.instr['camOnOff'])
        self.camBox.grid(row=0, column=0)
        lbl = tk.Label(
            self,
            text='FLIR Camera',
            font=("Arial Bold", 10)
        )
        lbl.grid(row=1, column=0,)
        # region Help Icon
        helpFrame = ttk.Frame(self)
        helpFrame.grid(row=0, column=6, columnspan=199, padx=(5, 2), sticky='e')
        helpMsg = '''Help - FLIR Camera to capture Thermal images. Used for specific tests only.'''
        imgArgLst = [
            helpFrame,
            helpMsg,
        ]
        make.help_icon(imgArgLst)
        # endregion
        FlirCamUI.varCamModel = StringVar()
        self.dropMenu = ttk.OptionMenu(
            self,
            self.varCamModel,
            self.camList[0],
            *self.camList,
            command=self.cam_option,
        )
        self.varCamModel.set(ConfigMgr.instr['flirCam'])
        self.dropMenu.grid(row=2, column=0)
        btn = ttk.Button(self, text='Update List', command=self.update_cam_list)
        btn.grid(row=3, column=0, pady=2)

    def display_cam(self, content):
        ConfigMgr.instr['camOnOff'] = str(content)
        return True

    def cam_option(self, content):
        ConfigMgr.instr['flirCam'] = str(content)
        return True

    def list_cams(self):
        try:
            graph = FilterGraph()
            return graph.get_input_devices()
        except:
            return ['None found']

    def update_cam_list(self):
        self.camList = self.list_cams()
        self.dropMenu = ttk.OptionMenu(
            self,
            self.varCamModel,
            self.camList[0],
            *self.camList,
            command=self.cam_option,
        )
        self.dropMenu.grid(row=2, column=0)

    @classmethod
    def update_variables(cls):
        cls.varCamBox.set(ConfigMgr.instr['camOnOff'])
        cls.varCamModel.set(ConfigMgr.instr['flirCam'])


if __name__ == '__main__':
    root = tk.Tk()
    fircam = FlirCamUI(root)
    fircam.grid(row=0, column=0, padx=5, pady=5)
    root.mainloop()