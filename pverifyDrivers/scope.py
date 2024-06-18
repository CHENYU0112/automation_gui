##############################################
#                DESCRIPTION                 #
##############################################
# Driver Library created to work with FFU GUI#
# This will make use of Ifx-PyVerify project #
# as a base driver and complement it with    #
# new functions using raw SCPI commands.     #
##############################################
#                  AUTHOR                    #
##############################################
# @Author: Johann Karl Muller                #
# @Email: JohannKarl.Muller@infineon.com     #
#                                            #
# @Date(yyyy-mm-dd): 2022-01-28              #
##############################################
#            EDITING INSTRUCTIONS            #
##############################################
# 1. Make sure every class refers to one     #
# type or one family of oscilloscopes.       #
# 2. The class can have extra methods not    #
# included on previous classes. If That new  #
# method is considered essential, please     #
# add it to all previous classes             #
##############################################
##############################################

#region - IFX-PYVERIFY IMPORTS
from pyvisa.resources.messagebased import MessageBasedResource as _MessageBasedResource
from pverify.drivers.SimplifiedLabInstruments.SimpleIviScope import SimpleIviScope
from pverify.drivers.Scope.tkmso5x.IIviScope import IIviScope as MSOiviScope
from pverify.drivers.Scope.tkdpo4k.IIviScope import IIviScope as DPO4kiviScope
from pverify.drivers.Scope.Tkdpo2k3k4k.IIviScope import IIviScope as Tkdpo2k3k4k
from pverify.drivers.Scope.tkdpo7k.IIviScope import IIviScope as DPO7kiviScope
from pverify.drivers.Scope.TekScope.IIviScope import IIviScope as TEKSCOPE
from pverify.postproc.waveform import Waveform
# from pverify.drivers.Scope.TekScope.IIviScopeTriggerEdge import
#endregion

#region IMPORTS
import pyvisa as _pyvisa
import tkinter
from time import sleep
import numpy as np
from struct import unpack
import matplotlib.pyplot as plt
#endregion

class ScopeBase:
    '''
    Base class for Oscilloscopes that will activate pyVerify SimpleScope object, pyvisa object and common functions
    that work the same in all Oscilloscope classes.
    '''

    def __init__(self, callback=None):
        if callback is not None:
            super(ScopeBase, self).__init__(callback)

    def __del__(self):
        try:
            self.pyvisa_instr.clear()
            self.pyvisa_instr.close()
        except:
            pass

    def is_num(self, num):
        try:
            int(num)
            return True
        except:
            try:
                float(num)
                return True
            except:
                return False

    def visa_from_simple_instrument(self, addr):
        """
        This method returns a VISA resource instance that shares the session with the supplied IIviInstrument instance.
        """
        rm = _pyvisa.ResourceManager()
        _pyvisa_instr = rm.open_resource(addr)
        return _pyvisa_instr

    def adjust_waveform_cursor(self, Cursor, ChannelIndex, Target, Err, Edge, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        Lower = kwargs['Lower'] if 'Lower' in kwargs else 0
        Higher = kwargs['Higher'] if 'Higher' in kwargs else 0
        StartPos = kwargs['StartPos'] if 'StartPos' in kwargs else 0.5
        positionsList = list()
        ch = self.GetChannel(ChannelIndex)
        wav = ch.GetProbeWaveform(Timeout=5)
        length = len(wav.data)
        if Edge.lower() == 'fall':
            pos = length - 1
        else:
            pos = int(length * StartPos)
        startPos = int(length * StartPos)
        horscale = self.get_horscale()
        horscale = float(horscale[0])
        scalePerPoints = horscale * 10 / length
        smallest_err = 99999.0
        smallest_pos = ''
        highPos = pos
        highRead = wav.data[pos]
        lowPos = pos
        lowRead = wav.data[pos]
        while (1):
            cur_read = wav.data[pos]
            if pos in positionsList:
                newPos = (smallest_pos - startPos) * scalePerPoints
                self.set_cursor_pos(Cursor, newPos, View=View, CursorN=CursorN)
                return
            positionsList.append(pos)
            err = abs(cur_read - Target)
            if err < smallest_err:
                smallest_err = err
                smallest_pos = pos
            if (Higher) and (cur_read > highRead):
                highRead = cur_read
                highPos = pos
            if (Lower) and (cur_read < lowRead):
                lowRead = cur_read
                lowPos = pos
            if (err <= Err) and (not Higher) and (not Lower):
                newPos = (smallest_pos - startPos) * scalePerPoints
                self.set_cursor_pos(Cursor, newPos, View=View, CursorN=CursorN)
                return
            if Lower or Higher:
                pos += 1
                if(pos >= length):
                    if Higher:
                        newPos = (highPos - startPos) * scalePerPoints
                        self.set_cursor_pos(Cursor, newPos, View=View, CursorN=CursorN)
                    elif Lower:
                        newPos = (lowPos - startPos) * scalePerPoints
                        self.set_cursor_pos(Cursor, newPos, View=View, CursorN=CursorN)
                    return
            elif Edge.lower() == 'rise':
                if cur_read < Target:
                    pos += 1
                    if pos >= length:
                        newPos = (smallest_pos - startPos) * scalePerPoints
                        self.set_cursor_pos(Cursor, newPos, View=View, CursorN=CursorN)
                        return
                else:
                    pos -= 1
            elif Edge.lower() == 'fall':
                if cur_read < Target:
                    pos -= 1
                    if pos < startPos:
                        newPos = (smallest_pos - startPos) * scalePerPoints
                        self.set_cursor_pos(Cursor, newPos, View=View, CursorN=CursorN)
                        return
                else:
                    pos += 1

class TEK_MSO5X(ScopeBase, SimpleIviScope):
    '''
    Supported Instruments
        MSO54, MSO56, MSO58, MSO58LP, MSO64, MSO44, MSO46, LDP_64, MSO64B, MSO66B, MSO68B
    '''

    ID = 'MSO5x'

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        super(TEK_MSO5X, self).__init__(MSOiviScope())
        self.Initialize(ResourceName=Address, IdQuery=True, Reset=reset, OptionString="simulate=" + str(simulate))
        self.pyvisa_instr = self.visa_from_simple_instrument(Address)

    def _write(self, command, *args, **kwargs):
        self.lld.dllwrap.WriteInstrData(writeBuffer=command)

    def _query(self, command, *args, **kwargs):
        self.lld.dllwrap.WriteInstrData(writeBuffer=command)
        data = self.lld.dllwrap.ReadInstrData(numBytes=1024)
        return data

    def horscale(self, scale, *args, **kwargs):
        """
        set the horizontal scale
        unit: n = "e-9"; u = "e-6"; m = "e-3"
        2n equals to 2e-9
        """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(scale).strip()
        if s[-1] == 's':
            s = s.rstrip('s')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write('HOR:MODE MAN')
        self._write('HOR:MODE:SAMPLER 1E37')
        sr = float(self._query('HOR:MODE:SAMPLER?'))
        rl = sr * float(s) * 10
        self._write(f'HOR:MODE:RECO {rl}')
        hs = float(self._query('HOR:MODE:SCALE?'))
        sleep(0.5)
        while (hs != float(s)) and (abs(hs - float(s)) > 0.1e-9):
            sr = float(self._query('HOR:MODE:SAMPLER?'))
            sr = sr / 2
            self._write(f'HOR:MODE:SAMPLER {sr}')
            rl = sr * float(s) * 10
            self._write(f'HOR:MODE:RECO {rl}')
            hs = float(self._query('HOR:MODE:SCALE?'))
            sleep(0.5)

    def verpos(self, Channel, Pos, *args, **kwargs):
        """ set the vertical position """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(Pos).strip()
        if s[-1] == 'v':
            s = s.rstrip('v')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write("CH" + str(Channel) + ":position " + str(s))

    def display_overlay(self, *args, **kwargs):
        '''
        Activate display overlay
        :param Waveview: (optional) standard value is 1
        '''
        wavev = kwargs['Waveview'] if 'Waveview' in kwargs else 1
        self._write('DIS:WAVEV' + str(wavev) + ':VIEWS OVE')

    def waveview_grid_type(self, type, *args, **kwargs):
        '''
        :param type: { MOVEABLE | FIXED }
        :return: None
        '''
        self._write(f'DIS:WAVEV:GRIDTYPE {type}')

    def set_channel_label(self, ChannelIndex=1, Label='', Xpos="5" , Ypos="4", *args, **kwargs):
        self._write('CH' + str(ChannelIndex) + ':label:name "' + str(Label) + '"')
        self._write('CH' + str(ChannelIndex) + ':label:xpos ' + str(Xpos))
        self._write('CH' + str(ChannelIndex) + ':label:ypos ' + str(Ypos))

    def set_screen_text(self, text="", text_no=1, xpos="", ypos="", *args, **kwargs):
        FontSize = kwargs['FontSize'] if 'FontSize' in kwargs else 10
        self._write(f'CALLOUTS:CALLOUT{text_no}:TEXT "{text}"')
        self._write(f'CALLOUTS:CALLOUT{text_no}:DISPLAYPOS:X {xpos}')
        self._write(f'CALLOUTS:CALLOUT{text_no}:DISPLAYPOS:Y {ypos}')
        self._write(f'CALLOUTS:CALLOUT{text_no}:COLOR "#FFFFFF"')
        self._write(f'CALLOUTS:CALLOUT{text_no}:FONT:BOLD 1')
        self._write(f'CALLOUTS:CALLOUT{text_no}:FONT:SIZE {FontSize}')
        self._write(f'CALLOUTS:CALLOUT{text_no} ON')

    def change_screentext(self, text='', txt_no=1, *args, **kwargs):
        self._write('CALLOUTS:CALLOUT' + str(txt_no) + ':TEXT "' + str(text) + '"')

    def set_measurement(self, MeasureIndex=1, MeasureType='FREQUENCY', State='ON', Source=1, Expand=False, *args, **kwargs):
        '''
        Set and configure measurements
        :param MeasureIndex: Index in the Measurement list 1 - ...
        :type MeasureIndex: int
        :param MeasureType: { ACCOMMONMODE | ACRMS | AMPLITUDE | AREA | BASE | BITAMPLITUDE | BITHIGH | BITLOW
                            | BURSTWIDTH | COMMONMODE | DATARATE | DCD | DDJ | DDRAOS | DDRAOSPERTCK | DDRAOSPERUI
                            | DDRAUS | DDRAUSPERTCK | DDRAUSPERUI | DDRHOLDDIFF | DDRSETUPDIFF | DDRTCHABS
                            | DDRTCHAVERAGE | DDRTCLABS | DDRTCLAVERAGE | DDRTERRMN | DDRTJITCC | DDRTJITDUTY
                            | DDRTJITPER | DDRTPST | DDRTRPRE | DDRTWPRE | DDRVIXAC | DDRTDQSCK | DELAY | DJ
                            | DJDIRAC | DPMOVERSHOOT | DPMUNDERSHOOT | DPMRIPPLE | DPMTURNOFFTIME | DPMTURNONTIME
                            | EYEHIGH | EYELOW | FALLSLEWRATE | FALLTIME | FREQUENCY | F2 | F4 | F8 | HIGH | HEIGHT
                            | HEIGHTBER | HIGHTIME | HOLD | IMDAPOWERQUALITY | IMDAHARMONICS | IMDAINPUTVOLTAGE
                            | IMDAINPUTCURRENT | IMDAINPUTPOWER | IMDAPHASORDIAGRAM | IMDAEFFICIENCY | IMDALINERIPPLE
                            | IMDASWITCHRIPPLE | JITTERSUMMARY | J2 | J9 | LOW | LOWTIME | MAXIMUM | MEAN | MINIMUM
                            | NDUTY | NPERIOD | NPJ | NOVERSHOOT | NWIDTH | PDUTTY | PERIOD | PHASE | PHASENOISE | PJ
                            | PK2PK | POVERSHOOT | PWIDTH | QFACTOR | RISESLEWRATE | RISETIME | RJ | RJDIRAC | RMS
                            | SRJ | SSCFREQDEV | SSCMODRATE | SETUP | SKEW | TIE | TIMEOUTSIDELEVEL | TJBER | TNTRATIO
                            | TOP | UNITINTERVAL | VDIFFXOVR | WIDTH | WIDTHBER }
        :type MeasureType: str
        :param State: ON or OFF
        :type State: str
        :param Source: Channel source of measurement
        :type Source: int
        '''
        if State.upper() == 'ON':
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':SOU CH' + str(Source) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':TYP ' + str(MeasureType) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')
            if Expand:
                self._write('MEASU:MEAS' + str(MeasureIndex) + ':DISPL:ENAB ON;')
            else:
                self._write('MEASU:MEAS' + str(MeasureIndex) + ':DISPL:ENAB OFF;')
        else:
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')

    def config_delay_measurement(self, MeasureIndex=1, Source1='3', Source2='4', Mid1='1.0', Mid2='1.0', Edge1='RISE', Edge2='FALL', *args, **kwargs):
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':TYP DELAY;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOURCE1 ' + str(Source1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOURCE2 ' + str(Source2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:METH PERC;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:ABS:RISEM ' + str(Mid1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:ABS:FALLM ' + str(Mid2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE1 ' + str(Edge1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE2 ' + str(Edge2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:DIRE FORW;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOU1:SIGT PULSE;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':STATE ON;')

    def config_top_base_method(self, source=1, method='AUTO', *args, **kwargs):
        '''
        :param source: Channel number <int>
        :param method: { AUTO | MINMax | MEANhistogram | MODEhistogram | EYEhistogram }
        :return: None
        '''
        self._write(f'MEASU:CH{source}:REFL:BASET {method}')

    def set_reflevel_method(self, source=1, method='PERC', *args, **kwargs):
        '''
        Select the Method used to calculate reference levels for the measurement.
        :param source: Channel number <int>
        :param method: { PERCent | ABSolute }
        :return: None
        '''
        self._write(f'MEASU:CH{source}:REFL:METH {method}')

    def set_reflevel_percent_type(self, source=1, type='TENN', *args, **kwargs):
        '''
        :param source: Channel number <int>
        :param type: { TENNinety | TWENtyeighty | CUSTom }
        :return: None
        '''
        self._write(f'MEASU:CH{source}:REFL:PERC:TYPE {type}')

    def hi_resolution(self, *args, **kwargs):
        self._write('ACQ:MOD HIR')

    def vertical_cursor_on(self, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':STATE ON')

    def vertical_cursor_off(self, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':STATE OFF')

    def set_cursor_function(self, func, *args, **kwargs):
        '''
        Options are: OFF | HBA | VBA | SCREEN | WAVEFORM
        '''
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':FUNC ' + str(func))

    def set_cursor_pos(self, cursor, pos, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        if cursor == 1:
            cursor = 'A'
        elif cursor == 2:
            cursor = 'B'
        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' +\
            str(CursorN) + ':WAVE:' + str(cursor) + 'POS ' + str(pos))

    def get_cursor_avpos(self, cursor, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        if cursor == 1:
            cursor = 'A'
        elif cursor == 2:
            cursor = 'B'
        try:
            return self._query(f'DIS:WAVEV{View}:CURS:CURSOR:WAVE:{cursor}VPOS?')
        except:
            print(
                'Error trying to get vpos of waveform cursor.\nMake sure your cursor value is either 1 | 2 | "A" | "B".')
            return 0

    def set_persistence(self, option, *args, **kwargs):
        '''
        :param option: { OFF | AUTO | INFPersist | INFInite | VARpersist | CLEAR }
        '''
        if self.is_num(option):
            self._write('DIS:PERS VAR')
            self._write(f'DIS:VAR {option}')
        else:
            self._write('DIS:PERS ' + str(option))

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def waveform_cursor_to_channel(self, cursor, ch, *args, **kwargs):
        '''
        This function changes to which wave the cursor is related.
        Syntax: waveform_cursor_to_channel(arg1, arg2)
            arg1: integer cursor number (usually 1 or 2)
            arg2: integer channel number to which the cursor will relate
        '''
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        if(cursor == 1):
            cursor = 'A'
        elif(cursor == 2):
            cursor = 'B'

        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':' + str(cursor) + 'SOU ' + 'CH' + str(ch))

    def cursor_split(self, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':SPLITMODE SPLIT')

    def reset_statistics(self, *args, **kwargs):
        self._write('MEASU:POPU:LIMIT:STATE ON')
        self._write('MEASU:POPU:LIMIT:VAL 1')
        self._write('MEASU:POPU:LIMIT:STATE OFF')

    def saveimage(self, Filename=None, *args, **kwargs):
        Background = kwargs['Background'] if 'Background' in kwargs else 'black'
        """ save the scope shoot image """
        if(Background.lower() == 'white'):
            self._write('DIS:COL INVERT')
        self._write('HARDC:PORT FILE')
        self._write('EXP:FORM PNG')
        self._write('HARDC:FILEN "C:/Temp.png"')
        self._write('SAVE:IMAGE "C:/Temp.png"')
        sleep(0.5)
        ldir = self._query('FILES:LDIR?')
        while 'Temp.png' not in ldir:
            ldir = self._query('FILES:LDIR?')
            sleep(0.5)
        self._write('FILESystem:READFile "C:/Temp.png"') #,GPIB
        sleep(0.5)
        data = self.pyvisa_instr.read_raw()
        img = bytearray(data)
        if Filename == None:
            tkinter.Tk().withdraw()
            Filename = tkinter.filedialog.asksaveasfilename(initialdir=self.data_dir, initialfile=self.imagefile)
        if Filename == '':
            return
        self.imagefile = Filename
        fn = open(Filename, 'wb')
        fn.write(img)
        fn.close()
        self._write(':FILESystem:DELEte "C:/Temp.png"')
        if(Background.lower() == 'white'):
            self._write('DIS:COL NORM')

    def get_val_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':VAL?')[0]

    def get_mean_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MEAN?')[0]

    def get_min_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MINI?')[0]

    def get_max_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MAX?')[0]

    def get_horscale(self, *args, **kwargs):
        """
        gets the horizontal scale
        """
        return self._query("HOR:SCA?")  # use "horizontal:scale instead of "horizontal:mode:scale

    def horizontal_delay(self, state='OFF', time=0, *args, **kwargs):
        if state.upper() == 'OFF':
            self._write('HOR:DEL:MOD OFF')
        else:
            self._write('HOR:DEL:MOD ON')
            self._write('HOR:DEL:TIM ' + str(time))

    def horpos(self, value, *args, **kwargs):
        self._write('HOR:POS ' + str(value))

    def horizontal_mode(self, mode='AUTO', *args, **kwargs):
        self._write('HOR:MODE ' + str(mode))

    def horizontal_sample_rate(self, value=5e+6, *args, **kwargs):
        self._write('HOR:MODE:SAMPLER ' + str(value))

    def get_delta_t(self, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        delta = self._query('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':VBA:DELT?')
        return delta[0]

    def set_attenuation(self, ch, value, *args, **kwargs):
        self._write(f'CH{ch}:PROBEF:EXTA {value}')

    def set_termination(self, ch, value, *args, **kwargs):
        '''
        :param ch: (int) Oscilloscope Channel to be changed
        :param value: { 50.0 | 1e+6 }
        :return: None
        '''
        self._write(f'CH{ch}:TER {value}')

    def set_persistence(self, option, *args, **kwargs):
        '''
        :param value: { OFF | CLEAR | AUTO | INFPersist | VARpersist | INFInite }
        '''
        self._write('DIS:PERS ' + str(option))

    def set_acquisition_mode(self, value, *args, **kwargs):
        '''
        :param value: { SAMple | PEAKdetect | HIRes | AVErage | ENVelope }
        '''
        self._write('ACQ:MOD ' + str(value))

    def set_fast_acq(self, state, *args, **kwargs):
        self._write('ACQ:FASTA:STATE ' + str(state))

    def set_acq_num(self, num, *args, **kwargs):
        self._write(f'ACQ:SEQ:NUMSEQ {num}')
        self._write(f'ACQ:STOPA SEQ')
        self._write(f'ACQ:STATE RUN')

    def get_acq_num(self):
        return self._query('ACQ:NUMAC?')

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")

    def set_record_length(self, value, *args, **kwargs):
        self._write('HOR:RECO ' + str(value))

    def set_vertical_scale(self, ch, value, *args, **kwargs):
        self._write('CH' + str(ch) + ':SCA ' + str(value))

    def trigger_mode(self, opt, *args, **kwargs):
        '''
        :param opt: { AUTO | NORMal }
        '''
        self._write('TRIG:A:MOD ' + str(opt))

    def probe_autozero(self, ch=1, *args, **kwargs):
        self._write(f'CH{ch}:PRO:AUTOZ EXEC')

    def get_vertical_scale(self, ch, *args, **kwargs):
        return self._query('CH' + str(ch) + ':SCAle?')[0]

    def get_verpos(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POSition?')[0]

    def get_trigger(self, *args, **kwargs):
        ch = kwargs['channel'] if 'channel' in kwargs else '1'
        return self._query(f'TRIG:A:LEV:CH{ch}?')[0]

    def set_trigger(self, ch=None, level=None, slope=None, coupling=None, *args, **kwargs):
        if ch is None:
            print('set_trigger require channel index for this scope model')
            return
        if ch is not None:
            self._write(f'TRIG:A:EDGE:SOU CH{ch}')
        if level is not None:
            self._write(f'TRIG:A:LEV:CH{ch} {level}')
        if slope is not None:
            self._write(f'TRIG:A:EDGE:SLO {slope}')
        if coupling is not None:
            self._write(f'TRIG:A:EDGE:COUP {coupling}')

    def delete_measurement(self, meas, *args, **kwargs):
        self._write(f'MEASU:DEL "MEAS{meas}"')

    def set_ch_offset(self, ch, offset, *args, **kwargs):
        self._write(f'CH{ch}:OFFS {offset}')

    def get_offset(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:OFFS?')[0]

    def get_position(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POS?')[0]

    def set_zoom_scale(self, ch=1, value=4e-6, *args, **kwargs):
        waveview = kwargs['waveview'] if 'waveview' in kwargs else 1
        self._write(f'DIS:WAVEV{waveview}:ZOOM:ZOOM{ch}:HOR:SCAL {value}')

    def set_zoom_pos(self, ch=1, value='50', *args, **kwargs):
        waveview = kwargs['waveview'] if 'waveview' in kwargs else 1
        self._write(f'DIS:WAVEV{waveview}:ZOOM:ZOOM{ch}:HOR:POS {value}')

    def zoom_mode(self, state='OFF', *args, **kwargs):
        waveview = kwargs['waveview'] if 'waveview' in kwargs else 1
        ch = kwargs['ch'] if 'ch' in kwargs else 1
        self._write(f'DIS:WAVEV{waveview}:ZOOM:ZOOM{ch}:STAT {state}')

class TEK_MSO5XB(ScopeBase):
    '''
        Supported Instruments
            MSO54, MSO56, MSO58, MSO58LP, MSO58B
        '''

    ID = 'MSO5xB'
    channel = None

    def __init__(self, Address, Reset=True, *args, **kwargs):
        super(TEK_MSO5XB, self).__init__(None)
        self.address = Address
        self.cmd = _pyvisa.ResourceManager().open_resource(Address)
        self.cmd.timeout = 5000
        self.cmd.chunk_size = 102400
        if Reset:
            self._write('*RST')

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, *args, **kwargs):
        data = self.cmd.query(command)
        return data

    def GetChannel(self, Index=1, *args, **kwargs):
        chObj = TEK_MSO5XB(Address=self.address, Reset=False)
        chObj.channel = Index
        return chObj

    def ProbeSetup(self, Coupling='DC', Bandwidth=None, Vrange=1, Offset=0, Position=0, Impedance=1e+6, Probe_Attn=1, *args, **kwargs):
        '''
        :param Coupling: { DC | AC | DCREJ }
        :param Bandwidth: Options might change from scope model and probe used
        :param Vrange: Vertical scale (10:1) when 10 is select it will set to 1V/div
        :param Offset:
        :param Position:
        :param Impedance: Also known as Termination { 50 | 1e+6 }
        :param Probe_Attn: examples 1x, 20x
        :return: None
        '''
        if self.channel is not None:
            self._write(f'CH{self.channel}:COUP {Coupling}')
            self._write(f'CH{self.channel}:TER {Impedance}')
            self._write(f'CH{self.channel}:PROBEF:EXTA {Probe_Attn}')
            self._write(f'CH{self.channel}:POS {Position}')
            if Bandwidth is not None:
                self._write(f'CH{self.channel}:BAN {Bandwidth}')
            self._write(f'CH{self.channel}:OFFS {Offset}')
            self._write(f'CH{self.channel}:SCA {float(Vrange)/10}')

    def Enable(self, state=True, *args, **kwargs):
        view = kwargs['View'] if 'View' in kwargs else 1
        if self.channel is not None:
            if state:
                self._write(f'DIS:WAVEV{view}:CH{self.channel}:STATE ON')
            else:
                self._write(f'DIS:WAVEV{view}:CH{self.channel}:STATE OFF')

    def Trigger_Edge(self, Level=1, Slope='RISE', Position=2, Coupling='DC', ChannelIndex=1, *args, **kwargs):
        # Position is not being used on this model
        letter = kwargs['letter'] if 'letter' in kwargs else 'A'
        self._write(f'TRIG:{letter}:EDGE:SOU CH{ChannelIndex}')
        self._write(f'TRIG:{letter}:EDGE:COUP {Coupling}')
        self._write(f'TRIG:{letter}:EDGE:SLO {Slope}')
        self._write(f'TRIG:{letter}:LEV:CH{ChannelIndex} {Level}')

    def Arm(self, state=True, *args, **kwargs):
        if state:
            self.run()
        else:
            self.stop()

    def GetProbeWaveform(self, Timeout=0.5, *args, **kwargs):
        if self.channel is not None:
            self.stop()
            acqState = self._query('ACQ:STATE?')
            recLen = self._query('HOR:RECO?')
            self._write(f'DAT:SOU CH{self.channel}')
            self._write('DAT:ENC SRI')
            self._write('WFMO:BYT_N 1')
            self._write('WFMO:BYT_Or LSB')
            yzero = float(self._query('WFMO:YZE?'))
            yOffset = float(self._query('WFMO:YOF?'))
            yMul = float(self._query('WFMO:YMU?'))
            xIncr = float(self._query('WFMO:XIN?'))
            xZero = float(self._query('WFMO:XZE?'))
            self._write('DAT:STAR 1')
            self._write(f'DAT:STOP {recLen}')
            self._write('CURV?')
            bytepts = self.cmd.read_raw()
            sleep(Timeout)
            startIndex = 2 + int(bytepts[1:2])
            waveformArray = bytepts[startIndex:-1]
            waveformArray = np.array(unpack("%sb" % (len(waveformArray)), waveformArray))
            data = (float(yMul) * (waveformArray - yOffset)) + yzero
            w = Waveform(
                time=np.arange(0, xIncr * len(data), xIncr)[:len(data)] + xZero,
                data=data,
            )
            return w

    def horscale(self, scale, *args, **kwargs):
        """
        set the horizontal scale
        unit: n = "e-9"; u = "e-6"; m = "e-3"
        2n equals to 2e-9
        """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(scale).strip()
        if s[-1] == 's':
            s = s.rstrip('s')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write('HOR:MODE MAN')
        self._write('HOR:MODE:SAMPLER 1E37')
        sr = float(self._query('HOR:MODE:SAMPLER?'))
        rl = sr * float(s) * 10
        self._write(f'HOR:MODE:RECO {rl}')
        hs = float(self._query('HOR:MODE:SCALE?'))
        sleep(0.5)
        while (hs != float(s)) and (abs(hs - float(s)) > 0.1e-9):
            sr = float(self._query('HOR:MODE:SAMPLER?'))
            sr = sr / 2
            self._write(f'HOR:MODE:SAMPLER {sr}')
            rl = sr * float(s) * 10
            self._write(f'HOR:MODE:RECO {rl}')
            hs = float(self._query('HOR:MODE:SCALE?'))
            sleep(0.5)

    def verpos(self, Channel, Pos, *args, **kwargs):
        """ set the vertical position """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(Pos).strip()
        if s[-1] == 'v':
            s = s.rstrip('v')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write("CH" + str(Channel) + ":position " + str(s))

    def display_overlay(self, *args, **kwargs):
        '''
        Activate display overlay
        :param Waveview: (optional) standard value is 1
        '''
        wavev = kwargs['Waveview'] if 'Waveview' in kwargs else 1
        self._write('DIS:WAVEV' + str(wavev) + ':VIEWS OVE')

    def waveview_grid_type(self, type, *args, **kwargs):
        '''
        :param type: { MOVEABLE | FIXED }
        :return: None
        '''
        self._write(f'DIS:WAVEV:GRIDTYPE {type}')

    def set_channel_label(self, ChannelIndex=1, Label='', Xpos="5", Ypos="4", *args, **kwargs):
        self._write('CH' + str(ChannelIndex) + ':label:name "' + str(Label) + '"')
        self._write('CH' + str(ChannelIndex) + ':label:xpos ' + str(Xpos))
        self._write('CH' + str(ChannelIndex) + ':label:ypos ' + str(Ypos))

    def set_screen_text(self, text="", text_no=1, xpos="", ypos="", *args, **kwargs):
        FontSize = kwargs['FontSize'] if 'FontSize' in kwargs else 10
        self._write(f'CALLOUTS:CALLOUT{text_no}:TEXT "{text}"')
        self._write(f'CALLOUTS:CALLOUT{text_no}:DISPLAYPOS:X {xpos}')
        self._write(f'CALLOUTS:CALLOUT{text_no}:DISPLAYPOS:Y {ypos}')
        self._write(f'CALLOUTS:CALLOUT{text_no}:COLOR "#FF0000"')
        self._write(f'CALLOUTS:CALLOUT{text_no}:FONT:BOLD 1')
        self._write(f'CALLOUTS:CALLOUT{text_no}:FONT:SIZE {FontSize}')
        self._write(f'CALLOUTS:CALLOUT{text_no} ON')

    def change_screentext(self, text='', txt_no=1, *args, **kwargs):
        self._write('CALLOUTS:CALLOUT' + str(txt_no) + ':TEXT "' + str(text) + '"')

    def set_measurement(self, MeasureIndex=1, MeasureType='FREQUENCY', State='ON', Source=1, Expand=False, *args, **kwargs):
        '''
        Set and configure measurements
        :param MeasureIndex: Index in the Measurement list 1 - ...
        :type MeasureIndex: int
        :param MeasureType: { ACCOMMONMODE | ACRMS | AMPLITUDE | AREA | BASE | BITAMPLITUDE | BITHIGH | BITLOW
                            | BURSTWIDTH | COMMONMODE | DATARATE | DCD | DDJ | DDRAOS | DDRAOSPERTCK | DDRAOSPERUI
                            | DDRAUS | DDRAUSPERTCK | DDRAUSPERUI | DDRHOLDDIFF | DDRSETUPDIFF | DDRTCHABS
                            | DDRTCHAVERAGE | DDRTCLABS | DDRTCLAVERAGE | DDRTERRMN | DDRTJITCC | DDRTJITDUTY
                            | DDRTJITPER | DDRTPST | DDRTRPRE | DDRTWPRE | DDRVIXAC | DDRTDQSCK | DELAY | DJ
                            | DJDIRAC | DPMOVERSHOOT | DPMUNDERSHOOT | DPMRIPPLE | DPMTURNOFFTIME | DPMTURNONTIME
                            | EYEHIGH | EYELOW | FALLSLEWRATE | FALLTIME | FREQUENCY | F2 | F4 | F8 | HIGH | HEIGHT
                            | HEIGHTBER | HIGHTIME | HOLD | IMDAPOWERQUALITY | IMDAHARMONICS | IMDAINPUTVOLTAGE
                            | IMDAINPUTCURRENT | IMDAINPUTPOWER | IMDAPHASORDIAGRAM | IMDAEFFICIENCY | IMDALINERIPPLE
                            | IMDASWITCHRIPPLE | JITTERSUMMARY | J2 | J9 | LOW | LOWTIME | MAXIMUM | MEAN | MINIMUM
                            | NDUTY | NPERIOD | NPJ | NOVERSHOOT | NWIDTH | PDUTTY | PERIOD | PHASE | PHASENOISE | PJ
                            | PK2PK | POVERSHOOT | PWIDTH | QFACTOR | RISESLEWRATE | RISETIME | RJ | RJDIRAC | RMS
                            | SRJ | SSCFREQDEV | SSCMODRATE | SETUP | SKEW | TIE | TIMEOUTSIDELEVEL | TJBER | TNTRATIO
                            | TOP | UNITINTERVAL | VDIFFXOVR | WIDTH | WIDTHBER }
        :type MeasureType: str
        :param State: ON or OFF
        :type State: str
        :param Source: Channel source of measurement
        :type Source: int
        '''
        if State.upper() == 'ON':
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':SOU CH' + str(Source) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':TYP ' + str(MeasureType) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')
            if Expand:
                self._write('MEASU:MEAS' + str(MeasureIndex) + ':DISPL:ENAB ON;')
            else:
                self._write('MEASU:MEAS' + str(MeasureIndex) + ':DISPL:ENAB OFF;')
        else:
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')

    def config_delay_measurement(self, MeasureIndex=1, Source1='3', Source2='4', Mid1='1.0', Mid2='1.0', Edge1='RISE',
                                 Edge2='FALL', *args, **kwargs):
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':TYP DELAY;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOURCE1 ' + str(Source1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOURCE2 ' + str(Source2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:METH PERC;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:ABS:RISEM ' + str(Mid1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:ABS:FALLM ' + str(Mid2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE1 ' + str(Edge1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE2 ' + str(Edge2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:DIRE FORW;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOU1:SIGT PULSE;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':STATE ON;')

    def config_top_base_method(self, source=1, method='AUTO', *args, **kwargs):
        '''
        :param source: Channel number <int>
        :param method: { AUTO | MINMax | MEANhistogram | MODEhistogram | EYEhistogram }
        :return: None
        '''
        self._write(f'MEASU:CH{source}:REFL:BASET {method}')

    def set_reflevel_method(self, source=1, method='PERC', *args, **kwargs):
        '''
        Select the Method used to calculate reference levels for the measurement.
        :param source: Channel number <int>
        :param method: { PERCent | ABSolute }
        :return: None
        '''
        self._write(f'MEASU:CH{source}:REFL:METH {method}')

    def set_reflevel_percent_type(self, source=1, type='TENN', *args, **kwargs):
        '''
        :param source: Channel number <int>
        :param type: { TENNinety | TWENtyeighty | CUSTom }
        :return: None
        '''
        self._write(f'MEASU:CH{source}:REFL:PERC:TYPE {type}')

    def hi_resolution(self, *args, **kwargs):
        self._write('ACQ:MOD HIR')

    def vertical_cursor_on(self, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':STATE ON')

    def vertical_cursor_off(self, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':STATE OFF')

    def set_cursor_function(self, func, *args, **kwargs):
        '''
        Options are: OFF | HBA | VBA | SCREEN | WAVEFORM
        '''
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':FUNC ' + str(func))

    def set_cursor_pos(self, cursor, pos, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        if cursor == 1:
            cursor = 'A'
        elif cursor == 2:
            cursor = 'B'
        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + \
                    str(CursorN) + ':WAVE:' + str(cursor) + 'POS ' + str(pos))

    def get_cursor_avpos(self, cursor, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        if cursor == 1:
            cursor = 'A'
        elif cursor == 2:
            cursor = 'B'
        try:
            return self._query(f'DIS:WAVEV{View}:CURS:CURSOR:WAVE:{cursor}VPOS?')
        except:
            print('Error trying to get vpos of waveform cursor.\nMake sure your cursor value is either 1 | 2 | "A" | "B".')
            return 0

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def waveform_cursor_to_channel(self, cursor, ch, *args, **kwargs):
        '''
        This function changes to which wave the cursor is related.
        Syntax: waveform_cursor_to_channel(arg1, arg2)
            arg1: integer cursor number (usually 1 or 2)
            arg2: integer channel number to which the cursor will relate
        '''
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        if (cursor == 1):
            cursor = 'A'
        elif (cursor == 2):
            cursor = 'B'

        self._write(
            'DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':' + str(cursor) + 'SOU ' + 'CH' + str(ch))

    def cursor_split(self, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        self._write('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':SPLITMODE SPLIT')

    def reset_statistics(self, *args, **kwargs):
        self._write('MEASU:POPU:LIMIT:STATE ON')
        self._write('MEASU:POPU:LIMIT:VAL 1')
        self._write('MEASU:POPU:LIMIT:STATE OFF')

    def saveimage(self, Filename=None, *args, **kwargs):
        Background = kwargs['Background'] if 'Background' in kwargs else 'black'
        """ save the scope shoot image """
        if (Background.lower() == 'white'):
            self._write('DIS:COL INVERT')
            self._write('SAV:IMAG:COMP INVE')
            sleep(0.35)
        self._write('HARDC:PORT FILE')
        self._write('EXP:FORM PNG')
        self._write('HARDC:FILEN "C:/Temp.png"')
        self._write('SAVE:IMAGE "C:/Temp.png"')
        sleep(0.5)
        ldir = self._query('FILES:LDIR?')
        while 'Temp.png' not in ldir:
            ldir = self._query('FILES:LDIR?')
            sleep(0.5)
        self._write('FILESystem:READFile "C:/Temp.png"')  # ,GPIB
        sleep(0.5)
        try:
            data = self.cmd.read_raw()
        except Exception as e:
            print(e)
            data = 0
        img = bytearray(data)
        if Filename is None:
            print('Filename cannot be None. saveimage failed.')
            if (Background.lower() == 'white'):
                self._write('DIS:COL NORM')
                self._write('SAV:IMAG:COMP NORM')
                sleep(0.5)
            return
        self.imagefile = Filename
        fn = open(Filename, 'wb')
        fn.write(img)
        fn.close()
        self._write(':FILESystem:DELEte "C:/Temp.png"')
        if (Background.lower() == 'white'):
            self._write('DIS:COL NORM')
            self._write('SAV:IMAG:COMP NORM')
            sleep(0.35)

    def get_val_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query(f'MEASU:MEAS{Index}:RESU:CURR:MEAN?')

    def get_mean_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query(f'MEASU:MEAS{Index}:RESU:ALLA:MEAN?')

    def get_min_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query(f'MEASU:MEAS{Index}:RESU:ALLA:MIN?')

    def get_max_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query(f'MEASU:MEAS{Index}:RESU:ALLA:MAX?')

    def get_horscale(self, *args, **kwargs):
        """
        gets the horizontal scale
        """
        return self._query("HOR:SCA?")  # use "horizontal:scale instead of "horizontal:mode:scale

    def horizontal_delay(self, state='OFF', time=0, *args, **kwargs):
        if state.upper() == 'OFF':
            self._write('HOR:DEL:MOD OFF')
        else:
            self._write('HOR:DEL:MOD ON')
            self._write('HOR:DEL:TIM ' + str(time))

    def horpos(self, value, *args, **kwargs):
        self._write('HOR:POS ' + str(value))

    def horizontal_mode(self, mode='AUTO', *args, **kwargs):
        self._write('HOR:MODE ' + str(mode))

    def horizontal_sample_rate(self, value=5e+6, *args, **kwargs):
        self._write('HOR:MODE:SAMPLER ' + str(value))

    def get_delta_t(self, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        delta = self._query('DIS:WAVEV' + str(View) + ':CURS:CURSOR' + str(CursorN) + ':VBA:DELT?')
        return delta

    def set_attenuation(self, ch, value, *args, **kwargs):
        self._write(f'CH{ch}:PROBEF:EXTA {value}')

    def set_termination(self, ch, value, *args, **kwargs):
        '''
        :param ch: (int) Oscilloscope Channel to be changed
        :param value: { 50.0 | 1e+6 }
        :return: None
        '''
        self._write(f'CH{ch}:TER {value}')

    def set_persistence(self, option, *args, **kwargs):
        '''
        if a value is passed in place of an option it will set to variable persistence and set it to that value
        :param option: { OFF | CLEAR | AUTO | INFPersist | VARpersist | INFInite | <value>}
        '''
        if self.is_num(option):
            if float(option) == 0:
                self._write('DIS:PERS OFF')
            else:
                self._write('DIS:PERS VAR')
                self._write(f'DIS:VAR {option}')
        else:
            self._write('DIS:PERS ' + str(option))

    def set_acquisition_mode(self, value, *args, **kwargs):
        '''
        :param value: { SAMple | PEAKdetect | HIRes | AVErage | ENVelope }
        '''
        self._write('ACQ:MOD ' + str(value))

    def set_fast_acq(self, state, *args, **kwargs):
        self._write('ACQ:FASTA:STATE ' + str(state))

    def set_acq_num(self, num, *args, **kwargs):
        self._write(f'ACQ:SEQ:NUMSEQ {num}')
        self._write(f'ACQ:STOPA SEQ')
        self._write(f'ACQ:STATE RUN')

    def get_acq_num(self):
        return self._query('ACQ:NUMAC?')

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")

    def set_record_length(self, value, *args, **kwargs):
        self._write('HOR:RECO ' + str(value))

    def set_vertical_scale(self, ch, value, *args, **kwargs):
        self._write('CH' + str(ch) + ':SCA ' + str(value))

    def trigger_mode(self, opt, *args, **kwargs):
        '''
        :param opt: { AUTO | NORMal }
        '''
        self._write('TRIG:A:MOD ' + str(opt))

    def probe_autozero(self, ch=1, *args, **kwargs):
        self._write(f'CH{ch}:PRO:AUTOZ EXEC')

    def get_vertical_scale(self, ch, *args, **kwargs):
        return self._query('CH' + str(ch) + ':SCAle?')

    def get_verpos(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POSition?')

    def get_trigger(self, *args, **kwargs):
        ch = kwargs['channel'] if 'channel' in kwargs else '1'
        return self._query(f'TRIG:A:LEV:CH{ch}?')

    def set_trigger(self, ch=None, level=None, slope=None, coupling=None, *args, **kwargs):
        if ch is None:
            print('set_trigger require channel index for this scope model')
            return
        if ch is not None:
            self._write(f'TRIG:A:EDGE:SOU CH{ch}')
        if level is not None:
            self._write(f'TRIG:A:LEV:CH{ch} {level}')
        if slope is not None:
            self._write(f'TRIG:A:EDGE:SLO {slope}')
        if coupling is not None:
            self._write(f'TRIG:A:EDGE:COUP {coupling}')

    def delete_measurement(self, meas, *args, **kwargs):
        self._write(f'MEASU:DEL "MEAS{meas}"')

    def set_ch_offset(self, ch, offset, *args, **kwargs):
        self._write(f'CH{ch}:OFFS {offset}')

    def get_offset(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:OFFS?')

    def get_position(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POS?')

    def set_zoom_scale(self, ch=1, value=4e-6, *args, **kwargs):
        waveview = kwargs['waveview'] if 'waveview' in kwargs else 1
        self._write(f'DIS:WAVEV{waveview}:ZOOM:ZOOM{ch}:HOR:SCAL {value}')

    def set_zoom_pos(self, ch=1, value='50', *args, **kwargs):
        waveview = kwargs['waveview'] if 'waveview' in kwargs else 1
        self._write(f'DIS:WAVEV{waveview}:ZOOM:ZOOM{ch}:HOR:POS {value}')

    def zoom_mode(self, state='OFF', *args, **kwargs):
        waveview = kwargs['waveview'] if 'waveview' in kwargs else 1
        ch = kwargs['ch'] if 'ch' in kwargs else 1
        self._write(f'DIS:WAVEV{waveview}:ZOOM:ZOOM{ch}:STAT {state}')

    def is_num(self, num):
        try:
            int(num)
            return True
        except:
            try:
                float(num)
                return True
            except:
                return False

class Tkdpo4k(ScopeBase, SimpleIviScope):
    '''
    Supported Instruments
        Tektronix DPO/MSO/MDO 2000,3000 and 4000 Series Oscilloscopes
        DPO3012, DPO3014, DPO3032, DPO3034, DPO3052, DPO3054, DPO4104, DPO4014B, DPO4032, DPO4034, DPO4034B, DPO4054,
        DPO4054B, DPO4102B, DPO4102B-L, DPO4104B, DPO4104B, MDO3012, MDO3014, MDO3022, MDO3024, MDO3032, MDO3034,
        MDO3052, MDO3054, MDO3102, MDO3104, MDO4014-3, MDO4014B-3, MDO4034-3, MDO4034B-3, MDO40543, MDO40546,
        MDO4054B-3, MDO4054B-6, MDO41043, MDO41046, MDO4104B-3, MDO4104B-6, MSO3012, MSO3014, MSO3032, MSO3034,
        MSO3052, MSO3054, MSO4014B, MSO4032, MSO4034, MSO4034B, MSO4054, MSO4054B, MSO4102B, MSO4102B-L, MSO4104, MSO4104B
    '''

    ID = '4k'

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        super(Tkdpo4k, self).__init__(DPO4kiviScope())
        self.Initialize(ResourceName=Address, IdQuery=True, Reset=reset, OptionString="simulate=" + str(simulate))
        self.pyvisa_instr = self.visa_from_simple_instrument(Address)

    def _write(self, command, *args, **kwargs):
        self.lld.dllwrap.WriteInstrData(writeBuffer=command)

    def _query(self, command, *args, **kwargs):
        self.lld.dllwrap.WriteInstrData(writeBuffer=command)
        data = self.lld.dllwrap.ReadInstrData(numBytes=1024)
        return data

    def horscale(self, scale, *args, **kwargs):
        """
        set the horizontal scale
        unit: n = "e-9"; u = "e-6"; m = "e-3"
        2n equals to 2e-9
        """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(scale).strip()
        if s[-1] == 's':
            s = s.rstrip('s')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write("HOR:SCA " + s)  # use "horizontal:scale instead of "horizontal:mode:scale

    def verpos(self, Channel, Pos, *args, **kwargs):
        """ set the vertical position """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(Pos).strip()
        if s[-1] == 'v':
            s = s.rstrip('v')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write("CH" + str(Channel) + ":position " + s)

    def display_overlay(self, *args, **kwargs):
        '''
        Not a function for these models
        Activate display overlay
        :param Waveview: (optional) standard value is 1
        '''
        pass

    def waveview_grid_type(self, type, *args, **kwargs):
        '''
        Not an option on this model
        :return: None
        '''
        pass

    def set_channel_label(self, ChannelIndex=1, Label='', Xpos="5" , Ypos="4", *args, **kwargs):
        self._write('CH' + str(ChannelIndex) + ':label "' + str(Label) + '"')

    def set_screen_text(self, text_no=1, text="", xpos="0", ypos="0", *args, **kwargs):
        self._write(f'MESS:STATE ON;')
        self._write(f'MESSage:BOX {20 + int(xpos)}, {18 + int(ypos)}')
        self._write(f'MESS:SHOW "{text}"')

    def change_screentext(self, txt_no=1, text='', *args, **kwargs):
        self._write('MESS:SHOW "' + str(text) + '";')

    def set_measurement(self, MeasureIndex=1, MeasureType='FREQUENCY', State='ON', Source=1, *args, **kwargs):
        '''
        Set and configure measurements
        :param MeasureIndex: Index in the Measurement list 1 - ...
        :type MeasureIndex: int
        :param MeasureType: { AMPLITUDE | AREA | BURST | CARea | CMEan | CRMs | DELay | FALL | FREQUENCY | HIGH | HITS
                            | LOW | MAXIMUM | MEAN | MEDian | MINIMUM | NDUTY | NEDGECount | NOVershoot | NPULSECount
                            | NWIdth | PEAKHits | PDUty | PEDGECount | PERIod | PHAse | PK2PK | POVershoot | PPULSECount
                            | PWIDTH | RISe | RMS | SIGMA1 | SIGMA2 | SIGMA3 | STDdev | WAVEFORMS }
        :type MeasureType: str
        :param State: ON or OFF
        :type State: str
        :param Source: Channel source of measurement
        :type Source: int
        '''
        if MeasureType.upper() == 'RISETIME':
            MeasureType = 'RISE'
        elif MeasureType.upper() == 'FALLTIME':
            MeasureType = 'FALL'
        elif MeasureType.upper() == 'PDUTTY':
            MeasureType = 'PDUTY'
        elif MeasureType.upper() == 'TOP':
            MeasureType = 'HIGH'
        elif MeasureType.upper() == 'BASE':
            MeasureType = 'LOW'

        typeList = [
            'AMPLITUDE', 'AREA', 'BURST', 'CAREA', 'CMEAN', 'CRMS', 'DELAY', 'FALL', 'FREQUENCY', 'HIGH', 'HITS', 'LOW',
            'MAXIMUM', 'MEAN', 'MEDIAN', 'MINIMUM', 'NDUTY', 'NEDGECOUNT', 'NOVERSHOOT', 'NPULSECOUNT', 'NWIDTH',
            'PEAKHITS', 'PDUTY', 'PEDGECOUNT', 'PERIOD', 'PHASE', 'PK2PK', 'POVERSHOOT', 'PPULSECOUNT', 'PWIDTH',
            'RISE', 'RMS', 'SIGMA1', 'SIGMA2', 'SIGMA3', 'STDDEV', 'WAVEFORMS',
        ]

        if MeasureType.upper() not in typeList:
            print(f'{MeasureType} is not defined on this Oscilloscope Model')
            return

        if State.upper() == 'ON':
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':SOU CH' + str(Source) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':TYP ' + str(MeasureType) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')
        else:
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')

    def config_delay_measurement(self, MeasureIndex=1, Source1='3', Source2='4', Mid1='1.0', Mid2='1.0', Edge1='RISE', Edge2='FALL', *args, **kwargs):
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':TYP DEL;')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':SOURCE1 ' + str(Source1) + ';')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':SOURCE2 ' + str(Source2) + ';')
        self._write('MEASU:REFL:METH PERC;')
        # self._write('MEASU:REFL:ABS:MID1 ' + str(Mid1) + ';')
        # self._write('MEASU:REFL:ABS:MID2 ' + str(Mid2) + ';')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE1 ' + str(Edge1) + ';')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE2 ' + str(Edge2) + ';')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':DEL:DIRE FORW;')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ON;')

    def config_top_base_method(self, source=1, method='AUTO', *args, **kwargs):
        '''
        This model works differently compared to more modern models. This will change method
        for all measurements, not just for top base.
        :param source: Channel number <int> NOT APPLICABLE TO THIS MODEL
        :param method: { AUTO | MINMax | HIStogram }
        :return: None
        '''
        self._write(f'MEASU:METH {method}')

    def set_reflevel_method(self, source=1, method='PERC', *args, **kwargs):
        '''
        Select the Method used to calculate reference levels for the measurement.
        :param source: Channel number <int> NOT APPLICABLE FOR THIS MODEL
        :param method: { PERCent | ABSolute }
        :return: None
        '''
        self._write(f'MEASU:REFL:METH {method}')

    def set_reflevel_percent_type(self, source=1, type='TENN', *args, **kwargs):
        '''
        The reflevel selected will be applied for all measurements
        :param source: Channel number <int> NOT APPLICABLE FOR THIS MODEL
        :param type: always CUSTOM (set "high" and "low" parameters)
        :return: None
        '''
        low = kwargs['low'] if 'low' in kwargs else 10
        high = kwargs['high'] if 'high' in kwargs else 90
        self._write(f'MEASU:REFL:PERC:HIGH {high}')
        self._write(f'MEASU:REFL:PERC:LOW {low}')

    def hi_resolution(self, *args, **kwargs):
        self._write('ACQ:MOD HIR')

    def vertical_cursor_on(self, *args, **kwargs):
        self._write('CURSor:STATE ON')

    def vertical_cursor_off(self, *args, **kwargs):
        self._write('Cursor:state off')

    def set_cursor_function(self, func, *args, **kwargs):
        '''
        Options are: OFF | HBA | VBA | SCREEN | WAVEFORM
        '''
        self._write('CURSor:FUNCtion ' + str(func))

    def set_cursor_pos(self, cursor, pos, *args, **kwargs):
        self._write('cursor:vbars:position' + str(cursor) + ' ' + str(pos))

    def get_cursor_avpos(self, cursor, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        if cursor == 1:
            cursor = 'A'
        elif cursor == 2:
            cursor = 'B'
        try:
            return self._query(f'DIS:WAVEV{View}:CURS:CURSOR:WAVE:{cursor}VPOS?')
        except:
            print('Error trying to get vpos of waveform cursor.\nMake sure your cursor value is either 1 | 2 | "A" | "B".')
            return 0

    def set_persistence(self, option, *args, **kwargs):
        '''
        :param option: { OFF | AUTO | INFPersist | INFInite | VARpersist | CLEAR }
        '''
        self._write('DIS:PERS ' + str(option))

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def waveform_cursor_to_channel(self, cursor, ch, *args, **kwargs):
        '''
        This function changes to which wave the cursor is related.
        Syntax: waveform_cursor_to_channel(arg1, arg2)
            arg1: integer cursor number (usually 1 or 2)
            arg2: integer channel number to which the cursor will relate
        '''
        self._write('CURS:SOUR CH' + str(ch))

    def cursor_split(self, *args, **kwargs):
        self._write('CURS:MOD IND')

    def reset_statistics(self, *args, **kwargs):
        self._write('MEASU:STATI RESET')

    def saveimage(self, Filename=None, *args, **kwargs):
        Background = kwargs['Background'] if 'Background' in kwargs else 'black'
        """ save the scope shoot image """
        self._write('USBD:CONF IMA')
        self._write('SAV:IMAG:FILEF PNG')
        if(Background.lower() == 'white'):
            self._write('SAV:IMAG:INKS ON')
        else:
            self._write('SAV:IMAG:INKS OFF')
        self._write('HARDC START')
        sleep(1)
        data = self.pyvisa_instr.read_raw()
        img = bytearray(data)
        if Filename == None:
            tkinter.Tk().withdraw()
            Filename = tkinter.filedialog.asksaveasfilename(initialdir=self.data_dir, initialfile=self.imagefile)
        if Filename == '':
            return
        self.imagefile = Filename
        with open(Filename, 'wb') as fn:
            fn.write(img)
        self._write('USBD:CONF USBT')

    def get_val_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query(f'MEASU:MEAS{Index}:VAL?')[0]

    def get_mean_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MEAN?')[0]

    def get_min_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MINIMUM?')[0]

    def get_max_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MAX?')[0]

    def get_horscale(self, *args, **kwargs):
        """
        gets the horizontal scale
        """
        return self._query("HOR:SCA?")  # use "horizontal:scale instead of "horizontal:mode:scale

    def horizontal_delay(self, state='OFF', time=0, *args, **kwargs):
        if state.upper() == 'OFF':
            self._write('HOR:DEL:MOD OFF')
        else:
            self._write('HOR:DEL:MOD ON')
            self._write('HOR:DEL:TIM ' + str(time))

    def horpos(self, value, *args, **kwargs):
        self._write('HOR:POS ' + str(value))

    def horizontal_mode(self, mode='AUTO', *args, **kwargs):
        # This model seems to not have this option
        pass

    def horizontal_sample_rate(self, value=5e+6, *args, **kwargs):
        self._write('HOR:SAMPLER ' + str(value))

    def get_delta_t(self, *args, **kwargs):
        delta = self._query('CURS:VBA:DELT?')
        return delta[0]

    def set_attenuation(self, ch, value, *args, **kwargs):
        self._write('CH' + str(ch) + ':PRO:GAIN ' + str(1.0/value))

    def set_termination(self, ch, value, *args, **kwargs):
        '''
        :param ch: (int) Oscilloscope Channel to be changed
        :param value: { 50.0 | 1e+6 }
        :return: None
        '''
        self._write(f'CH{ch}:TER {value}')

    def set_persistence(self, option, *args, **kwargs):
        '''
        :param value: { <number> | CLEAR | AUTO | MINImum | INFInite }
        '''
        if option.upper() == 'OFF':
            option = '-1'
        if option.upper() == 'INFP' or option.upper() == 'INFPERSIST':
            option = 'INFI'
        self._write('DIS:PERS ' + str(option))

    def set_acquisition_mode(self, value, *args, **kwargs):
        '''
        :param value: { SAMple | PEAKdetect | HIRes | AVErage | ENVelope }
        '''
        self._write('ACQ:MOD ' + str(value))

    def set_fast_acq(self, state, *args, **kwargs):
        # This model does not have fast acquisition.
        # This function uses the ENVELOPE mode to get similar result
        if state.upper() == 'ON':
            self.set_acquisition_mode('ENV')
        else:
            self.set_acquisition_mode('HIR')

    def set_acq_num(self, num, *args, **kwargs):
        '''
        These models don't have option to set number of acquisition. It can be set for envelope mode, but still it won't
        act like "sequence" where it will stop after the set number of acquisitions.
        :param num: any positive integer
        :return: None
        '''
        print('This scope model does not have option to set number of acquisition. Check Manual for more info.')

    def get_acq_num(self):
        return self._query('ACQ:NUMAC?')

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")

    def set_record_length(self, value, *args, **kwargs):
        self._write('HOR:RECO ' + str(value))

    def set_vertical_scale(self, ch, value, *args, **kwargs):
        self._write('CH' + str(ch) + ':SCA ' + str(value))

    def trigger_mode(self, opt, *args, **kwargs):
        '''
        :param opt: { AUTO | NORMal }
        '''
        self._write('TRIG:A:MOD ' + str(opt))

    def probe_autozero(self, ch=1, *args, **kwargs):
        self._write(f'CH{ch}:PRO:AUTOZ EXEC')

    def get_vertical_scale(self, ch, *args, **kwargs):
        return self._query('CH' + str(ch) + ':SCAle?')[0]

    def get_verpos(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POSition?')[0]

    def get_trigger(self, *args, **kwargs):
        return self._query('TRIG:A:LEV?')[0]

    def set_trigger(self, ch=None, level=None, slope=None, coupling=None, *args, **kwargs):
        if ch is not None:
            self._write(f'TRIG:A:EDGE:SOU CH{ch}')
        if level is not None:
            self._write(f'TRIG:A:LEV {level}')
        if slope is not None:
            self._write(f'TRIG:A:EDGE:SLO {slope}')
        if coupling is not None:
            self._write(f'TRIG:A:EDGE:COUP {coupling}')

    def delete_measurement(self, meas, *args, **kwargs):
        self._write(f'MEASU:MEAS{meas}:STATE OFF')

    def set_ch_offset(self, ch, offset, *args, **kwargs):
        self._write(f'CH{ch}:OFFS {offset}')

    def get_offset(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:OFFS?')[0]

    def get_position(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POS?')[0]

    def set_zoom_scale(self, ch=1, value=4e-6, *args, **kwargs):
        self._write(f'ZOO:ZOOM{ch}:SCA {value}')

    def set_zoom_pos(self, ch=1, value='50', *args, **kwargs):
        self._write(f'ZOO:ZOOM{ch}:POS {value}')

    def zoom_mode(self, state='OFF', *args, **kwargs):
        self._write(f'ZOO:MOD {state}')

class Tk2k3k4k(ScopeBase, SimpleIviScope):
    '''
    Supported Instruments
        Tektronix DPO/MSO/MDO 2000,3000 and 4000 Series Oscilloscopes
        DPO2002, DPO2002B, DPO2004B, DPO2012, DPO2012B, DPO2014, DPO2014B, DPO2022B, DPO2024, DPO2024B, MSO2002,
        MSO2002B, MSO2004B, MSO2012, MSO2012B, MSO2014, MSO2014B, MSO2022B, MSO2024, MSO2024B, DPO3012, DPO3014,
        DPO3032, DPO3034, DPO3052, DPO3054, MSO3012, MSO3014, MSO3032, MSO3034, MSO3054, MDO3012, MDO3014, MDO3022,
        MDO3024, MDO3032, MDO3034, MDO3052, MDO3054, MDO3102, MDO3104, DPO4014B, DPO4032, DPO4034, DPO4034B, DPO4054,
        DPO4054B, DPO4102B, DPO4102B-L, DPO4104, DPO4104B, DPO4104B-L, MSO4014B, MSO4032, MSO4034, MSO4034B, MSO4054,
        MSO4054B, MSO4102B, MSO4102B-L, MSO4104, MSO4104B, MSO4104B-L, MDO4014-3, MDO4014B-3, MDO4024C, MDO4034-3,
        MDO4034B-3, MDO4034C, MDO4054-3, MDO4054-6, MDO4054B-3, MDO4054B-6, MDO4054C, MDO4104-3, MDO4104-6, MDO4104B-3,
        MDO4104B-6, MDO4104C
    '''

    ID = '4k'

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        super(Tk2k3k4k, self).__init__(Tkdpo2k3k4k())
        self.Initialize(ResourceName=Address, IdQuery=True, Reset=reset, OptionString="simulate=" + str(simulate))
        self.cmd = _pyvisa.ResourceManager().open_resource(Address)

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, *args, **kwargs):
        data = self.cmd.query(command)
        return data

    def horscale(self, scale, *args, **kwargs):
        """
        set the horizontal scale
        unit: n = "e-9"; u = "e-6"; m = "e-3"
        2n equals to 2e-9
        """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(scale).strip()
        if s[-1] == 's':
            s = s.rstrip('s')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write("HOR:SCA " + s)  # use "horizontal:scale instead of "horizontal:mode:scale

    def verpos(self, Channel, Pos, *args, **kwargs):
        """ set the vertical position """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(Pos).strip()
        if s[-1] == 'v':
            s = s.rstrip('v')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write("CH" + str(Channel) + ":position " + s)

    def display_overlay(self, *args, **kwargs):
        '''
        Not a function for these models
        Activate display overlay
        :param Waveview: (optional) standard value is 1
        '''
        pass

    def waveview_grid_type(self, type, *args, **kwargs):
        '''
        Not an option on this model
        :return: None
        '''
        pass

    def set_channel_label(self, ChannelIndex=1, Label='', Xpos="5" , Ypos="4", *args, **kwargs):
        self._write('CH' + str(ChannelIndex) + ':label "' + str(Label) + '"')

    def set_screen_text(self, text_no=1, text="", xpos="0", ypos="0", *args, **kwargs):
        self._write(f'MESS:STATE ON;')
        self._write(f'MESSage:BOX {20 + int(xpos)}, {18 + int(ypos)}')
        self._write(f'MESS:SHOW "{text}"')

    def change_screentext(self, txt_no=1, text='', *args, **kwargs):
        self._write('MESS:SHOW "' + str(text) + '";')

    def set_measurement(self, MeasureIndex=1, MeasureType='FREQUENCY', State='ON', Source=1, *args, **kwargs):
        '''
        Set and configure measurements
        :param MeasureIndex: Index in the Measurement list 1 - ...
        :type MeasureIndex: int
        :param MeasureType: { AMPLITUDE | AREA | BURST | CARea | CMEan | CRMs | DELay | FALL | FREQUENCY | HIGH | HITS
                            | LOW | MAXIMUM | MEAN | MEDian | MINIMUM | NDUTY | NEDGECount | NOVershoot | NPULSECount
                            | NWIdth | PEAKHits | PDUty | PEDGECount | PERIod | PHAse | PK2PK | POVershoot | PPULSECount
                            | PWIDTH | RISe | RMS | SIGMA1 | SIGMA2 | SIGMA3 | STDdev | WAVEFORMS }
        :type MeasureType: str
        :param State: ON or OFF
        :type State: str
        :param Source: Channel source of measurement
        :type Source: int
        '''
        if MeasureType.upper() == 'RISETIME':
            MeasureType = 'RISE'
        elif MeasureType.upper() == 'FALLTIME':
            MeasureType = 'FALL'
        elif MeasureType.upper() == 'PDUTTY':
            MeasureType = 'PDUTY'

        typeList = [
            'AMPLITUDE', 'AREA', 'BURST', 'CAREA', 'CMEAN', 'CRMS', 'DELAY', 'FALL', 'FREQUENCY', 'HIGH', 'HITS', 'LOW',
            'MAXIMUM', 'MEAN', 'MEDIAN', 'MINIMUM', 'NDUTY', 'NEDGECOUNT', 'NOVERSHOOT', 'NPULSECOUNT', 'NWIDTH',
            'PEAKHITS', 'PDUTY', 'PEDGECOUNT', 'PERIOD', 'PHASE', 'PK2PK', 'POVERSHOOT', 'PPULSECOUNT', 'PWIDTH',
            'RISE', 'RMS', 'SIGMA1', 'SIGMA2', 'SIGMA3', 'STDDEV', 'WAVEFORMS',
        ]

        if MeasureType.upper() not in typeList:
            print(f'{MeasureType} is not defined on this Oscilloscope Model')
            return

        if State.upper() == 'ON':
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':SOU1 CH' + str(Source) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':TYP ' + str(MeasureType) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')
        else:
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')

    def config_delay_measurement(self, MeasureIndex=1, Source1='3', Source2='4', Mid1='1.0', Mid2='1.0', Edge1='RISE', Edge2='FALL', *args, **kwargs):
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':TYP DEL;')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':SOURCE1 ' + str(Source1) + ';')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':SOURCE2 ' + str(Source2) + ';')
        self._write('MEASU:REFL:METH PERC;')
        # self._write('MEASU:REFL:ABS:MID1 ' + str(Mid1) + ';')
        # self._write('MEASU:REFL:ABS:MID2 ' + str(Mid2) + ';')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE1 ' + str(Edge1) + ';')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE2 ' + str(Edge2) + ';')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':DEL:DIRE FORW;')
        self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ON;')

    def config_top_base_method(self, source=1, method='AUTO', *args, **kwargs):
        '''
        This model works differently compared to more modern models. This will change method
        for all measurements, not just for top base.
        :param source: Channel number <int> NOT APPLICABLE TO THIS MODEL
        :param method: { AUTO | MINMax | HIStogram }
        :return: None
        '''
        self._write(f'MEASU:METH {method}')

    def set_reflevel_method(self, source=1, method='PERC', *args, **kwargs):
        '''
        Select the Method used to calculate reference levels for the measurement.
        :param source: Channel number <int> NOT APPLICABLE FOR THIS MODEL
        :param method: { PERCent | ABSolute }
        :return: None
        '''
        self._write(f'MEASU:REFL:METH {method}')

    def set_reflevel_percent_type(self, source=1, type='TENN', *args, **kwargs):
        '''
        The reflevel selected will be applied for all measurements
        :param source: Channel number <int> NOT APPLICABLE FOR THIS MODEL
        :param type: always CUSTOM (set "high" and "low" parameters)
        :return: None
        '''
        low = kwargs['low'] if 'low' in kwargs else 10
        high = kwargs['high'] if 'high' in kwargs else 90
        self._write(f'MEASU:REFL:PERC:HIGH {high}')
        self._write(f'MEASU:REFL:PERC:LOW {low}')

    def hi_resolution(self, *args, **kwargs):
        self._write('ACQ:MOD HIR')

    def vertical_cursor_on(self, *args, **kwargs):
        self._write('CURSor:STATE ON')

    def vertical_cursor_off(self, *args, **kwargs):
        self._write('Cursor:state off')

    def set_cursor_function(self, func, *args, **kwargs):
        '''
        Options are: OFF | HBA | VBA | SCREEN | WAVEFORM
        '''
        self._write('CURSor:FUNCtion ' + str(func))

    def set_cursor_pos(self, cursor, pos, *args, **kwargs):
        self._write('cursor:vbars:position' + str(cursor) + ' ' + str(pos))

    def get_cursor_avpos(self, cursor, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        if cursor == 1:
            cursor = 'A'
        elif cursor == 2:
            cursor = 'B'
        try:
            return self._query(f'DIS:WAVEV{View}:CURS:CURSOR:WAVE:{cursor}VPOS?')
        except:
            print('Error trying to get vpos of waveform cursor.\nMake sure your cursor value is either 1 | 2 | "A" | "B".')
            return 0

    def set_persistence(self, option, *args, **kwargs):
        '''
        :param option: { OFF | AUTO | INFPersist | INFInite | VARpersist | CLEAR }
        '''
        self._write('DIS:PERS ' + str(option))

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def waveform_cursor_to_channel(self, cursor, ch, *args, **kwargs):
        '''
        This function changes to which wave the cursor is related.
        Syntax: waveform_cursor_to_channel(arg1, arg2)
            arg1: integer cursor number (usually 1 or 2)
            arg2: integer channel number to which the cursor will relate
        '''
        self._write('CURS:SOUR CH' + str(ch))

    def cursor_split(self, *args, **kwargs):
        self._write('CURS:MOD IND')

    def reset_statistics(self, *args, **kwargs):
        self._write('MEASU:STATI RESET')

    def saveimage(self, Filename=None, *args, **kwargs):
        Background = kwargs['Background'] if 'Background' in kwargs else 'black'
        """ save the scope shoot image """
        self._write('USBD:CONF IMA')
        self._write('SAV:IMAG:FILEF PNG')
        if(Background.lower() == 'white'):
            self._write('SAV:IMAG:INKS ON')
        else:
            self._write('SAV:IMAG:INKS OFF')
        self._write('HARDC START')
        sleep(1)
        data = self.cmd.read_raw()
        img = bytearray(data)
        if Filename == None:
            tkinter.Tk().withdraw()
            Filename = tkinter.filedialog.asksaveasfilename(initialdir=self.data_dir, initialfile=self.imagefile)
        if Filename == '':
            return
        self.imagefile = Filename
        with open(Filename, 'wb') as fn:
            fn.write(img)
        self._write('USBD:CONF USBT')

    def get_val_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query(f'MEASU:MEAS{Index}:VAL?')

    def get_mean_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MEAN?')

    def get_min_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MINIMUM?')

    def get_max_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MAX?')

    def get_horscale(self, *args, **kwargs):
        """
        gets the horizontal scale
        """
        return self._query("HOR:SCA?")  # use "horizontal:scale instead of "horizontal:mode:scale

    def horizontal_delay(self, state='OFF', time=0, *args, **kwargs):
        if state.upper() == 'OFF':
            self._write('HOR:DEL:MOD OFF')
        else:
            self._write('HOR:DEL:MOD ON')
            self._write('HOR:DEL:TIM ' + str(time))

    def horpos(self, value, *args, **kwargs):
        self._write('HOR:POS ' + str(value))

    def horizontal_mode(self, mode='AUTO', *args, **kwargs):
        # This model seems to not have this option
        pass

    def horizontal_sample_rate(self, value=5e+6, *args, **kwargs):
        self._write('HOR:SAMPLER ' + str(value))

    def get_delta_t(self, *args, **kwargs):
        delta = self._query('CURS:VBA:DELT?')
        return delta

    def set_attenuation(self, ch, value, *args, **kwargs):
        self._write('CH' + str(ch) + ':PRO:GAIN ' + str(1.0/value))

    def set_termination(self, ch, value, *args, **kwargs):
        '''
        :param ch: (int) Oscilloscope Channel to be changed
        :param value: { 50.0 | 1e+6 }
        :return: None
        '''
        self._write(f'CH{ch}:TER {value}')

    def set_persistence(self, option, *args, **kwargs):
        '''
        :param value: { <number> | CLEAR | AUTO | MINImum | INFInite }
        '''
        if option.upper() == 'OFF':
            option = '-1'
        if option.upper() == 'INFP' or option.upper() == 'INFPERSIST':
            option = 'INFI'
        self._write('DIS:PERS ' + str(option))

    def set_acquisition_mode(self, value, *args, **kwargs):
        '''
        :param value: { SAMple | PEAKdetect | HIRes | AVErage | ENVelope }
        '''
        self._write('ACQ:MOD ' + str(value))

    def set_fast_acq(self, state, *args, **kwargs):
        # This function will only work for MDO3000, MDO4000/B, or MDO4000C models with option SA3 or SA6.
        if state.upper() == 'ON':
            self._write(f'ACQ:FASTA:STATE {state}')
        else:
            self._write(f'ACQ:FASTA:STATE OFF')

    def set_acq_num(self, num, *args, **kwargs):
        '''
        These models don't have option to set number of acquisition. It can be set for envelope mode, but still it won't
        act like "sequence" where it will stop after the set number of acquisitions.
        :param num: any positive integer
        :return: None
        '''
        print('This scope model does not have option to set number of acquisition. Check Manual for more info.')

    def get_acq_num(self):
        return self._query('ACQ:NUMAC?')

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")
        sleep(0.5)

    def set_record_length(self, value, *args, **kwargs):
        self._write('HOR:RECO ' + str(value))

    def set_vertical_scale(self, ch, value, *args, **kwargs):
        self._write('CH' + str(ch) + ':SCA ' + str(value))

    def trigger_mode(self, opt, *args, **kwargs):
        '''
        :param opt: { AUTO | NORMal }
        '''
        self._write('TRIG:A:MOD ' + str(opt))

    def probe_autozero(self, ch=1, *args, **kwargs):
        self._write(f'CH{ch}:PRO:AUTOZ EXEC')

    def get_vertical_scale(self, ch, *args, **kwargs):
        return self._query('CH' + str(ch) + ':SCAle?')

    def get_verpos(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POSition?')

    def get_trigger(self, *args, **kwargs):
        return self._query('TRIG:A:LEV?')

    def set_trigger(self, ch=None, level=None, slope=None, coupling=None, *args, **kwargs):
        if ch is not None:
            self._write(f'TRIG:A:EDGE:SOU CH{ch}')
        if level is not None:
            self._write(f'TRIG:A:LEV {level}')
        if slope is not None:
            self._write(f'TRIG:A:EDGE:SLO {slope}')
        if coupling is not None:
            self._write(f'TRIG:A:EDGE:COUP {coupling}')

    def delete_measurement(self, meas, *args, **kwargs):
        self._write(f'MEASU:MEAS{meas}:STATE OFF')

    def set_ch_offset(self, ch, offset, *args, **kwargs):
        self._write(f'CH{ch}:OFFS {offset}')

    def get_offset(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:OFFS?')

    def get_position(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POS?')

    def set_zoom_scale(self, ch=1, value=4e-6, *args, **kwargs):
        self._write(f'ZOO:ZOOM{ch}:SCA {value}')

    def set_zoom_pos(self, ch=1, value='50', *args, **kwargs):
        self._write(f'ZOO:ZOOM{ch}:POS {value}')

    def zoom_mode(self, state='OFF', *args, **kwargs):
        self._write(f'ZOO:MOD {state}')

class Tkdpo7k(ScopeBase, SimpleIviScope):
    '''
        Supported Instruments
            Tektronix DPO 7000 Series Oscilloscopes
            DPO7104, DPO7054, DPO7254, DPO7354, DPO70404, DPO70604, DPO70804, DPO71254, DPO71604, DPO72004, DSA70404,
            DSA70604, DSA70804, DSA71254, DSA71604, DSA72004, MSO70404, MSO70604, MSO70804, MSO71254, MSO71604,
            MSO72004, MSO5034, MSO5054, MSO5104, MSO5204, DPO5034, DPO5054, DPO5104, DPO5204
        '''

    ID = '7k'

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        super(Tkdpo7k, self).__init__(DPO7kiviScope())
        self.Initialize(ResourceName=Address, IdQuery=True, Reset=reset, OptionString="simulate=" + str(simulate))
        self.pyvisa_instr = self.visa_from_simple_instrument(Address)

    def _write(self, command, *args, **kwargs):
        self.lld.dllwrap.WriteInstrData(writeBuffer=command)

    def _query(self, command, *args, **kwargs):
        self.lld.dllwrap.WriteInstrData(writeBuffer=command)
        data = self.lld.dllwrap.ReadInstrData(numBytes=1024)
        return data

    def horscale(self, scale, *args, **kwargs):
        """
        set the horizontal scale
        unit: n = "e-9"; u = "e-6"; m = "e-3"
        2n equals to 2e-9
        """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(scale).strip()
        if s[-1] == 's':
            s = s.rstrip('s')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write("HOR:MODE:SCA " + s)  # use "horizontal:scale instead of "horizontal:mode:scale

    def verpos(self, Channel, Pos, *args, **kwargs):
        """ set the vertical position """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(Pos).strip()
        if s[-1] == 'v':
            s = s.rstrip('v')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write("CH" + str(Channel) + ":position " + s)

    def display_overlay(self, *args, **kwargs):
        '''
        Not a function for these models
        Activate display overlay
        :param Waveview: (optional) standard value is 1
        '''
        pass

    def waveview_grid_type(self, type, *args, **kwargs):
        '''
        Not an option on this model
        :return: None
        '''
        pass

    def set_channel_label(self, ChannelIndex=1, Label='', Xpos="5" , Ypos="4", *args, **kwargs):
        Xpos = eval(Xpos) / 10
        Ypos = eval(Ypos) / 10
        self._write('CH' + str(ChannelIndex) + ':LAB:NAM "' + str(Label) + '"')
        self._write('CH' + str(ChannelIndex) + ':label:xpos ' + str(Xpos))
        self._write('CH' + str(ChannelIndex) + ':label:ypos ' + str(Ypos))

    def set_screen_text(self, text_no=1, text="", xpos="", ypos="", *args, **kwargs):
        FontSize = kwargs['FontSize'] if 'FontSize' in kwargs else 10
        if int(xpos) < 0 or int(xpos) > 500:
            print('Invalid Xpos value!')
            return
        if int(ypos) < 0 or int(ypos) > 385:
            print('Invalid Ypos value!')
            return
        self._write(f"DIS:SCREENTE:STATE ON")
        self._write(f"DIS:SCREENTE:LAB{text_no}:STATE ON")
        self._write(f"DIS:SCREENTE:LAB{text_no}:NAM '{text}'")
        self._write(f"DIS:SCREENTE:LAB{text_no}:XPOS {xpos}")
        self._write(f"DIS:SCREENTE:LAB{text_no}:YPOS {ypos}")
        self._write(f'DIS:SCREENTE:LAB{text_no}:FONTCO "#FF0000"')
        self._write(f'DIS:SCREENTE:LAB{text_no}:FONTS {FontSize}')

    def change_screentext(self, txt_no=1, text='', *args, **kwargs):
        self._write('DIS:SCREENTE:LAB' + str(txt_no) + ':NAM "' + str(text) + '"')

    def set_measurement(self, MeasureIndex=1, MeasureType='FREQUENCY', State='ON', Source=1, *args, **kwargs):
        '''
        Set and configure measurements
        :param MeasureIndex: Index in the Measurement list 1 - ...
        :type MeasureIndex: int
        :param MeasureType: { AMPLITUDE | AREA | BURST | CARea | CMEan | CRMs | DELAY | DISTDUty | EXTINCTDB | EXTINCTPCT
                            | EXTINCTRATIO | EYEHeight | EYEWIdth | FALL | FREQUENCY | HIGH | HITs | LOW | MAXIMUM
                            | MEAN | MEDian | MINIMUM | NCROss | NDUTY | NOVERSHOOT | NWIDTH | PBASe | PCROss | PCTCROss
                            | PDUTY | PEAKHits | PERIOD | PHASE | PK2PK | PKPKJitter | PKPKNoise | POVERSHOOT | PTOP
                            | PWIDTH | QFACTOR | RISE | RMS | RMSJitter | RMSNoise | SIGMA1 | SIGMA2 | SIGMA3
                            | SIXSigmajit | SNRatio | STDdev | UNDEFINED | WAVEFORMS }
        :type MeasureType: str
        :param State: ON or OFF
        :type State: str
        :param Source: Channel source of measurement
        :type Source: int
        '''
        if MeasureType.upper() == 'RISETIME':
            MeasureType = 'RISE'
        elif MeasureType.upper() == 'FALLTIME':
            MeasureType = 'FALL'
        elif MeasureType.upper() == 'PDUTTY':
            MeasureType = 'PDUTY'

        typeList = [
            'AMPLITUDE', 'AREA', 'BURST', 'CAREA', 'CMEAN', 'CRMS', 'DELAY', 'DISTDUTY', 'EXTINCTDB', 'EXTINCTPCT',
            'EXTINCTRATIO', 'EYEHEIGHT', 'EYEWIDTH', 'FALL', 'FREQUENCY', 'HIGH', 'HITS', 'LOW', 'MAXIMUM', 'MEAN',
            'MEDIAN', 'MINIMUM', 'NCROSS', 'NDUTY', 'NOVERSHOOT', 'NWIDTH', 'PBASE', 'PCROSS', 'PCTCROSS', 'PDUTY',
            'PEAKHITS', 'PERIOD', 'PHASE', 'PK2PK', 'PKPKJITTER', 'PKPKNOISE', 'POVERSHOOT', 'PTOT', 'PWIDTH',
            'QFACTOR', 'RISE', 'RMS', 'RMSNOISE', 'SIGMA1', 'SIGMA2', 'SIGMA3', 'SIXSIGMAJIT', 'SNRATIO', 'STDDEV',
            'UNDEFINED', 'WAVEFORMS',
        ]

        if MeasureType.upper() not in typeList:
            print(f'{MeasureType} is not defined on this Oscilloscope Model')
            return

        if State.upper() == 'ON':
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':SOU CH' + str(Source) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':TYP ' + str(MeasureType) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')
        else:
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')

    def config_delay_measurement(self, MeasureIndex=1, Source1='3', Source2='4', Mid1='1.0', Mid2='1.0', Edge1='RISE', Edge2='FALL', *args, **kwargs):
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':TYP DEL;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOURCE1 ' + str(Source1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOURCE2 ' + str(Source2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:METH PERC;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:ABS:MID1 ' + str(Mid1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:ABS:MID2 ' + str(Mid2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE1 ' + str(Edge1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE2 ' + str(Edge2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:DIRE FORW;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOU1:SIGT PULSE;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':STATE ON;')

    def config_top_base_method(self, source=1, method='AUTO', *args, **kwargs):
        '''
        This model works differently compared to more modern models. This will change method
        based on measurement number [1:8].
        :param source: Channel number <int> NOT APPLICABLE TO THIS MODEL
        :param method: { MEAN | MINMax | HIStogram } When AUTO is selected it will apply MEAN
        :param meas_num: Measurement number [1:8]
        :return: None
        '''
        meas_num = kwargs['meas_num'] if 'meas_num' in kwargs else '1'
        if method.upper() == 'AUTO':
            method = 'MEAN'
        self._write(f'MEASU:MEAS{meas_num}:METH {method}')

    def set_reflevel_method(self, source=1, method='PERC', *args, **kwargs):
        '''
        Select the Method used to calculate reference levels for the measurement.
        :param source: Channel number <int> NOT APPLICABLE FOR THIS MODEL
        :param method: { PERCent | ABSolute }
        :return: None
        '''
        meas_num = kwargs['meas_num'] if 'meas_num' in kwargs else '1'
        self._write(f'MEASU:MEAS{meas_num}:REFL:METH {method}')

    def set_reflevel_percent_type(self, source=1, type='TENN', *args, **kwargs):
        '''
        The reflevel selected will be applied for all measurements
        :param source: Channel number <int> NOT APPLICABLE FOR THIS MODEL
        :param type: always CUSTOM (set "high" and "low" parameters)
        :return: None
        '''
        low = kwargs['low'] if 'low' in kwargs else 10
        high = kwargs['high'] if 'high' in kwargs else 90
        self._write(f'MEASU:REFL:PERC:HIGH {high}')
        self._write(f'MEASU:REFL:PERC:LOW {low}')

    def hi_resolution(self, *args, **kwargs):
        self._write('ACQ:MOD HIR')

    def vertical_cursor_on(self, *args, **kwargs):
        self._write('CURSor:STATE ON')

    def vertical_cursor_off(self, *args, **kwargs):
        self._write('Cursor:state off')

    def set_cursor_function(self, func, *args, **kwargs):
        '''
        Options are: OFF | HBA | VBA | SCREEN | WAVEFORM
        '''
        self._write('CURSor:FUNCtion ' + str(func))

    def set_cursor_pos(self, cursor, pos, *args, **kwargs):
        self._write('CURS:WAVE:POS' + str(cursor) + ' ' + str(pos))

    def get_cursor_avpos(self, cursor, *args, **kwargs):
        View = kwargs['View'] if 'View' in kwargs else 1
        CursorN = kwargs['CursorN'] if 'CursorN' in kwargs else 1
        if cursor == 1:
            cursor = 'A'
        elif cursor == 2:
            cursor = 'B'
        try:
            return self._query(f'DIS:WAVEV{View}:CURS:CURSOR:WAVE:{cursor}VPOS?')
        except:
            print('Error trying to get vpos of waveform cursor.\nMake sure your cursor value is either 1 | 2 | "A" | "B".')
            return 0

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def waveform_cursor_to_channel(self, cursor, ch, *args, **kwargs):
        '''
        This function changes to which wave the cursor is related.
        Syntax: waveform_cursor_to_channel(arg1, arg2)
            arg1: integer cursor number (usually 1 or 2)
            arg2: integer channel number to which the cursor will relate
        '''
        self._write('CURS:SOUR' + str(cursor) + ' CH' + str(ch))

    def cursor_split(self, *args, **kwargs):
        self._write('CURS:MOD IND')

    def reset_statistics(self, *args, **kwargs):
        self._write('MEASU:STATI:COUN RESET')

    def saveimage(self, Filename=None, *args, **kwargs):
        Background = kwargs['Background'] if 'Background' in kwargs else 'black'
        self._write('HARDCopy:PORT FILE')
        self._write('EXPort:FORMat PNG')
        self._write('HARDCopy:FILEName "C:/Temp.png"')
        if Background.upper() == 'WHITE':
            self._write('HARDC:PALE INKS')
        else:
            self._write('HARDC:PALE COLO')
        self._write('HARDCopy STARt')
        sleep(0.5)
        self._write('FILESystem:READFile "C:/Temp.png"')
        sleep(0.5)
        data = self.pyvisa_instr.read_raw()
        img = bytearray(data)
        if Filename == None:
            tkinter.Tk().withdraw()
            Filename = tkinter.filedialog.asksaveasfilename(initialdir=self.data_dir, initialfile=self.imagefile)
        if Filename == '':
            return
        self.imagefile = Filename
        fn = open(Filename, 'wb')
        fn.write(img)
        fn.close()
        self._write(':FILESystem:DELEte "C:/Temp.png"')

    def get_val_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':VAL?')[0]

    def get_mean_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MEAN?')[0]

    def get_min_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MINIMUM?')[0]

    def get_max_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MAX?')[0]

    def get_horscale(self, *args, **kwargs):
        """
        gets the horizontal scale
        """
        return self._query("HOR:SCA?")  # use "horizontal:scale instead of "horizontal:mode:scale

    def horizontal_delay(self, state='OFF', time=0, *args, **kwargs):
        if state.upper() == 'OFF':
            self._write('HOR:DEL:MOD OFF')
        else:
            self._write('HOR:DEL:MOD ON')
            self._write('HOR:DEL:TIM ' + str(time))

    def horpos(self, value, *args, **kwargs):
        self._write('HOR:POS ' + str(value))

    def horizontal_mode(self, mode='AUTO', *args, **kwargs):
        '''
        :param mode: { AUTO | CONStant | MANual }
        '''
        self._write('HOR:MODE ' + str(mode))

    def horizontal_sample_rate(self, value=5e+6, *args, **kwargs):
        self._write('HOR:MODE:SAMPLER ' + str(value))

    def get_delta_t(self, *args, **kwargs):
        delta = self._query('CURS:VBA:DELT?')
        return delta[0]

    def set_attenuation(self, ch, value, *args, **kwargs):
        self._write('CH' + str(ch) + ':PROBEF:EXTA ' + str(value))

    def set_termination(self, ch, value, *args, **kwargs):
        '''
        :param ch: (int) Oscilloscope Channel to be changed
        :param value: { 50.0 | 1e+6 }
        :return: None
        '''
        self._write(f'CH{ch}:TER {value}')

    def set_persistence(self, option, *args, **kwargs):
        '''
        :param value: { OFF | VARpersist | INFPersist }
        '''
        if self.is_num(option):
            if float(option) == 0:
                self._write('DIS:PERS OFF')
            else:
                self._write('DIS:PERS VAR')
                self._write(f'DIS:VAR {option}')
            return
        elif option.upper() == 'INFI' or option.upper() == 'INFINITE':
            option = 'INFP'
            self._write('DIS:PERS ' + str(option))
        elif option.upper() == 'OFF' or option.upper() == 'VAR' or option.upper() == 'VARPERSIST' or option.upper() == 'INFP' or option.upper() == 'INFPERSIST':
            self._write('DIS:PERS ' + str(option))
        else:
            self._write('DIS:PERS OFF')

    def set_acquisition_mode(self, value, *args, **kwargs):
        '''
        :param value: { SAMple | PEAKdetect | HIRes | AVErage | WFMDB | ENVelope }
        '''
        self._write('ACQ:MOD ' + str(value))

    def set_fast_acq(self, state, *args, **kwargs):
        self._write('FASTA:STATE ' + str(state))

    def set_acq_num(self, num, *args, **kwargs):
        self._write(f'ACQ:NUMSAM {num}')
        self._write(f'ACQ:STOPA SEQ')
        self._write(f'ACQ:STATE RUN')

    def get_acq_num(self):
        return self._query('ACQ:NUMAC?')

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")

    def set_record_length(self, value, *args, **kwargs):
        self._write('HOR:MODE:RECO ' + str(value))

    def set_vertical_scale(self, ch, value, *args, **kwargs):
        self._write('CH' + str(ch) + ':SCA ' + str(value))

    def trigger_mode(self, opt, *args, **kwargs):
        '''
        :param opt: { AUTO | NORMal }
        '''
        self._write('TRIG:A:MOD ' + str(opt))

    def probe_autozero(self, ch=1, *args, **kwargs):
        self._write(f'CH{ch}:PRO:AUTOZ EXEC')

    def get_vertical_scale(self, ch, *args, **kwargs):
        return self._query('CH' + str(ch) + ':SCAle?')

    def get_verpos(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POSition?')[0]

    def get_trigger(self, *args, **kwargs):
        return self._query('TRIG:A:LEV?')[0]

    def set_trigger(self, ch=None, level=None, slope=None, coupling=None, *args, **kwargs):
        if ch is not None:
            self._write(f'TRIG:A:EDGE:SOU CH{ch}')
        if level is not None:
            self._write(f'TRIG:A:LEV {level}')
        if slope is not None:
            self._write(f'TRIG:A:EDGE:SLO {slope}')
        if coupling is not None:
            self._write(f'TRIG:A:EDGE:COUP {coupling}')

    def delete_measurement(self, meas, *args, **kwargs):
        self._write(f'MEASU:MEAS{meas}:STATE OFF')

    def set_ch_offset(self, ch, offset, *args, **kwargs):
        self._write(f'CH{ch}:OFFS {offset}')

    def get_offset(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:OFFS?')[0]

    def get_position(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POS?')[0]

    def set_zoom_scale(self, ch=1, value=4e-6, *args, **kwargs):
        wfm = kwargs['wfm'] if 'wfm' in kwargs else 'CH1'
        self._write(f'ZOO:ZOOM{ch}:{wfm}:HOR:SCA {value}')

    def set_zoom_pos(self, ch=1, value='50', *args, **kwargs):
        wfm = kwargs['wfm'] if 'wfm' in kwargs else 'CH1'
        self._write(f'ZOO:ZOOM{ch}:{wfm}:HOR:POS {value}')

    def zoom_mode(self, state='OFF', *args, **kwargs):
        self._write(f'ZOO:MOD {state}')

class TekScope(ScopeBase, SimpleIviScope):
    '''
            Supported Instruments
                TDS7054, TDS7104, TDS7154, TDS7154B, TDS7254, TDS7254B, TDS7404, TDS7404B, TDS7704B, TDS6124C, TDS6154C,
                TDS6404, TDS6604, TDS6604B, TDS6804B, CSA7154, CSA7404, CSA7404B, TDS5032, TDS5032B, TDS5034, TDS5034B,
                TDS5054, TDS5052, TDS5052B, TDS5054B, TDS5054BE, TDS5104, TDS5104B, DPO5034B, DPO5054, DPO5054B,
                DPO5104, DPO5104B, DPO5204, DPO5204B, MSO5034, MSO5034B, MSO5054, MSO5054B, MSO5104, MSO5104B, MSO5204,
                MSO5204B, DPO7054, DPO7104, DPO7254, DPO7354, DPO7054C, DPO7104C, DPO7254C, DPO7354C, DPO70404,
                DPO70604, DPO70804, DPO70404B, DPO70604B, DPO70804B, DPO70404C, DPO70604C, DPO70804C, DSA70404,
                DSA70404B, DSA70404C, DSA70604, DSA70604B, DSA70604C, DSA70804, DSA70804B, DSA70804C, DPO71254,
                DPO71254B, DPO71254C, DPO71604, DPO71604B, DPO71604C, DPO72004, DPO72004B, DPO72004C, DSA71254,
                DSA71254B, DSA71254C, DSA71604, DSA71604B, DSA71604C, DSA72004, DSA72004B, DSA72004C, MSO70404,
                MSO70404C, MSO70604, MSO70604C, MSO70804, MSO70804C, MSO71254, MSO71254C, MSO71604, MSO71604C, MSO72004,
                MSO72004C, DPO72504D, DPO72504DX, DPO73304D, DPO73304DX, DSA72504D, DSA73304D, DPO72304DX, MSO72304DX,
                MSO72504DX, MSO73304DX, DPO73304SX
            '''

    ID = 'TekScope'

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        super(TekScope, self).__init__(TEKSCOPE())
        self.Initialize(ResourceName=Address, IdQuery=True, Reset=reset, OptionString="simulate=" + str(simulate))
        self.pyvisa_instr = self.visa_from_simple_instrument(Address)

    def _write(self, command, *args, **kwargs):
        self.pyvisa_instr.write(command)

    def _query(self, command, delay=None, *args, **kwargs):
        if delay is None:
            return self.pyvisa_instr.query(command)
        else:
            return self.pyvisa_instr.query(command, delay=delay)

    def Trigger_Edge(self, Level=2.00, Slope='RISE', Position=2, Coupling='DC', ChannelIndex=1, *args, **kwargs):
        self._write('TRIG:A:EDGE:SOU CH' + str(ChannelIndex))
        self._write('TRIG:A:EDGE:COUP ' + str(Coupling))
        self._write('TRIG:A:EDGE:SLO ' + str(Slope))
        self._write('TRIG:A:LEV ' + str(Level))

    def horscale(self, scale, *args, **kwargs):
        """
        set the horizontal scale
        unit: n = "e-9"; u = "e-6"; m = "e-3"
        2n equals to 2e-9
        """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(scale).strip()
        if s[-1] == 's':
            s = s.rstrip('s')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write("HOR:SCA " + s)  # use "horizontal:scale instead of "horizontal:mode:scale

    def verpos(self, Channel, Pos, *args, **kwargs):
        """ set the vertical position """
        unit = {'m': "e-3", 'u': "e-6", 'n': "e-9"}
        s = str(Pos).strip()
        if s[-1] == 'v':
            s = s.rstrip('v')
        if s[-1] in unit:
            s = s.replace(s[-1], unit[s[-1]])
        self._write("CH" + str(Channel) + ":position " + s)

    def display_overlay(self, *args, **kwargs):
        '''
        Not a function for these models
        Activate display overlay
        :param Waveview: (optional) standard value is 1
        '''
        pass

    def waveview_grid_type(self, type, *args, **kwargs):
        '''
        Not an option on this model
        :return: None
        '''
        pass

    def set_channel_label(self, ChannelIndex=1, Label='', Xpos="5", Ypos="4", *args, **kwargs):
        Xpos = eval(Xpos) / 10
        Ypos = eval(Ypos) / 10
        self._write('CH' + str(ChannelIndex) + ':LAB:NAM "' + str(Label) + '"')
        self._write('CH' + str(ChannelIndex) + ':label:xpos ' + str(Xpos))
        self._write('CH' + str(ChannelIndex) + ':label:ypos ' + str(Ypos))

    def set_screen_text(self, text_no=1, text="", xpos="", ypos="", *args, **kwargs):
        if int(xpos) < 0 or int(xpos) > 500:
            print('Invalid Xpos value!')
            return
        if int(ypos) < 0 or int(ypos) > 385:
            print('Invalid Ypos value!')
            return
        self._write(f"DIS:SCREENTE:STATE ON")
        self._write(f"DIS:SCREENTE:LAB{text_no}:NAM '{text}'")
        self._write(f"DIS:SCREENTE:LAB{text_no}:XPOS {xpos}")
        self._write(f"DIS:SCREENTE:LAB{text_no}:YPOS {ypos}")

    def change_screentext(self, txt_no=1, text='', *args, **kwargs):
        self._write('DIS:SCREENTE:LAB' + str(txt_no) + ':NAM "' + str(text) + '"')

    def set_measurement(self, MeasureIndex=1, MeasureType='FREQUENCY', State='ON', Source=1, *args, **kwargs):
        '''
        Set and configure measurements
        :param MeasureIndex: Index in the Measurement list 1 - ...
        :type MeasureIndex: int
        :param MeasureType: { AMPlitude | AREa | BURst | CARea | CMEan | CRMs | DELAY | DISTDUty | EXTINCTDB
                            | EXTINCTPCT | EXTINCTRATIO | EYEHeight | EYEWidth | FALL | FREQUENCY | HIGH | HITs
                            | LOW | MAXIMUM | MEAN | MEDian | MINIMUM | NCROss | NDUty | NOVERSHOOT | NWIDTH
                            | PBASe | PCROss | PCTCROss | PDUty | PEAKHits | PERIOD | PHAse | PK2PK | PKPKJitter
                            | PKPKNoise | POVershoot | PTOT | PWIdth | QFACtor | RISE | RMS | RMSJitter
                            | RMSNoise | SIGMA1 | SIGMA2 | SIGMA3 | SIXSigmajit | SNRatio | STDDev | UNDEFINED
                            | WAVEFORMS }
        :type MeasureType: str
        :param State: ON or OFF
        :type State: str
        :param Source: Channel source of measurement
        :type Source: int
        '''
        if MeasureType.upper() == 'RISETIME':
            MeasureType = 'RISE'
        elif MeasureType.upper() == 'FALLTIME':
            MeasureType = 'FALL'
        elif MeasureType.upper() == 'PDUTTY':
            MeasureType = 'PDUTY'

        typeList = [
            'AMPLITUDE', 'AREA', 'BURST', 'CAREA', 'CMEAN', 'CRMS', 'DELAY', 'DISTDUTY', 'EXTINCTDB', 'EXTINCTPCT',
            'EXTINCTRATIO', 'EYEHEIGHT', 'EYEWIDTH', 'FALL', 'FREQUENCY', 'HIGH', 'HITS', 'LOW', 'MAXIMUM', 'MEAN',
            'MEDIAN', 'MINIMUM', 'NCROSS', 'NDUTY', 'NOVERSHOOT', 'NWIDTH', 'PBASE', 'PCROSS', 'PCTCROSS', 'PDUTY',
            'PEAKHITS', 'PERIOD', 'PHASE', 'PK2PK', 'PKPKJITTER', 'PKPKNOISE', 'POVERSHOOT', 'PTOT', 'PWIDTH',
            'QFACTOR', 'RISE', 'RMS', 'RMSNOISE', 'SIGMA1', 'SIGMA2', 'SIGMA3', 'SIXSIGMAJIT', 'SNRATIO', 'STDDEV',
            'UNDEFINED', 'WAVEFORMS',
        ]

        if MeasureType.upper() not in typeList:
            print(f'{MeasureType} is not defined on this Oscilloscope Model')
            return

        if State.upper() == 'ON':
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':SOU CH' + str(Source) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':TYP ' + str(MeasureType) + ';')
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')
        else:
            self._write('MEASU:MEAS' + str(MeasureIndex) + ':STATE ' + str(State) + ';')

    def config_delay_measurement(self, MeasureIndex=1, Source1='3', Source2='4', Mid1='1.0', Mid2='1.0', Edge1='RISE',
                                 Edge2='FALL', *args, **kwargs):
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':TYP DEL;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOURCE1 ' + str(Source1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOURCE2 ' + str(Source2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:METH PERC;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:ABS:MID1 ' + str(Mid1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':REFL:ABS:MID2 ' + str(Mid2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE1 ' + str(Edge1) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:EDGE2 ' + str(Edge2) + ';')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':DEL:DIRE FORW;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':SOU1:SIGT PULSE;')
        self._write(':MEASU:MEAS' + str(MeasureIndex) + ':STATE ON;')

    def config_top_base_method(self, source=1, method='AUTO', *args, **kwargs):
        '''
        This model works differently compared to more modern models. This will change method
        for all measurements.
        :param source: Channel number <int> NOT APPLICABLE TO THIS MODEL
        :param method: { MEAN | MINMax | HIStogram } When AUTO is selected it will apply MEAN
        :return: None
        '''
        if method.upper() == 'AUTO':
            method = 'MEAN'
        self._write(f'MEASU:MEAS:METH {method}')

    def set_reflevel_method(self, source=1, method='PERC', *args, **kwargs):
        '''
        Select the Method used to calculate reference levels for the measurement.
        :param source: Channel number <int> NOT APPLICABLE FOR THIS MODEL
        :param method: { PERCent | ABSolute }
        :return: None
        '''
        meas_num = kwargs['meas_num'] if 'meas_num' in kwargs else '1'
        self._write(f'MEASU:MEAS{meas_num}:REFL:METH {method}')

    def set_reflevel_percent_type(self, source=1, type='TENN', *args, **kwargs):
        '''
        The reflevel selected will be applied for all measurements
        :param source: Channel number <int> NOT APPLICABLE FOR THIS MODEL
        :param type: always CUSTOM (set "high" and "low" parameters)
        :return: None
        '''
        low = kwargs['low'] if 'low' in kwargs else 10
        high = kwargs['high'] if 'high' in kwargs else 90
        self._write(f'MEASU:REFL:PERC:HIGH {high}')
        self._write(f'MEASU:REFL:PERC:LOW {low}')

    def hi_resolution(self, *args, **kwargs):
        self._write('ACQ:MOD HIR')

    def vertical_cursor_on(self, *args, **kwargs):
        self._write('CURSor:STATE ON')

    def vertical_cursor_off(self, *args, **kwargs):
        self._write('Cursor:state off')

    def set_cursor_function(self, func, *args, **kwargs):
        '''
        Options are: OFF | HBA | VBA | SCREEN | WAVEFORM
        '''
        self._write('CURSor:FUNCtion ' + str(func))

    def set_cursor_pos(self, cursor, pos, *args, **kwargs):
        self._write('cursor:vbars:position' + str(cursor) + ' ' + str(pos))

    def set_persistence(self, option, *args, **kwargs):
        '''
        :param option: { OFF | AUTO | INFPersist | INFInite | VARpersist | CLEAR }
        '''
        if option.upper() == 'AUTO' or option.upper() == 'CLEAR':
            option = 'OFF'
        elif option.upper() == 'INFINITE' or option.upper() == 'INFI':
            option = 'INFPERSIST'
        if self.is_num(option):
            self._write('DIS:PERS VAR')
            self._write(f'DIS:VAR {option}')
        else:
            self._write('DIS:PERS ' + str(option))

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def waveform_cursor_to_channel(self, cursor, ch, *args, **kwargs):
        '''
        This function changes to which wave the cursor is related.
        Syntax: waveform_cursor_to_channel(arg1, arg2)
            arg1: integer cursor number (usually 1 or 2)
            arg2: integer channel number to which the cursor will relate
        '''
        self._write('CURS:SOUR' + str(cursor) + ' CH' + str(ch))

    def cursor_split(self, *args, **kwargs):
        self._write('CURS:MOD IND')

    def reset_statistics(self, *args, **kwargs):
        self._write('MEASU:STATI:COUN RESET')

    def saveimage(self, Filename=None, *args, **kwargs):
        Background = kwargs['Background'] if 'Background' in kwargs else 'black'
        self._write('EXP:FORM PNG')
        if Background.lower() == 'black':
            self._write('EXP:IMAG NORM')
        else:
            self._write('EXP:IMAG ENHAN')
        self._write('EXP:FILEN "C:/Temp.png"')
        self._write('EXP:VIEW FULLSCREEN')
        self._write('EXP STA')
        sleep(4)
        self._write('FILESystem:READFile "C:/Temp.png"')  # ,GPIB
        data = self.pyvisa_instr.read_raw()
        img = bytearray(data)
        if Filename == None:
            tkinter.Tk().withdraw()
            Filename = tkinter.filedialog.asksaveasfilename(initialdir=self.data_dir, initialfile=self.imagefile)
        if Filename == '':
            return
        self.imagefile = Filename
        fn = open(Filename, 'wb')
        fn.write(img)
        fn.close()
        self._write(':FILESystem:DELEte "C:\Temp\Temp.png"')

    def get_val_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':VAL?')

    def get_mean_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MEAN?')

    def get_min_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MINIMUM?')

    def get_max_measurement(self, *args, **kwargs):
        Index = kwargs['Index'] if 'Index' in kwargs else 1
        return self._query('MEASU:MEAS' + str(Index) + ':MAX?')

    def get_horscale(self, *args, **kwargs):
        """
        gets the horizontal scale
        """
        return self._query("HOR:SCA?")  # use "horizontal:scale instead of "horizontal:mode:scale

    def horizontal_delay(self, state='OFF', time=0, *args, **kwargs):
        if state.upper() == 'OFF':
            self._write('HOR:DEL:MOD OFF')
        else:
            self._write('HOR:DEL:MOD ON')
            self._write('HOR:DEL:TIM ' + str(time))

    def horpos(self, value, *args, **kwargs):
        self._write('HOR:POS ' + str(value))

    def horizontal_mode(self, mode='AUTO', *args, **kwargs):
        '''
        :param mode: { AUTO | CONStant | MANual }
        '''
        self._write('HOR:MODE ' + str(mode))

    def horizontal_sample_rate(self, value=5e+6, *args, **kwargs):
        self._write('HOR:MODE:SAMPLER ' + str(value))

    def get_delta_t(self, *args, **kwargs):
        delta = self._query('CURS:VBA:DELT?')
        return delta[0]

    def set_attenuation(self, ch, value, *args, **kwargs):
        self._write('CH' + str(ch) + ':PRO:SET "ATTEN ' + str(value) + 'X"')

    def set_termination(self, ch, value, *args, **kwargs):
        '''
        :param ch: (int) Oscilloscope Channel to be changed
        :param value: { 50.0 | 1e+6 }
        :return: None
        '''
        self._write(f'CH{ch}:TER {value}')

    def set_persistence(self, option, *args, **kwargs):
        '''
        :param value: { OFF | VARpersist | INFPersist }
        '''
        if option.upper() == 'INFI' or option.upper() == 'INFINITE':
            option = 'INFP'
        if option.upper() == 'OFF' or option.upper() == 'VAR' or option.upper() == 'VARPERSIST' or option.upper() == 'INFP' or option.upper() == 'INFPERSIST':
            self._write('DIS:PERS ' + str(option))
        else:
            self._write('DIS:PERS OFF')

    def set_acquisition_mode(self, value, *args, **kwargs):
        '''
        :param value: { SAMple | PEAKdetect | HIRes | AVErage | WFMDB | ENVelope }
        '''
        self._write('ACQ:MOD ' + str(value))

    def set_fast_acq(self, state, *args, **kwargs):
        self._write('FASTA:STATE ' + str(state))

    def set_acq_num(self, num, *args, **kwargs):
        self._write(f'ACQ:NUMSAM {num}')
        self._write(f'ACQ:STOPA SEQ')
        self._write(f'ACQ:STATE RUN')

    def get_acq_num(self):
        return self._query('ACQ:NUMAC?')

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")

    def set_record_length(self, value, *args, **kwargs):
        self._write('HOR:RECO ' + str(value))

    def set_vertical_scale(self, ch, value, *args, **kwargs):
        self._write('CH' + str(ch) + ':SCA ' + str(value))

    def trigger_mode(self, opt, *args, **kwargs):
        '''
        :param opt: { AUTO | NORMal }
        '''
        self._write('TRIG:A:MOD ' + str(opt))

    def probe_autozero(self, ch=1, *args, **kwargs):
        # Some of these models don't have this option.
        pass

    def get_vertical_scale(self, ch, *args, **kwargs):
        return self._query('CH' + str(ch) + ':SCAle?')

    def get_verpos(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POSition?')

    def get_trigger(self, *args, **kwargs):
        return self._query('TRIG:A:LEV?')

    def set_trigger(self, ch=None, level=None, slope=None, coupling=None, *args, **kwargs):
        if ch is not None:
            self._write(f'TRIG:A:EDGE:SOU CH{ch}')
        if level is not None:
            self._write(f'TRIG:A:LEV {level}')
        if slope is not None:
            self._write(f'TRIG:A:EDGE:SLO {slope}')
        if coupling is not None:
            self._write(f'TRIG:A:EDGE:COUP {coupling}')

    def delete_measurement(self, meas, *args, **kwargs):
        self._write(f'MEASU:MEAS{meas}:STATE OFF')

    def set_ch_offset(self, ch, offset, *args, **kwargs):
        self._write(f'CH{ch}:OFFS {offset}')

    def get_offset(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:OFFS?')

    def get_position(self, ch, *args, **kwargs):
        return self._query(f'CH{ch}:POS?')

    def set_zoom_scale(self, ch=1, value=4e-6, *args, **kwargs):
        wfm = kwargs['wfm'] if 'wfm' in kwargs else 'CH1'
        self._write(f'ZOO:ZOOM{ch}:{wfm}:HOR:SCA {value}')

    def set_zoom_pos(self, ch=1, value='50', *args, **kwargs):
        wfm = kwargs['wfm'] if 'wfm' in kwargs else 'CH1'
        self._write(f'ZOO:ZOOM{ch}:{wfm}:HOR:POS {value}')

    def zoom_mode(self, state='OFF', *args, **kwargs):
        self._write(f'ZOO:MOD {state}')

if __name__ == '__main__':
    # scope = Tkdpo7k('GPIB0::6::INSTR', Simulate=False, Reset=True)
    scope = Tkdpo4k('USB0::0x0699::0x0401::C020401::INSTR', Simulate=False, Reset=True)
    scope.Arm(Continuous=True)
    try:
        ch1 = scope.GetChannel(Index=1)
        ch1.Enable(False)
    except:
        print('inside except')
    try:
        swCh = 4
        scopeSwCh = scope.GetChannel(Index=swCh)
        scopeSwCh.Enable(True)
        scope.set_attenuation(swCh, 20)
    except Exception as e:
        pass

    # Overlay display
    scope.display_overlay()
    scope.horizontal_delay('OFF')
    scope.set_persistence('OFF')
    scope.set_acquisition_mode('HIR')

    # Config Probe Channels
    if swCh:
        scopeSwCh.ProbeSetup(
            Coupling="DC",
            Bandwidth=None,
            Vrange=int(30),
            Offset=0,
            Position=0,
            Impedance=50,
            Probe_Attn=20
        )

    # Trigger
    if swCh:
        scope.Trigger_Edge(
            Level=2.00,
            Slope='RISE',
            Position=2,
            Coupling='DC',
            ChannelIndex=int(4)
        )

        # Vertical Position
        scope.verpos(4, -3)
        scope.set_channel_label(4, 'SW', '50', '-30')

    # Horizontal Scale
    scope.horscale('4e-9')
    scope.horizontal_mode('AUTO')
    scope.horizontal_sample_rate('5e+9')
    scope.horpos(50)

    # Measurements
    scope.set_measurement(
        MeasureIndex=5,
        MeasureType='FREQUENCY',
        State='ON',
        Source=4,
    )

    # Scope Run
    scope.Arm(Continuous=True)
    scope.set_persistence('1')
    scope.set_screen_text(text_no=1, text='', xpos='10', ypos='10', FontSize='22')
    scope.vertical_cursor_on()
    scope.set_cursor_function('WAVEFORM')
    scope.cursor_split()
    scope.waveform_cursor_to_channel(cursor=1, ch=4)
    scope.waveform_cursor_to_channel(cursor=2, ch=4)
    scopeSwCh.ProbeSetup(
        Coupling="DC",
        Bandwidth=None,
        Vrange=50,
        Offset=0,
        Position=0,
        Impedance=50,
        Probe_Attn=20,
    )
    scope.display_overlay()
    scope.horizontal_delay('OFF')
    scope.set_persistence('OFF')
    scope.set_acquisition_mode('HIR')
    scope.Trigger_Edge(
        Level=2.00,
        Slope='RISE',
        Position=2,
        Coupling='DC',
        ChannelIndex=4
    )
    scope.change_screentext(f'Vin={12}V, Load={10}A, Vout={3.3}V, Fsw={600}kHz')

    scope.reset_statistics()
    sleep(1.0)


    scope.set_vertical_scale(ch=4, value=0.2)
    scope.verpos(4, 0)
    scope.set_record_length(1000000)
    scope.horpos(75)
    sleep(0.75)
    # Stop Scope
    scope.stop()
    sleep(0.5)

    pointA = 0
    pointB = 0
    wave = scopeSwCh.GetProbeWaveform(Timeout=0.5)
    # plt.plot([wave.index_to_time(x) - (wave.index_to_time(-1)/2) for x in range(len(wave.data))], wave.data)
    # plt.show()
    # slicedWave = wave.slice_by_time(start_time=-20e-9, stop_time=20e-9)
    slicedWave = wave
    for data in slicedWave:
        if data < -0.2:
            print((slicedWave.index_to_time(-1) * 0.75))
            pointA = slicedWave.Measurements_Utils.find_nth_crossing(data, "fall", 0) - (slicedWave.index_to_time(-1) * 0.75)
            slicedWave2 = wave.slice_by_time(start_time=pointA, stop_time=slicedWave.index_to_time(-1))
            pointB = slicedWave2.Measurements_Utils.find_nth_crossing(0, 'rise', 0) - (slicedWave.index_to_time(-1) * 0.75)
            break
    scope.set_cursor_pos(cursor=1, pos=pointA)
    scope.set_cursor_pos(cursor=2, pos=pointB)
    print('pointA rise =', pointA)
    print('pointB rise =', pointB)
    sleep(0.5)
    deadRise = pointB - pointA

    # Waveform
    fileName_i = 'scope_test01.png'
    scope.saveimage(fileName_i, Background='white')

    scope.run()
    exit(0)
    sleep(0.1)
    scope.horpos(25)
    scope.Trigger_Edge(
        Level=2.0,
        Slope='FALL',
        Position=2,
        Coupling='DC',
        ChannelIndex=int(4)
    )
    scope.reset_statistics()
    sleep(1.0)

    scope.stop()
    sleep(0.5)
    wave = scopeSwCh.GetProbeWaveform(Timeout=0.5)
    slicedWave = wave.slice_by_time(start_time=-20e-9, stop_time=20e-9)
    slicedWave2 = wave.slice_by_time(start_time=6e-9, stop_time=12e-9)
    pointA = slicedWave.Measurements_Utils.find_nth_crossing(0, "fall", 0)
    pointB = slicedWave2.Measurements_Utils.argmax()
    if pointA == None:
        pointA = 0
    if pointB == None:
        pointB = 0

    scope.set_cursor_pos(cursor=1, pos=pointA)
    scope.set_cursor_pos(cursor=2, pos=pointB)
    print('pointA fall =', pointA)
    print('pointB fall =', pointB)
    sleep(0.5)
    deadFall = pointB - pointA
    print('end')

