import tkinter as tk
from pygrabber.dshow_graph import FilterGraph
from guiFiles import configmgr, instruments, tabs, scrollcanvas, efficiencygui, efficiencyframe, polefficiencyframe


def run():
    config = configmgr.ConfigMgr()
    graph = FilterGraph()
    window = efficiencygui.EFFICIENCYGUI()
    notebook = tabs.Tabs(window)

    #region TAB 0
    tab0 = tk.Frame(notebook)
    tab0.pack(fill=tk.BOTH, expand=True)
    notebook.add(tab0, text='Instruments')
    tab0Canvas = scrollcanvas.ScrollCanvas(tab0)
    tab0Canvas.pack(fill=tk.BOTH, expand=True)
    # 0 - PSapp; 1 - POLapp
    tab0Frame = instruments.Instruments(tab0Canvas, 0)
    tab0Canvas.create_window((0,0), window=tab0Frame, anchor='nw')
    #endregion

    #region TAB 1
    tab1 = tk.Frame(notebook)
    tab1.pack(fill=tk.BOTH, expand=True)
    notebook.add(tab1, text='PS Efficiency')
    tab1Canvas = scrollcanvas.ScrollCanvas(tab1)
    tab1Canvas['background'] = 'white'
    tab1Canvas.pack(fill=tk.BOTH, expand=True)
    tab1Frame = efficiencyframe.EffFrame(tab1Canvas)
    tab1Canvas.create_window((0, 0), window=tab1Frame, anchor='nw')
    #endregion

    # region TAB 2
    # tab2 = tk.Frame(notebook)
    # tab2.pack(fill=tk.BOTH, expand=True)
    # notebook.add(tab2, text='POL Efficiency')
    # tab2Canvas = scrollcanvas.ScrollCanvas(tab2)
    # tab2Canvas['background'] = 'white'
    # tab2Canvas.pack(fill=tk.BOTH, expand=True)
    # tab2Frame = polefficiencyframe.EffFrame(tab2Canvas)
    # tab2Canvas.create_window((0, 0), window=tab2Frame, anchor='nw')
    # endregion

    #region RUN MAIN LOOP
    window.mainloop()
    #endregion


if __name__ == '__main__':
    run()