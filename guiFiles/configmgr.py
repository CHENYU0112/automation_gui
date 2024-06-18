from configparser import ConfigParser
import atexit


class ConfigMgr(ConfigParser):
    instr = {
        'scopeOnOff': '0',
        'scopeModel': 'MSO56',
        'scopeAddr': 'USB0::0x0699::0x0522::B020140::INSTR',
        'scopeVertScaleCh1': '2',
        'scopeVertScaleCh2': '0.1',
        'scopeVertScaleCh3': '5',
        'scopeVertScaleCh4': '5',
        'scopeVertScaleCh5': '1',
        'scopeVertScaleCh6': '1',
        'scopeVertScaleCh7': '1',
        'scopeVertScaleCh8': '1',
        'scopeTermCh1': '1.0e+6',
        'scopeTermCh2': '1.0e+6',
        'scopeTermCh3': '1.0e+6',
        'scopeTermCh4': '1.0e+6',
        'scopeTermCh5': '1.0e+6',
        'scopeTermCh6': '1.0e+6',
        'scopeTermCh7': '1.0e+6',
        'scopeTermCh8': '1.0e+6',
        'scopeHorScale': '200e-9',
        'scopeVertPosCh1': '2',
        'scopeVertPosCh2': '0',
        'scopeVertPosCh3': '-3',
        'scopeVertPosCh4': '-3',
        'scopeVertPosCh5': '0',
        'scopeVertPosCh6': '0',
        'scopeVertPosCh7': '0',
        'scopeVertPosCh8': '0',
        'scopeAttnCh1': '1',
        'scopeAttnCh2': '1',
        'scopeAttnCh3': '1',
        'scopeAttnCh4': '1',
        'scopeAttnCh5': '1',
        'scopeAttnCh6': '1',
        'scopeAttnCh7': '1',
        'scopeAttnCh8': '1',
        'loadOnOff': '0',
        'loadModel': 'Chroma 6312A',
        'loadChannel': 'CH1',
        'loadAddr': 'GPIB0::1::INSTR',
        'thermOnOff': '0',
        'thermModel': 'F4T',
        'thermAddr': '10.46.92.10',
        'vinPSOnOff': '0',
        'vinPSModel': 'Xantrex XHR 33-33',
        'vinPSAddr': 'GPIB0::2::INSTR',
        'vinPSCh': '1',
        'vinCh': '1',
        'fgenOnOff': '0',
        'fgenModel': 'Agilent 33250A',
        'fgenChannel': 'CH1',
        'fgenAddr': 'GPIB0::10::INSTR',
        'keithOnOff': '0',
        'keithModel': '2700',
        'keithAddr': 'GPIB0::16::INSTR',
        'vccPSOnOff': '0',
        'vccPSModel': '',
        'vccPSAddr': '',
        'vcc5VCh': '1',
        'enPSOnOff': '0',
        'enPSModel': '',
        'enPSAddr': '',
        'enPSCh': '2',
        'customPSOnOff': '0',
        'customPSModel': '',
        'customPSAddr': '',
        'customPSCh': '2',
        'biasPSOnOff': '0',
        'biasPSModel': 'Xantrex XHR 33-33',
        'biasPSAddr': 'GPIB0::2::INSTR',
        'biasPSCh': '1',
        'camOnOff': '0',
        'flirCam': 'FLIR',
        'dongleOnOff': '0',
        'dongleModel': 'Acadia',
        'polBoardFamily': 'Coronado',
        'polBoardModel': 'TDA38825',
        'polBoardFamilyCustom': '',
        'polBoardSilicRev': '',
        'psBoardFamily': 'Custom',
        'psBoardModel': '',
        'psBoardFamilyCustom': '',
        'psBoardSilicRev': '',
        'bom': 'Insert comment here',
        'bodeOnOff': '0',
        'bodeFreq1': '1000',
        'bodeFreq2': '',
        'bodeFreq3': '',
        'bodeFreq4': '',
        'bodeFreq5': '',
        'bodeDbm1': '-19',
        'bodeDbm2': '',
        'bodeDbm3': '',
        'bodeDbm4': '',
        'bodeDbm5': '',
    }

    tempSteps = {
        '1' : '-40',
        '2' : '25',
        '3' : '125',
        '4' : '',
        '5' : '',
        '6' : '',
    }

    testConditions101 = {
        'test101' : '0',
        'fallImg' : '0',
        'persis' : '1',
        'scopePwmCh' : '1',
        'scopeGateLCh' : '3',
        'scopeSwCh' : '4',
        'scopeVdshCh' : '2',
        'currOpt': 'incr',
        'startCurr' : '0',
        'endCurr' : '60',
        'stepCurr' : '5',
        'startCurr2': '0',
        'endCurr2': '60',
        'stepCurr2': '5',
        'pvinOpt': 'incr',
        'startPVin' : '12',
        'endPVin' : '12',
        'stepPVin' : '12',
        'PVin1' : '12',
        'PVin2' : '',
        'PVin3' : '',
        'PVin4' : '',
        'PVin5' : '',
        'PVin6' : '',
        'pvinOpt' : 'incr',
        'startVout' : '1.8',
        'endVout' : '1.8',
        'stepVout' : '0.1',
        'voutOpt' : 'incr',
        'vout1' : '0.8',
        'vout2' : '',
        'vout3' : '',
        'vout4' : '',
        'vout5' : '',
        'vout6' : '',
        'fswOpt': 'incr',
        'startFsw' : '600',
        'endFsw' : '1500',
        'stepFsw' : '100',
        'fsw1': '600',
        'fsw2': '',
        'fsw3': '',
        'fsw4': '',
        'fsw5': '',
        'fsw6': '',
        'fsw7': '',
        'fsw8': '',
        'fsw9': '',
        'soak' : '12',
        'vccLdo': '0',
        'vccExt': '1',
        'startVcc': '3',
        'endVcc': '3.3',
        'stepVcc': '0.1',
        'kiin' : '1',
        'kimon' : '2',
        'kvout' : '3',
        'ktmon' : '4',
        'kvin' : '5',
        'kiout' : '6',
        'kioutr' : '0.0001885',
        'kiinr' : '0.0001982',
        'kvcc' : '7',
        'kicc' : '8',
        'kiccr' : '0.001999',
        'kven' : '18',
        'kien' : '',
        'kienr' : '200',
        'kvoutsw' : '9',
        'coolDOpt' : 'temp',
        'enOpt': 'External',
        'en1': '3.3',
        'en2': '',
        'en3': '',
        'enPvin': '',
        'biasOpt': '0',
        'bias1': '0.5',
        'bias2': '',
        'bias3': '',
        'inductorVal': '',
        'background': 'white',
        'run1': '1',
        'run2': '0',
        'run3': '0',
        'modeDEM': '0',
        'modeFCCM': '0',
        'refLevel' : '-0.2',
        'crossNum' : '1',
        'snapScopeZoom': '1',
        'loadRest': '1',
        'loadRestTime': '10',
        'snapPause': '0',
    }

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigMgr, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def __init__(self):
        super(ConfigMgr, self).__init__()
        self.filePath = 'guiFiles/config.ini'
        self.read(self.filePath)
        self.update_dict()
        atexit.register(self.cleanup)

    def update_dict(self):
        # instr
        self.instr['scopeOnOff'] = self.get('instr', 'scopeonoff')
        self.instr['scopeModel'] = self.get('instr', 'scopeModel')
        self.instr['scopeAddr'] = self.get('instr', 'scopeAddr')
        self.instr['scopeVertScaleCh1'] = self.get('instr', 'scopeVertScaleCh1')
        self.instr['scopeVertScaleCh2'] = self.get('instr', 'scopeVertScaleCh2')
        self.instr['scopeVertScaleCh3'] = self.get('instr', 'scopeVertScaleCh3')
        self.instr['scopeVertScaleCh4'] = self.get('instr', 'scopeVertScaleCh4')
        self.instr['scopeVertScaleCh5'] = self.get('instr', 'scopeVertScaleCh5')
        self.instr['scopeVertScaleCh6'] = self.get('instr', 'scopeVertScaleCh6')
        self.instr['scopeVertScaleCh7'] = self.get('instr', 'scopeVertScaleCh7')
        self.instr['scopeVertScaleCh8'] = self.get('instr', 'scopeVertScaleCh8')
        self.instr['scopeTermCh1'] = self.get('instr', 'scopeTermCh1')
        self.instr['scopeTermCh2'] = self.get('instr', 'scopeTermCh2')
        self.instr['scopeTermCh3'] = self.get('instr', 'scopeTermCh3')
        self.instr['scopeTermCh4'] = self.get('instr', 'scopeTermCh4')
        self.instr['scopeTermCh5'] = self.get('instr', 'scopeTermCh5')
        self.instr['scopeTermCh6'] = self.get('instr', 'scopeTermCh6')
        self.instr['scopeTermCh7'] = self.get('instr', 'scopeTermCh7')
        self.instr['scopeTermCh8'] = self.get('instr', 'scopeTermCh8')
        self.instr['scopeHorScale'] = self.get('instr', 'scopeHorScale')
        self.instr['scopeVertPosCh1'] = self.get('instr', 'scopeVertPosCh1')
        self.instr['scopeVertPosCh2'] = self.get('instr', 'scopeVertPosCh2')
        self.instr['scopeVertPosCh3'] = self.get('instr', 'scopeVertPosCh3')
        self.instr['scopeVertPosCh4'] = self.get('instr', 'scopeVertPosCh4')
        self.instr['scopeVertPosCh5'] = self.get('instr', 'scopeVertPosCh5')
        self.instr['scopeVertPosCh6'] = self.get('instr', 'scopeVertPosCh6')
        self.instr['scopeVertPosCh7'] = self.get('instr', 'scopeVertPosCh7')
        self.instr['scopeVertPosCh8'] = self.get('instr', 'scopeVertPosCh8')
        self.instr['scopeAttnCh1'] = self.get('instr', 'scopeAttnCh1')
        self.instr['scopeAttnCh2'] = self.get('instr', 'scopeAttnCh2')
        self.instr['scopeAttnCh3'] = self.get('instr', 'scopeAttnCh3')
        self.instr['scopeAttnCh4'] = self.get('instr', 'scopeAttnCh4')
        self.instr['scopeAttnCh5'] = self.get('instr', 'scopeAttnCh5')
        self.instr['scopeAttnCh6'] = self.get('instr', 'scopeAttnCh6')
        self.instr['scopeAttnCh7'] = self.get('instr', 'scopeAttnCh7')
        self.instr['scopeAttnCh8'] = self.get('instr', 'scopeAttnCh8')
        self.instr['loadOnOff'] = self.get('instr', 'loadOnOff')
        self.instr['loadModel'] = self.get('instr', 'loadModel')
        self.instr['loadChannel'] = self.get('instr', 'loadChannel')
        self.instr['loadAddr'] = self.get('instr', 'loadAddr')
        self.instr['thermOnOff'] = self.get('instr', 'thermOnOff')
        self.instr['thermModel'] = self.get('instr', 'thermModel')
        self.instr['thermAddr'] = self.get('instr', 'thermAddr')
        self.instr['vinPSOnOff'] = self.get('instr', 'vinPSOnOff')
        self.instr['vinPSModel'] = self.get('instr', 'vinPSModel')
        self.instr['vinPSAddr'] = self.get('instr', 'vinPSAddr')
        self.instr['vinPSCh'] = self.get('instr', 'vinPSCh')
        self.instr['fgenOnOff'] = self.get('instr', 'fgenOnOff')
        self.instr['fgenModel'] = self.get('instr', 'fgenModel')
        self.instr['fgenChannel'] = self.get('instr', 'fgenChannel')
        self.instr['fgenAddr'] = self.get('instr', 'fgenAddr')
        self.instr['keithOnOff'] = self.get('instr', 'keithOnOff')
        self.instr['keithModel'] = self.get('instr', 'keithModel')
        self.instr['keithAddr'] = self.get('instr', 'keithAddr')
        self.instr['vccPSOnOff'] = self.get('instr', 'vccPSOnOff')
        self.instr['vccPSModel'] = self.get('instr', 'vccPSModel')
        self.instr['vccPSAddr'] = self.get('instr', 'vccPSAddr')
        self.instr['vcc5VCh'] = self.get('instr', 'vcc5VCh')
        self.instr['enPSOnOff'] = self.get('instr', 'enPSOnOff')
        self.instr['enPSModel'] = self.get('instr', 'enPSModel')
        self.instr['enPSAddr'] = self.get('instr', 'enPSAddr')
        self.instr['enPSCh'] = self.get('instr', 'enPSCh')
        self.instr['customPSOnOff'] = self.get('instr', 'customPSOnOff')
        self.instr['customPSModel'] = self.get('instr', 'customPSModel')
        self.instr['customPSAddr'] = self.get('instr', 'customPSAddr')
        self.instr['customPSCh'] = self.get('instr', 'customPSCh')
        self.instr['biasPSOnOff'] = self.get('instr', 'biasPSOnOff')
        self.instr['biasPSModel'] = self.get('instr', 'biasPSModel')
        self.instr['biasPSAddr'] = self.get('instr', 'biasPSAddr')
        self.instr['biasPSCh'] = self.get('instr', 'biasPSCh')
        self.instr['camOnOff'] = self.get('instr', 'camOnOff')
        self.instr['flirCam'] = self.get('instr', 'flirCam')
        self.instr['dongleOnOff'] = self.get('instr', 'dongleOnOff')
        self.instr['dongleModel'] = self.get('instr', 'dongleModel')
        self.instr['bom'] = self.get('instr', 'bom')
        self.instr['bodeOnOff'] = self.get('instr', 'bodeOnOff')
        self.instr['dongleOnOff'] = self.get('instr', 'dongleOnOff')
        self.instr['dongleModel'] = self.get('instr', 'dongleModel')
        # tempSteps
        self.tempSteps['1'] = self.get('tempSteps', '1')
        self.tempSteps['2'] = self.get('tempSteps', '2')
        self.tempSteps['3'] = self.get('tempSteps', '3')
        self.tempSteps['4'] = self.get('tempSteps', '4')
        self.tempSteps['5'] = self.get('tempSteps', '5')
        self.tempSteps['6'] = self.get('tempSteps', '6')
        # testConditions101
        self.testConditions101['test101'] = self.get('testConditions101', 'test101')
        self.testConditions101['fallImg'] = self.get('testConditions101', 'fallImg')
        self.testConditions101['persis'] = self.get('testConditions101', 'persis')
        self.testConditions101['scopePwmCh'] = self.get('testConditions101', 'scopePwmCh')
        self.testConditions101['scopeGateLCh'] = self.get('testConditions101', 'scopeGateLCh')
        self.testConditions101['scopeSwCh'] = self.get('testConditions101', 'scopeSwCh')
        self.testConditions101['scopeVdshCh'] = self.get('testConditions101', 'scopeVdshCh')
        self.testConditions101['startCurr'] = self.get('testConditions101', 'startCurr')
        self.testConditions101['endCurr'] = self.get('testConditions101', 'endCurr')
        self.testConditions101['stepCurr'] = self.get('testConditions101', 'stepCurr')
        self.testConditions101['startCurr2'] = self.get('testConditions101', 'startCurr2')
        self.testConditions101['endCurr2'] = self.get('testConditions101', 'endCurr2')
        self.testConditions101['stepCurr2'] = self.get('testConditions101', 'stepCurr2')
        self.testConditions101['startPVin'] = self.get('testConditions101', 'startPVin')
        self.testConditions101['endPVin'] = self.get('testConditions101', 'endPVin')
        self.testConditions101['stepPVin'] = self.get('testConditions101', 'stepPVin')
        self.testConditions101['startVout'] = self.get('testConditions101', 'startVout')
        self.testConditions101['endVout'] = self.get('testConditions101', 'endVout')
        self.testConditions101['stepVout'] = self.get('testConditions101', 'stepVout')
        self.testConditions101['startFsw'] = self.get('testConditions101', 'startFsw')
        self.testConditions101['endFsw'] = self.get('testConditions101', 'endFsw')
        self.testConditions101['stepFsw'] = self.get('testConditions101', 'stepFsw')
        self.testConditions101['soak'] = self.get('testConditions101', 'soak')
        self.testConditions101['startVcc'] = self.get('testConditions101', 'startVcc')
        self.testConditions101['endVcc'] = self.get('testConditions101', 'endVcc')
        self.testConditions101['stepVcc'] = self.get('testConditions101', 'stepVcc')
        self.testConditions101['kiin'] = self.get('testConditions101', 'kiin')
        self.testConditions101['kimon'] = self.get('testConditions101', 'kimon')
        self.testConditions101['kvout'] = self.get('testConditions101', 'kvout')
        self.testConditions101['ktmon'] = self.get('testConditions101', 'ktmon')
        self.testConditions101['kvin'] = self.get('testConditions101', 'kvin')
        self.testConditions101['kiout'] = self.get('testConditions101', 'kiout')
        self.testConditions101['kioutr'] = self.get('testConditions101', 'kioutr')
        self.testConditions101['kiinr'] = self.get('testConditions101', 'kiinr')
        self.testConditions101['kvcc'] = self.get('testConditions101', 'kvcc')
        self.testConditions101['kicc'] = self.get('testConditions101', 'kicc')
        self.testConditions101['kiccr'] = self.get('testConditions101', 'kiccr')
        self.testConditions101['kven'] = self.get('testConditions101', 'kven')
        self.testConditions101['kien'] = self.get('testConditions101', 'kien')
        self.testConditions101['kienr'] = self.get('testConditions101', 'kienr')
        self.testConditions101['kvoutsw'] = self.get('testConditions101', 'kvoutsw')
        self.testConditions101['coolDOpt'] = self.get('testConditions101', 'coolDOpt')
        self.testConditions101['enOpt'] = self.get('testConditions101', 'enOpt')
        self.testConditions101['en1'] = self.get('testConditions101', 'en1')
        self.testConditions101['en2'] = self.get('testConditions101', 'en2')
        self.testConditions101['en3'] = self.get('testConditions101', 'en3')
        self.testConditions101['enPvin'] = self.get('testConditions101', 'enPvin')
        self.testConditions101['biasOpt'] = self.get('testConditions101', 'biasOpt')
        self.testConditions101['bias1'] = self.get('testConditions101', 'bias1')
        self.testConditions101['bias2'] = self.get('testConditions101', 'bias2')
        self.testConditions101['bias3'] = self.get('testConditions101', 'bias3')
        self.testConditions101['inductorVal'] = self.get('testConditions101', 'inductorVal')
        self.testConditions101['background'] = self.get('testConditions101', 'background')
        self.testConditions101['run1'] = self.get('testConditions101', 'run1')
        self.testConditions101['run2'] = self.get('testConditions101', 'run2')
        self.testConditions101['run3'] = self.get('testConditions101', 'run3')
        self.testConditions101['modeDEM'] = self.get('testConditions101', 'modeDEM')
        self.testConditions101['modeFCCM'] = self.get('testConditions101', 'modeFCCM')
        self.testConditions101['refLevel'] = self.get('testConditions101', 'refLevel')
        self.testConditions101['crossNum'] = self.get('testConditions101', 'crossNum')
        self.testConditions101['snapScopeZoom'] = self.get('testConditions101', 'snapScopeZoom')
        self.testConditions101['loadRest'] = self.get('testConditions101', 'loadRest')
        self.testConditions101['loadRestTime'] = self.get('testConditions101', 'loadRestTime')
        self.testConditions101['snapPause'] = self.get('testConditions101', 'snapPause')

    def save_config(self, filePath):
        for key in self.instr:
            self.set('instr', str(key), str(self.instr[key]))
        for key in self.tempSteps:
            self.set('tempSteps', str(key), str(self.tempSteps[key]))
        for key in self.testConditions101:
            self.set('testConditions101', str(key), str(self.testConditions101[key]))

        with open(filePath, 'w') as f:
            self.write(f)

    def cleanup(self):
        self.save_config('guiFiles/config.ini')

