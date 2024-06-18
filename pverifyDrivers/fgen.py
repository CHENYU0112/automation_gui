
from pyvisa.resources.messagebased import MessageBasedResource as _MessageBasedResource
from pverify.drivers.Fgen.hp33120a.IIviFgen import IIviFgen as IviHp33120a
from pverify.drivers.Fgen.tkafg3k.IIviFgen import IIviFgen as IviTkafg3k
from pverify.drivers.Fgen.tkafg31k.IIviFgen import IIviFgen as IviTkafg31k
from pverify.drivers.SimplifiedLabInstruments.SimpleIviFgen import SimpleIviFgen
from pverify import Waveform
# from pverify.drivers.SimplifiedLabInstruments._simple_instr.simple_fgen import SimpleFgen_ABC

# BEGIN AUX IMPORTS
import pyvisa as _pyvisa
import tkinter
from time import sleep
from typing import Optional, Union
import numpy as np
from struct import pack, unpack
# END

class FgenBase:
    def __init__(self, callback):
        super(FgenBase, self).__init__(callback)

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

class Hp33120a(FgenBase, SimpleIviFgen):
    '''
    Supported Function Generators:
    33120A, 33210A, 33220A, 33250A, E1441A
    '''

    def __init__(self, Address, *args, **kwargs):
        simulate = kwargs['Simulate'] if 'Simulate' in kwargs else False
        reset = kwargs['Reset'] if 'Reset' in kwargs else True
        super(Hp33120a, self).__init__(IviHp33120a())
        self.Initialize(ResourceName=Address, IdQuery=True, Reset=reset, OptionString="simulate=" + str(simulate))
        self.pyvisa_instr = self.visa_from_simple_instrument()

    def _write(self, command, *args, **kwargs):
        self.lld.dllwrap.WriteInstrData(writeBuffer=command)

    def _query(self, command, *args, **kwargs):
        self.lld.dllwrap.WriteInstrData(writeBuffer=command)
        data = self.lld.dllwrap.ReadInstrData(numBytes=1024)
        return data

class Tkafg3k():
    '''
    Supported Function Generators
    AFG3021, AFG3022, AFG3101, AFG3102, AFG3251, AFG3252, AFG3021B, AFG3022B, AFG2021 AFG3011C, AFG3021C, AFG3022C,
    AFG3051C, AFG3052C, AFG3101C, AFG3102C, AFG3251C, AFG3252C
    '''

    channel = None
    Initialized = None
    ID = 'Tkafg31k'
    drivername = ID

    def __init__(self, Address='', Reset=True, *args, **kwargs):
        self.address = Address
        rm = _pyvisa.ResourceManager()
        self.cmd = rm.open_resource(Address)
        if Reset:
            self._write('*RST')
        self.Initialized = True

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, delay=None, *args, **kwargs):
        if delay:
            return self.cmd.query(command, delay=delay)
        else:
            return self.cmd.query(command)

    # Pyverify Function Generator Functions start here
    def AbortGeneration(self):
        '''
        Placehold for pyverify compatibility
        '''
        pass

    def Close(self):
        '''
        Placehold for pyverify compatibility
        '''
        pass

    def FgenSetup(self, InternalTriggerRate=None, ReferenceClockSource=None, *args, **kwargs):
        """
        Common Fgen setup.

        :param InternalTriggerRate: The rate at which the function generator's internal trigger source produces a
                                    trigger, in triggers per second.
        :type InternalTriggerRate: float
        :param ReferenceClockSource: The source of the reference clock. The function generator derives frequencies
                                     and sample rates that it uses to generate waveforms from the reference clock.
        :type ReferenceClockSource: choice(Internal,External)
        """
        if ReferenceClockSource == 'External':
            self.set_trigger_source('EXT')
        else:
            self.set_trigger_source()
            if InternalTriggerRate:
                self.set_trigger_rate(InternalTriggerRate)

    def GetChannel(self, Index=1, *args, **kwargs):
        '''
        :param Index: (int) – The index of the channel
        :return: Returns a channel object. The different channels can be set up indepentently from each other
        '''
        ch = Tkafg3k(Address=self.address, Reset=False)
        self.channel = int(Index)
        ch.channel = int(Index)
        return ch

    def Initialize(self, *args, **kwargs):
        '''
        Placehold for pyverify compatibility
        '''
        pass

    def InitiateGeneration(self):
        '''
        Placehold for pyverify compatibility
        '''
        pass

    def SendSoftwareTrigger(self):
        '''
        Placehold for pyverify compatibility
        '''
        pass

    # PyVerify Channel functions start here
    def ChannelSetup(self, Impedance=None, OperationMode=None, BurstCount=None, TriggerSource=None, *args, **kwargs):
        """
        Common setup for the Fgen channel

        :param Impedance: The impedance of the output channel. The units are Ohms. 0 means INFINITE.
        :type Impedance: float
        :param OperationMode: The mode that determines how the function generator produces output on a channel.

            - Continuous: When in the Output Generation State, the function generator produces output continuously.
            - Burst: When in the Output Generation State, the function generator produces a burst of waveform cycles
                     based on a trigger condition. A burst consists of a discrete number of waveform cycles.

        :type OperationMode: choice(Continuous,Burst)
        :param BurstCount: The number of waveform cycles that the function generator produces after it receives a
                           trigger.
        :type BurstCount: int
        :param TriggerSource: The trigger source.
        :type TriggerSource: choice(Internal,External)
        """
        if Impedance is not None:
            if float(Impedance) == 0:
                self.set_impedance('INF')
            elif float(Impedance) < 0:
                self.set_impedance('MIN')
            else:
                self.set_impedance(Impedance)
        if OperationMode is not None:
            if 'cont' in OperationMode.lower():
                self._write(f'SOUR{self.channel}:BURS:STAT OFF')
            else:
                self._write(f'SOUR{self.channel}:BURS:STAT ON')
        if BurstCount is not None:
            self._write(f'SOUR{self.channel}:BURS:NCYC {BurstCount}')
        if TriggerSource is not None:
            if 'ext' in TriggerSource.lower():
                self._write(f'TRIG:SOUR {TriggerSource}')
            else:
                self._write(f'TRIG:SOUR TIM')

    def Configure_Arbitrary(self, Data: Union[list, np.ndarray], Gain: float, Offset: float = 0,
                            SampleRate: float = 10e3, *args, **kwargs):
        """
        Configures an arbitrary waveform output.

        :param Data: Specifies the array of data to use for the new arbitrary waveform.
                     The array's elements must be normalized between -1.00 and +1.00.
        :param Gain: The gain of the arbitrary waveform the function generator produces. This value is unitless.
        :param Offset: The offset of the arbitrary waveform the function generator produces. The units are volts.
        :param SampleRate: The sample rate of the arbitrary waveforms the function generator produces. The units are
                           samples per second.
        :param progress: bool - it will add some prints showing status progress. Default set to False
        """
        print_progress = kwargs['progress'] if 'progress' in kwargs else False
        imp = float(self._query(f'OUTP{self.channel}:IMP?'))
        factor = imp / (imp + 50)

        # Sample Rate
        self._write(f'SOUR{self.channel}:FREQ {SampleRate}')

        # Arb Waveform
        if isinstance(Data, list):
            waveform = np.array(Data)
        else:
            waveform = Data

        minimum = np.min(Data) * Gain * factor
        maximum = np.max(Data) * Gain * factor

        try:
            self._check_arb_waveform_type_and_range(waveform)
        except ValueError as err:
            if print_progress:
                print(f"\n  {err}")
                print("Trying again normalising the waveform..", end=" ")
        waveform = self._normalise_to_waveform(waveform)
        if print_progress:
            print("ok")
            print("Transfer waveform to function generator..", end=" ")
            # Transfer waveform
        self.cmd.write_binary_values(
            "DATA:DATA EMEMory,", waveform, datatype="H", is_big_endian=True
        )
        self._write(f'SOUR{self.channel}:FUNC:SHAP EMEM')

        # Offset
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:OFFS {Offset}')

        # Gain
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:HIGH {maximum}')
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:LOW {minimum}')

        return waveform

    def Configure_ArbitraryFromWaveform(self, WaveformObj: Waveform, SampleRate: Optional[float] = None, *args,
                                        **kwargs):
        """
        Configures an arbitrary waveform output.

        :param WaveformObj: The waveform to be configured as output
        :param SampleRate: The sample rate of the arbitrary waveforms the function generator produces. The units are
                           samples per second. If specified the waveform object is sampled to the specified rate.
        """

        if not isinstance(WaveformObj, Waveform):
            raise TypeError("WaveformObj has to be of type 'Waveform'")

        wave = WaveformObj.copy()
        if SampleRate is not None:
            wave.change_samplerate(SampleRate)
        mean = (wave.Measurements_Base.max() + wave.Measurements_Base.min()) / 2.0
        wave -= mean
        max1 = abs(wave).Measurements_Base.max()
        wave.scale_to_absmax(1.0)
        max2 = abs(wave).Measurements_Base.max()
        gain = max1 / max2
        self.Configure_Arbitrary(Data=wave.data, Gain=gain, Offset=mean, SampleRate=wave.samplerate)

    def Configure_DC(self, DCOffset: float, *args, **kwargs):
        """
        Configures a DC wave output.

        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('DC')
        self.set_offset(DCOffset)

    def Configure_Sine(self, Amplitude: float, Frequency: float = 10e3, StartPhase: float = 0, DCOffset: float = 0,
                       *args, **kwargs):
        """
        Configures a sine wave output.

        :param Amplitude: The amplitude of the standard waveform output by the function generator. The units are volts.
        :param Frequency: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param StartPhase: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('SIN')
        self.set_amplitude(Amplitude, units='VPP')
        self.set_offset(DCOffset)
        self.set_frequency(Frequency)
        self.set_phase(StartPhase)

    def Configure_Square(self, Amplitude: float, DutyCycleHigh: float = 25, Frequency: float = 10e3,
                         DCOffset: float = 0, *args, **kwargs):
        """
        Configures a square wave output.

        :param DutyCycleHigh: The duty cycle for a square waveform. The value is expressed as a percentage.
        :param Amplitude: The amplitude of the standard waveform output by the function generator. The units are volts.
        :param Frequency: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('SQU')
        self.set_amplitude(Amplitude)
        self.set_offset(DCOffset)
        self.set_frequency(Frequency)
        self.set_phase(0)

    def Configure_Triangle(self, Amplitude: float, Frequency: float = 10e3, DCOffset: float = 0, *args, **kwargs):
        """
        Configures a triangle wave output.

        :param Amplitude: The amplitude of the standard waveform output by the function generator. The units are volts.
        :param Frequency: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('RAMP')
        self.set_amplitude(Amplitude)
        self.set_offset(DCOffset)
        self.set_frequency(Frequency)
        self.set_phase(0)
        self.set_ramp_symmetry(50)

    def Configure_RampUp(self, Amplitude: float, Frequency: float = 10e3, DCOffset: float = 0, *args, **kwargs):
        """
        Configures a positive ramp waveform output.

        :param Amplitude: The amplitude of the standard waveform output by the function generator. The units are volts.
        :param Frequency: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('RAMP')
        self.set_amplitude(Amplitude)
        self.set_offset(DCOffset)
        self.set_frequency(Frequency)
        self.set_phase(0)
        self.set_ramp_symmetry(100)

    def Configure_RampDown(self, Amplitude: float, Frequency: float = 10e3, DCOffset: float = 0, *args, **kwargs):
        """
        Configures a positive ramp waveform output.

        :param Amplitude: The amplitude of the standard waveform output by the function generator. The units are volts.
        :param Frequency: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('RAMP')
        self.set_amplitude(Amplitude)
        self.set_offset(DCOffset)
        self.set_frequency(Frequency)
        self.set_phase(0)
        self.set_ramp_symmetry(0)

    def Enable_AM(self, Depth: float, Frequency: float = 10e3, ModulationWaveform: str = "Sine"):
        """
        Enables amplitude modulation on the configured output waveform.

        :param Depth: The extent of modulation the function generator applies to the carrier waveform. The unit is
                      percentage.
        :param Frequency: The frequency of the internal modulating waveform source. The units are Hertz.
        :param ModulationWaveform: The waveform of the internal modulating waveform source.
                                   choice(Sine,Square,Triangle,RampUp,RampDown)
        """
        self._write(f'SOUR{self.channel}:AM:STAT ON')
        self._write(f'SOUR{self.channel}:AM:SOUR INT')
        self._write(f'SOUR{self.channel}:AM:INT:FREQ {Frequency}')
        self._write(f'SOUR{self.channel}:AM:INT:FUNC {ModulationWaveform}')
        self._write(f'SOUR{self.channel}:AM:DEPT {Depth}')
        modwave = ModulationWaveform.lower()
        if "sine" in modwave:
            self._write(f'SOUR{self.channel}:AM:FUNC SIN')
        elif "square" in modwave:
            self._write(f'SOUR{self.channel}:AM:FUNC SQU')
        elif "tri" in modwave:
            self._write(f'SOUR{self.channel}:AM:FUNC TRI')
        elif "up" in modwave:
            self._write(f'SOUR{self.channel}:AM:FUNC RAMP')
        elif "down" in modwave:
            self._write(f'SOUR{self.channel}:AM:FUNC NRAM')

    def Disable_AM(self):
        self._write(f'SOUR{self.channel}:AM:STAT OFF')

    def Enable_FM(self, Deviation: float = 100, Frequency: float = 10e3, ModulationWaveform: str = "Sine"):
        """
        Enables frequency modulation on the configured output waveform.

        :param Deviation: The maximum frequency deviation the function generator applies to the carrier waveform.
        :param Frequency: The frequency of the internal modulating waveform source. The units are Hertz.
        :param ModulationWaveform: The waveform of the internal modulating waveform source.
                                   choice(Sine,Square,Triangle,RampUp,RampDown)
        """
        self._write(f'SOUR{self.channel}:FM:STAT ON')
        self._write(f'SOUR{self.channel}:FM:SOUR INT')
        self._write(f'SOUR{self.channel}:FM:INT:FREQ {Frequency}')
        self._write(f'SOUR{self.channel}:FM:DEV {Deviation}')
        modwave = ModulationWaveform.lower()
        if "sine" in modwave:
            self._write(f'SOUR{self.channel}:FM:FUNC SIN')
        elif "square" in modwave:
            self._write(f'SOUR{self.channel}:FM:FUNC SQU')
        elif "tri" in modwave:
            self._write(f'SOUR{self.channel}:FM:FUNC TRI')
        elif "up" in modwave:
            self._write(f'SOUR{self.channel}:FM:FUNC RAMP')
        elif "down" in modwave:
            self._write(f'SOUR{self.channel}:FM:FUNC NRAM')

    def Disable_FM(self):
        self._write(f'SOUR{self.channel}:FM:STAT OFF')

    def Enable(self):
        '''
        Enables the channel.
        '''
        if self.channel is not None:
            self._write(f'OUTPut{self.channel}:STATe ON')
        else:
            print('Use GetChannel() to select the channel')

    def Disable(self):
        '''
        Disables the channel.
        '''
        if self.channel is not None:
            self._write(f'OUTPut{self.channel}:STATe OFF')
        else:
            print('Use GetChannel() to select the channel')

    # Supplemental functions
    def set_function(self, func, *args, **kwargs):
        '''
        :param func: { SINusoid | SQUare | PULSe | RAMP | PRNoise | DC | SINC | GAUSsian | LORentz | ERISe | EDECay |
                    HAVersine | EMEMory | EFILe }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:FUNC:SHAP {func}')

    def set_offset(self, offset, *args, **kwargs):
        '''
        :param offset: voltage level
        :return: None
        '''
        imp = float(self._query(f'OUTP{self.channel}:IMP?'))
        factor = imp / (imp + 50)
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:OFFS {float(offset) * factor}')

    def set_amplitude(self, amplitude, units='VPP', *args, **kwargs):
        '''
        :param amplitude: Amplitude in VPP
        :param units: { VPP | VRMS | DBM }
        :return: None
        '''
        imp = float(self._query(f'OUTP{self.channel}:IMP?'))
        factor = imp / (imp + 50)
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:AMPL {float(amplitude) * factor}VPP')
        self._write(f'SOUR{self.channel}:VOLT:UNIT {units}')

    def set_frequency(self, frequency, *args, **kwargs):
        '''
        :param frequency: { <frequency> | MINimum | MAXimum }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:FREQ {frequency}')

    def set_phase(self, phase, *args, **kwargs):
        '''
        :param phase: { <phase> | MINimum | MAXimum }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:PHAS:ADJ {phase}')

    def set_pwm_dcycle(self, dutyCycle, *args, **kwargs):
        '''
        :param dutyCycle: { <dutyCycle> | MINimum | MAXimum }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:PWM:DEV:DCYC {dutyCycle}')

    def set_ramp_symmetry(self, symmetry, *args, **kwargs):
        '''
        :param symmetry: Percentage [0:100]
        :return: None
        '''
        self._write(f'SOUR{self.channel}:FUNC:RAMP:SYMM {symmetry}')

    def set_trigger_source(self, source='TIM', *args, **kwargs):
        '''
        :param source: { TIMer | EXTernal }
        :type: str
        :return: None
        '''
        self._write(f'TRIG:SOUR {source}')

    def get_trigger_source(self, *args, **kwargs):
        '''
        :return: Returns trigger source { TIMer | EXTernal }
        '''
        return self._query('TRIG:SOUR?')

    def set_trigger_rate(self, rate='1e-6', *args, **kwargs):
        '''
        This command sets the period of an internal clock when you select the internal clock as the trigger source with
        set_trigger_source(). The setting range is 1us to 500.0s
        :param rate: A value in the range of 1us to 500.0s
        :return: None
        '''
        self._write(f'TRIG:TIM {rate}')

    def get_trigger_rate(self, *args, **kwargs):
        '''
        This command queries the period of an internal clock when you select the internal clock as the trigger source with
        set_trigger_source().
        :return: A value in the range of 1us to 500.0s
        '''
        return self._query('TRIG:TIM?')

    def set_impedance(self, value, *args, **kwargs):
        '''
        :param value: { <ohms> | INFinity | MINimum | MAXimum }
        :return: None
        '''
        self._write(f'OUTP{self.channel}:IMP {value}')

    def get_impedance(self, *args, **kwargs):
        '''
        :return: Returns the current load impedance setting in ohms. If load impedance is set to INFinity, the query command
        returns "9.9E+37".
        '''
        return self._query(f'OUTP{self.channel}:IMP?')

    def _check_arb_waveform_type_and_range(self, waveform: np.ndarray):
        """Checks if waveform is of int/np.int32 type and within the resolution
        of the function generator
        Parameters
        ----------
        waveform : array_like
            Waveform or voltage list to be checked
        Raises
        ------
        ValueError
            If the waveform values are not int, np.uint16 or np.int32, or the
            values are not within the permitted range
        """
        for value in waveform:
            if not isinstance(value, (int, np.uint16, np.int32)):
                raise ValueError(
                    "The waveform contains values that are not"
                    "int, np.uint16 or np.int32"
                )
            if (value < 0) or (value > 16383):
                raise ValueError(
                    f"The waveform contains values out of range "
                    f"({value} is not within the resolution "
                    f"[0, 16383])"
                )

    def _normalise_to_waveform(self, shape: np.ndarray) -> np.ndarray:
        """Normalise a shape of any discretisation and range to a waveform that
        can be transmitted to the function generator
        .. note::
            If you are transferring a flat/constant waveform, do not use this
            normaisation function. Transfer a waveform like
            `int(self._arbitrary_waveform_resolution/2)*np.ones(2).astype(np.int32)`
            without normalising for a well behaved flat function.
        Parameters
        ----------
        shape : array_like
            Array to be transformed to waveform, can be ints or floats,
            any normalisation or discretisation
        Returns
        -------
        waveform : ndarray
            Waveform as ints spanning the resolution of the function gen
        """
        # Check if waveform data is suitable
        self._check_arb_waveform_length(shape)
        # Normalise
        waveform = shape - np.min(shape)
        normalisation_factor = np.max(waveform)
        if not normalisation_factor:
            waveform = shape * 16383
        else:
            waveform = waveform / normalisation_factor * 16383
        return waveform.astype(np.uint16)

    def _check_arb_waveform_length(self, waveform: np.ndarray):
        """Checks if waveform is within the acceptable length
        Parameters
        ----------
        waveform : array_like
            Waveform or voltage list to be checked
        Raises
        ------
        ValueError
            If the waveform is not within the permitted length
        """
        if (len(waveform) < 2) or (len(waveform) > 8192):
            msg = (
                "The waveform is of length {}, which is not within the "
                "acceptable length {} < len < {}"
                "".format(len(waveform), *self._arbitrary_waveform_length)
            )
            raise ValueError(msg)

    def set_edge_time(self, edge_time, mode, *args, **kwargs):
        '''
        Function to set edge times for Pulse mode only
        :param edge_time: (float) for edge time
        :param mode: { LEAD | TRAIL | BOTH }
        :return: None
        '''
        if mode == "BOTH":
            self._write(f'SOUR{self.channel}:PULS:TRAN:LEAD {edge_time}')
            self._write(f'SOUR{self.channel}:PULS:TRAN:TRA {edge_time}')
        elif mode == "LEAD":
            self._write(f'SOUR{self.channel}:PULS:TRAN:LEAD {edge_time}')
        else:
            self._write(f'SOUR{self.channel}:PULS:TRAN:TRA {edge_time}')

    def set_duty_cycle(self, dutycycle, *args, **kwargs):
        '''
        Sets the duty cycle on pulse mode only.
        :param dutycycle: Percentage of duty cycle
        :return: None
        '''
        self._write(f'SOUR{self.channel}:PULS:DCYC {dutycycle}')

    def set_high_level(self, level, *args, **kwargs):
        '''
        :param level: Level in Volts
        :return: None
        '''
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:HIGH {level}')

    def set_low_level(self, level, *args, **kwargs):
        '''
        :param level: Level in Volts
        :return: None
        '''
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:LOW {level}')

    def set_period(self, period, *args, **kwargs):
        '''
        :param period: Period in seconds
        :return: None
        '''
        self._write(f'SOUR{self.channel}:PULS:PER {period}')

    def set_busrt_mode(self, mode, *args, **kwargs):
        '''
        :param mode: { TRIGgered | GATed }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:BURS:MODE {mode}')

    def set_burst_ncycles(self, cycles, *args, **kwargs):
        '''
        :param cycles: { <cycles> | INFinity | MINimum | MAXimum }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:BURS:NCYC {cycles}')

    def set_burst_state(self, state, *args, **kwargs):
        '''
        :param state: { ON | OFF }
        :return: None
        '''
        if state.upper() == 'ON':
            self._write(f'SOUR{self.channel}:BURS:STAT ON')
        else:
            self._write(f'SOUR{self.channel}:BURS:STAT OFF')

    def rearm_burst(self, *args, **kwargs):
        '''
        Rearms burst mode.
        :return: None
        '''
        self._write(f'SOUR{self.channel}:BURS:INFI:REAR')

    def get_leading(self, *args, **kwargs):
        '''
        :return: (float) leading time
        '''
        return float(self._query(f'SOUR{self.channel}:PULS:TRAN:LEAD?'))

    def get_trailing(self, *args, **kwargs):
        '''
        :return: (float) trailing time
        '''
        return float(self._query(f'SOUR{self.channel}:PULS:TRAN:TRA?'))

    def get_period(self, *args, **kwargs):
        '''
        :return: (float)
        '''
        return float(self._query(f'SOUR{self.channel}:PULS:PER?'))

    def get_frequency(self, *args, **kwargs):
        '''
        :return: (float) frequency in kHz
        '''
        return float(self._query(f'SOUR{self.channel}:FREQuency:FIXed?')) / 1000

    def get_dcycle(self, *args, **kwargs):
        '''
        :return: (float) duty cycle in percentage
        '''
        return float(self._query(f'SOUR{self.channel}:PULSe:DCYCLe?'))

    def get_high_level(self, *args, **kwargs):
        '''
        :return: (float) high level in Volts
        '''
        return float(self._query(f'SOUR{self.channel}:VOLT:LEV:IMM:HIGH?'))

    def get_low_level(self, *args, **kwargs):
        '''
        :return: (float) low level in Volts
        '''
        return float(self._query(f'SOUR{self.channel}:VOLT:LEV:IMM:LOW?'))

    def reset(self, *args, **kwargs):
        '''
        Resets the instrument. "*RST"
        :return: None
        '''
        self._write('*RST')

    def trigger(self, *args, **kwargs):
        '''
        Sends a Trigger signal. Same as "*TRG"
        :return: None
        '''
        self._write('TRIG')

    def set_delay(self, value, *args, **kwargs):
        '''
        :param value: { <delay> | MINimum | MAXimum }
        :return: None
        '''
        if self.channel:
            self._write(f'SOUR{self.channel}:PULS:DEL {value}')
        else:
            print('Channel related function')

class Tkafg31k:
    '''
    Supported Function Generators
    AFG31021, AFG31022, AFG31101, AFG31102, AFG31051, AFG31052, AFG31151, AFG31152, AFG31251, AFG31252
    '''

    channel = None
    Initialized = None
    ID = 'Tkafg31k'
    drivername = ID

    def __init__(self, Address='', Reset=True, *args, **kwargs):
        self.address = Address
        rm = _pyvisa.ResourceManager()
        self.cmd = rm.open_resource(Address)
        if Reset:
            self._write('*RST')
        self.Initialized = True

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, delay=None, *args, **kwargs):
        if delay:
            return self.cmd.query(command, delay=delay)
        else:
            return self.cmd.query(command)

    # Pyverify Function Generator Functions start here
    def AbortGeneration(self):
        '''
        Placehold for pyverify compatibility
        '''
        pass

    def Close(self):
        '''
        Placehold for pyverify compatibility
        '''
        pass

    def FgenSetup(self, InternalTriggerRate=None, ReferenceClockSource=None, *args, **kwargs):
        """
        Common Fgen setup.

        :param InternalTriggerRate: The rate at which the function generator's internal trigger source produces a
                                    trigger, in triggers per second.
        :type InternalTriggerRate: float
        :param ReferenceClockSource: The source of the reference clock. The function generator derives frequencies
                                     and sample rates that it uses to generate waveforms from the reference clock.
        :type ReferenceClockSource: choice(Internal,External)
        """
        if ReferenceClockSource == 'External':
            self.set_trigger_source('EXT')
        else:
            self.set_trigger_source()
            if InternalTriggerRate:
                self.set_trigger_rate(InternalTriggerRate)

    def GetChannel(self, Index=1, *args, **kwargs):
        '''
        :param Index: (int) – The index of the channel
        :return: Returns a channel object. The different channels can be set up indepentently from each other
        '''
        ch = Tkafg31k(Address=self.address, Reset=False)
        self.channel = int(Index)
        ch.channel = int(Index)
        return ch

    def Initialize(self, *args, **kwargs):
        '''
        Placehold for pyverify compatibility
        '''
        pass

    def InitiateGeneration(self):
        '''
        Placehold for pyverify compatibility
        '''
        pass

    def SendSoftwareTrigger(self):
        '''
        Placehold for pyverify compatibility
        '''
        pass

    # PyVerify Channel functions start here
    def ChannelSetup(self, Impedance=None, OperationMode=None, BurstCount=None, TriggerSource=None, *args, **kwargs):
        """
        Common setup for the Fgen channel

        :param Impedance: The impedance of the output channel. The units are Ohms. 0 means INFINITE.
        :type Impedance: float
        :param OperationMode: The mode that determines how the function generator produces output on a channel.

            - Continuous: When in the Output Generation State, the function generator produces output continuously.
            - Burst: When in the Output Generation State, the function generator produces a burst of waveform cycles
                     based on a trigger condition. A burst consists of a discrete number of waveform cycles.

        :type OperationMode: choice(Continuous,Burst)
        :param BurstCount: The number of waveform cycles that the function generator produces after it receives a
                           trigger.
        :type BurstCount: int
        :param TriggerSource: The trigger source.
        :type TriggerSource: choice(Internal,External)
        """
        if Impedance is not None:
            if float(Impedance) == 0:
                self.set_impedance('INF')
            elif float(Impedance) < 0:
                self.set_impedance('MIN')
            else:
                self.set_impedance(Impedance)
        if OperationMode is not None:
            if 'cont' in OperationMode.lower():
                self._write(f'SOUR{self.channel}:BURS:STAT OFF')
            else:
                self._write(f'SOUR{self.channel}:BURS:STAT ON')
        if BurstCount is not None:
            self._write(f'SOUR{self.channel}:BURS:NCYC {BurstCount}')
        if TriggerSource is not None:
            if 'ext' in TriggerSource.lower():
                self._write(f'TRIG:SOUR {TriggerSource}')
            else:
                self._write(f'TRIG:SOUR TIM')

    def Configure_Arbitrary(self, Data: Union[list, np.ndarray], Gain: float, Offset: float = 0, SampleRate: float = 10e3, *args, **kwargs):
        """
        Configures an arbitrary waveform output.

        :param Data: Specifies the array of data to use for the new arbitrary waveform.
                     The array's elements must be normalized between -1.00 and +1.00.
        :param Gain: The gain of the arbitrary waveform the function generator produces. This value is unitless.
        :param Offset: The offset of the arbitrary waveform the function generator produces. The units are volts.
        :param SampleRate: The sample rate of the arbitrary waveforms the function generator produces. The units are
                           samples per second.
        :param progress: bool - it will add some prints showing status progress. Default set to False
        """
        print_progress = kwargs['progress'] if 'progress' in kwargs else False
        imp = float(self._query(f'OUTP{self.channel}:IMP?'))
        factor = imp / (imp + 50)

        # Sample Rate
        self._write(f'SOUR{self.channel}:FREQ {SampleRate}')

        # Arb Waveform
        if isinstance(Data, list):
            waveform = np.array(Data)
        else:
            waveform = Data

        minimum = np.min(Data) * Gain * factor
        maximum = np.max(Data) * Gain * factor

        try:
            self._check_arb_waveform_type_and_range(waveform)
        except ValueError as err:
            if print_progress:
                print(f"\n  {err}")
                print("Trying again normalising the waveform..", end=" ")
        waveform = self._normalise_to_waveform(waveform)
        if print_progress:
            print("ok")
            print("Transfer waveform to function generator..", end=" ")
            # Transfer waveform
        self.cmd.write_binary_values(
            "DATA:DATA EMEMory,", waveform, datatype="H", is_big_endian=True
        )
        self._write(f'SOUR{self.channel}:FUNC:SHAP EMEM1')

        # Offset
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:OFFS {Offset}')

        # Gain
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:HIGH {maximum}')
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:LOW {minimum}')

        return waveform

    def Configure_ArbitraryFromWaveform(self, WaveformObj: Waveform, SampleRate: Optional[float] = None, *args, **kwargs):
        """
        Configures an arbitrary waveform output.

        :param WaveformObj: The waveform to be configured as output
        :param SampleRate: The sample rate of the arbitrary waveforms the function generator produces. The units are
                           samples per second. If specified the waveform object is sampled to the specified rate.
        """

        if not isinstance(WaveformObj, Waveform):
            raise TypeError("WaveformObj has to be of type 'Waveform'")

        wave = WaveformObj.copy()
        if SampleRate is not None:
            wave.change_samplerate(SampleRate)
        mean = (wave.Measurements_Base.max() + wave.Measurements_Base.min()) / 2.0
        wave -= mean
        max1 = abs(wave).Measurements_Base.max()
        wave.scale_to_absmax(1.0)
        max2 = abs(wave).Measurements_Base.max()
        gain = max1 / max2
        self.Configure_Arbitrary(Data=wave.data, Gain=gain, Offset=mean, SampleRate=wave.samplerate)

    def Configure_DC(self, DCOffset: float, *args, **kwargs):
        """
        Configures a DC wave output.

        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('DC')
        self.set_offset(DCOffset)

    def Configure_Sine(self, Amplitude: float, Frequency: float = 10e3, StartPhase: float = 0, DCOffset: float = 0, *args, **kwargs):
        """
        Configures a sine wave output.

        :param Amplitude: The amplitude of the standard waveform output by the function generator. The units are volts.
        :param Frequency: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param StartPhase: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('SIN')
        self.set_amplitude(Amplitude, units='VPP')
        self.set_offset(DCOffset)
        self.set_frequency(Frequency)
        self.set_phase(StartPhase)

    def Configure_Square(self, Amplitude: float, DutyCycleHigh: float = 25, Frequency: float = 10e3, DCOffset: float = 0, *args, **kwargs):
        """
        Configures a square wave output.

        :param DutyCycleHigh: The duty cycle for a square waveform. The value is expressed as a percentage.
        :param Amplitude: The amplitude of the standard waveform output by the function generator. The units are volts.
        :param Frequency: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('SQU')
        self.set_amplitude(Amplitude)
        self.set_offset(DCOffset)
        self.set_frequency(Frequency)
        self.set_phase(0)

    def Configure_Triangle(self, Amplitude: float, Frequency: float = 10e3, DCOffset: float = 0, *args, **kwargs):
        """
        Configures a triangle wave output.

        :param Amplitude: The amplitude of the standard waveform output by the function generator. The units are volts.
        :param Frequency: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('RAMP')
        self.set_amplitude(Amplitude)
        self.set_offset(DCOffset)
        self.set_frequency(Frequency)
        self.set_phase(0)
        self.set_ramp_symmetry(50)

    def Configure_RampUp(self, Amplitude: float, Frequency: float = 10e3, DCOffset: float = 0, *args, **kwargs):
        """
        Configures a positive ramp waveform output.

        :param Amplitude: The amplitude of the standard waveform output by the function generator. The units are volts.
        :param Frequency: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('RAMP')
        self.set_amplitude(Amplitude)
        self.set_offset(DCOffset)
        self.set_frequency(Frequency)
        self.set_phase(0)
        self.set_ramp_symmetry(100)

    def Configure_RampDown(self, Amplitude: float, Frequency: float = 10e3, DCOffset: float = 0, *args, **kwargs):
        """
        Configures a positive ramp waveform output.

        :param Amplitude: The amplitude of the standard waveform output by the function generator. The units are volts.
        :param Frequency: The frequency of the standard waveform output by the function generator. The units are Hertz.
        :param DCOffset: The DC offset of the standard waveform output by the function generator. The units are volts.
        """
        self.set_function('RAMP')
        self.set_amplitude(Amplitude)
        self.set_offset(DCOffset)
        self.set_frequency(Frequency)
        self.set_phase(0)
        self.set_ramp_symmetry(0)

    def Enable_AM(self, Depth: float, Frequency: float = 10e3, ModulationWaveform: str = "Sine"):
        """
        Enables amplitude modulation on the configured output waveform.

        :param Depth: The extent of modulation the function generator applies to the carrier waveform. The unit is
                      percentage.
        :param Frequency: The frequency of the internal modulating waveform source. The units are Hertz.
        :param ModulationWaveform: The waveform of the internal modulating waveform source.
                                   choice(Sine,Square,Triangle,RampUp,RampDown)
        """
        self._write(f'SOUR{self.channel}:AM:STAT ON')
        self._write(f'SOUR{self.channel}:AM:SOUR INT')
        self._write(f'SOUR{self.channel}:AM:INT:FREQ {Frequency}')
        self._write(f'SOUR{self.channel}:AM:INT:FUNC {ModulationWaveform}')
        self._write(f'SOUR{self.channel}:AM:DEPT {Depth}')
        modwave = ModulationWaveform.lower()
        if "sine" in modwave:
            self._write(f'SOUR{self.channel}:AM:FUNC SIN')
        elif "square" in modwave:
            self._write(f'SOUR{self.channel}:AM:FUNC SQU')
        elif "tri" in modwave:
            self._write(f'SOUR{self.channel}:AM:FUNC TRI')
        elif "up" in modwave:
            self._write(f'SOUR{self.channel}:AM:FUNC RAMP')
        elif "down" in modwave:
            self._write(f'SOUR{self.channel}:AM:FUNC NRAM')

    def Disable_AM(self):
        self._write(f'SOUR{self.channel}:AM:STAT OFF')

    def Enable_FM(self, Deviation: float = 100, Frequency: float = 10e3, ModulationWaveform: str = "Sine"):
        """
        Enables frequency modulation on the configured output waveform.

        :param Deviation: The maximum frequency deviation the function generator applies to the carrier waveform.
        :param Frequency: The frequency of the internal modulating waveform source. The units are Hertz.
        :param ModulationWaveform: The waveform of the internal modulating waveform source.
                                   choice(Sine,Square,Triangle,RampUp,RampDown)
        """
        self._write(f'SOUR{self.channel}:FM:STAT ON')
        self._write(f'SOUR{self.channel}:FM:SOUR INT')
        self._write(f'SOUR{self.channel}:FM:INT:FREQ {Frequency}')
        self._write(f'SOUR{self.channel}:FM:DEV {Deviation}')
        modwave = ModulationWaveform.lower()
        if "sine" in modwave:
            self._write(f'SOUR{self.channel}:FM:FUNC SIN')
        elif "square" in modwave:
            self._write(f'SOUR{self.channel}:FM:FUNC SQU')
        elif "tri" in modwave:
            self._write(f'SOUR{self.channel}:FM:FUNC TRI')
        elif "up" in modwave:
            self._write(f'SOUR{self.channel}:FM:FUNC RAMP')
        elif "down" in modwave:
            self._write(f'SOUR{self.channel}:FM:FUNC NRAM')

    def Disable_FM(self):
        self._write(f'SOUR{self.channel}:FM:STAT OFF')

    def Enable(self):
        '''
        Enables the channel.
        '''
        if self.channel is not None:
            self._write(f'OUTPut{self.channel}:STATe ON')
        else:
            print('Use GetChannel() to select the channel')

    def Disable(self):
        '''
        Disables the channel.
        '''
        if self.channel is not None:
            self._write(f'OUTPut{self.channel}:STATe OFF')
        else:
            print('Use GetChannel() to select the channel')

    # Supplemental functions
    def set_function(self, func, *args, **kwargs):
        '''
        :param func: { SINusoid | SQUare | PULSe | RAMP | PRNoise | DC | SINC | GAUSsian | LORentz | ERISe | EDECay |
                    HAVersine | EMEMory[1] | EMEMory2 | EFILe }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:FUNC:SHAP {func}')

    def set_offset(self, offset, *args, **kwargs):
        '''
        :param offset: voltage level
        :return: None
        '''
        imp = float(self._query(f'OUTP{self.channel}:IMP?'))
        factor = imp / (imp + 50)
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:OFFS {float(offset) * factor}')

    def set_amplitude(self, amplitude, units='VPP', *args, **kwargs):
        '''
        :param amplitude: Amplitude in VPP
        :param units: { VPP | VRMS | DBM }
        :return: None
        '''
        imp = float(self._query(f'OUTP{self.channel}:IMP?'))
        factor = imp / (imp + 50)
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:AMPL {float(amplitude) * factor}VPP')
        self._write(f'SOUR{self.channel}:VOLT:UNIT {units}')

    def set_frequency(self, frequency, *args, **kwargs):
        '''
        :param frequency: { <frequency> | MINimum | MAXimum }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:FREQ {frequency}')

    def set_phase(self, phase, *args, **kwargs):
        '''
        :param phase: { <phase> | MINimum | MAXimum }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:PHAS:ADJ {phase}')

    def set_pwm_dcycle(self, dutyCycle, *args, **kwargs):
        '''
        :param dutyCycle: { <dutyCycle> | MINimum | MAXimum }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:PWM:DEV:DCYC {dutyCycle}')

    def set_ramp_symmetry(self, symmetry, *args, **kwargs):
        '''
        :param symmetry: Percentage [0:100]
        :return: None
        '''
        self._write(f'SOUR{self.channel}:FUNC:RAMP:SYMM {symmetry}')

    def set_trigger_source(self, source='TIM', *args, **kwargs):
        '''
        :param source: { TIMer | EXTernal }
        :type: str
        :return: None
        '''
        self._write(f'TRIG:SOUR {source}')

    def get_trigger_source(self, *args, **kwargs):
        '''
        :return: Returns trigger source { TIMer | EXTernal }
        '''
        return self._query('TRIG:SOUR?')

    def set_trigger_rate(self, rate='1e-6', *args, **kwargs):
        '''
        This command sets the period of an internal clock when you select the internal clock as the trigger source with
        set_trigger_source(). The setting range is 1us to 500.0s
        :param rate: A value in the range of 1us to 500.0s
        :return: None
        '''
        self._write(f'TRIG:TIM {rate}')

    def get_trigger_rate(self, *args, **kwargs):
        '''
        This command queries the period of an internal clock when you select the internal clock as the trigger source with
        set_trigger_source().
        :return: A value in the range of 1us to 500.0s
        '''
        return self._query('TRIG:TIM?')

    def set_impedance(self, value, *args, **kwargs):
        '''
        :param value: { <ohms> | INFinity | MINimum | MAXimum }
        :return: None
        '''
        self._write(f'OUTP{self.channel}:IMP {value}')

    def get_impedance(self, *args, **kwargs):
        '''
        :return: Returns the current load impedance setting in ohms. If load impedance is set to INFinity, the query command
        returns "9.9E+37".
        '''
        return self._query(f'OUTP{self.channel}:IMP?')

    def _check_arb_waveform_type_and_range(self, waveform: np.ndarray):
        """Checks if waveform is of int/np.int32 type and within the resolution
        of the function generator
        Parameters
        ----------
        waveform : array_like
            Waveform or voltage list to be checked
        Raises
        ------
        ValueError
            If the waveform values are not int, np.uint16 or np.int32, or the
            values are not within the permitted range
        """
        for value in waveform:
            if not isinstance(value, (int, np.uint16, np.int32)):
                raise ValueError(
                    "The waveform contains values that are not"
                    "int, np.uint16 or np.int32"
                )
            if (value < 0) or (value > 16383):
                raise ValueError(
                    f"The waveform contains values out of range "
                    f"({value} is not within the resolution "
                    f"[0, 16383])"
                )

    def _normalise_to_waveform(self, shape: np.ndarray) -> np.ndarray:
        """Normalise a shape of any discretisation and range to a waveform that
        can be transmitted to the function generator
        .. note::
            If you are transferring a flat/constant waveform, do not use this
            normaisation function. Transfer a waveform like
            `int(self._arbitrary_waveform_resolution/2)*np.ones(2).astype(np.int32)`
            without normalising for a well behaved flat function.
        Parameters
        ----------
        shape : array_like
            Array to be transformed to waveform, can be ints or floats,
            any normalisation or discretisation
        Returns
        -------
        waveform : ndarray
            Waveform as ints spanning the resolution of the function gen
        """
        # Check if waveform data is suitable
        self._check_arb_waveform_length(shape)
        # Normalise
        waveform = shape - np.min(shape)
        normalisation_factor = np.max(waveform)
        if not normalisation_factor:
            waveform = shape * 16383
        else:
            waveform = waveform / normalisation_factor * 16383
        return waveform.astype(np.uint16)

    def _check_arb_waveform_length(self, waveform: np.ndarray):
        """Checks if waveform is within the acceptable length
        Parameters
        ----------
        waveform : array_like
            Waveform or voltage list to be checked
        Raises
        ------
        ValueError
            If the waveform is not within the permitted length
        """
        if (len(waveform) < 2) or (len(waveform) > 8192):
            msg = (
                "The waveform is of length {}, which is not within the "
                "acceptable length {} < len < {}"
                "".format(len(waveform), *self._arbitrary_waveform_length)
            )
            raise ValueError(msg)

    def set_edge_time(self, edge_time, mode, *args, **kwargs):
        '''
        Function to set edge times for Pulse mode only
        :param edge_time: (float) for edge time
        :param mode: { LEAD | TRAIL | BOTH }
        :return: None
        '''
        if mode == "BOTH":
            self._write(f'SOUR{self.channel}:PULS:TRAN:LEAD {edge_time}')
            self._write(f'SOUR{self.channel}:PULS:TRAN:TRA {edge_time}')
        elif mode == "LEAD":
            self._write(f'SOUR{self.channel}:PULS:TRAN:LEAD {edge_time}')
        else:
            self._write(f'SOUR{self.channel}:PULS:TRAN:TRA {edge_time}')

    def set_duty_cycle(self, dutycycle, *args, **kwargs):
        '''
        Sets the duty cycle on pulse mode only.
        :param dutycycle: Percentage of duty cycle
        :return: None
        '''
        self._write(f'SOUR{self.channel}:PULS:DCYC {dutycycle}')

    def set_high_level(self, level, *args, **kwargs):
        '''
        :param level: Level in Volts
        :return: None
        '''
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:HIGH {level}')

    def set_low_level(self, level, *args, **kwargs):
        '''
        :param level: Level in Volts
        :return: None
        '''
        self._write(f'SOUR{self.channel}:VOLT:LEV:IMM:LOW {level}')

    def set_period(self, period, *args, **kwargs):
        '''
        :param period: Period in seconds
        :return: None
        '''
        self._write(f'SOUR{self.channel}:PULS:PER {period}')

    def set_busrt_mode(self, mode, *args, **kwargs):
        '''
        :param mode: { TRIGgered | GATed }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:BURS:MODE {mode}')

    def set_burst_ncycles(self, cycles, *args, **kwargs):
        '''
        :param cycles: { <cycles> | INFinity | MINimum | MAXimum }
        :return: None
        '''
        self._write(f'SOUR{self.channel}:BURS:NCYC {cycles}')

    def set_burst_state(self, state, *args, **kwargs):
        '''
        :param state: { ON | OFF }
        :return: None
        '''
        if state.upper() == 'ON':
            self._write(f'SOUR{self.channel}:BURS:STAT ON')
        else:
            self._write(f'SOUR{self.channel}:BURS:STAT OFF')

    def rearm_burst(self, *args, **kwargs):
        '''
        Rearms burst mode.
        :return: None
        '''
        self._write(f'SOUR{self.channel}:BURS:INFI:REAR')

    def get_leading(self, *args, **kwargs):
        '''
        :return: (float) leading time
        '''
        return float(self._query(f'SOUR{self.channel}:PULS:TRAN:LEAD?'))

    def get_trailing(self, *args, **kwargs):
        '''
        :return: (float) trailing time
        '''
        return float(self._query(f'SOUR{self.channel}:PULS:TRAN:TRA?'))

    def get_period(self, *args, **kwargs):
        '''
        :return: (float)
        '''
        return float(self._query(f'SOUR{self.channel}:PULS:PER?'))

    def get_frequency(self, *args, **kwargs):
        '''
        :return: (float) frequency in kHz
        '''
        return float(self._query(f'SOUR{self.channel}:FREQuency:FIXed?')) / 1000

    def get_dcycle(self, *args, **kwargs):
        '''
        :return: (float) duty cycle in percentage
        '''
        return float(self._query(f'SOUR{self.channel}:PULSe:DCYCLe?'))

    def get_high_level(self, *args, **kwargs):
        '''
        :return: (float) high level in Volts
        '''
        return float(self._query(f'SOUR{self.channel}:VOLT:LEV:IMM:HIGH?'))

    def get_low_level(self, *args, **kwargs):
        '''
        :return: (float) low level in Volts
        '''
        return float(self._query(f'SOUR{self.channel}:VOLT:LEV:IMM:LOW?'))

    def reset(self, *args, **kwargs):
        '''
        Resets the instrument. "*RST"
        :return: None
        '''
        self._write('*RST')

    def trigger(self, *args, **kwargs):
        '''
        Sends a Trigger signal. Same as "*TRG"
        :return: None
        '''
        self._write('TRIG')

    def set_delay(self, value, *args, **kwargs):
        '''
        :param value: { <delay> | MINimum | MAXimum }
        :return: None
        '''
        if self.channel:
            self._write(f'SOUR{self.channel}:PULS:DEL {value}')
        else:
            print('Channel related function')


if __name__ == '__main__':
    # print(type(SimpleFgen))
    # fgen = Hp33120a(Address='GPIB0::10::INSTR', Reset=False)
    # fgenCh = fgen.GetChannel(Index=1)
    # fgen.FgenSetup(InternalTriggerRate=None, ReferenceClockSource="Internal")
    # dt = [0.825 for i in range(100)]
    # for i in range(20):
    #     dt[i] = 1.65
    # # print(dt)
    #
    # arb = Waveform(data=dt, time=[0, 1e-6]).up_sample_interp(1000)
    # fgenCh.Configure_ArbitraryFromWaveform(WaveformObj=arb)

    # Testing code for minislammer
    fgen = Tkafg3k(Address='GPIB0::8::INSTR', Reset=True)
    fgenCh = fgen.GetChannel(Index=1)
    fgen.FgenSetup(InternalTriggerRate=None, ReferenceClockSource="Internal")
    dt = [0 for i in range(100)]
    for i in range(50):
        dt[i] = 1.25
    arb = Waveform(data=dt, time=[0, 4e-3]).up_sample_interp(1000)
    fgenCh.Configure_ArbitraryFromWaveform(WaveformObj=arb)
    fgenCh.Enable()

