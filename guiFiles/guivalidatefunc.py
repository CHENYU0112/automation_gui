from time import sleep

def temperature(argList):
    argList[1]['1'] = argList[3].get()
    argList[1]['2'] = argList[4].get()
    argList[1]['3'] = argList[5].get()
    argList[1]['4'] = argList[6].get()
    argList[1]['5'] = argList[7].get()
    argList[1]['6'] = argList[8].get()
    return True

def current(argList):
    argList[1]['curr1'] = argList[3].get()
    argList[1]['curr2'] = argList[4].get()
    argList[1]['curr3'] = argList[5].get()
    argList[1]['curr4'] = argList[6].get()
    argList[1]['curr5'] = argList[7].get()
    argList[1]['curr6'] = argList[8].get()
    argList[1]['startCurr'] = argList[10].get()
    argList[1]['endCurr'] = argList[11].get()
    argList[1]['stepCurr'] = argList[12].get()
    return True

def current_204(argList):
    argList[0]['curr1'] = argList[1].get()
    return True

def frequency(argList):
    argList[2]['fsw1'] = argList[4].get()
    argList[2]['fsw2'] = argList[5].get()
    argList[2]['fsw3'] = argList[6].get()
    argList[2]['fsw4'] = argList[7].get()
    argList[2]['fsw5'] = argList[8].get()
    argList[2]['fsw6'] = argList[9].get()
    argList[2]['fsw7'] = argList[10].get()
    argList[2]['fsw8'] = argList[11].get()
    argList[2]['fsw9'] = argList[12].get()
    argList[2]['startFsw'] = argList[13].get()
    argList[2]['endFsw'] = argList[14].get()
    argList[2]['stepFsw'] = argList[15].get()
    return True

def test_conditions(argList):
    argList[1]['cout'] = argList[2].get()
    argList[1]['inductance'] = argList[4].get()
    argList[1]['soak'] = argList[5].get()
    if argList[6]:
        argList[1]['relax'] = argList[7].get()
    return True

def register_temp(argList):
    argList[1]['registerTemp'] = argList[2].get()
    return True

def run_test(argList):
    if argList[6] == 'test101':
        argList[7]['test101'] = '1' if eval(argList[1]['test101']) else '0'
        argList[7]['test104'] = '1' if eval(argList[1]['test104']) else '0'
    else:
        argList[7][argList[6]] = argList[4].get()
    if argList[4].get() == '1':
        argList[8].configure(style="Green.TCheckbutton")
    else:
        argList[8].configure(style="Red.TCheckbutton")
    return True

def document(argList):
    argList[1]['document'] = argList[2].get()
    try:
        argList[3]['state'] = 'normal' if eval(argList[2].get()) else 'disabled'
    except:
        pass
    return True

def current_opt(argList):
    opt = argList[4].get()
    argList[1]['currOpt'] = opt
    if (opt == 'fixed'):
        argList[7].grid_remove()
        argList[6].grid()
    else:
        argList[6].grid_remove()
        argList[7].grid()
    return True

def frequency_opt(argList):
    opt = argList[5].get()
    argList[1]['fswOpt'] = opt
    if (opt == 'fixed'):
        argList[9].grid_remove()
        argList[8].grid()
    else:
        argList[8].grid_remove()
        argList[9].grid()
    return True

def mode(argList):
    argList[1]['modeDEM'] = str(argList[3].get())
    argList[1]['modeFCCM'] = str(argList[4].get())
    return True

def ldo_ext(varList):
    '''
    :param varList: parent, varRadioBtn, configMgrObj, varEntry, validateFunc, validateEntryFunc, vccLbl, vccEntry
                    vccUnitLbl
    :return:
    '''
    varList[3]['vccLdo'] = varList[1].get()
    varList[3]['vccExt'] = varList[2].get()
    if varList[2].get() == '1':
        varList[9].grid()
        varList[10]['state'] = 'normal'
        varList[11]['state'] = 'normal'
        varList[12]['state'] = 'normal'
        varList[13]['state'] = 'normal'
        varList[14]['state'] = 'normal'
        varList[15]['state'] = 'normal'
        varList[16]['state'] = 'normal'
        varList[17]['state'] = 'normal'
        varList[18]['state'] = 'normal'
    else:
        varList[9].grid_remove()
        varList[10]['state'] = 'disabled'
        varList[11]['state'] = 'disabled'
        varList[12]['state'] = 'disabled'
        varList[13]['state'] = 'disabled'
        varList[14]['state'] = 'disabled'
        varList[15]['state'] = 'disabled'
        varList[16]['state'] = 'disabled'
        varList[17]['state'] = 'disabled'
        varList[18]['state'] = 'disabled'
    return True

def en_ext(argList):
    argList[2]['enOpt'] = argList[1].get()
    if argList[1].get() == 'EN':
        argList[8].grid_remove()
        argList[10].tkraise()
    else:
        argList[8].grid()
        argList[11].tkraise()
    return True

def keithley_channels(argList):
    argList[1]['kvin'] = argList[3].get()
    argList[1]['kiin'] = argList[4].get()
    argList[1]['kiinr'] = argList[5].get()
    argList[1]['kvout'] = argList[6].get()
    argList[1]['kiout'] = argList[7].get()
    argList[1]['kioutr'] = argList[8].get()
    argList[1]['kvcc'] = argList[9].get()
    argList[1]['kicc'] = argList[10].get()
    argList[1]['kiccr'] = argList[11].get()
    argList[1]['ktmon'] = argList[12].get()
    argList[1]['kimon'] = argList[13].get()
    argList[1]['kpgood'] = argList[14].get()
    return True

def ps_keithley_channels(argList):
    argList[1]['kvin'] = argList[3].get()
    argList[1]['kiin'] = argList[4].get()
    argList[1]['kiinr'] = argList[5].get()
    argList[1]['kvout'] = argList[6].get()
    argList[1]['kiout'] = argList[7].get()
    argList[1]['kioutr'] = argList[8].get()
    argList[1]['kvcc'] = argList[9].get()
    argList[1]['kicc'] = argList[10].get()
    argList[1]['kiccr'] = argList[11].get()
    argList[1]['ktmon'] = argList[12].get()
    argList[1]['kimon'] = argList[13].get()
    argList[1]['kvoutsw'] = argList[14].get()
    argList[1]['kven'] = argList[15].get()
    argList[1]['kien'] = argList[16].get()
    argList[1]['kienr'] = argList[17].get()
    return True

def keithley_channels_derating(argList):
    argList[1]['kvin'] = argList[3].get()
    argList[1]['kiin'] = argList[4].get()
    argList[1]['kiinr'] = argList[5].get()
    argList[1]['kvout'] = argList[6].get()
    argList[1]['kiout'] = argList[7].get()
    argList[1]['kioutr'] = argList[8].get()
    argList[1]['kvcc'] = argList[9].get()
    argList[1]['kicc'] = argList[10].get()
    argList[1]['kiccr'] = argList[11].get()
    argList[1]['ktmon'] = argList[12].get()
    argList[1]['kimon'] = argList[13].get()
    argList[1]['kpgood'] = argList[14].get()
    argList[1]['tCase'] = argList[15].get()
    argList[1]['tBoard'] = argList[16].get()
    argList[1]['tAmb1'] = argList[17].get()
    argList[1]['tAmb2'] = argList[18].get()
    argList[1]['tAC'] = argList[19].get()
    return True

def keithley_channels_307(argList):
    argList[0]['kIoutCh'] = argList[1].get()
    argList[0]['ioutShunt'] = argList[2].get()
    return True

def il_sample_time(argList):
    argList[0]['ilTime1'] = argList[1].get()
    argList[0]['ilTime2'] = argList[2].get()
    return True

def vcc_entry(varList):
    '''
    :param varList: parent, varRadioBtn, configMgrObj, varEntry, validateFunc, validateEntryFunc
    '''
    varList[3]['startVcc'] = varList[4].get()
    varList[3]['endVcc'] = varList[5].get()
    varList[3]['stepVcc'] = varList[6].get()
    return True

def en_entry(argList):
    argList[2]['en1'] = argList[3].get()
    argList[2]['en2'] = argList[4].get()
    argList[2]['en3'] = argList[5].get()
    argList[2]['enPvin'] = argList[9].get()
    return True

def vin_opt(argList):
    argList[1]['vinOpt'] = argList[3].get()
    if argList[3].get() == 'External':
        argList[7]['state'] = 'normal'
        argList[6].grid_remove()
    elif argList[3].get() == 'PVin':
        argList[7]['state'] = 'disabled'
        argList[6].grid()
    else:
        argList[7]['state'] = 'disabled'
        argList[6].grid_remove()
    return True

def vin_ext(argList):
    argList[1]['vinExt'] = argList[4].get()
    return True

def pvin_incr(argList):
    argList[1]['startPVin'] = argList[3].get()
    argList[1]['endPVin'] = argList[4].get()
    argList[1]['stepPVin'] = argList[5].get()
    return True

def pvin_fixed(argList):
    for i in range(argList[3]):
        argList[1][f'PVin{i+1}'] = argList[4+i].get()

def vout(argList):
    argList[1]['vout1'] = argList[3].get()
    argList[1]['vout2'] = argList[4].get()
    argList[1]['vout3'] = argList[5].get()
    if argList[6] == 5:
        argList[1]['vout4'] = argList[7].get()
        argList[1]['vout5'] = argList[8].get()

def bias(argList):
    for i in range(argList[4]):
        argList[1][f'bias{i+1}'] = argList[6+i].get()

def bias_opt(argList):
    argList[1]['biasOpt'] = argList[5].get()
    idx = -1
    if eval(argList[5].get()):
        for i in range(argList[4]):
            argList[idx][0]['state'] = 'normal'
            argList[idx][1]['state'] = 'normal'
            idx -= 1
    else:
        for i in range(argList[4]):
            argList[idx][0]['state'] = 'disabled'
            argList[idx][1]['state'] = 'disabled'
            idx -= 1

def selection101(argList):
    for i in range(argList[3]):
        argList[1][argList[6+2*i].replace(' ', '')] = argList[5+2*i].get()

    if argList[7].get() == '0':
        argList[4].grid_remove()
        argList[9].grid_remove()
    else:
        argList[4].grid()
        argList[9].grid()

    if argList[5].get() == '0':
        argList[10].grid_remove()
        argList[11].grid_remove()
    else:
        argList[10].grid()
        argList[11].grid()
    argList[0].master.master.master.update_idletasks()
    argList[0].master.master.master.configure(scrollregion=argList[0].master.master.bbox('all'))
    return True

def selection201(argList):
    for i in range(argList[3]):
        argList[1][argList[6+2*i].replace(' ', '')] = argList[5+2*i].get()

    argList[0].master.master.master.update_idletasks()
    argList[0].master.master.master.configure(scrollregion=argList[0].master.master.bbox('all'))
    return True

def dem_boundary(argList):
    for i in range(argList[3]):
        argList[1][f'demBoundary'] = argList[4+i].get()
    return True

def vcc_incr(argList):
    argList[2]['startVcc'] = argList[3].get()
    argList[2]['endVcc'] = argList[4].get()
    argList[2]['stepVcc'] = argList[5].get()
    return True

def scope_ch_104(argList):
    argList[0]['scopeVoutCh'] = argList[1].get()
    argList[0]['scopeSwCh'] = argList[2].get()
    return True

def scope_ch_101(argList):
    argList[0]['scopeSwCh'] = argList[1].get()
    return True

def scope_ch_201(argList):
    argList[0]['scopeSwCh'] = argList[1].get()
    argList[0]['scopeVdshCh'] = argList[2].get()
    argList[0]['scopeVinCh'] = argList[3].get()
    argList[0]['scopeVoutCh'] = argList[4].get()
    return True

def scope_ch_202(argList):
    argList[0]['scopeSwCh'] = argList[1].get()
    argList[0]['scopeVinCh'] = argList[2].get()
    argList[0]['scopeVoutCh'] = argList[3].get()
    return True

def scope_ch_204(argList):
    argList[0]['scopeSwCh'] = argList[1].get()
    argList[0]['scopeILCh'] = argList[2].get()
    argList[0]['scopeVoutCh'] = argList[3].get()
    return True

def scope_ch_205(argList):
    argList[0]['scopeSwCh'] = argList[1].get()
    argList[0]['scopeVoutCh'] = argList[2].get()
    argList[0]['scopeGateLCh'] = argList[3].get()
    argList[0]['scopeBootCh'] = argList[4].get()
    return True

def scope_ch_301(argList):
    argList[0]['scopeSwCh'] = argList[1].get()
    argList[0]['scopeVccCh'] = argList[2].get()
    argList[0]['scopePgoodCh'] = argList[3].get()
    argList[0]['scopeVoutCh'] = argList[4].get()
    argList[0]['scopeEnCh'] = argList[5].get()
    argList[0]['scopePvinCh'] = argList[6].get()
    argList[0]['scopeCus1Ch'] = argList[7].get()
    argList[0]['scopeCus1Lbl'] = argList[8].get()
    argList[0]['scopeCus1Ch'] = argList[9].get()
    argList[0]['scopeCus1Lbl'] = argList[10].get()
    return True

def scope_ch_307(argList):
    argList[0]['scopeSwCh'] = argList[1].get()
    argList[0]['scopeCSCh'] = argList[2].get()
    argList[0]['scopeILCh'] = argList[3].get()
    argList[0]['scopeVoutCh'] = argList[4].get()
    argList[0]['scopeCus1Ch'] = argList[5].get()
    argList[0]['scopeCus1Lbl'] = argList[6].get()
    argList[0]['scopeCus2Ch'] = argList[7].get()
    argList[0]['scopeCus2Lbl'] = argList[8].get()
    return True

def dbm(argList):
    argList[0]['dbm'] = argList[1].get()
    return True

def rise_opt(argList):
    same = eval(argList[4].get())
    argList[1]['riseOpt'] = argList[4].get()
    if same:
        argList[8].set(argList[5].get())
        argList[9].set(argList[6].get())
        argList[10].set(argList[7].get())
        argList[1]['fall1'] = argList[5].get()
        argList[1]['fall2'] = argList[6].get()
        argList[1]['fall3'] = argList[7].get()
        argList[11]['state'] = 'disabled'
        argList[12]['state'] = 'disabled'
        argList[13]['state'] = 'disabled'
    else:
        argList[11]['state'] = 'normal'
        argList[12]['state'] = 'normal'
        argList[13]['state'] = 'normal'

    return True

def rise_fall_time(argList):
    argList[1]['rise1'] = argList[5].get()
    argList[1]['rise2'] = argList[6].get()
    argList[1]['rise3'] = argList[7].get()
    argList[1]['fall1'] = argList[8].get()
    argList[1]['fall2'] = argList[9].get()
    argList[1]['fall3'] = argList[10].get()
    return True

def vcc_rise_opt(argList):
    same = eval(argList[4].get())
    argList[1]['vccRiseOpt'] = argList[4].get()
    if same:
        argList[8].set(argList[5].get())
        argList[9].set(argList[6].get())
        argList[10].set(argList[7].get())
        argList[1]['vccFall1'] = argList[5].get()
        argList[1]['vccFall2'] = argList[6].get()
        argList[1]['vccFall3'] = argList[7].get()
        argList[11]['state'] = 'disabled'
        argList[12]['state'] = 'disabled'
        argList[13]['state'] = 'disabled'
    else:
        argList[11]['state'] = 'normal'
        argList[12]['state'] = 'normal'
        argList[13]['state'] = 'normal'
    return True

def vcc_rise_fall_time(argList):
    argList[1]['vccRise1'] = argList[5].get()
    argList[1]['vccRise2'] = argList[6].get()
    argList[1]['vccRise3'] = argList[7].get()
    argList[1]['vccFall1'] = argList[8].get()
    argList[1]['vccFall2'] = argList[9].get()
    argList[1]['vccFall3'] = argList[10].get()
    return True

def en_rise_opt(argList):
    same = eval(argList[4].get())
    argList[1]['enRiseOpt'] = argList[4].get()
    if same:
        argList[8].set(argList[5].get())
        argList[9].set(argList[6].get())
        argList[10].set(argList[7].get())
        argList[1]['enFall1'] = argList[5].get()
        argList[1]['enFall2'] = argList[6].get()
        argList[1]['enFall3'] = argList[7].get()
        argList[11]['state'] = 'disabled'
        argList[12]['state'] = 'disabled'
        argList[13]['state'] = 'disabled'
    else:
        argList[11]['state'] = 'normal'
        argList[12]['state'] = 'normal'
        argList[13]['state'] = 'normal'
    return True

def en_rise_fall_time(argList):
    argList[1]['enRise1'] = argList[5].get()
    argList[1]['enRise2'] = argList[6].get()
    argList[1]['enRise3'] = argList[7].get()
    argList[1]['enFall1'] = argList[8].get()
    argList[1]['enFall2'] = argList[9].get()
    argList[1]['enFall3'] = argList[10].get()
    return True

def cus_rise_opt(argList):
    same = eval(argList[4].get())
    argList[1]['cusRiseOpt'] = argList[4].get()
    if same:
        argList[8].set(argList[5].get())
        argList[9].set(argList[6].get())
        argList[10].set(argList[7].get())
        argList[1]['cusFall1'] = argList[5].get()
        argList[1]['cusFall2'] = argList[6].get()
        argList[1]['cusFall3'] = argList[7].get()
        argList[11]['state'] = 'disabled'
        argList[12]['state'] = 'disabled'
        argList[13]['state'] = 'disabled'
    else:
        argList[11]['state'] = 'normal'
        argList[12]['state'] = 'normal'
        argList[13]['state'] = 'normal'
    return True

def cus_rise_fall_time(argList):
    argList[1]['cusRise1'] = argList[5].get()
    argList[1]['cusRise2'] = argList[6].get()
    argList[1]['cusRise3'] = argList[7].get()
    argList[1]['cusFall1'] = argList[8].get()
    argList[1]['cusFall2'] = argList[9].get()
    argList[1]['cusFall3'] = argList[10].get()
    return True

def tiping(argList):
    argList[1]['tipTemp'] = argList[3].get()
    argList[1]['maxTemp'] = argList[4].get()
    argList[1]['maxCurr'] = argList[5].get()
    return True

def pows_scope_chs(argList):
    argList[1]['pvinScopeCh'] = argList[4].get()
    argList[1]['vccScopeCh'] = argList[5].get()
    argList[1]['enScopeCh'] = argList[6].get()
    argList[1]['voutScopeCh'] = argList[7].get()
    argList[1]['pgoodScopeCh'] = argList[8].get()
    return True

def pows_custom_scope_ch(argList):
    argList[1]['customScopeCh'] = argList[9].get()
    argList[1]['customScopeLbl'] = argList[10].get()
    return True

def cs_gain(argList):
    argList[0]['csMin'] = argList[1].get()
    argList[0]['csTyp'] = argList[2].get()
    argList[0]['csMax'] = argList[3].get()
    return True

def cs_res(argList):
    argList[0]['csRes'] = argList[1].get()
    return True

def which_test201(argList):
    '''
    "Validate" partial options for test 2.01. It saves the value into ConfigMgr to be used when running test.
    :param argList: [
        self.whichTestFrame,
        ConfigMgr.testConditions201,
        validate.which_test201,
        self.varPeakRise,
        self.varDTeValley,
        self.varFswTon,
        self.varPeakFall,
        self.varDTFall,
        self.varDTFallMan,
        self.varJitter,
        self.varJitterMan,
        self.varDTeValleyMan,
    ]
    :return: True (it accepts any value always)
    '''
    argList[1]['peakRise'] == argList[3].get()
    argList[1]['dTeValley'] == argList[4].get()
    argList[1]['fswTon'] == argList[5].get()
    argList[1]['peakFall'] == argList[6].get()
    argList[1]['dTFall'] == argList[7].get()
    argList[1]['dTFallMan'] == argList[8].get()
    argList[1]['jitter'] == argList[9].get()
    argList[1]['jitterMan'] == argList[10].get()
    argList[1]['dTeValleyMan'] == argList[11].get()
    return True

def inductor(argList):
    '''
    :param argList: [ConfigMgr.testConditions101, self.varInductorVal ]
    '''
    argList[0]['inductorVal'] = argList[1].get()
    return True

def background_color(argList):
    '''
    :param argList: [ConfigMgr.testConditions101, self.varBackgndColor]
    '''
    argList[0]['background'] = argList[1].get()
    return True

def run(argList):
    argList[0]['run3'] = argList[3].get()
    if argList[3].get() == "1":
        argList[1].set("0")
        argList[2].set("0")
    argList[0]['run2'] = argList[2].get()
    argList[0]['run1'] = argList[1].get()
    return True

def sw_only_fall_dt(argList):
    '''
    :param argList: [
            self.swOnlyFrame,
            ConfigMgr.testConditions101,
            self.varRefLevel,
            self.varCrossNum,
        ]
    :return: True
    '''
    argList[1]['refLevel'] = argList[2].get()
    argList[1]['crossNum'] = argList[3].get()
    return True

def snap_opt(argList):
    '''
    :param argList: [
                    ConfigMgr.testConditions101,
                    self.snapZoomShot,
                    self.loadTimeOff,
                    self.loadRest,
                    self.snapPause,
                    ]
    :return: None
    '''
    argList[0]['snapScopeZoom'] = argList[1].get()
    argList[0]['loadRest'] = argList[2].get()
    argList[0]['loadRestTime'] = argList[3].get()
    argList[0]['snapPause'] = argList[4].get()