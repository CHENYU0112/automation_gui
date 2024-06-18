from pverify.drivers.DCPwr.AgE36xx.IIviDCPwr import IIviDCPwr as AGE36XX
from pverify.drivers.DCPwr.AgN67xx.IIviDCPwr import IIviDCPwr as AGN67XX
from pverify.drivers.SimplifiedLabInstruments.SimpleIviDcPwr import SimpleIviDcPwr

import pyvisa as visa

class PSBase:

    def __init__(self, callback):
        super(PSBase, self).__init__(callback)

    def __del__(self):
        try:
            self.pyvisa_instr.clear()
            self.pyvisa_instr.close()
        except:
            pass

    def visa_from_simple_instrument(self, addr):
        """
        This method returns a VISA resource instance that shares the session with the supplied IIviInstrument instance.
        """
        rm = visa.ResourceManager()
        _pyvisa_instr = rm.open_resource(addr)
        return _pyvisa_instr

# region VINs

class Xantrex_XHR_Series():
    """
    powersupply:
    below are the functions defined for the instrument class: (XHR series)
        __init__    =   initiate the instrument
        idn         =   gives us the identification Character of the Intrument
    """

    ID = 'Xantrex_XHR_Series'
    channel = None

    def __init__(self, Address, *args, **kwargs) -> None:
        self.cmd = visa.ResourceManager().open_resource(Address)
        self.manufacturer = 'Xantrex'
        self.address = Address

    def _query(self, command, delay=None, *args, **kwargs):
        if delay is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=delay)

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def GetChannel(self, Index=1, *args, **kwargs):
        newObj = Xantrex_XHR_Series(self.address)
        newObj.channel = int(Index)
        return newObj

    def Configure_VoltageLevel(self, Level, CurrentLimit, VoltageLimit=None, *args, **kwargs):
        self.set_voltage(voltage=Level)
        self.set_current(current=CurrentLimit)

    def Enable(self, state=False):
        self.output_on_off(state=state)

    def Measure_Current(self):
        return eval(self.get_current())

    def Measure_Voltage(self):
        return eval(self.get_voltage())

    def idn(self, *args, **kwargs):
        '''idn = gives us the identification Character of the Instrument
                syntax: idn()'''
        return self._query('ID?')

    def clear(self, *args, **kwargs):
        self._write('CLR')

    def output_on_off(self, state=False, *args, **kwargs):
        '''Syntax: output_on_off(arg1)
                arg1: Boolean
                    it will turn on output when True
                    it will turn off output when False
                    if no value is informed it will turn off'''
        if (state):
            self._write('OUT 1')
        else:
            self._write('OUT 0')

    def set_voltage(self, voltage, *args, **kwargs):
        self._write('VSET ' + str(voltage))

    def get_voltage(self, *args, **kwargs):
        return self._query('vset?')

    def set_current(self, current, *args, **kwargs):
        self._write('ISET ' + str(current))

    def get_current(self, *args, **kwargs):
        return self._query('iset?')

    def set_max_current(self, current, *args, **kwargs):
        self._write('imax ' + str(current))

    def get_max_current(self, *args, **kwargs):
        return self._query('imax?')

    def set_max_voltage(self, voltage, *args, **kwargs):
        self._write('vmax ' + str(voltage))

    def get_max_volgate(self, *args, **kwargs):
        return self._query('vmax?')

    def set_over_voltage_protection(self, voltage, *args, **kwargs):
        self._write('ovset ' + str(voltage))

    def get_over_voltage_protection(self, *args, **kwargs):
        return self._query('ovset?')

    def set_voltage_slew_rise(self, slewRate, *args, **kwargs):
        # This model does not have slew control
        pass

    def set_under_voltage_limit(self, voltage):
        pass
        #not implemented yet

    def get_over_voltage_limit(self):
        pass
        #not implemented yet

class HP603X(Xantrex_XHR_Series):
    '''
        Power Supply Models:
            HP 6030A, HP 6031A, HP 6032A, HP 6033A, HP 6035A, HP 6038A
    '''

    ID = 'HP603X'

    def __init__(self, Address, *args, **kwargs):
        super(HP603X, self).__init__(Address)

class Keith_2260B:
    '''
    Power Supply Models:
        Keithley 2260B 80-40, Gw Instek PSU Series, BK Precision 9205, BK Precision 9117
    '''

    ID = 'Keith_2260B'
    channel = None

    def __init__(self, Address, *args, **kwargs) -> None:
        self.cmd = visa.ResourceManager().open_resource(Address)
        self.address = Address

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, delay=None, *args, **kwargs):
        if delay is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=delay)

    def GetChannel(self, Index=1, *args, **kwargs):
        newObj = Keith_2260B(self.address)
        newObj.channel = int(Index)
        return newObj

    def Configure_VoltageLevel(self, Level, CurrentLimit, VoltageLimit=None, *args, **kwargs):
        self.set_voltage(voltage=Level)
        self.set_current(current=CurrentLimit)

    def Enable(self, state=False):
        self.output_on_off(output=state)

    def Measure_Current(self):
        return eval(self.get_current())

    def Measure_Voltage(self):
        return eval(self.get_voltage())

    def idn(self, *args, **kwargs):
        '''idn = gives us the identification Character of the Instrument
                syntax: idn()'''
        return self._query('*IDN?')

    def clear(self, *args, **kwargs):
        self._write('*CLS')

    def output_on_off(self, output=False):
        '''Syntax: output_on_off(arg1)
                arg1: Boolean
                    it will turn on output when True
                    it will turn off output when False
                    if no value is informed it will turn off'''
        if (output):
            self._write('OUTP 1')
        else:
            self._write('OUTP 0')

    def set_voltage(self, voltage, *args, **kwargs):
        self._write('VOLT ' + str(voltage))

    def get_voltage(self, *args, **kwargs):
        return self._query('VOLT?')

    def set_current(self, current, *args, **kwargs):
        self._write('CURR ' + str(current))

    def get_current(self, *args, **kwargs):
        return self._query('CURR?')

    def set_max_current(self, current, *args, **kwargs):
        self._write('CURR:PROT ' + str(current))

    def get_max_current(self, *args, **kwargs):
        return self._query('CURR:PROT?')

    def set_max_voltage(self, voltage, *args, **kwargs):
        self._write('VOLT:PROT ' + str(voltage))

    def get_max_volgate(self, *args, **kwargs):
        return self._query('VOLT:PROT?')

    def set_over_voltage_protection(self, voltage, *args, **kwargs):
        self._write('VOLT:PROT ' + str(voltage))

    def get_over_voltage_protection(self, *args, **kwargs):
        return self._query('VOLT:PROT?')

    def set_voltage_slew_rise(self, slewRate, *args, **kwargs):
        '''
        :param slewRate: { MIN | MAX | 0.01 <= x <= 0.1 }
        '''
        self._write(f'VOLT:SLEW:RIS {slewRate}')

    def set_under_voltage_limit(self, voltage):
        pass
        #not implemented yet

    def get_over_voltage_limit(self):
        pass
        #not implemented yet

class TdkLambda():
    '''
        TK-LAMBDA SERIES
    '''

    ID = 'TKLAMBDA'
    channel = None

    def __init__(self, Address, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        self.manufacturer = 'TK-LAMBDA'
        self.address = Address

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, d=None, *args, **kwargs):
        if d is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=d)

    def GetChannel(self, Index=1, *args, **kwargs):
        # different approach because the instrument wasn't accepting multiple connections
        # newObj = TdkLambda(self.address)
        # newObj.channel = int(Index)
        self.channel = int(Index)
        return self

    def Configure_VoltageLevel(self, Level, CurrentLimit, VoltageLimit=None, *args, **kwargs):
        self.set_channel()
        self.set_voltage(voltage=Level)
        self.set_current(current=CurrentLimit)

    def Enable(self, state=False):
        self.set_channel()
        self.output_on_off(state=state)

    def Measure_Current(self):
        self.set_channel()
        return eval(self.get_current())

    def Measure_Voltage(self):
        self.set_channel()
        return eval(self.get_voltage())

    def idn(self):
        '''idn = gives us the identification Character of the Instrument
                syntax: idn()'''
        return self._query('*IDN?')

    def clear(self):
        self._write('*CLS')

    def output_on_off(self, state=False):
        '''Syntax: output_on_off(arg1)
                arg1: Boolean
                    it will turn on output when True
                    it will turn off output when False
                    if no value is informed it will turn off'''
        if (state):
            self._write('OUTP:STAT 1')
        else:
            self._write('OUTP:STAT 0')

    def set_channel(self):
        # channel number is part of command
        pass

    def set_voltage(self, voltage):
        self.set_channel()
        self._write(f'VOLT {voltage}')

    def get_voltage(self):
        self.set_channel()
        return self._query('VOLT?')

    def set_current(self, current):
        self.set_channel()
        self._write('CURR ' + str(current))

    def get_current(self):
        self.set_channel()
        return self._query('CURR?')

    def set_max_current(self, current):
        self.set_channel()
        self._write('CURR:PROT:LEV ' + str(current))

    def get_max_current(self):
        self.set_channel()
        return self._query('CURR:PROT:LEV?')

    def set_max_voltage(self, voltage):
        self.set_channel()
        self._write('VOLT:PROT:LEV ' + str(voltage))

    def get_max_volgate(self):
        self.set_channel()
        return self._query(f'VOLT:PROT:LEV?')

    def set_over_voltage_protection(self, voltage):
        self.set_channel()
        self._write('VOLT:PROT:LEV ' + str(voltage))

    def get_over_voltage_protection(self):
        self.set_channel()
        return self._query('VOLT:PROT:LEV?')

    def set_under_voltage_limit(self, voltage):
        self.set_channel()
        self._write('VOLT:LIM:LOW ' + str(voltage))

    def get_over_voltage_limit(self):
        self.set_channel()
        return self._query('VOLT:LIM:LOW?')

    def set_foldback(self, state='ON', *args, **kwargs):
        '''
        :param state: <string> { "ON" | "OFF" }
        :return: None
        '''
        self._write(f'CURR:PROT:STAT {state}')

    def read_foldback_tripped(self):
        '''
        :return: '0' when no FB fault is active or '1' when supply is shut-down because of a FB fault
        '''
        return self._query("CURR:PROT:TRIP?")

# endregion

# region VCCs

class AgE36xx(PSBase, SimpleIviDcPwr):
    '''
    Supported Instruments:
        E3649A, E3648A, E3647A, E3646A, E3645A, E3644A, E3643A E3642A, E3641A, E3640A, E3634A, E3633A, E3632A, E3631A
        E36102A, E36103A, E36104A, E36105A, E36106A E36102B, E36103B, E36104B, E36105B, E36106B E36311A, E36312A,
        E36313A, EDU36311A E36231A, E36232A, E36233A,E36234A
    '''

    ID = 'AgE36xx'

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        super(AgE36xx, self).__init__(AGE36XX())
        self.Initialize(ResourceName=Address, IdQuery=True, Reset=reset, OptionString=f"simulate={simulate}")
        self.pyvisa_instr = self.visa_from_simple_instrument(Address)

    def _query(self, command, *args, **kwargs):
        return self.pyvisa_instr.query(command)

    def _write(self, command, *args, **kwargs):
        self.pyvisa_instr.write(command)

    def idn(self, *args, **kwargs):
        '''idn = gives us the identification Character of the Instrument
                syntax: idn()'''
        pass

    def clear(self):
        pass

    def output_on_off(self, state=False, *args, **kwargs):
        '''Syntax: output_on_off(arg1)
                arg1: Boolean
                    it will turn on output when True
                    it will turn off output when False
                    if no value is informed it will turn off'''
        if (state):
            self._write('OUTP ON')
        else:
            self._write('OUTP OFF')

    def set_voltage(self, voltage, *args, **kwargs):
        self._write('VOLT ' + str(voltage))

    def get_voltage(self, *args, **kwargs):
        return self._query('VOLT?')

    def set_current(self, current, *args, **kwargs):
        self._write('CURR ' + str(current))

    def get_current(self, *args, **kwargs):
        return self._query('CURR?')

    def set_max_current(self, current, *args, **kwargs):
        pass

    def get_max_current(self, *args, **kwargs):
        pass

    def set_max_voltage(self, voltage, *args, **kwargs):
        pass

    def get_max_volgate(self, *args, **kwargs):
        pass

    def set_over_voltage_protection(self, voltage, *args, **kwargs):
        pass

    def get_over_voltage_protection(self, *args, **kwargs):
        pass

class AgN67xx(PSBase, SimpleIviDcPwr):

    '''
    Obs: We got some errors trying to make it work with N6705C. For this model use specific class
    '''

    ID = 'AgN67xx'

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        super(AgN67xx, self).__init__(AGN67XX())
        self.Initialize(ResourceName=Address, IdQuery=True, Reset=reset, OptionString=f"simulate={simulate}")
        self.pyvisa_instr = self.visa_from_simple_instrument(Address)

    def _query(self, command, *args, **kwargs):
        return self.pyvisa_instr.query(command)

    def _write(self, command, *args, **kwargs):
        self.pyvisa_instr.write(command)

    def idn(self, *args, **kwargs):
        '''idn = gives us the identification Character of the Instrument
                syntax: idn()'''
        pass

    def clear(self):
        pass

    def output_on_off(self, state=False, *args, **kwargs):
        '''Syntax: output_on_off(arg1)
                arg1: Boolean
                    it will turn on output when True
                    it will turn off output when False
                    if no value is informed it will turn off'''
        if (state):
            self._write('OUTP ON')
        else:
            self._write('OUTP OFF')

    def set_voltage(self, voltage, *args, **kwargs):
        self._write('VOLT ' + str(voltage))

    def get_voltage(self, *args, **kwargs):
        return self._query('VOLT?')

    def set_current(self, current, *args, **kwargs):
        self._write('CURR ' + str(current))

    def get_current(self, *args, **kwargs):
        return self._query('CURR?')

    def set_max_current(self, current, *args, **kwargs):
        pass

    def get_max_current(self, *args, **kwargs):
        pass

    def set_max_voltage(self, voltage, *args, **kwargs):
        pass

    def get_max_volgate(self, *args, **kwargs):
        pass

    def set_over_voltage_protection(self, voltage, *args, **kwargs):
        pass

    def get_over_voltage_protection(self, *args, **kwargs):
        pass

class N6705C():
    '''
        Power Supply Models:
            N6705C
    '''

    ID = 'N6705C'
    channel = None
    arbFunc = None
    arbType = None

    def __init__(self, Address, *args, **kwargs) -> None:
        self.address = Address
        self.cmd = visa.ResourceManager().open_resource(Address)

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, delay=None, *args, **kwargs):
        if delay is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=delay)

    def GetChannel(self, Index=1, *args, **kwargs):
        newObj = N6705C(self.address)
        newObj.channel = int(Index)
        return newObj

    def Configure_VoltageLevel(self, Level, CurrentLimit, VoltageLimit=None, *args, **kwargs):
        self.set_voltage(voltage=Level)
        self.set_current(current=CurrentLimit)

    def Enable(self, state=False):
        self.output_on_off(output=state)

    def Measure_Current(self):
        return eval(self.get_current())

    def Measure_Voltage(self):
        return eval(self.get_voltage())

    def idn(self, *args, **kwargs):
        '''idn = gives us the identification Character of the Instrument
                syntax: idn()'''
        return self._query('*IDN?')

    def clear(self, *args, **kwargs):
        self._write('*CLS')

    def output_on_off(self, output=False):
        '''Syntax: output_on_off(arg1)
                arg1: Boolean
                    it will turn on output when True
                    it will turn off output when False
                    if no value is informed it will turn off'''
        if (output):
            self._write(f'OUTP 1, (@{self.channel})')
        else:
            self._write(f'OUTP 0, (@{self.channel})')

    def set_voltage(self, voltage, *args, **kwargs):
        self._write(f'VOLT {voltage}, (@{self.channel})')

    def get_voltage(self, *args, **kwargs):
        return self._query(f'VOLT? (@{self.channel})')

    def set_current(self, current, *args, **kwargs):
        self._write(f'CURR {current}, (@{self.channel})')

    def get_current(self, *args, **kwargs):
        return self._query(f'CURR? (@{self.channel})')

    def set_max_current(self, current, *args, **kwargs):
        self._write(f'CURR:PROT {current}, (@{self.channel})')

    def get_max_current(self, *args, **kwargs):
        return self._query(f'CURR:PROT? (@{self.channel})')

    def set_max_voltage(self, voltage, *args, **kwargs):
        self._write(f'VOLT:PROT {voltage}, (@{self.channel})')

    def get_max_volgate(self, *args, **kwargs):
        return self._query(f'VOLT:PROT? (@{self.channel})')

    def set_over_voltage_protection(self, voltage, *args, **kwargs):
        self._write(f'VOLT:PROT {voltage}, (@{self.channel})')

    def get_over_voltage_protection(self, *args, **kwargs):
        return self._query(f'VOLT:PROT? (@{self.channel})')

    def set_voltage_slew_rise(self, slewRate, *args, **kwargs):
        #@TODO
        pass

    def set_voltage_mode(self, mode, *args, **kwargs):
        self._write(f'VOLT:MODE {mode}, (@{self.channel})')

    def set_arb_function(self, function, *args, **kwargs):
        '''
        :param function: { STEP | RAMP | STAircase | SINusoid | PULSe | TRAPezoid | EXPonential | UDEFined | CDWell
                        | SEQuence | NONE }
        '''
        self.arbFunc = str(function)
        self._write(f'ARB:FUNC:SHAP {function}, (@{self.channel})')

    def set_arb_function_type(self, type, *args, **kwargs):
        '''
        :param type: { CURRent | VOLTage }
        '''
        self.arbType = str(type)
        self._write(f'ARB:FUNC:TYPE {type}, (@{self.channel})')

    def set_arb_top_level(self, level, *args, **kwargs):
        if self.arbFunc is None or self.arbType is None:
            print('One should first set_arb_function and set_arb_function_type before setting top level')
            return
        self._write(f'ARB:{self.arbType}:{self.arbFunc}:TOP:LEV {level}, (@{self.channel})')

    def set_arb_top_time(self, topT, *args, **kwargs):
        if self.arbFunc is None or self.arbType is None:
            print('One should first set_arb_function and set_arb_function_type before setting top level')
            return
        self._write(f'ARB:{self.arbType}:{self.arbFunc}:TOP:TIM {topT}, (@{self.channel})')

    def set_arb_start_time(self, time, *args, **kwargs):
        if self.arbFunc is None or self.arbType is None:
            print('One should first set_arb_function and set_arb_function_type before setting top level')
            return
        self._write(f'ARB:{self.arbType}:{self.arbFunc}:STAR:TIM {time}, (@{self.channel})')

    def set_arb_start_level(self, level, *args, **kwargs):
        if self.arbFunc is None or self.arbType is None:
            print('One should first set_arb_function and set_arb_function_type before setting top level')
            return
        self._write(f'ARB:{self.arbType}:{self.arbFunc}:STAR:LEV {level}, (@{self.channel})')

    def set_arb_end_time(self, endT, *args, **kwargs):
        if self.arbFunc is None or self.arbType is None:
            print('One should first set_arb_function and set_arb_function_type before setting top level')
            return
        self._write(f'ARB:{self.arbType}:{self.arbFunc}:END:TIM {endT}, (@{self.channel})')

    def set_arb_rise_time(self, riseT, *args, **kwargs):
        if self.arbFunc is None or self.arbType is None:
            print('One should first set_arb_function and set_arb_function_type before setting top level')
            return
        self._write(f'ARB:{self.arbType}:{self.arbFunc}:RTIM {riseT}, (@{self.channel})')

    def set_arb_fall_time(self, fallT, *args, **kwargs):
        if self.arbFunc is None or self.arbType is None:
            print('One should first set_arb_function and set_arb_function_type before setting top level')
            return
        self._write(f'ARB:{self.arbType}:{self.arbFunc}:FTIM {fallT}, (@{self.channel})')

    def set_trigger_source(self, source, *args, **kwargs):
        '''
        :param source: { BUS | EXTernal | IMMediate | PIN<n> | TRANsient<n> }
        '''
        self._write(f'TRIG:TRAN:SOUR {source}, (@{self.channel})')

    def trigger_transient(self, ch2='', ch3='', ch4='', *args, **kwargs):
        '''
        :param ch2: int channel to be added to trigger init
        :param ch3: int channel to be added to trigger init
        :param ch4: int channel to be added to trigger init
        '''
        command = f'(@{self.channel}'
        if ch2 != '':
            command = command + f',{ch2}'
        if ch3 != '':
            command = command + f',{ch3}'
        if ch4 != '':
            command = command + f',{ch4}'
        command = command + ')'
        self._write(f'INIT:TRAN {command}')

    def abort_transient(self):
        self._write(f'ABOR:TRAN (@{self.channel})')

    def set_arb_count(self, opt, *args, **kwargs):
        '''
        :param opt: { 1 - 16777216 | MIN | MAX | INFinite }
        '''
        self._write(f'ARB:COUN {opt}, (@{self.channel})')

class BK_9130B():
    '''
    BK Precision 9130B has 3 channels
    '''

    ID = 'BK_9130B'
    channel = None

    def __init__(self, Address, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        self.manufacturer = 'BK Precision'
        self.address = Address

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, d=None, *args, **kwargs):
        if d is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=d)

    def GetChannel(self, Index=1, *args, **kwargs):
        newObj = BK_9130B(self.address)
        newObj.channel = int(Index)
        return newObj

    def Configure_VoltageLevel(self, Level, CurrentLimit, VoltageLimit=None, *args, **kwargs):
        self.set_channel()
        self.set_voltage(voltage=Level)
        self.set_current(current=CurrentLimit)

    def Enable(self, state=False):
        self.set_channel()
        self.output_on_off(state=state)

    def Measure_Current(self):
        self.set_channel()
        return eval(self.get_current())

    def Measure_Voltage(self):
        self.set_channel()
        return eval(self.get_voltage())

    def idn(self):
        '''idn = gives us the identification Character of the Instrument
                syntax: idn()'''
        return self._query('*IDN?')

    def clear(self):
        self._write('*CLS')

    def output_on_off(self, state=False):
        '''Syntax: output_on_off(arg1)
                arg1: Boolean
                    it will turn on output when True
                    it will turn off output when False
                    if no value is informed it will turn off'''
        self.set_channel()
        if (state):
            self._write('CHAN:OUTP 1')
        else:
            self._write('CHAN:OUTP 0')

    def set_channel(self):
        self._write('INST CH' + str(self.channel))

    def set_voltage(self, voltage):
        self.set_channel()
        self._write('VOLT ' + str(voltage))

    def get_voltage(self):
        self.set_channel()
        return self._query('VOLT?')

    def set_current(self, current):
        self.set_channel()
        self._write('CURR ' + str(current))

    def get_current(self):
        self.set_channel()
        return self._query('CURR?')

    def set_max_current(self, current):
        self.set_channel()
        self._write('CURR:PROT ' + str(current))

    def get_max_current(self):
        self.set_channel()
        return self._query('CURR:PROT?')

    def set_max_voltage(self, voltage):
        self.set_channel()
        self._write('VOLT:PROT ' + str(voltage))

    def get_max_volgate(self):
        self.set_channel()
        return self._query('VOLT:PROT?')

    def set_over_voltage_protection(self, voltage):
        self.set_channel()
        self._write('VOLT:PROT ' + str(voltage))

    def get_over_voltage_protection(self):
        self.set_channel()
        return self._query('VOLT:PROT?')

class GWPST():
    '''
        GW PST, PSS AND PSH SERIES
    '''

    ID = 'GWPST'
    channel = None

    def __init__(self, Address, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        self.manufacturer = 'GW'
        self.address = Address

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, d=None, *args, **kwargs):
        if d is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=d)

    def GetChannel(self, Index=1, *args, **kwargs):
        newObj = GWPST(self.address)
        newObj.channel = int(Index)
        return newObj

    def Configure_VoltageLevel(self, Level, CurrentLimit, VoltageLimit=None, *args, **kwargs):
        self.set_channel()
        self.set_voltage(voltage=Level)
        self.set_current(current=CurrentLimit)

    def Enable(self, state=False):
        self.set_channel()
        self.output_on_off(state=state)

    def Measure_Current(self):
        self.set_channel()
        return eval(self.get_current())

    def Measure_Voltage(self):
        self.set_channel()
        return eval(self.get_voltage())

    def idn(self):
        '''idn = gives us the identification Character of the Instrument
                syntax: idn()'''
        return self._query('*IDN?')

    def clear(self):
        self._write('*CLS')

    def output_on_off(self, state=False):
        '''Syntax: output_on_off(arg1)
                arg1: Boolean
                    it will turn on output when True
                    it will turn off output when False
                    if no value is informed it will turn off'''
        if (state):
            self._write('OUTP:STAT 1')
        else:
            self._write('OUTP:STAT 0')

    def set_channel(self):
        # channel number is part of command
        pass

    def set_voltage(self, voltage):
        self.set_channel()
        self._write(f'CHAN{self.channel}:VOLT ' + str(voltage))

    def get_voltage(self):
        self.set_channel()
        return self._query(f'CHAN{self.channel}:MEAS:VOLT?')

    def set_current(self, current):
        self.set_channel()
        self._write(f'CHAN{self.channel}:CURR ' + str(current))

    def get_current(self):
        self.set_channel()
        return self._query(f'CHAN{self.channel}:MEAS:CURR?')

    def set_max_current(self, current):
        self.set_channel()
        self._write(f'CHAN{self.channel}:PROT:CURR ' + str(current))

    def get_max_current(self):
        self.set_channel()
        return self._query(f'CHAN{self.channel}:PROT:CURR?')

    def set_max_voltage(self, voltage):
        self.set_channel()
        self._write(f'CHAN{self.channel}:PROT:VOLT ' + str(voltage))

    def get_max_volgate(self):
        self.set_channel()
        return self._query(f'CHAN{self.channel}:PROT:VOLT?')

    def set_over_voltage_protection(self, voltage):
        self.set_channel()
        self._write(f'CHAN{self.channel}:PROT:VOLT ' + str(voltage))

    def get_over_voltage_protection(self):
        self.set_channel()
        return self._query(f'CHAN{self.channel}:PROT:VOLT?')

class HMPSeries():
    '''
    Rhode & Schwartz HMP
    '''

    ID = 'HMPSeries'
    channel = None

    def __init__(self, Address, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        self.manufacturer = 'Rhode and Schwartz'
        self.address = Address

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, d=None, *args, **kwargs):
        if d is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=d)

    def GetChannel(self, Index=1, *args, **kwargs):
        newObj = HMPSeries(self.address)
        newObj.channel = int(Index)
        return newObj

    def Configure_VoltageLevel(self, Level, CurrentLimit, VoltageLimit=None, *args, **kwargs):
        self.set_channel()
        self.set_voltage(voltage=Level)
        self.set_current(current=CurrentLimit)

    def Enable(self, state=False):
        self.set_channel()
        self.output_on_off(state=state)

    def Measure_Current(self):
        self.set_channel()
        return eval(self.get_current())

    def Measure_Voltage(self):
        self.set_channel()
        return eval(self.get_voltage())

    def idn(self):
        '''idn = gives us the identification Character of the Instrument
                syntax: idn()'''
        return self._query('*IDN?')

    def clear(self):
        self._write('*CLS')

    def output_on_off(self, state=False):
        '''Syntax: output_on_off(arg1)
                arg1: Boolean
                    it will turn on output when True
                    it will turn off output when False
                    if no value is informed it will turn off'''
        self.set_channel()
        if (state):
            self._write('OUTP:SEL 1')
        else:
            self._write('OUTP:SEL 0')

    def set_channel(self):
        '''
        Selects the channel by number
        :return: None
        '''
        self._write(f'INST:NSEL {self.channel}')

    def set_voltage(self, voltage):
        '''
        Set Voltage Level
        :param voltage: float
        :return: None
        '''
        self.set_channel()
        self._write('VOLT ' + str(voltage))

    def get_voltage(self):
        self.set_channel()
        return self._query('VOLT?')

    def set_current(self, current):
        self.set_channel()
        self._write('CURR ' + str(current))

    def get_current(self):
        self.set_channel()
        return self._query('CURR?')

    def set_max_current(self, current):
        '''
        Apparently this model does not have max current or current protection
        :param current: float
        :return: None
        '''
        pass

    def get_max_current(self):
        '''
        Apparently this model does not have current max or current protection.
        :return: This function will return the set current
        '''
        self.set_channel()
        return self._query('CURR?')

    def set_max_voltage(self, voltage):
        self.set_channel()
        self._write('VOLT:PROT ' + str(voltage))

    def get_max_volgate(self):
        self.set_channel()
        return self._query('VOLT:PROT?')

    def set_over_voltage_protection(self, voltage):
        self.set_channel()
        self._write('VOLT:PROT ' + str(voltage))

    def get_over_voltage_protection(self):
        self.set_channel()
        return self._query('VOLT:PROT?')

class PWS4000Series():
    '''

    '''

    ID = 'PWS4000'
    channel = None

    def __init__(self, Address, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        self.manufacturer = 'Tektronix'
        self.address = Address

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, d=None, *args, **kwargs):
        if d is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=d)

    def GetChannel(self, Index=1, *args, **kwargs):
        newObj = BK_9130B(self.address)
        newObj.channel = int(Index)
        return newObj

    def Configure_VoltageLevel(self, Level, CurrentLimit, VoltageLimit=None, *args, **kwargs):
        self.set_channel()
        self.set_voltage(voltage=Level)
        self.set_current(current=CurrentLimit)

    def Enable(self, state=False):
        self.set_channel()
        self.output_on_off(state=state)

    def Measure_Current(self):
        self.set_channel()
        return eval(self.get_current())

    def Measure_Voltage(self):
        self.set_channel()
        return eval(self.get_voltage())

    def idn(self):
        '''idn = gives us the identification Character of the Instrument
                syntax: idn()'''
        return self._query('*IDN?')

    def clear(self):
        self._write('*CLS')

    def output_on_off(self, state=False):
        '''Syntax: output_on_off(arg1)
                arg1: Boolean
                    it will turn on output when True
                    it will turn off output when False
                    if no value is informed it will turn off'''
        self.set_channel()
        if (state):
            self._write('SOUR:OUTP 1')
        else:
            self._write('SOUR:OUTP 0')

    def set_channel(self):
        # Apparently this model only has one channel
        pass

    def set_voltage(self, voltage):
        self.set_channel()
        self._write('VOLT ' + str(voltage))

    def get_voltage(self):
        self.set_channel()
        return self._query('VOLT?')

    def set_current(self, current):
        self.set_channel()
        self._write('CURR ' + str(current))

    def get_current(self):
        self.set_channel()
        return self._query('CURR?')

    def set_max_current(self, current):
        #Apparently this model does not have current protection
        pass

    def get_max_current(self):
        # Apparently this model does not have current protection
        pass

    def set_max_voltage(self, voltage):
        self.set_channel()
        self._write('VOLT:PROT ' + str(voltage))

    def get_max_volgate(self):
        self.set_channel()
        return self._query('VOLT:PROT?')

    def set_over_voltage_protection(self, voltage):
        self.set_channel()
        self._write('VOLT:PROT ' + str(voltage))

    def get_over_voltage_protection(self):
        self.set_channel()
        return self._query('VOLT:PROT?')


# endregion

if __name__ == '__main__':
    vin = Xantrex_XHR_Series('GPIB0::2::INSTR')
    print(vin._query('ID?'))