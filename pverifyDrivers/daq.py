########################################################
# Supported Models:                                    #
#   Keithley 2700 - not supported by ifx-pyverify      #
#   Keithley DAQ6510 - not supported by ifx-pyverify   #
#                                                      #
########################################################

from pverify.drivers.SimplifiedLabInstruments.SimpleIviDmm import SimpleIviDmm
from pverify.drivers.Dmm.Ag34970 import Ag34970

import pyvisa as visa
from time import sleep

class DaqBase:
    '''
    Base DAQ class for initialization of IFX-PyVerify drivers and common functions that work the same throughout the
    libraris.
    '''

    def __init__(self, callback=None):
        '''
        Initializes IFX-PyVerify driver
        :param callback: Callback function from IFX-PyVerify library that should be initialized.
        '''
        if callback is None:
            super(DaqBase, self).__init__()
        else:
            super(DaqBase, self).__init__(callback)

    def __del__(self):
        '''
        Destructor to remove object when done working.
        :return: None
        '''
        try:
            self.pyvisa_instr.clear()
            self.pyvisa_instr.close()
        except:
            pass

    def visa_from_simple_instrument(self, addr):
        '''
        Creates a pyvisa object to allow direct SCPI commands to be sent.
        :param addr: Instrument Address { GPIB | TCPIP | USB | RS232 }
        :return: a VISA resource instance that shares the session with the supplied IIviInstrument instance.
        '''
        rm = visa.ResourceManager()
        _pyvisa_instr = rm.open_resource(addr)
        return _pyvisa_instr

class AG34970(DaqBase, Ag34970):
    '''
    Supported Instruments:
        34970A, 34972A
    '''

    def __init__(self, Address, *args, **kwargs):
        '''
        Initialize AG34970 object extending the Base Class and IFX-PyVerify drivers
        :param Address: Instrument Address { GPIB | TCPIP | USB | RS232 }
        :param Reset (optinal): (bool) Default set to True. It resets the instruments when initializing the object.
        :param Simulate (optional): (bool) Default set to False. It creates a simulation behavior for IFX-PyVerify
        related functions and drivers. Does not work for non IFX-PyVerify functions and libraries.
        '''
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        super(AG34970, self).__init__()
        self.Initialize(ResourceName=Address, IdQuery=True, Reset=reset, OptionString="simulate=" + str(simulate))
        self.pyvisa_instr = self.visa_from_simple_instrument(Address)

    def _write(self, command, *args, **kwargs):
        '''
        Private function to pass commands for the pyvisa object of the instrument.
        :param command: The SCPI command that should be sent to the instruments in a write method
        :return: None
        '''
        self.pyvisa_instr.write(command)

    def _query(self, command, d=None, *args, **kwargs):
        '''
        Private function to pass commands for the pyvisa object of the instrument.
        :param command: The SCPI command that should be sent to the instruments in a query method
        :param d (optional): delay in seconds that the query command should wait for a reply before timing out.
        :return: String with the value returned by the query command
        '''
        if d is None:
            return self.pyvisa_instr.query(command)
        else:
            return self.pyvisa_instr.query(command, delay=d)

    def reset_keithley(self, *args, **kwargs):
        '''
        Sequence of SCPI commands to reset, clear, clear errors and clear buffer
        :return: None
        '''
        self._write('*RST')
        self._write('*CLS')
        self._write('STAT:PRES')
        self._write('TRAC:CLE')

    def clear_buffer(self, *args, **kwargs):
        '''
        Command to clear buffer only.
        :return: None
        '''
        self._write('TRAC:CLE')

    def select_function(self, function, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | VOLTage:AC | CURRent[:DC] | CURRent:AC
                            | RESistance | FRESistance | TEMPerature | FREQuency
                            | PERiod | CONTinuity }
        :type function: string
        :param channel: simple channel 101 or range of channels (@101:120)
        :type channel: string
        :return: None
        '''
        self._write('FUNC "' + str(function) + '", ' + str(channel))

    def select_range(self, function, range, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | VOLTage:AC | CURRent[:DC] | CURRent:AC
                            | RESistance | FRESistance }
        :param range:   { AUTO <b> | UPPer <n> }
                        <b> ON | OFF
                        <n> range from 0 to 1010
        :param channel: simple channel 101 or range of channels (@101:120)
        :return: None
        '''
        self._write(str(function) + ':RANG:' + str(range) + ', ' + str(channel))

    def route_to_scan(self, channel, *args, **kwargs):
        '''
        :param channel: simple channel 101 or range of channels (@101:120)
        :return: None
        '''
        self._write('ROUT:SCAN ' + str(channel))

    def enable_scan(self, option, *args, **kwargs):
        '''
        :param option: ON | OFF
        :return: None
        '''
        #apparently not needed for this model. It will work by just setting a list of channels for scan
        pass

    def number_of_channels_to_scan(self, num, *args, **kwargs):
        '''
        :param num: number of channels to scan. (integer)
        '''
        #Apparently there is no number os channels to scan. It relies on scan list
        pass

    def data_elements(self, reading=0, units=0, tstamp=0, rnumber=0, channel=0, limits=0, *args, **kwargs):
        '''
        :param reading: DMM reading (always on)
        :param units: Units
        :param tstamp: Time Stamp
        :param rnumber: Reading Number (it does not exist for this model)
        :param channel: channel number
        :param limits: Limits reading (it does not exist for this model)
        '''
        if units:
            self._write('FORM:READ:UNIT ON')
        else:
            self._write('FORM:READ:UNIT OFF')
        if tstamp:
            self._write('FORM:READ:TIME ON')
        else:
            self._write('FORM:READ:TIME OFF')
        if channel:
            self._write('FORM:READ:CHAN ON')
        else:
            self._write('FORM:READ:CHAN OFF')




        #@TODO
        pass

    def set_nplc(self, function, value, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | RESistance | TEMPerature | VOLTage[:DC]:RATio | FRESistance | CURRent[:DC] | DIODe }
        :param value: { MIN | MAX | 0.02 | 0.2 | 1 | 2 | 10 | 20 | 100 | 200 }
        :param channel: example -> "(@101)" or "(@101:120)"
        '''
        if value.upper() == 'MIN':
            value = '0.02'
        elif value.upper() == 'MAX':
            value = '200'
        elif value.upper() == 'DEF':
            value = '2'
        self._write(f'{function}:NPLC {value}, {channel}')

    def set_apperture(self, function, value, channel, *args, **kwargs):
        '''
        Set integration rate in seconds
        :param function: { VOLT:DC | VOLT:AC | CURR:DC | CURR:AC | RES | FRES | TEMP | FREQ }
        :param value: [300e-6, 1]
        :param channel: channel or channel list to be applied.
        :return: None
        '''
        if value.upper() == 'MIN':
            value = '1.67e-4'
        elif value.upper() == 'MAX':
            value = '1'
        elif value.upper() == 'DEF':
            value = '1'
        self._write(f'{function}:APER {value}, {channel}')

    def read(self, *args, **kwargs):
        '''
        Stops any going reading and fetches data from buffer.
        :return: String with data returned from data acquisition device (coma separated)
        '''
        delay = kwargs['delay'] if 'delay' in kwargs else None
        if delay is not None:
            self._write('ABOR')
            self._write('INIT')
            sleep(float(delay))
            return self._query('FETCH?')
        else:
            self._write('ABOR')
            self._write('INIT')
            return self._query('FETCH?')

class Keithley3700:

    def __init__(self, Address, *args, **kwargs):
        '''
        Initialize Keithley3700 object
        :param Address: Instrument Address { GPIB | TCPIP | USB | RS232 }
        :param Reset (optinal): (bool) Default set to True. It resets the instruments when initializing the object.
        :return None
        '''
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        self.cmd = visa.ResourceManager().open_resource(Address)
        if reset:
            self.reset_keithley()

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, d=None, *args, **kwargs):
        if d is None:
            self.cmd.query(command)
        else:
            self.cmd.query(command, delay=d)

    def reset_keithley(self, *args, **kwargs):
        self._write('scan.reset()')
        self._write('display.clear()')
        self._write('clearcache()')
        self._write('dmm.reset("all")')
        self._write('errorqueue.clear()')
        self._write('eventlog.clear()')
        self._write('reset(true)')

    def clear_buffer(self, *args, **kwargs):
        self._write('TRAC:CLE')

    def select_function(self, function, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | VOLTage:AC | CURRent[:DC] | CURRent:AC
                            | RESistance | FRESistance | TEMPerature | FREQuency
                            | PERiod | CONTinuity }
        :type function: string
        :param channel: simple channel 101 or range of channels (@101:120)
        :type channel: string
        '''
        self._write('FUNC "' + str(function) + '", ' + str(channel))

    def select_range(self, function, range, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | VOLTage:AC | CURRent[:DC] | CURRent:AC
                            | RESistance | FRESistance }
        :param range:   { AUTO <b> | UPPer <n> }
                        <b> ON | OFF
                        <n> range from 0 to 1010
        :param channel: simple channel 101 or range of channels (@101:120)
        '''
        self._write(str(function) + ':RANG:' + str(range) + ', ' + str(channel))

    def route_to_scan(self, channel, *args, **kwargs):
        '''
        :param channel: simple channel 101 or range of channels (@101:120)
        '''
        self._write('ROUT:SCAN ' + str(channel))

    def enable_scan(self, option, *args, **kwargs):
        '''
        :param option: ON | OFF
        '''
        #@TODO
        pass

    def number_of_channels_to_scan(self, num, *args, **kwargs):
        '''
        :param num: number of channels to scan. (integer)
        '''
        #@TODO
        pass

    def data_elements(self, reading=0, units=0, tstamp=0, rnumber=0, channel=0, limits=0, *args, **kwargs):
        #@TODO
        pass

    def set_nplc(self, function, value, channel, *args, **kwargs):
        #@ TODO
        pass

    def read(self, *args, **kwargs):
        num = kwargs['num'] if 'num' in kwargs else 20
        self._write('INIT')
        sleep(1)
        mystr = 'TRAC:DATA? 1, ' + str(num)
        return self._query(mystr)

class Keithley2700:

    def __init__(self, Address, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)

    def _write(self, command):
        self.cmd.write(command)

    def _query(self, command, d=None):
        if d is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=d)

    def reset_keithley(self, *args, **kwargs):
        self._write('*RST')
        self._write('*CLS')
        self._write('STAT:PRES')
        self._write('TRAC:CLE')

    def clear_buffer(self, *args, **kwargs):
        self._write('TRAC:CLE')

    def select_function(self, function, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | VOLTage:AC | CURRent[:DC] | CURRent:AC
                            | RESistance | FRESistance | TEMPerature | FREQuency
                            | PERiod | CONTinuity }
        :type function: string
        :param channel: simple channel 101 or range of channels (@101:120)
        :type channel: string
        '''
        self._write('FUNC "' + str(function) + '", ' + str(channel))

    def select_range(self, function, range, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | VOLTage:AC | CURRent[:DC] | CURRent:AC
                            | RESistance | FRESistance }
        :param range:   { AUTO <b> | UPPer <n> }
                        <b> ON | OFF
                        <n> range from 0 to 1010
        :param channel: simple channel 101 or range of channels (@101:120)
        '''
        self._write(str(function) + ':RANG:' + str(range) + ', ' + str(channel))

    def route_to_scan(self, channel, *args, **kwargs):
        '''
        :param channel: simple channel 101 or range of channels (@101:120)
        '''
        self._write('ROUT:SCAN ' + str(channel))

    def enable_scan(self, option, *args, **kwargs):
        '''
        :param option: ON | OFF
        '''
        if option.lower() == 'on':
            self._write('ROUT:SCAN:LSEL INT')
        else:
            self._write('ROUT:SCAN:LSEL NONE')

    def number_of_channels_to_scan(self, num, *args, **kwargs):
        '''
        :param num: number of channels to scan. (integer)
        '''
        self._write('SAMP:COUN ' + str(num))

    def data_elements(self, reading=0, units=0, tstamp=0, rnumber=0, channel=0, limits=0, *args, **kwargs):
        '''
        :param reading: DMM reading
        :param units: Units
        :param tstamp: Time Stamp
        :param rnumber: Reading Number
        :param channel: channel number
        :param limits: Limits reading
        '''
        read = 'READ' if reading else ''
        unit = 'UNIT' if units else ''
        tst = 'TST' if tstamp else ''
        rnum = 'RNUM' if rnumber else ''
        ch = 'CHAN' if channel else ''
        lim = 'LIM' if limits else ''
        option = [read, unit, tst, rnum, ch, lim]
        count = 0
        finalString = ''
        for opt in option:
            if opt != '':
                if count:
                    finalString += ', ' + opt
                else:
                    finalString += opt
                count += 1
        self._write('FORM:ELEM ' + finalString)

    def set_nplc(self, function, value, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | RESistance | TEMPerature | VOLTage[:DC]:RATio | FRESistance | CURRent[:DC] | DIODe }
        :param value: { DEF | MIN | MAX | 0.01 to 60 }
        :param channel: example -> "(@101)" or "(@101:120)"
        '''
        if value.upper() == 'MIN':
            value = '0.01'
        elif value.upper() == 'MAX':
            value = '60'
        elif value.upper() == 'DEF':
            value = '5'
        self._write(f'{function}:NPLC {value}, {channel}')

    def set_apperture(self, function, value, channel, *args, **kwargs):
        '''
        Set integration rate in seconds
        :param function: { VOLT:DC | VOLT:AC | CURR:DC | CURR:AC | RES | FRES | TEMP | FREQ }
        :param value: [1.67e-4, 1]
        :param channel: channel or channel list to be applied.
        :return: None
        '''
        if value.upper() == 'MIN':
            value = '1.67e-4'
        elif value.upper() == 'MAX':
            value = '1'
        elif value.upper() == 'DEF':
            value = '1'
        self._write(f'{function}:APER {value}, {channel}')

    def read(self, *args, **kwargs):
        delay = kwargs['delay'] if 'delay' in kwargs else None
        if delay is not None:
            self._write('ABOR')
            self._write('INIT')
            sleep(float(delay))
            return self._query('FETCH?')
        else:
            self._write('ABOR')
            self._write('INIT')
            return self._query('FETCH?')

class Keithley6510:

    def __init__(self, Address, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        self.dataElements = 'READ'

    def _write(self, command):
        self.cmd.write(command)

    def _query(self, command, d=None, *args, **kwargs):
        if d is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=d)

    def reset_keithley(self, *args, **kwargs):
        self._write('*RST')
        self._write('*CLS')
        self._write('STAT:PRES')
        self._write('TRAC:CLE')

    def clear_buffer(self, *args, **kwargs):
        self._write('TRAC:CLE')

    def select_function(self, function, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | VOLTage:AC | CURRent[:DC] | CURRent:AC
                            | RESistance | FRESistance | TEMPerature | FREQuency
                            | PERiod | CONTinuity }
        :type function: string
        :param channel: simple channel 101 or range of channels (@101:120)
        :type channel: string
        '''
        self._write('FUNC "' + str(function) + '", ' + str(channel))

    def select_range(self, function, range, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | VOLTage:AC | CURRent[:DC] | CURRent:AC
                            | RESistance | FRESistance }
        :param range:   { AUTO <b> | UPPer <n> }
                        <b> ON | OFF
                        <n> range from 0 to 1010
        :param channel: simple channel 101 or range of channels (@101:120)
        '''
        self._write(str(function) + ':RANG:' + str(range) + ', ' + str(channel))

    def route_to_scan(self, channel, *args, **kwargs):
        '''
        :param channel: simple channel 101 or range of channels (@101:120)
        '''
        self._write('ROUT:SCAN ' + str(channel))

    def enable_scan(self, option, *args, **kwargs):
        '''
        :param option: ON | OFF
        '''
        #@TODO
        pass

    def number_of_channels_to_scan(self, num, *args, **kwargs):
        '''
        :param num: number of channels to scan. (integer)
        '''
        # This model does not have to set the number of channels to scan. This value is passed on the read command
        pass

    def data_elements(self, reading=0, units=0, tstamp=0, rnumber=0, channel=0, limits=0, *args, **kwargs):
        '''
                :param reading: DMM reading
                :param units: Units
                :param tstamp: Time Stamp
                :param rnumber: Reading Number
                :param channel: channel number
                :param limits: Limits reading
                '''
        read = 'READ' if reading else ''
        unit = 'UNIT' if units else ''
        tst = 'TST' if tstamp else ''
        rnum = 'RNUM' if rnumber else ''
        ch = 'CHAN' if channel else ''
        lim = 'LIM' if limits else ''
        option = [read, unit, tst, ch]
        count = 0
        finalString = ''
        for opt in option:
            if opt != '':
                if count:
                    finalString += ', ' + opt
                else:
                    finalString += opt
                count += 1
        self.dataElement = finalString

    def set_nplc(self, function, value, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | RESistance | TEMPerature | VOLTage[:DC]:RATio | FRESistance | CURRent[:DC] | DIODe }
        :param value: { DEF | MIN | MAX | 0.0005 to 15 }
        :param channel: example -> "(@101)" or "(@101:120)"
        '''
        self._write(f'{function}:NPLC {value}, {channel}')

    def set_apperture(self, function, value, channel, *args, **kwargs):
        '''
        Set integration rate in seconds
        :param function: { VOLT:DC | VOLT:AC | CURR:DC | CURR:AC | RES | FRES | TEMP | FREQ }
        :param value: [8.333e-6, 0.25]
        :param channel: channel or channel list to be applied.
        :return: None
        '''
        if value.upper() == 'MIN':
            value = '8.333e-6'
        elif value.upper() == 'MAX':
            value = '0.25'
        elif value.upper() == 'DEF':
            value = '0.25'
        self._write(f'{function}:APER {value}, {channel}')

    def read(self, *args, **kwargs):
        delay = kwargs['delay'] if 'delay' in kwargs else None
        start = kwargs['start'] if 'start' in kwargs else 1
        num = kwargs['num'] if 'num' in kwargs else 20
        buffer = kwargs['buffer'] if 'buffer' in kwargs else 'defbuffer1'
        mystr = f'TRAC:DATA? {start}, {num}, "{buffer}", {self.dataElements}'
        if delay is not None:
            self._write('ABOR')
            self._write('INIT')
            sleep(float(delay))
            return self._query(mystr)
        else:
            self._write('ABOR')
            self._write('INIT')
            return self._query(mystr)


class DAQ970A:
    '''
    Keysight DAQ970A/DAQ973A
    '''

    def __init__(self, Address, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        self.dataElements = 'READ'

    def _write(self, command):
        self.cmd.write(command)

    def _query(self, command, d=None, *args, **kwargs):
        if d is None:
            return self.cmd.query(command)
        else:
            return self.cmd.query(command, delay=d)

    def reset_keithley(self, *args, **kwargs):
        self._write('*RST')
        self._write('*CLS')
        self._write('STAT:PRES')

    def clear_buffer(self, *args, **kwargs):
        pass
        # did not find specific command to clear buffer. *RST will do, but it would also reset scan list etc.
        return

    def select_function(self, function, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | VOLTage:AC | CURRent[:DC] | CURRent:AC
                            | RESistance | FRESistance | TEMPerature | FREQuency
                            | PERiod | CONTinuity }
        :type function: string
        :param channel: simple channel 101 or range of channels (@101:120)
        :type channel: string
        '''
        self._write(f'CONF:{function}, {channel}')

    def select_range(self, function, range, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | VOLTage:AC | CURRent[:DC] | CURRent:AC
                            | RESistance | FRESistance }
        :param range:   { AUTO <b> | UPPer <n> }
                        <b> ON | OFF
                        <n> range from 0 to 1010
        :param channel: simple channel 101 or range of channels (@101:120)
        '''
        self._write(str(function) + ':RANG:' + str(range) + ', ' + str(channel))

    def route_to_scan(self, channel, *args, **kwargs):
        '''
        :param channel: simple channel 101 or range of channels (@101:120)
        '''
        self._write('ROUT:SCAN ' + str(channel))

    def enable_scan(self, option, *args, **kwargs):
        '''
        :param option: ON | OFF
        '''
        #@TODO
        pass

    def number_of_channels_to_scan(self, num, *args, **kwargs):
        '''
        :param num: number of channels to scan. (integer)
        '''
        # This model does not have to set the number of channels to scan. This value is passed on the read command
        pass

    def data_elements(self, reading=0, units=0, tstamp=0, rnumber=0, channel=0, limits=0, *args, **kwargs):
        '''
            Setting each parameter to 0 will disable and setting to 1 will include the information on output format
                :param reading: DMM reading
                :param units: Units
                :param tstamp: Time Stamp
                :param rnumber: Reading Number
                :param channel: channel number
                :param limits: Limits reading
                :param alarm: alarm info
        '''
        alarm = kwargs['alarm'] if 'alarm' in kwargs else 0
        self._write(f'FORM:READ:ALAR {alarm}')
        self._write(f'FORM:READ:CHAN {channel}')
        self._write(f'FORM:READ:TIME {tstamp}')
        self._write(f'FORM:READ:TIME:TYPE REL')
        self._write(f'FORM:READ:UNIT {units}')
        self._write(f'FORM:DATA ASC')

    def set_nplc(self, function, value, channel, *args, **kwargs):
        '''
        :param function: { VOLTage[:DC] | RESistance | TEMPerature | VOLTage[:DC]:RATio | FRESistance | CURRent[:DC] | DIODe }
        :param value: { DEF | MIN | MAX | 0.0005 to 15 }
        :param channel: example -> "(@101)" or "(@101:120)"
        '''
        self._write(f'{function}:NPLC {value}, {channel}')

    def set_apperture(self, function, value, channel, *args, **kwargs):
        '''
        Set integration rate in seconds
        :param function: { VOLT:DC | VOLT:AC | CURR:DC | CURR:AC | RES | FRES | TEMP | FREQ }
        :param value: [8.333e-6, 0.25]
        :param channel: channel or channel list to be applied.
        :return: None
        '''
        if value.upper() == 'MIN':
            value = '8.333e-6'
        elif value.upper() == 'MAX':
            value = '0.25'
        elif value.upper() == 'DEF':
            value = '0.25'
        self._write(f'{function}:APER {value}, {channel}')

    def read(self, *args, **kwargs):
        delay = kwargs['delay'] if 'delay' in kwargs else None
        if delay is not None:
            self._write('ABOR')
            self._write('INIT')
            sleep(float(delay))
            return self._query('FETCH?')
        else:
            self._write('ABOR')
            self._write('INIT')
            return self._query('FETCH?')



if __name__ == '__main__':
    # k = Keithley6510('USB0::0x05E6::0x6510::04531298::INSTR')
    # k.reset_keithley()
    # k._write('FUNC "VOLT:DC", (@101:120)')
    # k._write('VOLT:DC:RANG:AUTO ON, (@101:120)')
    # k._write('ROUT:SCAN (@101:120)')
    # k.read()
    k = AG34970('USB0::0x05E6::0x6510::04531298::INSTR')