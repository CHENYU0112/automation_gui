import tkinter as tk
from tkinter import ttk, StringVar
import subprocess, os, platform, sys
from PIL import Image, ImageTk
from guiFiles.tk_tooltip import CreateToolTip


def open_documentation(filePath):
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filePath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filePath)
    else:  # linux variants
        subprocess.call(('xdg-open', filePath))

def vcc_box(argList):
    '''
    :param argList: parent, varRadioBtn, configMgrObj, varEntry, validateFunc, validateEntryFunc
    '''
    vccEntryFrame = ttk.Frame(argList[0])
    vccEntryFrame.grid(row=1, column=0, columnspan=2, pady=2)
    startVccLbl = ttk.Label(vccEntryFrame, text='Start Vcc:')
    startVccLbl.grid(row=0, column=0, sticky='w')
    startVccEntry = ttk.Entry(
        vccEntryFrame,
        textvariable=argList[3],
        validate='focusout',
        validatecommand=lambda: argList[7](argList),
        width=4,
    )
    startVccEntry.grid(row=0, column=1, sticky='w')
    startVccUnitLbl = ttk.Label(vccEntryFrame, text='V')
    startVccUnitLbl.grid(row=0, column=2, sticky='w')
    argList.append(startVccLbl)
    argList.append(startVccEntry)
    argList.append(startVccUnitLbl)
    endVccLbl = ttk.Label(vccEntryFrame, text='End Vcc:')
    endVccLbl.grid(row=1, column=0, sticky='w')
    endVccEntry = ttk.Entry(
        vccEntryFrame,
        textvariable=argList[4],
        validate='focusout',
        validatecommand=lambda: argList[7](argList),
        width=4,
    )
    endVccEntry.grid(row=1, column=1, sticky='w')
    endVccUnitLbl = ttk.Label(vccEntryFrame, text='V')
    endVccUnitLbl.grid(row=1, column=2, sticky='w')
    argList.append(endVccLbl)
    argList.append(endVccEntry)
    argList.append(endVccUnitLbl)
    stepVccLbl = ttk.Label(vccEntryFrame, text='Step Vcc:')
    stepVccLbl.grid(row=2, column=0, sticky='w')
    stepVccEntry = ttk.Entry(
        vccEntryFrame,
        textvariable=argList[5],
        validate='focusout',
        validatecommand=lambda: argList[7](argList),
        width=4,
    )
    stepVccEntry.grid(row=2, column=1, sticky='w')
    stepVccUnitLbl = ttk.Label(vccEntryFrame, text='V')
    stepVccUnitLbl.grid(row=2, column=2, sticky='w')
    argList.append(stepVccLbl)
    argList.append(stepVccEntry)
    argList.append(stepVccUnitLbl)
    vccRadioButton = ttk.Radiobutton(
        argList[0],
        text='LDO',
        value='LDO',
        variable=argList[1],
        command=lambda: argList[6](argList),
    )
    vccRadioButton.grid(row=0, column=0)
    vccRadioButton1 = ttk.Radiobutton(
        argList[0],
        text='External',
        value='External',
        variable=argList[1],
        command=lambda: argList[6](argList),
    )
    vccRadioButton1.grid(row=0, column=1)

def ics_box(argList):
    # entry for soak time
    soakLbl = ttk.Label(argList[0], text='Soak Time:')
    soakLbl.grid(row=0, column=0, pady=2, sticky='e')
    soakEntry = ttk.Entry(
        argList[0],
        textvariable=argList[5],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    soakEntry.grid(row=0, column=1, pady=2, sticky='w')
    soakUnitLbl = ttk.Label(argList[0], text='min')
    soakUnitLbl.grid(row=0, column=2, pady=2, sticky='w')
    if argList[6]:
        # Relaxation Time
        relaxLbl = ttk.Label(argList[0], text='Relax. Time:')
        relaxLbl.grid(row=1, column=0, pady=2, sticky='e')
        relaxEntry = ttk.Entry(
            argList[0],
            textvariable=argList[7],
            validate='focusout',
            validatecommand=lambda: argList[3](argList),
            width=4,
        )
        relaxEntry.grid(row=1, column=1, pady=2, sticky='w')
        relaxUnitLbl = ttk.Label(argList[0], text='s')
        relaxUnitLbl.grid(row=1, column=2, pady=2, sticky='w')

def temp_register_box(argList):
    regTemp = ttk.Checkbutton(
        argList[0],
        text='Read Temp. Reg.',
        variable=argList[2],
        command=lambda: argList[3](argList),
    )
    regTemp.grid(row=0, column=0, sticky='w')
    runTest = ttk.Checkbutton(
        argList[0],
        text='Run Test',
        variable=argList[4],
        command=lambda: argList[5](argList),
    )
    runTest.grid(row=1, column=0, sticky='w')
    runTest.configure(style="Red.TCheckbutton")
    runTest['state'] = 'disabled'
    argList.append(runTest)
    return runTest

def document_link(argList):
    docLink = tk.Label(argList[0], text="Check Setup Documentation", fg="blue", cursor="hand2")
    docLink.grid(row=0, column=1, sticky='w')
    docLink.bind("<Button-1>", lambda e: open_documentation("document.pdf"))
    docBox = ttk.Checkbutton(
        argList[0],
        variable=argList[2],
        command=lambda: argList[4](argList),
    )
    docBox.grid(row=0, column=0, sticky='w')

def help_icon(argList):
    image = Image.open('guiFiles/img/question_mark_icon2.png')
    resizedImage = image.resize((10, 10))
    img = ImageTk.PhotoImage(resizedImage)
    imgLbl = tk.Label(argList[0], image=img)
    imgLbl.image = img
    imgLbl.grid(row=0, column=0)
    CreateToolTip(imgLbl, argList[1])

def current_box(argList):
    curr1Label = ttk.Label(argList[0], text='1:')
    curr1Label.grid(row=0, column=0, padx=2, sticky='e')
    curr1Entry = ttk.Entry(
        argList[0],
        textvariable=argList[3],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    curr1Entry.grid(row=0, column=1, pady=5, sticky='w')
    curr2Label = ttk.Label(argList[0], text='2:')
    curr2Label.grid(row=0, column=2, pady=5, padx=2, sticky='e')
    curr2Entry = ttk.Entry(
        argList[0],
        textvariable=argList[4],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    curr2Entry.grid(row=0, column=3, pady=5, sticky='w')
    curr3Label = ttk.Label(argList[0], text='3:')
    curr3Label.grid(row=1, column=0, pady=5, padx=2, sticky='e')
    curr3Entry = ttk.Entry(
        argList[0],
        textvariable=argList[5],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    curr3Entry.grid(row=1, column=1, pady=5, sticky='w')
    curr4Label = ttk.Label(argList[0], text='4:')
    curr4Label.grid(row=1, column=2, pady=5, padx=2, sticky='e')
    curr4Entry = ttk.Entry(
        argList[0],
        textvariable=argList[6],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    curr4Entry.grid(row=1, column=3, pady=5, sticky='w')
    curr5Label = ttk.Label(argList[0], text='5:')
    curr5Label.grid(row=2, column=0, pady=5, padx=2, sticky='e')
    curr5Entry = ttk.Entry(
        argList[0],
        textvariable=argList[7],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    curr5Entry.grid(row=2, column=1, pady=5, sticky='w')
    curr6Label = ttk.Label(argList[0], text='6:')
    curr6Label.grid(row=2, column=2, pady=5, padx=2, sticky='e')
    curr6Entry = ttk.Entry(
        argList[0],
        textvariable=argList[8],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    curr6Entry.grid(row=2, column=3, pady=5, sticky='w')
    # incremental
    startCurrLabel = ttk.Label(argList[9], text='Start Current:')
    startCurrLabel.grid(row=0, column=0, padx=2, pady=5, sticky='w')
    startCurrEntry = ttk.Entry(
        argList[9],
        textvariable=argList[10],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    startCurrEntry.grid(row=0, column=1, pady=5, sticky='e')
    endCurrLabel = ttk.Label(argList[9], text='End Current:')
    endCurrLabel.grid(row=1, column=0, padx=2, pady=5, sticky='w')
    endCurrEntry = ttk.Entry(
        argList[9],
        textvariable=argList[11],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    endCurrEntry.grid(row=1, column=1, pady=5, sticky='e')
    stepCurrLabel = ttk.Label(argList[9], text='Step Current:')
    stepCurrLabel.grid(row=2, column=0, padx=2, pady=5, sticky='w')
    stepCurrEntry = ttk.Entry(
        argList[9],
        textvariable=argList[12],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    stepCurrEntry.grid(row=2, column=1, pady=5, sticky='e')
    argList[9].grid_remove()

def frequency_box(argList):
    fsw1Lbl = ttk.Label(argList[0], text='1:')
    fsw1Lbl.grid(row=0, column=0, padx=2, pady=5, sticky='e')
    fsw1Entry = ttk.Entry(
        argList[0],
        textvariable=argList[4],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    fsw1Entry.grid(row=0, column=1, pady=5, sticky='w')
    fsw2Lbl = ttk.Label(argList[0], text='2:')
    fsw2Lbl.grid(row=0, column=2, padx=2, pady=5, sticky='e')
    fsw2Entry = ttk.Entry(
        argList[0],
        textvariable=argList[5],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    fsw2Entry.grid(row=0, column=3, pady=5, sticky='e')
    fsw3Lbl = ttk.Label(argList[0], text='3:')
    fsw3Lbl.grid(row=0, column=4, padx=2, pady=5, sticky='w')
    fsw3Entry = ttk.Entry(
        argList[0],
        textvariable=argList[6],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    fsw3Entry.grid(row=0, column=5, padx=2, pady=5)
    fsw4Lbl = ttk.Label(argList[0], text='4:')
    fsw4Lbl.grid(row=1, column=0, padx=2, pady=5, sticky='w')
    fsw4Entry = ttk.Entry(
        argList[0],
        textvariable=argList[7],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    fsw4Entry.grid(row=1, column=1, pady=5, sticky='e')
    fsw5Lbl = ttk.Label(argList[0], text='5:')
    fsw5Lbl.grid(row=1, column=2, padx=2, pady=5, sticky='w')
    fsw5Entry = ttk.Entry(
        argList[0],
        textvariable=argList[8],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    fsw5Entry.grid(row=1, column=3, pady=5, sticky='e')
    fsw6Lbl = ttk.Label(argList[0], text='6:')
    fsw6Lbl.grid(row=1, column=4, padx=2, pady=5, sticky='w')
    fsw6Entry = ttk.Entry(
        argList[0],
        textvariable=argList[9],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    fsw6Entry.grid(row=1, column=5, padx=2, pady=5)
    fsw7Lbl = ttk.Label(argList[0], text='7:')
    fsw7Lbl.grid(row=2, column=0, padx=2, pady=5, sticky='w')
    fsw7Entry = ttk.Entry(
        argList[0],
        textvariable=argList[10],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    fsw7Entry.grid(row=2, column=1, pady=5, sticky='e')
    fsw8Lbl = ttk.Label(argList[0], text='8:')
    fsw8Lbl.grid(row=2, column=2, padx=2, pady=5, sticky='w')
    fsw8Entry = ttk.Entry(
        argList[0],
        textvariable=argList[11],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    fsw8Entry.grid(row=2, column=3, pady=5, sticky='e')
    fsw9Lbl = ttk.Label(argList[0], text='9:')
    fsw9Lbl.grid(row=2, column=4, padx=2, pady=5, sticky='w')
    fsw9Entry = ttk.Entry(
        argList[0],
        textvariable=argList[12],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    fsw9Entry.grid(row=2, column=5, padx=2, pady=5)
    startFswLbl = ttk.Label(argList[1], text='Start Frequency:')
    startFswLbl.grid(row=0, column=0, padx=2, pady=5, sticky='e')
    startFswEntry = ttk.Entry(
        argList[1],
        textvariable=argList[13],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    startFswEntry.grid(row=0, column=1, pady=5, sticky='w')
    endFswLbl = ttk.Label(argList[1], text='End Frequency:')
    endFswLbl.grid(row=1, column=0, padx=2, pady=5, sticky='e')
    endFswEntry = ttk.Entry(
        argList[1],
        textvariable=argList[14],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    endFswEntry.grid(row=1, column=1, pady=5, sticky='w')
    stepFswLbl = ttk.Label(argList[1], text='Step Frequency:')
    stepFswLbl.grid(row=2, column=0, padx=2, pady=5, sticky='e')
    stepFswEntry = ttk.Entry(
        argList[1],
        textvariable=argList[15],
        validate='focusout',
        validatecommand=lambda: argList[3](argList),
        width=4,
    )
    stepFswEntry.grid(row=2, column=1, pady=5, sticky='w')
    argList[1].grid_remove()

def option_box(argList):
    currOptLabel = ttk.Label(argList[0], text='Current Input')
    currOptLabel.grid(row=0, column=0, pady=2)
    currOptRadioButton1 = ttk.Radiobutton(
        argList[0],
        text='Fixed Steps',
        variable=argList[4],
        value='fixed',
        command=lambda: argList[2](argList),
    )
    currOptRadioButton2 = ttk.Radiobutton(
        argList[0],
        text='Increment Steps',
        variable=argList[4],
        value='incr',
        command=lambda: argList[2](argList),
    )
    currOptRadioButton1.grid(row=1, column=0, pady=2, sticky='w')
    currOptRadioButton2.grid(row=2, column=0, pady=2, sticky='w')

    # HORIZONTAL LINE
    verticalLine = ttk.Separator(argList[0], orient='horizontal')
    verticalLine.grid(row=3, column=0, sticky='we', pady=5)

    # frequency input
    freqOptLabel = ttk.Label(argList[0], text='Frequency Input')
    freqOptLabel.grid(row=4, column=0, pady=2)

    freqOptRadioButton1 = ttk.Radiobutton(
        argList[0],
        text='Fixed Steps',
        variable=argList[5],
        value='fixed',
        command=lambda: argList[3](argList),
    )
    freqOptRadioButton2 = ttk.Radiobutton(
        argList[0],
        text='Increment Steps',
        variable=argList[5],
        value='incr',
        command=lambda: argList[3](argList),
    )
    freqOptRadioButton1.grid(row=5, column=0, pady=2, sticky='w')
    freqOptRadioButton2.grid(row=6, column=0, pady=2, sticky='w')

def pvin_box(argList):
    pVinLbl1 = ttk.Label(argList[0], text='Start PVin:')
    pVinLbl1.grid(row=0, column=0, pady=5, sticky='e')
    pVinEntry1 = ttk.Entry(
        argList[0],
        textvariable=argList[3],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    pVinEntry1.grid(row=0, column=1, pady=5, sticky='w')
    pVinLbl2 = ttk.Label(argList[0], text='End PVin:')
    pVinLbl2.grid(row=1, column=0, pady=5, sticky='e')
    pVinEntry2 = ttk.Entry(
        argList[0],
        textvariable=argList[4],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    pVinEntry2.grid(row=1, column=1, pady=5, sticky='w')
    pVinLbl3 = ttk.Label(argList[0], text='Step PVin:')
    pVinLbl3.grid(row=2, column=0, pady=5, sticky='e')
    pVinEntry3 = ttk.Entry(
        argList[0],
        textvariable=argList[5],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    pVinEntry3.grid(row=2, column=1, pady=5, sticky='w')
    if argList[1]['vinOpt'] == 'PVin':
        pass
    else:
        argList[0].grid_remove()

def pvin_box_fixed(argList):
    if argList[3] < 1:
        print('numOfInput must be 1 or higher')
    else:
        for i in range(argList[3]):
            pVinLbl1 = ttk.Label(argList[0], text=f'{1+i}:')
            pVinLbl1.grid(row=0+i, column=0, pady=5, sticky='e')
            pVinEntry1 = ttk.Entry(
                argList[0],
                textvariable=argList[4+i],
                validate='focusout',
                validatecommand=lambda: argList[2](argList),
                width=4,
            )
            pVinEntry1.grid(row=0+i, column=1, pady=5, sticky='w')
    if argList[1]['vinOpt'] == 'PVin':
        pass
    else:
        argList[0].grid_remove()

def vin_opt(argList):
    vinOptRbtn2Frame = ttk.Frame(argList[0])
    vinOptRbtn2Frame.grid(row=1, column=0, pady=5, sticky='w')
    vinExtEntry = ttk.Entry(
        vinOptRbtn2Frame,
        textvariable=argList[4],
        width=4,
        validate='focusout',
        validatecommand=lambda: argList[5](argList),
    )
    vinExtEntry.grid(row=0, column=1)
    vinExtUnitLbl = ttk.Label(vinOptRbtn2Frame, text='V')
    vinExtUnitLbl.grid(row=0, column=2)
    argList.append(vinExtEntry)
    vinOptRbtn2 = ttk.Radiobutton(
        vinOptRbtn2Frame,
        text='External',
        variable=argList[3],
        value='External',
        command=lambda: argList[2](argList),
    )
    vinOptRbtn2.grid(row=0, column=0)
    if argList[3].get() == 'External':
        vinExtEntry['state'] = 'normal'
    else:
        vinExtEntry['state'] = 'disabled'
    vinOptRbtn1 = ttk.Radiobutton(
        argList[0],
        text='Pvin',
        variable=argList[3],
        value='PVin',
        command=lambda: argList[2](argList),
    )
    vinOptRbtn1.grid(row=0, column=0, pady=5, sticky='w')
    vinOptRbtn3 = ttk.Radiobutton(
        argList[0],
        text='Short to VCC',
        variable=argList[3],
        value='Short',
        command=lambda: argList[2](argList),
    )
    vinOptRbtn3.grid(row=2, column=0, pady=5, sticky='w')

def vout_box(argList):
    voutLbl1 = ttk.Label(argList[0], text='1:')
    voutLbl1.grid(row=0, column=0, pady=5, sticky='e')
    voutEntry1 = ttk.Entry(
        argList[0],
        textvariable=argList[3],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    voutEntry1.grid(row=0, column=1, pady=5, sticky='w')
    voutLbl2 = ttk.Label(argList[0], text='2:')
    voutLbl2.grid(row=1, column=0, pady=5, sticky='e')
    voutEntry2 = ttk.Entry(
        argList[0],
        textvariable=argList[4],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    voutEntry2.grid(row=1, column=1, pady=5, sticky='w')
    voutLbl3 = ttk.Label(argList[0], text='3:')
    voutLbl3.grid(row=2, column=0, pady=5, sticky='e')
    voutEntry3 = ttk.Entry(
        argList[0],
        textvariable=argList[5],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    voutEntry3.grid(row=2, column=1, pady=5, sticky='w')
    if argList[6] == 5:
        voutLbl4 = ttk.Label(argList[0], text='4:')
        voutLbl4.grid(row=3, column=0, pady=5, sticky='e')
        voutEntry4 = ttk.Entry(
            argList[0],
            textvariable=argList[7],
            validate='focusout',
            validatecommand=lambda: argList[2](argList),
            width=4,
        )
        voutEntry4.grid(row=3, column=1, pady=5, sticky='w')
        voutLbl5 = ttk.Label(argList[0], text='5:')
        voutLbl5.grid(row=4, column=0, pady=5, sticky='e')
        voutEntry5 = ttk.Entry(
            argList[0],
            textvariable=argList[8],
            validate='focusout',
            validatecommand=lambda: argList[2](argList),
            width=4,
        )
        voutEntry5.grid(row=4, column=1, pady=5, sticky='w')

def mode_box(argList):
    modeRadioBtn = ttk.Radiobutton(
        argList[0],
        text='FCCM',
        variable=argList[3],
        value='FCCM',
        command=lambda: argList[2](argList),
    )
    modeRadioBtn2 = ttk.Radiobutton(
        argList[0],
        text='DEM',
        variable=argList[3],
        value='DEM',
        command=lambda: argList[2](argList),
    )
    modeRadioBtn.grid(row=0, column=0, sticky='w')
    modeRadioBtn2.grid(row=1, column=0, sticky='w')

def jira_box():
    jiraLink = tk.Label(text="https://jirard.intra.infineon.com/projects/EFFFFU/issues/EFFFFU-3?filter=allopenissues", font=('Arial', 8), background='#FFB4A4')
    jiraLink.grid(row=1, column=0, padx=2, pady=2, sticky='w')

def temperature_box(argList):
    tempStep1 = tk.Label(argList[0], text='1:', font=('Arial', 8), background='#FFB4A4')
    tempStep1.grid(row=1, column=0, padx=2, pady=2, sticky='e')
    tempEntry = ttk.Entry(
        argList[0],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        textvariable=argList[3],
        width=3,
    )
    tempEntry.grid(row=1, column=1, padx=2, pady=2, sticky='w')
    tempStep2 = tk.Label(argList[0], text='2:', font=('Arial', 8), background='#FFB4A4')
    tempStep2.grid(row=1, column=2, padx=2, pady=2, sticky='e')
    tempEntry = ttk.Entry(
        argList[0],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        textvariable=argList[4],
        width=3,
    )
    tempEntry.grid(row=1, column=3, padx=2, pady=2, sticky='w')
    tempStep3 = tk.Label(argList[0], text='3:', font=('Arial', 8), background='#FFB4A4')
    tempStep3.grid(row=1, column=4, padx=2, pady=2, sticky='e')
    tempEntry = ttk.Entry(
        argList[0],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        textvariable=argList[5],
        width=3
    )
    tempEntry.grid(row=1, column=5, padx=2, pady=2, sticky='w')
    tempStep4 = tk.Label(argList[0], text='4:', font=('Arial', 8), background='#FFB4A4')
    tempStep4.grid(row=1, column=6, padx=2, pady=2, sticky='e')
    tempEntry = ttk.Entry(
        argList[0],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        textvariable=argList[6],
        width=3
    )
    tempEntry.grid(row=1, column=7, padx=2, pady=2, sticky='w')
    tempStep5 = tk.Label(argList[0], text='5:', font=('Arial', 8), background='#FFB4A4')
    tempStep5.grid(row=1, column=8, padx=2, pady=2, sticky='e')
    tempEntry = ttk.Entry(
        argList[0],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        textvariable=argList[7],
        width=3
    )
    tempEntry.grid(row=1, column=9, padx=2, pady=2, sticky='w')
    tempStep6 = tk.Label(argList[0], text='6:', font=('Arial', 8), background='#FFB4A4')
    tempStep6.grid(row=1, column=10, padx=2, pady=2, sticky='e')
    tempEntry = ttk.Entry(
        argList[0],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        textvariable=argList[8],
        width=3
    )
    tempEntry.grid(row=1, column=11, padx=2, pady=2, sticky='w')

def bias_box(argList):
    pass

def selection_box(argList):
    hr = 0
    hc = 0
    for i in range(argList[3]):
        chkbx = ttk.Checkbutton(
            argList[0],
            text=argList[6+2*i],
            variable=argList[5+2*i],
            command=lambda: argList[2](argList),
        )
        chkbx.grid(row=hr, column=hc)
        hr += 1
        if hr == 3:
            hr = 0
            hc += 1

def horizontal_scale_box(argList):
    hr = 0
    hc = 0
    for i in range(argList[3]):
        lbl = ttk.Label(argList[0], text=f'Hor. Scale {1+i}:')
        lbl.grid(row=hr, column=hc, sticky='e')
        entry = ttk.Entry(
            argList[0],
            textvariable=argList[4+i],
            validate='focusout',
            validatecommand=lambda: argList[2](argList),
            width=6,
        )
        entry.grid(row=hr, column=hc+1, sticky='w')
        hr += 1
        if hr == 3:
            hc += 1
            hr = 0

def vcc_incr(argList):
    lbl1 = ttk.Label(argList[0], text='Start VCC:')
    lbl1.grid(row=0, column=0, pady=5, sticky='e')
    entry1 = ttk.Entry(
        argList[0],
        textvariable=argList[3],
        validate='focusout',
        validatecommand=argList[2],
        width=4,
    )
    entry1.grid(row=0, column=1, pady=5, sticky='w')
    lbl2 = ttk.Label(argList[0], text='End VCC:')
    lbl2.grid(row=1, column=0, pady=5, sticky='e')
    entry2 = ttk.Entry(
        argList[0],
        textvariable=argList[4],
        validate='focusout',
        validatecommand=argList[2],
        width=4,
    )
    entry2.grid(row=1, column=1, pady=5, sticky='w')
    lbl3 = ttk.Label(argList[0], text='Step VCC:')
    lbl3.grid(row=2, column=0, pady=5, sticky='e')
    entry3 = ttk.Entry(
        argList[0],
        textvariable=argList[5],
        validate='focusout',
        validatecommand=argList[2],
        width=4,
    )
    entry3.grid(row=2, column=1, pady=5, sticky='w')

def keithley_channel(argList):
    lbl1 = tk.Label(argList[0], text='Vin Ch:', background='#A4E1FF')
    lbl1.grid(row=0, column=0, padx=2, pady=2, sticky='w')
    entry1 = ttk.Entry(
        argList[0],
        textvariable=argList[3],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry1.grid(row=0, column=1, padx=2, pady=2, sticky='w')

    lbl2 = tk.Label(argList[0], text='Iin Ch:', background='#A4E1FF')
    lbl2.grid(row=0, column=2, padx=2, pady=2, sticky='w')
    entry2 = ttk.Entry(
        argList[0],
        textvariable=argList[4],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry2.grid(row=0, column=3, padx=2, pady=2, sticky='w')

    lbl3 = tk.Label(argList[0], text='Iin shunt:', background='#A4E1FF')
    lbl3.grid(row=0, column=4, padx=2, pady=2, sticky='w')
    entry3 = ttk.Entry(
        argList[0],
        textvariable=argList[5],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry3.grid(row=0, column=5, padx=2, pady=2, sticky='w')
    lbl3unt = tk.Label(argList[0], text='m\u03A9', background='#A4E1FF')
    lbl3unt.grid(row=0, column=6, padx=2, pady=2, sticky='w')

    lbl4 = tk.Label(argList[0], text='Vout Ch:', background='#A4E1FF')
    lbl4.grid(row=0, column=7, padx=2, pady=2, sticky='w')
    entry4 = ttk.Entry(
        argList[0],
        textvariable=argList[6],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry4.grid(row=0, column=8, padx=2, pady=2, sticky='w')

    lbl5 = tk.Label(argList[0], text='Iout Ch:', background='#A4E1FF')
    lbl5.grid(row=0, column=9, padx=2, pady=2, sticky='w')
    entry5 = ttk.Entry(
        argList[0],
        textvariable=argList[7],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry5.grid(row=0, column=10, padx=2, pady=2, sticky='w')

    lbl6 = tk.Label(argList[0], text='Iout shunt:', background='#A4E1FF')
    lbl6.grid(row=0, column=11, padx=2, pady=2, sticky='w')
    entry6 = ttk.Entry(
        argList[0],
        textvariable=argList[8],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry6.grid(row=0, column=12, padx=2, pady=2, sticky='w')
    lbl6unt = tk.Label(argList[0], text='m\u03A9', background='#A4E1FF')
    lbl6unt.grid(row=0, column=13, padx=2, pady=2, sticky='w')

    lbl7 = tk.Label(argList[0], text='Vcc Ch:', background='#A4E1FF')
    lbl7.grid(row=1, column=0, padx=2, pady=2, sticky='w')
    entry7 = ttk.Entry(
        argList[0],
        textvariable=argList[9],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry7.grid(row=1, column=1, padx=2, pady=2, sticky='w')

    lbl8 = tk.Label(argList[0], text='Icc Ch:', background='#A4E1FF')
    lbl8.grid(row=1, column=2, padx=2, pady=2, sticky='w')
    entry8 = ttk.Entry(
        argList[0],
        textvariable=argList[10],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry8.grid(row=1, column=3, padx=2, pady=2, sticky='w')

    lbl9 = tk.Label(argList[0], text='Icc shunt:', background='#A4E1FF')
    lbl9.grid(row=1, column=4, padx=2, pady=2, sticky='w')
    entry9 = ttk.Entry(
        argList[0],
        textvariable=argList[11],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry9.grid(row=1, column=5, padx=2, pady=2, sticky='w')
    lbl9unt = tk.Label(argList[0], text='m\u03A9', background='#A4E1FF')
    lbl9unt.grid(row=1, column=6, padx=2, pady=2, sticky='w')

    lbl10 = tk.Label(argList[0], text='Tmon Ch:', background='#A4E1FF')
    lbl10.grid(row=1, column=7, padx=2, pady=2, sticky='w')
    entry10 = ttk.Entry(
        argList[0],
        textvariable=argList[12],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry10.grid(row=1, column=8, padx=2, pady=2, sticky='w')

    lbl11 = tk.Label(argList[0], text='Imon:', background='#A4E1FF')
    lbl11.grid(row=1, column=9, padx=2, pady=2, sticky='w')
    entry11 = ttk.Entry(
        argList[0],
        textvariable=argList[13],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry11.grid(row=1, column=10, padx=2, pady=2, sticky='w')

    lbl12 = tk.Label(argList[0], text='Pgood Ch:', background='#A4E1FF')
    lbl12.grid(row=1, column=11, padx=2, pady=2, sticky='w')
    entry12 = ttk.Entry(
        argList[0],
        textvariable=argList[14],
        validate='focusout',
        validatecommand=lambda: argList[2](argList),
        width=4,
    )
    entry12.grid(row=1, column=12, padx=2, pady=2, sticky='w')


