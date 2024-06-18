from guiFiles.configmgr import ConfigMgr

#region INSTRUMENTS DRIVERS
from pygrabber.dshow_graph import FilterGraph
from pverifyDrivers import (
    dongle,
    cameras,
    powsup,
    scope,
    purescope,
    load,
    fgen,
    thermchamber,
    daq,
)
#endregion

def dongles():
    d = None
    if eval(ConfigMgr.instr['dongleOnOff']):
        model = ConfigMgr.instr['dongleModel']
        if model in ['Acadia']:
            d = dongle.Acadia()
        elif model in ['Sierra']:
            d = dongle.Sierra()
        elif model in ['Pollino', 'Sequoia']:
            d = dongle.Pollino()
        elif model in ['McKinley']:
            d = dongle.McKinley()
    return d

def cam():
    if eval(ConfigMgr.instr['camOnOff']):
        graph = FilterGraph()
        cam = cameras.FlirCam()
        return cam

def oscilloscope():
    sc = None
    if eval(ConfigMgr.instr['scopeOnOff']):
        scopeModel = ConfigMgr.instr['scopeModel']
        addr = ConfigMgr.instr['scopeAddr']
        if scopeModel in ['TDS5104B', 'MSO5204B', 'MSO5204']:
            sc = scope.TekScope(addr, Simulate=False, Reset=True)
        # elif (scopeModel in ['MSO56', 'MSO54', 'MSO58', 'MSO58LP']): # THIS DRIVER IS NOT WORKING PROPERLY FOR NOW
        #     sc = scope.TEK_MSO5X(addr, Simulate=False, Reset=True)
        elif (scopeModel in ['MSO56', 'MSO54', 'MSO58', 'MSO58LP', 'MSO58B']):
            sc = scope.TEK_MSO5XB(addr, Simulate=False, Reset=True)
        elif (scopeModel in ['MSO4104', 'MDO3104']):
            sc = scope.Tkdpo4k(addr, Simulate=False, Reset=True)
        elif (scopeModel in ['DPO7104', 'DPO7104C']):
            sc = scope.Tkdpo7k(addr, Simulate=False, Reset=True)
        else:
            print('Oscilloscope not defined.')
        if sc is not None:
            sc.Arm(Continuous=True)
    return sc

def pure_scope():
    sc = None
    if eval(ConfigMgr.instr['scopeOnOff']):
        scopeModel = ConfigMgr.instr['scopeModel']
        addr = ConfigMgr.instr['scopeAddr']
        if scopeModel in ['TDS5104B', 'MSO5204B', 'MSO5204']:
            sc = purescope.TekScope(addr, Simulate=False, Reset=True)
        # elif (scopeModel in ['MSO56', 'MSO54', 'MSO58', 'MSO58LP']): # THIS DRIVER IS NOT WORKING PROPERLY FOR NOW
        #     sc = purescope.TEK_MSO5X(addr, Simulate=False, Reset=True)
        elif (scopeModel in ['MSO56', 'MSO54', 'MSO58', 'MSO58LP', 'MSO58B']):
            sc = purescope.TEK_MSO5XB(addr, Simulate=False, Reset=True)
        elif (scopeModel in ['MSO4104', 'MDO3104']):
            sc = purescope.Tkdpo4k(addr, Simulate=False, Reset=True)
        elif (scopeModel in ['DPO7104', 'DPO7104C']):
            sc = purescope.Tkdpo7k(addr, Simulate=False, Reset=True)
        else:
            print('Oscilloscope not defined.')
    return sc

def eload():
    ld = None
    if eval(ConfigMgr.instr['loadOnOff']):
        model = ConfigMgr.instr['loadModel']
        address = ConfigMgr.instr['loadAddr']
        if model in ['Chroma 6312A', 'Chroma 6312/14']:
            ld = load.Chroma631x(address)
        elif model in ['Chroma 63600']:
            ld = load.Chroma63600(address)
        elif model in ['XBL Series']:
            ld = load.XBLSeries(address)
        elif model in ['AMETEK PLA800']:
            ld = load.AMETEKPLA800(address)
        if ld is not None:
            ld.chIdx = eval(ConfigMgr.instr['loadChannel'][-1])
    return ld

def therm_cham():
    therm = None
    if eval(ConfigMgr.instr['thermOnOff']):
        model = ConfigMgr.instr['thermModel']
        address = ConfigMgr.instr['thermAddr']
        if model in ['F4T']:
            therm = thermchamber.F4t(ip=address)
    return therm

def vin():
    _vin = None
    if eval(ConfigMgr.instr['vinPSOnOff']):
        model = ConfigMgr.instr['vinPSModel']
        addr = ConfigMgr.instr['vinPSAddr']
        if model in ['Xantrex XHR 33-33']:
            _vin = powsup.Xantrex_XHR_Series(addr)
            if _vin is not None:
                _vin.ch = _vin.GetChannel(Index=1)
        elif model in ['Gw Instek PSU Series', 'Keithley 2260B', 'BK Precision 9205', 'BK Precision 9117', 'BK Precision 9115']:
            _vin = powsup.Keith_2260B(addr)
            if _vin is not None:
                _vin.ch = _vin.GetChannel(Index=1)
        elif model in ['HP 603X']:
            _vin = powsup.HP603X(addr)
            if _vin is not None:
                _vin.ch = _vin.GetChannel(Index=1)
        elif model in ['TDK-Lambda']:
            _vin = powsup.TdkLambda(addr)
            if _vin is not None:
                _vin.ch = _vin.GetChannel(Index=1)
        elif model in ['Keysight N6705C']:
            _vin = powsup.N6705C(addr)
            if _vin is not None:
                try:
                    _vin.ch = _vin.GetChannel(Index=eval(ConfigMgr.instr['vinCh']))
                except:
                    print('failed to Create Channel Object for Vin')
        else:
            print('Vin Power Supply not initialized. Some Models are still not added on this version.')
    return _vin

def fgen():
    fg = None
    if eval(ConfigMgr.instr['fgenOnOff']):
        addr = ConfigMgr.instr['fgenAddr']
        model = ConfigMgr.instr['fgenModel']
        if model in ['Agilent 33250A']:
            fg = fgen.Hp33120a(Address=addr, Simulate=False, Reset=True)
        elif model in ['AFG 3022C']:
            fg = fgen.Tkafg3k(Address=addr, Simulate=False, Reset=True)
    return fg

def keith():
    _keith = None
    if eval(ConfigMgr.instr['keithOnOff']):
        addr = ConfigMgr.instr['keithAddr']
        model = ConfigMgr.instr['keithModel']
        if model in ['Keithley 2700']:
            _keith = daq.Keithley2700(Address=addr, Simulate=False, Reset=True)
        elif model in ['Keithley DAQ6510']:
            _keith = daq.Keithley6510(Address=addr, Simulate=False, Reset=True)
        elif model in ['Keithley 3706A']:
            _keith = daq.Keithley3700(Address=addr, Simulate=False, Reset=True)
        elif model in ['Agilent 34970A']:
            _keith = daq.Ag34970(Address=addr, Simulate=False, Reset=True)
    return _keith

def vcc():
    _vcc = None
    if eval(ConfigMgr.instr['vccPSOnOff']):
        addr = ConfigMgr.instr['vccPSAddr']
        model = ConfigMgr.instr['vccPSModel']
        if model in ['E3631A']:
            _vcc = powsup.AgE36xx(Address=addr, Simulate=False, Reset=False)
            if _vcc is not None:
                _vcc.vdrvCh = _vcc.GetChannel(Index=eval(ConfigMgr.instr['vcc5VCh']))
        elif model in ['BK Precision 9130B']:
            _vcc = powsup.BK_9130B(Address=addr, Simulate=False, Reset=False)
            if _vcc is not None:
                _vcc.vdrvCh = _vcc.GetChannel(Index=eval(ConfigMgr.instr['vcc5VCh']))
        elif model in ['E3642A']:
            _vcc = powsup.AgE36xx(Address=addr, Simulate=False, Reset=False)
            if _vcc is not None:
                _vcc.vdrvCh = _vcc.GetChannel(Index=1)
        elif model in ['Keysight N6705C']:
            _vcc = powsup.N6705C(Address=addr, Simulate=False, Reset=False)
            if _vcc is not None:
                _vcc.vdrvCh = _vcc.GetChannel(Index=eval(ConfigMgr.instr['vcc5VCh']))
        elif model in ['GW PST 3202']:
            _vcc = powsup.GWPST(Address=addr, Simulate=False, Reset=False)
            if _vcc is not None:
                _vcc.vdrvCh = _vcc.GetChannel(Index=eval(ConfigMgr.instr['vcc5VCh']))
        elif model in ['PWS4000 Series']:
            _vcc = powsup.PWS4000Series(Address=addr, Simulate=False, Reset=False)
            if _vcc is not None:
                _vcc.vdrvCh = _vcc.GetChannel(Index=1)
    return _vcc

def enable():
    _en = None
    if eval(ConfigMgr.instr['enPSOnOff']):
        addr = ConfigMgr.instr['enPSAddr']
        model = ConfigMgr.instr['enPSModel']
        if model in ['E3631A']:
            _en = powsup.AgE36xx(Address=addr, Simulate=False, Reset=False)
            if _en is not None:
                _en.ch = _en.GetChannel(Index=eval(ConfigMgr.instr['enPSCh']))
        elif model in ['BK Precision 9130B']:
            _en = powsup.BK_9130B(Address=addr, Simulate=False, Reset=False)
            if _en is not None:
                _en.ch = _en.GetChannel(Index=eval(ConfigMgr.instr['enPSCh']))
        elif model in ['E3642A']:
            _en = powsup.AgE36xx(Address=addr, Simulate=False, Reset=False)
            if _en is not None:
                _en.ch = _en.GetChannel(Index=1)
        elif model in ['Keysight N6705C']:
            _en = powsup.N6705C(Address=addr, Simulate=False, Reset=False)
            if _en is not None:
                _en.ch = _en.GetChannel(Index=eval(ConfigMgr.instr['enPSCh']))
        elif model in ['GW PST 3202']:
            _en = powsup.GWPST(Address=addr, Simulate=False, Reset=False)
            if _en is not None:
                _en.ch = _en.GetChannel(Index=eval(ConfigMgr.instr['enPSCh']))
        elif model in ['PWS4000 Series']:
            _en = powsup.PWS4000Series(Address=addr, Simulate=False, Reset=False)
            if _en is not None:
                _en.ch = _en.GetChannel(Index=1)
    return _en

def custom():
    _cus = None
    if eval(ConfigMgr.instr['customPSOnOff']):
        addr = ConfigMgr.instr['customPSAddr']
        model = ConfigMgr.instr['customPSModel']
        if model in ['E3631A']:
            _cus = powsup.AgE36xx(Address=addr, Simulate=False, Reset=False)
            if _cus is not None:
                _cus.ch = _cus.GetChannel(Index=eval(ConfigMgr.instr['customPSCh']))
        elif model in ['BK Precision 9130B']:
            _cus = powsup.BK_9130B(Address=addr, Simulate=False, Reset=False)
            if _cus is not None:
                _cus.ch = _cus.GetChannel(Index=eval(ConfigMgr.instr['customPSCh']))
        elif model in ['E3642A']:
            _cus = powsup.AgE36xx(Address=addr, Simulate=False, Reset=False)
            if _cus is not None:
                _cus.ch = _cus.GetChannel(Index=1)
        elif model in ['Keysight N6705C']:
            _cus = powsup.N6705C(Address=addr, Simulate=False, Reset=False)
            if _cus is not None:
                _cus.ch = _cus.GetChannel(Index=eval(ConfigMgr.instr['customPSCh']))
        elif model in ['GW PST 3202']:
            _cus = powsup.GWPST(Address=addr, Simulate=False, Reset=False)
            if _cus is not None:
                _cus.ch = _cus.GetChannel(Index=eval(ConfigMgr.instr['customPSCh']))
        elif model in ['PWS4000 Series']:
            _cus = powsup.PWS4000Series(Address=addr, Simulate=False, Reset=False)
            if _cus is not None:
                _cus.ch = _cus.GetChannel(Index=1)
    return _cus

def prebias():
    _bias = None
    if eval(ConfigMgr.instr['biasPSOnOff']):
        addr = ConfigMgr.instr['biasPSAddr']
        model = ConfigMgr.instr['biasPSModel']
        if model in ['E3631A']:
            _bias = powsup.AgE36xx(Address=addr, Simulate=False, Reset=False)
            if _bias is not None:
                _bias.ch = _bias.GetChannel(Index=eval(ConfigMgr.instr['biasPSCh']))
        elif model in ['BK Precision 9130B']:
            _bias = powsup.BK_9130B(Address=addr, Simulate=False, Reset=False)
            if _bias is not None:
                _bias.ch = _bias.GetChannel(Index=eval(ConfigMgr.instr['biasPSCh']))
        elif model in ['E3642A']:
            _bias = powsup.AgE36xx(Address=addr, Simulate=False, Reset=False)
            if _bias is not None:
                _bias.ch = _bias.GetChannel(Index=1)
        elif model in ['Keysight N6705C']:
            _bias = powsup.N6705C(Address=addr, Simulate=False, Reset=False)
            if _bias is not None:
                _bias.ch = _bias.GetChannel(Index=eval(ConfigMgr.instr['biasPSCh']))
        elif model in ['GW PST 3202']:
            _bias = powsup.GWPST(Address=addr, Simulate=False, Reset=False)
            if _bias is not None:
                _bias.ch = _bias.GetChannel(Index=eval(ConfigMgr.instr['biasPSCh']))
        elif model in ['PWS4000 Series']:
            _bias = powsup.PWS4000Series(Address=addr, Simulate=False, Reset=False)
            if _bias is not None:
                _bias.ch = _bias.GetChannel(Index=1)
    return _bias
