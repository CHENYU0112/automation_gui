# BEGIN - IFX-PYVERIFY IMPORTS
from pyvisa.resources.messagebased import MessageBasedResource as _MessageBasedResource
from pverify.drivers.ProgrammableLoad.chr6310 import IIfxELoad
from pverify.drivers.ProgrammableLoad.chr6310.chr6310_simple import chr6310Simple
# END

# BEGIN AUX IMPORTS
from pverify.drivers.BaseInstrument import BaseVisaInstrument
import pyvisa as _pyvisa
from time import sleep
# END


class LoadBase:

    def __init__(self, callback):
        super(LoadBase, self).__init__(callback)

    def visa_from_simple_instrument(self):
        """
        This method returns a VISA resource instance that shares the session with the supplied IIviInstrument instance.
        Repeated calls to this method will return the previously instantiated VISA resource.

        Parameters
        ----------
        self: SimpleInstrument
            A SimpleInstrument instance from one of the pverify driver library.

        Returns
        -------
        _visa_instrument: MessageBasedResource
            A VISA resource instance.
        """
        resource_name = "LPT1"
        _resource_manager = _pyvisa.ResourceManager()
        _visa_instrument = _MessageBasedResource(_resource_manager, resource_name)
        # Due to changes in the internal PyVerify structure following workaround is needed to be still backwards
        # compatible
        try:
            # Inicio Version 1.2.2.0 and earlier
            _visa_instrument.session = self._lowlevel_driver.vi
        except AttributeError:
            # Since/For Inicio Version 1.3.3.0
            _visa_instrument.session = self._lowlevel_driver.dllwrap._vi
        # Note: changing read_termination to "\n" will break screenshot capturing

        return _visa_instrument

    def get_interface(self):
        return self.lld.interface

class Chroma631x(LoadBase, chr6310Simple):

    option = None
    ID = 'Crhoma631x'

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        super(Chroma631x, self).__init__(IIfxELoad())
        self.Initialize(ResourceName=Address, IdQuery=False, Reset=reset)
        self.interface = self.get_interface()

    def _write(self, command):
        self.interface.vi_write(command)

    def _query(self, command):
        return self.interface.vi_query(command)

    def output(self, state='OFF', *args, **kwargs):
        if state.lower() == 'off':
            self._write('LOAD OFF')
        else:
            self._write('LOAD ON')

    def set_mode(self, mode, *args, **kwargs):
        '''
        :param mode: load mode { CCL | CCH | CCDL | CCDH | CRL | CRH | CV }
        :type: string
        :return: None
        '''
        self._write('MODE ' + str(mode))

    def set_channel(self, index=1, *args, **kwargs):
        self._write('CHAN ' + str(index))

    def set_current(self, option, value, *args, **kwargs):
        '''
        :param option: { STATic | DYNamic }
        :type: string
        :param value: value of current to set
        :type: float
        :return: None
        '''
        line = kwargs['line'] if 'line' in kwargs else 'L1'
        self._write(f'CURR:{option}:{line} {value}')
        self.option = option.upper()

    def set_rise_fall(self, rise, fall, *args, **kwargs):
        '''
        :param rise: A/us
        :param fall: A/us
        '''
        self._write(f'CURR:{self.option}:RISE {rise}')
        self._write(f'CURR:{self.option}:FALL {fall}')

    def set_duration(self, t1, t2, *args, **kwargs):
        '''
        :param t1: ms
        :param t2: ms
        '''
        self._write(f'CURR:DYN:T1 {t1}')
        self._write(f'CURR:DYN:T2 {t2}')

class Chroma63600:

    option = None
    ID = 'Crhoma63600'
    mode = None
    currentLevel = None

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        self.interface = _pyvisa.ResourceManager().open_resource(Address)
        if reset:
            self.interface.write('*RST')

    def _write(self, command):
        self.interface.vi_write(command)

    def _query(self, command):
        return self.interface.vi_query(command)

    def output(self, state='OFF', *args, **kwargs):
        if state.lower() == 'off':
            self._write('LOAD OFF')
        else:
            self._write('LOAD ON')

    def set_mode(self, mode, *args, **kwargs):
        '''
        :param mode: load mode { CCL | CCH | CCDL | CCDH | CRL | CRH | CV }
        :type: string
        :return: None
        '''
        self._write('MODE ' + str(mode))

    def set_channel(self, index=1, *args, **kwargs):
        self._write('CHAN ' + str(index))

    def set_current(self, option, value, *args, **kwargs):
        '''
        :param option: { STATic | DYNamic }
        :type: string
        :param value: value of current to set
        :type: float
        :return: None
        '''
        line = kwargs['line'] if 'line' in kwargs else 'L1'
        self._write(f'CURR:{option}:{line} {value}')
        self.option = option.upper()

    def set_rise_fall(self, rise, fall, *args, **kwargs):
        '''
        :param rise: A/us
        :param fall: A/us
        '''
        self._write(f'CURR:{self.option}:RISE {rise}')
        self._write(f'CURR:{self.option}:FALL {fall}')

    def set_duration(self, t1, t2, *args, **kwargs):
        '''
        :param t1: ms
        :param t2: ms
        '''
        self._write(f'CURR:DYN:T1 {t1}')
        self._write(f'CURR:DYN:T2 {t2}')

class XBLSeries():

    option = None
    ID = 'XBLSeries'
    mode = None
    currentLevel = None

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        self.interface = _pyvisa.ResourceManager().open_resource(Address)
        if reset:
            self.interface.write('*RST')

    def _write(self, command, *args, **kwargs):
        self.interface.write(command)

    def _query(self, command, *args, **kwargs):
        d = kwargs['delay'] if 'delay' in kwargs else None
        if d:
            return self.interface.query(command, delay=d)
        else:
            return self.interface.query(command)

    def output(self, state='OFF', *args, **kwargs):
        if state.lower() == 'off':
            self._write('LOAD OFF')
        else:
            self._write('LOAD ON')

    def set_mode(self, mode, *args, **kwargs):
        '''
        :param mode: load mode { CCL | CCH | CCDL | CCDH | CRL | CRH | CV }
        :type: string
        :return: None
        '''
        modes = {
            'CCL' : 'CI',
            'CCH' : 'CI',
            'CCDL' : 'CI',
            'CCDH' : 'CI',
            'CRL' : 'CR LOW',
            'CRH' : 'CR HIGH',
            'CV' : 'CV',
        }
        self.mode = modes[mode]

    def set_channel(self, index=1, *args, **kwargs):
        # apparently no channel selection for this model
        pass

    def set_current(self, option, value, *args, **kwargs):
        '''
        :param option: { STATic | DYNamic }
        :type: string
        :param value: value of current to set
        :type: float
        :return: None
        '''
        self._write(f'{self.mode} {value}')
        self.currentLevel = float(value)
        self.option = option.upper()
        sleep(1.5)

    def set_rise_fall(self, rise, fall, *args, **kwargs):
        '''
        This model uses slew time instead of rate. To make it compatible to other models and function calls the current
        level must be set first. Then when applying a rate in A/us the function will convert that into microseconds to
        set the instrument correctly.
        :param rise: A/us
        :param fall: A/us
        '''
        if not self.currentLevel:
            print('This model requires a current level to be set before setting the slew rate.')
            return
        riseTime = self.currentLevel / rise
        fallTime = self.currentLevel / fall
        self._write(f'S1 {riseTime}')
        self._write(f'S2 {fallTime}')

    def set_duration(self, t1, t2, *args, **kwargs):
        '''
        :param t1: ms
        :param t2: ms
        '''
        self._write(f'T1 {float(t1) * 1000}')
        self._write(f'T2 {float(t2) * 1000}')

class AMETEKPLA800():

    option = None
    ID = 'AMETEKPLA800'
    mode = None
    currentLevel = None

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        self.interface = _pyvisa.ResourceManager().open_resource(Address)
        if reset:
            self.interface.write('*RST')

    def _write(self, command, *args, **kwargs):
        self.interface.write(command)

    def _query(self, command, *args, **kwargs):
        d = kwargs['delay'] if 'delay' in kwargs else None
        if d:
            return self.interface.query(command, delay=d)
        else:
            return self.interface.query(command)

    def output(self, state='OFF', *args, **kwargs):
        if state.lower() == 'off':
            self._write('OUTP OFF')
        else:
            self._write('OUTP ON')

    def set_mode(self, mode, *args, **kwargs):
        '''
        :param mode: load mode { CCL | CCH | CCDL | CCDH | CRL | CRH | CV }
        :type: string
        :return: None
        '''
        modes = {
            'CCL' : 'CURR',
            'CCH' : 'CURR',
            'CCDL' : 'CURR',
            'CCDH' : 'CURR',
            'CRL' : 'RES',
            'CRH' : 'RES',
            'CV' : 'VOLT',
        }
        Range = {
            'CCL': '0',
            'CCH': '2',
            'CCDL': '0',
            'CCDH': '2',
            'CRL': '0',
            'CRH': '2',
            'CV': '2',
        }
        self.mode = modes[mode]
        self.range = Range[mode]
        self._write(f'MOD {self.mode}')
        self._write(f'MOD:RANG {self.range}')

    def set_channel(self, index=1, *args, **kwargs):
        # apparently no channel selection for this model
        pass

    def set_current(self, option=None, value=0, *args, **kwargs):
        '''
        :param option: no option to be used here.
        :type: string
        :param value: value of current to set
        :type: float
        :return: None
        '''
        self._write(f'CURR {value}')
        self.currentLevel = float(value)
        self.option = option.upper()
        sleep(0.5)

    def set_rise_fall(self, rise, fall, *args, **kwargs):
        '''
        This model uses slew time instead of rate. To make it compatible to other models and function calls the current
        level must be set first. Then when applying a rate in A/us the function will convert that into microseconds to
        set the instrument correctly.
        :param rise: A/us
        :param fall: A/us
        '''
        if not self.currentLevel:
            print('This model requires a current level to be set before setting the slew rate.')
            return
        riseTime = self.currentLevel / rise
        fallTime = self.currentLevel / fall
        self._write(f'CURR:SLEW:POS {riseTime}')
        self._write(f'CURR:SLEW:NEG {fallTime}')

    def set_duration(self, t1, t2, *args, **kwargs):
        '''
        :param t1: ms
        :param t2: ms
        '''
        self._write(f'STEP:CURR:TIM {float(t2) - float(t1)}')


if __name__ == '__main__':
    load = XBLSeries('GPIB0::10::INSTR')
    load.set_mode(mode='CCH')
    load.set_current(option='STATIC', value=10)
    sleep(0.5)
    load.output(state='ON')
    # sleep(2)
    # load.output(state='OFF')

