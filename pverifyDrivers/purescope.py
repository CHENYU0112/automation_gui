import pyvisa as visa
from time import sleep

class TEK_MSO5X():
    '''
    Supported Instruments
        MSO54, MSO56, MSO58, MSO58LP, MSO64, MSO44, MSO46, LDP_64, MSO64B, MSO66B, MSO68B
    '''

    ID = 'MSO5x'

    def __init__(self, Address, Reset=False, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        if Reset:
            self._write('*RST')

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, *args, **kwargs):
        data = self.cmd.query(command)
        return data

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")

    def saveimage(self, Filename=None, *args, **kwargs):
        Background = kwargs['Background'] if 'Background' in kwargs else 'black'
        """ save the scope shoot image """
        if(Background.lower() == 'white'):
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
        self._write('FILESystem:READFile "C:/Temp.png"') #,GPIB
        sleep(0.5)
        data = self.cmd.read_raw()
        img = bytearray(data)
        fn = open(Filename, 'wb')
        fn.write(img)
        fn.close()
        self._write(':FILESystem:DELEte "C:/Temp.png"')
        if(Background.lower() == 'white'):
            self._write('DIS:COL NORM')
            self._write('SAV:IMAG:COMP NORM')
            sleep(0.35)

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

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")


class TEK_MSO5XB():
    '''
        Supported Instruments
            MSO58B
        '''

    ID = 'MSO5xB'
    channel = None

    def __init__(self, Address, Reset=True, *args, **kwargs):
        self.address = Address
        self.cmd = visa.ResourceManager().open_resource(Address)
        if Reset:
            self._write('*RST')

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, *args, **kwargs):
        data = self.cmd.query(command)
        return data

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")

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
        data = self.cmd.read_raw()
        img = bytearray(data)
        fn = open(Filename, 'wb')
        fn.write(img)
        fn.close()
        self._write(':FILESystem:DELEte "C:/Temp.png"')
        if (Background.lower() == 'white'):
            self._write('DIS:COL NORM')
            self._write('SAV:IMAG:COMP NORM')
            sleep(0.35)

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

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")


class Tkdpo4k():

    ID = '4k'

    def __init__(self, Address, Reset=False, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        if Reset:
            self._write('*RST')

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, *args, **kwargs):
        data = self.cmd.query(command)
        return data

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")


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
        with open(Filename, 'wb') as fn:
            fn.write(img)
        self._write('USBD:CONF USBT')

    def set_trigger(self, ch=None, level=None, slope=None, coupling=None, *args, **kwargs):
        if ch is not None:
            self._write(f'TRIG:A:EDGE:SOU CH{ch}')
        if level is not None:
            self._write(f'TRIG:A:LEV {level}')
        if slope is not None:
            self._write(f'TRIG:A:EDGE:SLO {slope}')
        if coupling is not None:
            self._write(f'TRIG:A:EDGE:COUP {coupling}')

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")


class Tkdpo7k():
    '''
        Supported Instruments
            Tektronix DPO 7000 Series Oscilloscopes
            DPO7104, DPO7054, DPO7254, DPO7354, DPO70404, DPO70604, DPO70804, DPO71254, DPO71604, DPO72004, DSA70404,
            DSA70604, DSA70804, DSA71254, DSA71604, DSA72004, MSO70404, MSO70604, MSO70804, MSO71254, MSO71604,
            MSO72004, MSO5034, MSO5054, MSO5104, MSO5204, DPO5034, DPO5054, DPO5104, DPO5204
        '''

    ID = '7k'

    def __init__(self, Address, Reset=False, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        if Reset:
            self._write('*RST')

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, *args, **kwargs):
        data = self.cmd.query(command)
        return data

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")

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
        data = self.cmd.read_raw()
        img = bytearray(data)
        fn = open(Filename, 'wb')
        fn.write(img)
        fn.close()
        self._write(':FILESystem:DELEte "C:/Temp.png"')

    def set_trigger(self, ch=None, level=None, slope=None, coupling=None, *args, **kwargs):
        if ch is not None:
            self._write(f'TRIG:A:EDGE:SOU CH{ch}')
        if level is not None:
            self._write(f'TRIG:A:LEV {level}')
        if slope is not None:
            self._write(f'TRIG:A:EDGE:SLO {slope}')
        if coupling is not None:
            self._write(f'TRIG:A:EDGE:COUP {coupling}')

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")


class TekScope():
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

    def __init__(self, Address, Reset=False, *args, **kwargs):
        self.cmd = visa.ResourceManager().open_resource(Address)
        if Reset:
            self._write('*RST')

    def _write(self, command, *args, **kwargs):
        self.cmd.write(command)

    def _query(self, command, *args, **kwargs):
        data = self.cmd.query(command)
        return data

    def run(self, *args, **kwargs):
        """ run the scope/screen """
        self._write("acquire:stopafter runstop")
        self._write("acquire:state run")

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
        data = self.cmd.read_raw()
        img = bytearray(data)
        fn = open(Filename, 'wb')
        fn.write(img)
        fn.close()
        self._write(':FILESystem:DELEte "C:\Temp\Temp.png"')

    def set_trigger(self, ch=None, level=None, slope=None, coupling=None, *args, **kwargs):
        if ch is not None:
            self._write(f'TRIG:A:EDGE:SOU CH{ch}')
        if level is not None:
            self._write(f'TRIG:A:LEV {level}')
        if slope is not None:
            self._write(f'TRIG:A:EDGE:SLO {slope}')
        if coupling is not None:
            self._write(f'TRIG:A:EDGE:COUP {coupling}')

    def single_trg(self):
        self._write('ACQ:STOPA SEQ')
        self._write('ACQ:STATE RUN')

    def stop(self, *args, **kwargs):
        """ stop the screen """
        self._write("acquire:state stop")





