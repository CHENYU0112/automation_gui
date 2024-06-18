import math
import time
import clr

if __name__ == '__main__':
    clr.AddReference('USB007_x64')
    clr.FindAssembly('USB007_x64')
else:
    clr.AddReference('pverifyDrivers/USB007_x64')
    clr.FindAssembly('pverifyDrivers/USB007_x64')


from USB007_x64 import USB007

class Acadia():

    _addrList = list()

    def __init__(self):
        self.i2c = USB007()
        self.i2c.Connect()
        self._addrList = self._scan_i2c()
        self._i2cAddr = self._addrList[0]
        self._slaveAddr = self._addrList[1]

    def _set_page(self, slaveAddr):
        page_register = 0x00
        freq_page = 0x00
        # setting to page 0
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, page_register, [freq_page])
        self.i2c.MrwExecute(True)

    def _read2bytes(self, reg, slaveAddr=0):
        # return list [high byte, low byte]
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        data = [reg]
        self.i2c.MrwInitialize()
        self.i2c.MrwReadWrite(slaveAddr, data, 2)
        ret = self.i2c.MrwExecute(True)
        ret = [ret[1], ret[0]]
        return ret

    def _scan_i2c(self):
        retList = list()
        for _ in range(128):
            try:
                self.i2c.ReadRegister(_, 0)
                retList.append(_)
            except:
                continue
        return retList

    def scan_i2c(self):
        ret = list()
        for item in self._addrList:
            ret.append(hex(item))
        return ret

    def set_frequency(self, freq, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        freq_register = 0x33
        # creating data for frequency
        freq_data = [0, 0]
        f2bytes = int(freq / 2).to_bytes(2, 'little')
        freq_data[0] = f2bytes[0]
        freq_data[1] = f2bytes[1] | 0b00001000
        # setting frequency
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, freq_register, freq_data)
        self.i2c.MrwExecute(True)

    def set_vout(self, voltage, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        vout_register = 0x21
        # select loop 1
        self.i2c.WriteRegister(self._i2cAddr, 0xff, int(0x04).to_bytes(1, 'little'))
        # get value from register 0x2A
        data = self.i2c.ReadRegister(self._i2cAddr, 0x2A)
        # change bit to activate pmbus control
        newData = data | 0b01000000
        # re-write register 2A value
        self.i2c.WriteRegister(self._i2cAddr, 0x2A, int(newData).to_bytes(1, 'little'))
        # setting to page 0
        self._set_page(slaveAddr)
        # creating data for vout
        volt_data = [0, 0]
        voltage = math.ceil(voltage / 0.003906)
        v2bytes = int(voltage).to_bytes(2, 'little')
        volt_data[0] = v2bytes[0]
        volt_data[1] = v2bytes[1]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, vout_register, volt_data)
        self.i2c.MrwExecute(True)

    def pwm_on_off(self, state='ON', slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        self.i2c.WriteRegister(slaveAddr, 0x02, int(0x1F).to_bytes(1, 'little'))
        if state.upper() == 'ON':
            self.i2c.WriteRegister(slaveAddr, 0x01, int(0x80).to_bytes(1, 'little'))
        else:
            self.i2c.WriteRegister(slaveAddr, 0x01, int(0x00).to_bytes(1, 'little'))

    def check_status(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        #get reg0x79 value, read Status word
        reg = self._read2bytes(0x79, slaveAddr)
        status_L = reg[0]
        status_H = reg[1]
        fault = 0
        if status_H & 128 == 128:
            print("Vout fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7A)
            if(reg2 & 128) == 128:
                print('OV Fault')
            if reg2 & 64 == 64:
                print('OV Warning')
            if reg2 & 32 == 32:
                print('UV Warning')
            if reg2 & 16 == 16:
                print("UV Fault")
            if reg2 & 8 == 8:
                print('VOUT MAX WARNING')
            if reg2 & 4 == 4:
                print('TON MAX FAULT')
            fault += 1
        if status_H & 64 == 64:
            print("Iout fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7B)
            if reg2 & 128 == 128:
                print('OC Fault')
            if reg2 & 32 == 32:
                print('OC Warning')
            if reg2 & 8 == 8:
                print('IOUT Current Share')
            fault += 2
        if status_H & 32 == 32:
            print("Vin fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7C)
            if reg2 & 128 == 128:
                print('VIN OV Fault')
            if reg2 & 32 == 32:
                print('VIN UV Warning')
            if reg2 & 8 == 8:
                print('VIN UV Fault')
            if reg2 & 2 == 2:
                print('IIN OC Warning')
            fault += 4
        if status_H & 16 == 16:
            print("MFR Fault, possible driver fault")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x80)
            if reg2 & 128 == 128:
                print('Phase Fault')
            if reg2 & 8 == 8:
                print('IOUT phase current imbalance')
            if reg2 & 4 == 4:
                print('VAUX UV Fault')
            if reg2 & 2 == 2:
                print('TSEN Fault')
            if reg2 & 1 == 1:
                print('Phase Fault')
            fault += 8
        if status_H & 8 == 8:
            print("Negated POWER_GOOD")
            fault += 16
        if status_L & 64 == 64:
            print("No Power to Output.")
            fault += 32
        if status_L & 32 == 32:
            print("Vout OVP fault")
            fault += 64
        if status_L & 16 == 16:
            print("Iout OCP fault")
            fault += 128
        if status_L & 8 == 8:
            print("IUVP fault")
            fault += 256
        if status_L & 4 == 4:
            print("Temperature fault OTP")
            fault += 512
        if status_L & 2 == 2:
            print("A Dongle communication, memory, or logic warning.")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7E)
            if reg2 & 128 == 128:
                print('Invalid / Unsupported Command')
            if reg2 & 64 == 64:
                print('Invalid / Unsupported Data')
            if reg2 & 32 == 32:
                print('Packet Error Check Failed')
            if reg2 & 2 == 2:
                print('Other Communication Fault')
            fault += 1024
        if status_L & 1 == 1:
            print("Status not listed")
            fault += 2048

        return fault

    def get_temp(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        toutBytes = self._read2bytes(0x8D, slaveAddr)
        tout_c = toutBytes[1] | ((toutBytes[0] & 0b00000111) << 8)
        print(tout_c)
        return tout_c

    def set_pid_kp(self, value, i2cAddr=0):
        if i2cAddr == 0:
            i2cAddr = self._i2cAddr
        mask = 0b11000000
        self.i2c.WriteRegister(i2cAddr, 0xff, int(0x04).to_bytes(1, 'little'))
        data = self.i2c.ReadRegister(i2cAddr, 0x23)
        value = (data & mask) | value
        self.i2c.WriteRegister(i2cAddr, 0x23, int(value).to_bytes(1, 'little'))

    def enable_8_phases_control(self):
        # register to enable phase selection
        enPhaseCalibrationReg = 0x82
        # register to change the phase
        loop1SelectPhaseReg = 0x94
        # register to activate phases
        loop1ActivePhaseReg = 0x24
        self.i2c.WriteRegister(self._i2cAddr, 0xFF, int(0x00).to_bytes(1, 'little'))
        self.i2c.WriteRegister(self._i2cAddr, loop1SelectPhaseReg, int(0x00).to_bytes(1, 'little'))
        self.i2c.WriteRegister(self._i2cAddr, enPhaseCalibrationReg + 1, int(0x01).to_bytes(1, 'little'))
        self.i2c.WriteRegister(self._i2cAddr, loop1ActivePhaseReg, int(7).to_bytes(1, 'little'))

    def select_phase(self, Phase=1):
        loop1SelectPhaseReg = 0x94
        self.i2c.WriteRegister(self._i2cAddr, loop1SelectPhaseReg + 1, int(Phase * 4).to_bytes(1, 'little'))

    def diode_emulation(self, state='OFF', cutoff=8):
        if state.upper() == 'ON':
            self.i2c.WriteRegister(self._i2cAddr, 0xFF, int(0x00).to_bytes(1, 'little'))
            self.i2c.WriteRegister(self._slaveAddr, 0x01, int(0x80).to_bytes(1, 'little'))
            time.sleep(2)
            self.i2c.WriteRegister(self._i2cAddr, 0xFF, int(0x04).to_bytes(1, 'little'))
            self.i2c.WriteRegister(self._i2cAddr, 0x32, int(0x10).to_bytes(1, 'little'))
            # for 7A -> 0x1C, 8A -> 0x20
            cutoff = 0x40 + 4 * cutoff
            self.i2c.WriteRegister(self._i2cAddr, 0x40, int(cutoff).to_bytes(1, 'little'))
        else:
            self.i2c.WriteRegister(self._i2cAddr, 0x32, int(0x00).to_bytes(1, 'little'))

    def clear_faults(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        data = int(0xFF).to_bytes(1, 'little')
        self._set_page(slaveAddr)
        self.i2c.WriteRegister(slaveAddr, 0x03, data)

    def close(self):
        self.i2c.Close()

class Sierra():
    _addrList = list()

    def __init__(self):
        self.i2c = USB007()
        self.i2c.Connect()
        self._addrList = self._scan_i2c()
        self._i2cAddr = self._addrList[0]
        self._slaveAddr = self._i2cAddr

    def _set_page(self, slaveAddr, page=0x00):
        page_register = 0x00
        # setting to page 0
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, page_register, [page])
        self.i2c.MrwExecute(True)

    def _read2bytes(self, reg, slaveAddr=0):
        # return list [high byte, low byte]
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        data = [reg]
        self.i2c.MrwInitialize()
        self.i2c.MrwReadWrite(slaveAddr, data, 2)
        ret = self.i2c.MrwExecute(True)
        ret = [ret[1], ret[0]]
        return ret

    def _scan_i2c(self):
        retList = list()
        for _ in range(128):
            try:
                self.i2c.ReadRegister(_, 0)
                retList.append(_)
            except:
                continue
        return retList

    def _get_nph_max(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        time.sleep(1)
        self._set_page(slaveAddr, page=0x20)
        nph_max_read = self._read2bytes(0x1e, slaveAddr)
        nph_max = (nph_max_read[1] & 0b11110000) >> 4
        return nph_max

    def scan_i2c(self):
        ret = list()
        for item in self._addrList:
            ret.append(hex(item))
        return ret

    def set_frequency(self, freq, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self.pwm_on_off(state='OFF')
        time.sleep(1)
        self._set_page(slaveAddr, page=0x20)
        freq_register = 0x27
        nph_max = self._get_nph_max()
        data = self._read2bytes(freq_register, slaveAddr)
        # creating data for frequency
        freq_data = [0, 0]
        if nph_max == 0:
            nph_max = 1
        freq_data[0] = int(50000.0 / float(freq * nph_max))
        freq_data[1] = data[0]
        # setting frequency
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, freq_register, freq_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.5)
        self.pwm_on_off(state='ON')

    def set_vout(self, voltage, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        vout_register = 0x21
        # setting to page 0
        self._set_page(slaveAddr)
        # creating data for vout
        volt_data = [0, 0]
        voltage = (1 + (voltage - 0.5) / 0.01)
        v2bytes = int(voltage).to_bytes(2, 'little')
        volt_data[0] = v2bytes[0]
        volt_data[1] = v2bytes[1]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, vout_register, volt_data)
        self.i2c.MrwExecute(True)

    def pwm_on_off(self, state='ON', slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        self.i2c.WriteRegister(slaveAddr, 0x02, int(0x1F).to_bytes(1, 'little'))
        if state.upper() == 'ON':
            self.i2c.WriteRegister(slaveAddr, 0x01, int(0x80).to_bytes(1, 'little'))
        else:
            self.i2c.WriteRegister(slaveAddr, 0x01, int(0x00).to_bytes(1, 'little'))

    def check_status(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        # get reg0x79 value, read Status word
        reg = self._read2bytes(0x79, slaveAddr)
        status_L = reg[0]
        status_H = reg[1]
        fault = 0
        if status_H & 128 == 128:
            print("Vout fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7A)
            if (reg2 & 128) == 128:
                print('OV Fault')
            if reg2 & 64 == 64:
                print('OV Warning')
            if reg2 & 32 == 32:
                print('UV Warning')
            if reg2 & 16 == 16:
                print("UV Fault")
            if reg2 & 8 == 8:
                print('VOUT MAX WARNING')
            if reg2 & 4 == 4:
                print('TON MAX FAULT')
            fault += 1
        if status_H & 64 == 64:
            print("Iout fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7B)
            if reg2 & 128 == 128:
                print('OC Fault')
            if reg2 & 32 == 32:
                print('OC Warning')
            if reg2 & 8 == 8:
                print('IOUT Current Share')
            fault += 2
        if status_H & 32 == 32:
            print("Vin fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7C)
            if reg2 & 128 == 128:
                print('VIN OV Fault')
            if reg2 & 32 == 32:
                print('VIN UV Warning')
            if reg2 & 8 == 8:
                print('VIN UV Fault')
            if reg2 & 2 == 2:
                print('IIN OC Warning')
            fault += 4
        if status_H & 16 == 16:
            print("MFR Fault, possible driver fault")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x80)
            if reg2 & 128 == 128:
                print('Phase Fault')
            if reg2 & 8 == 8:
                print('IOUT phase current imbalance')
            if reg2 & 4 == 4:
                print('VAUX UV Fault')
            if reg2 & 2 == 2:
                print('TSEN Fault')
            if reg2 & 1 == 1:
                print('Phase Fault')
            fault += 8
        if status_H & 8 == 8:
            print("Negated POWER_GOOD")
            fault += 16
        if status_L & 64 == 64:
            print("No Power to Output.")
            fault += 32
        if status_L & 32 == 32:
            print("Vout OVP fault")
            fault += 64
        if status_L & 16 == 16:
            print("Iout OCP fault")
            fault += 128
        if status_L & 8 == 8:
            print("IUVP fault")
            fault += 256
        if status_L & 4 == 4:
            print("Temperature fault OTP")
            fault += 512
        if status_L & 2 == 2:
            print("A Dongle communication, memory, or logic warning.")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7E)
            if reg2 & 128 == 128:
                print('Invalid / Unsupported Command')
            if reg2 & 64 == 64:
                print('Invalid / Unsupported Data')
            if reg2 & 32 == 32:
                print('Packet Error Check Failed')
            if reg2 & 2 == 2:
                print('Other Communication Fault')
            fault += 1024
        if status_L & 1 == 1:
            print("Status not listed")
            fault += 2048

        return fault

    def get_temp(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        toutBytes = self._read2bytes(0x8D, slaveAddr)
        tout_c = toutBytes[1] | ((toutBytes[0] & 0b00000111) << 8)
        print(tout_c)
        return tout_c

    def set_pid_kp(self, value, i2cAddr=0):
        if i2cAddr == 0:
            i2cAddr = self._i2cAddr
        mask = 0b11000000
        self._set_page(i2cAddr, page=0x20)
        data = self._read2bytes(0x25, i2cAddr)
        data[1] = (data[1] & mask) | value
        dataW = [data[1], data[0]]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(i2cAddr, 0x25, dataW)
        self.i2c.MrwExecute(True)

    def enable_8_phases_control(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self.pwm_on_off(state='OFF')
        time.sleep(1)
        # get frequency to correct after changing nph (frequency is dependent on nph)
        nph_max = self._get_nph_max()
        osrate = self._read2bytes(0x27, slaveAddr)[1]
        frequency = 50000 / (nph_max * osrate)
        # set to Page 0x20
        self._set_page(slaveAddr, page=0x20)
        # set nph_max to 8
        nph_max_read = self._read2bytes(0x1E, slaveAddr)
        nph_max_byte = (nph_max_read[1] & 0b00001111) | 0b10000000
        nph_max_data = [nph_max_byte, nph_max_read[0]]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x1E, nph_max_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.1)
        # set nph_ps0_max to 8
        nph_ps0_max_read = self._read2bytes(0x2C, slaveAddr)
        nph_ps0_max_byte = (nph_ps0_max_read[1] & 0b11110000) | 0b00001000
        nph_ps0_max_data = [nph_ps0_max_byte, nph_ps0_max_read[0]]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x2C, nph_ps0_max_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.1)
        # set autophase_startup to 0
        autophase_startup_read = self._read2bytes(0x38, slaveAddr)
        autophase_startup_byte = (autophase_startup_read[1] & 0b11101111)
        autophase_startup_data = [autophase_startup_byte, autophase_startup_read[0]]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x38, autophase_startup_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.1)
        # set autophase_pd_en to 0
        autophase_pd_en_read = self._read2bytes(0x2B, slaveAddr)
        autophase_pd_en_byte = (autophase_pd_en_read[0] & 0b11110000)
        autophase_pd_en_data = [autophase_pd_en_read[1], autophase_pd_en_byte]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x2B, autophase_pd_en_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.1)
        self.set_frequency(freq=frequency)
        time.sleep(0.1)
        self.pwm_on_off(state='ON')
        time.sleep(0.5)
        return

    def select_phase(self, Phase=1, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self.pwm_on_off(state='OFF')
        time.sleep(1)
        # set to Page 0x30
        self._set_page(slaveAddr, page=0x30)
        # set cal_mode to 0 and call_mask to Phase
        cal_mode_read = self._read2bytes(0x04, slaveAddr)
        cal_mode_byte = (cal_mode_read[0] | 0b00000001)
        if Phase < 1:
            cal_mask_byte = 0x00
        elif Phase > 8:
            Phase = 8
            cal_mask_byte = 2 ** (Phase-1)
        else:
            cal_mask_byte = 2 ** (Phase-1)
        cal_mode_data = [cal_mask_byte, cal_mode_byte]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x04, cal_mode_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.1)
        self.pwm_on_off(state='ON')
        time.sleep(0.5)
        return

    def diode_emulation(self, state='OFF', cutoff=8):
        pass
        # need to be verified. Function inactive for this controller.
        return
        if state.upper() == 'ON':
            self.i2c.WriteRegister(self._i2cAddr, 0xFF, int(0x00).to_bytes(1, 'little'))
            self.i2c.WriteRegister(self._slaveAddr, 0x01, int(0x80).to_bytes(1, 'little'))
            time.sleep(2)
            self.i2c.WriteRegister(self._i2cAddr, 0xFF, int(0x04).to_bytes(1, 'little'))
            self.i2c.WriteRegister(self._i2cAddr, 0x32, int(0x10).to_bytes(1, 'little'))
            # for 7A -> 0x1C, 8A -> 0x20
            cutoff = 0x40 + 4 * cutoff
            self.i2c.WriteRegister(self._i2cAddr, 0x40, int(cutoff).to_bytes(1, 'little'))
        else:
            self.i2c.WriteRegister(self._i2cAddr, 0x32, int(0x00).to_bytes(1, 'little'))

    def clear_faults(self, slaveAddr=0):
        pass
        # Not allowing to write into register. Not working.
        return
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        dataW = [0, 0]
        data = int(0xFF).to_bytes(1, 'little')
        self._set_page(slaveAddr, page=0x70)
        self.i2c.WriteRegister(slaveAddr, 0x03, data)
        # self.i2c.MrwInitialize()
        # self.i2c.MrwWrite(slaveAddr, 0x03, dataW)
        # self.i2c.MrwExecute(True)
        time.sleep(0.1)

    def close(self):
        self.i2c.Close()

class Pollino():
    _addrList = list()

    def __init__(self):
        self.i2c = USB007()
        self.i2c.Connect()
        self._addrList = self._scan_i2c()
        self._i2cAddr = self._addrList[0]
        self._slaveAddr = self._i2cAddr

    def _set_page(self, slaveAddr, page=0x00):
        page_register = 0x00
        # setting to page 0
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, page_register, [page])
        self.i2c.MrwExecute(True)

    def _read2bytes(self, reg, slaveAddr=0):
        # return list [high byte, low byte]
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        data = [reg]
        self.i2c.MrwInitialize()
        self.i2c.MrwReadWrite(slaveAddr, data, 2)
        ret = self.i2c.MrwExecute(True)
        ret = [ret[1], ret[0]]
        return ret

    def _scan_i2c(self):
        retList = list()
        for _ in range(128):
            try:
                self.i2c.ReadRegister(_, 0)
                retList.append(_)
            except:
                continue
        return retList

    def _get_nph_max(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        time.sleep(1)
        self._set_page(slaveAddr, page=0x20)
        nph_max_read = self._read2bytes(0x1e, slaveAddr)
        nph_max = (nph_max_read[1] & 0b11110000) >> 4
        return nph_max

    def scan_i2c(self):
        ret = list()
        for item in self._addrList:
            ret.append(hex(item))
        return ret

    def set_frequency(self, freq, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self.pwm_on_off(state='OFF')
        time.sleep(1)
        self._set_page(slaveAddr, page=0x20)
        freq_register = 0x27
        nph_max = self._get_nph_max()
        data = self._read2bytes(freq_register, slaveAddr)
        # creating data for frequency
        freq_data = [0, 0]
        if nph_max == 0:
            nph_max = 1
        freq_data[0] = int(50000.0 / float(freq * nph_max))
        freq_data[1] = data[0]
        # setting frequency
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, freq_register, freq_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.5)
        self.pwm_on_off(state='ON')

    def set_vout(self, voltage, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        vout_register = 0x21
        # setting to page 0
        self._set_page(slaveAddr)
        # creating data for vout
        volt_data = [0, 0]
        voltage = (1 + (voltage - 0.5) / 0.01)
        v2bytes = int(voltage).to_bytes(2, 'little')
        volt_data[0] = v2bytes[0]
        volt_data[1] = v2bytes[1]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, vout_register, volt_data)
        self.i2c.MrwExecute(True)

    def pwm_on_off(self, state='ON', slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        self.i2c.WriteRegister(slaveAddr, 0x02, int(0x1F).to_bytes(1, 'little'))
        if state.upper() == 'ON':
            self.i2c.WriteRegister(slaveAddr, 0x01, int(0x80).to_bytes(1, 'little'))
        else:
            self.i2c.WriteRegister(slaveAddr, 0x01, int(0x00).to_bytes(1, 'little'))

    def check_status(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        # get reg0x79 value, read Status word
        reg = self._read2bytes(0x79, slaveAddr)
        status_L = reg[0]
        status_H = reg[1]
        fault = 0
        if status_H & 128 == 128:
            print("Vout fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7A)
            if (reg2 & 128) == 128:
                print('OV Fault')
            if reg2 & 64 == 64:
                print('OV Warning')
            if reg2 & 32 == 32:
                print('UV Warning')
            if reg2 & 16 == 16:
                print("UV Fault")
            if reg2 & 8 == 8:
                print('VOUT MAX WARNING')
            if reg2 & 4 == 4:
                print('TON MAX FAULT')
            fault += 1
        if status_H & 64 == 64:
            print("Iout fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7B)
            if reg2 & 128 == 128:
                print('OC Fault')
            if reg2 & 32 == 32:
                print('OC Warning')
            if reg2 & 8 == 8:
                print('IOUT Current Share')
            fault += 2
        if status_H & 32 == 32:
            print("Vin fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7C)
            if reg2 & 128 == 128:
                print('VIN OV Fault')
            if reg2 & 32 == 32:
                print('VIN UV Warning')
            if reg2 & 8 == 8:
                print('VIN UV Fault')
            if reg2 & 2 == 2:
                print('IIN OC Warning')
            fault += 4
        if status_H & 16 == 16:
            print("MFR Fault, possible driver fault")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x80)
            if reg2 & 128 == 128:
                print('Phase Fault')
            if reg2 & 8 == 8:
                print('IOUT phase current imbalance')
            if reg2 & 4 == 4:
                print('VAUX UV Fault')
            if reg2 & 2 == 2:
                print('TSEN Fault')
            if reg2 & 1 == 1:
                print('Phase Fault')
            fault += 8
        if status_H & 8 == 8:
            print("Negated POWER_GOOD")
            fault += 16
        if status_L & 64 == 64:
            print("No Power to Output.")
            fault += 32
        if status_L & 32 == 32:
            print("Vout OVP fault")
            fault += 64
        if status_L & 16 == 16:
            print("Iout OCP fault")
            fault += 128
        if status_L & 8 == 8:
            print("IUVP fault")
            fault += 256
        if status_L & 4 == 4:
            print("Temperature fault OTP")
            fault += 512
        if status_L & 2 == 2:
            print("A Dongle communication, memory, or logic warning.")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7E)
            if reg2 & 128 == 128:
                print('Invalid / Unsupported Command')
            if reg2 & 64 == 64:
                print('Invalid / Unsupported Data')
            if reg2 & 32 == 32:
                print('Packet Error Check Failed')
            if reg2 & 2 == 2:
                print('Other Communication Fault')
            fault += 1024
        if status_L & 1 == 1:
            print("Status not listed")
            fault += 2048

        return fault

    def get_temp(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        toutBytes = self._read2bytes(0x8D, slaveAddr)
        tout_c = toutBytes[1] | ((toutBytes[0] & 0b00000111) << 8)
        print(tout_c)
        return tout_c

    def set_pid_kp(self, value, i2cAddr=0):
        if i2cAddr == 0:
            i2cAddr = self._i2cAddr
        mask = 0b11000000
        self._set_page(i2cAddr, page=0x20)
        data = self._read2bytes(0x25, i2cAddr)
        data[1] = (data[1] & mask) | value
        dataW = [data[1], data[0]]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(i2cAddr, 0x25, dataW)
        self.i2c.MrwExecute(True)

    def enable_8_phases_control(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self.pwm_on_off(state='OFF')
        time.sleep(1)
        # get frequency to correct after changing nph (frequency is dependent on nph)
        nph_max = self._get_nph_max()
        osrate = self._read2bytes(0x27, slaveAddr)[1]
        frequency = 50000 / (nph_max * osrate)
        # set to Page 0x20
        self._set_page(slaveAddr, page=0x20)
        # set nph_max to 8
        nph_max_read = self._read2bytes(0x1E, slaveAddr)
        nph_max_byte = (nph_max_read[1] & 0b00001111) | 0b10000000
        nph_max_data = [nph_max_byte, nph_max_read[0]]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x1E, nph_max_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.1)
        # set nph_ps0_max to 8
        nph_ps0_max_read = self._read2bytes(0x2C, slaveAddr)
        nph_ps0_max_byte = (nph_ps0_max_read[1] & 0b11110000) | 0b00001000
        nph_ps0_max_data = [nph_ps0_max_byte, nph_ps0_max_read[0]]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x2C, nph_ps0_max_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.1)
        # set autophase_startup to 0
        autophase_startup_read = self._read2bytes(0x38, slaveAddr)
        autophase_startup_byte = (autophase_startup_read[1] & 0b11101111)
        autophase_startup_data = [autophase_startup_byte, autophase_startup_read[0]]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x38, autophase_startup_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.1)
        # set autophase_pd_en to 0
        autophase_pd_en_read = self._read2bytes(0x2B, slaveAddr)
        autophase_pd_en_byte = (autophase_pd_en_read[0] & 0b11110000)
        autophase_pd_en_data = [autophase_pd_en_read[1], autophase_pd_en_byte]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x2B, autophase_pd_en_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.1)
        self.set_frequency(freq=frequency)
        time.sleep(0.1)
        self.pwm_on_off(state='ON')
        time.sleep(0.5)
        return

    def select_phase(self, Phase=1, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self.pwm_on_off(state='OFF')
        time.sleep(1)
        # set to Page 0x30
        self._set_page(slaveAddr, page=0x30)
        # set cal_mode to 0 and call_mask to Phase
        cal_mode_read = self._read2bytes(0x04, slaveAddr)
        cal_mode_byte = (cal_mode_read[0] | 0b00000001)
        if Phase < 1:
            cal_mask_byte = 0x00
        elif Phase > 8:
            Phase = 8
            cal_mask_byte = 2 ** (Phase-1)
        else:
            cal_mask_byte = 2 ** (Phase-1)
        cal_mode_data = [cal_mask_byte, cal_mode_byte]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x04, cal_mode_data)
        self.i2c.MrwExecute(True)
        time.sleep(0.1)
        self.pwm_on_off(state='ON')
        time.sleep(0.5)
        return

    def diode_emulation(self, state='OFF', cutoff=8):
        pass
        # need to be verified. Function inactive for this controller.
        return
        if state.upper() == 'ON':
            self.i2c.WriteRegister(self._i2cAddr, 0xFF, int(0x00).to_bytes(1, 'little'))
            self.i2c.WriteRegister(self._slaveAddr, 0x01, int(0x80).to_bytes(1, 'little'))
            time.sleep(2)
            self.i2c.WriteRegister(self._i2cAddr, 0xFF, int(0x04).to_bytes(1, 'little'))
            self.i2c.WriteRegister(self._i2cAddr, 0x32, int(0x10).to_bytes(1, 'little'))
            # for 7A -> 0x1C, 8A -> 0x20
            cutoff = 0x40 + 4 * cutoff
            self.i2c.WriteRegister(self._i2cAddr, 0x40, int(cutoff).to_bytes(1, 'little'))
        else:
            self.i2c.WriteRegister(self._i2cAddr, 0x32, int(0x00).to_bytes(1, 'little'))

    def clear_faults(self, slaveAddr=0):
        pass
        # Not allowing to write into register. Not working.
        return
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        dataW = [0, 0]
        data = int(0xFF).to_bytes(1, 'little')
        self._set_page(slaveAddr, page=0x70)
        self.i2c.WriteRegister(slaveAddr, 0x03, data)
        # self.i2c.MrwInitialize()
        # self.i2c.MrwWrite(slaveAddr, 0x03, dataW)
        # self.i2c.MrwExecute(True)
        time.sleep(0.1)

    def close(self):
        self.i2c.Close()

class McKinley():
    _addrList = list()

    def __init__(self):
        self.i2c = USB007()
        self.i2c.Connect()
        self._addrList = self._scan_i2c()
        self._i2cAddr = self._addrList[0]
        self._slaveAddr = self._i2cAddr
        # self._set_pmbus()

    def _set_page(self, slaveAddr, page=0x00):
        page_register = 0x00
        # setting to page 0
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, page_register, [page])
        self.i2c.MrwExecute(True)

    def _read2bytes(self, reg, slaveAddr=0):
        # return list [high byte, low byte]
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        data = [reg]
        self.i2c.MrwInitialize()
        self.i2c.MrwReadWrite(slaveAddr, data, 2)
        ret = self.i2c.MrwExecute(True)
        ret = [ret[1], ret[0]]
        return ret

    def _scan_i2c(self):
        retList = list()
        for _ in range(128):
            try:
                self.i2c.ReadRegister(_, 0)
                retList.append(_)
            except:
                continue
        return retList

    def _get_nph_max(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        time.sleep(1)
        self._set_page(slaveAddr, page=0x20)
        nph_max_read = self._read2bytes(0x1e, slaveAddr)
        nph_max = (nph_max_read[1] & 0b11110000) >> 4
        return nph_max

    def _set_pmbus(self, slaveAddr=None):
        #for now this function is not being used. It is creating a "lock" on controller functionalities
        if slaveAddr is None:
            slaveAddr = self._slaveAddr
        reg_0x200585B0 = self.i2c.AHBRead(slaveAddr, 0xCE, 0xDF, 0x200585B0)
        pmbusByteArray = [0x40, reg_0x200585B0[1], reg_0x200585B0[2], reg_0x200585B0[3]]
        self.i2c.AHBWrite(slaveAddr, 0xCE, 0xDE, 0x200585B0, pmbusByteArray)
        reg_0x700001404 =self.i2c.AHBRead(slaveAddr, 0xCE, 0xDF, 0x70001404)
        pmbusByteArray = [((reg_0x700001404[0] | 0b01000000) & 0b01111111), reg_0x700001404[1], reg_0x700001404[2], reg_0x700001404[3]]
        self.i2c.AHBWrite(slaveAddr, 0xCE, 0xDE, 0x70001404, pmbusByteArray)
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0x01, [0x80])
        self.i2c.MrwExecute(True)
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, 0xFE, [0x1D])
        self.i2c.MrwExecute(True)
        self.pwm_on_off(state='OFF')
        time.sleep(1)
        self.pwm_on_off(state='ON')

    def scan_i2c(self):
        ret = list()
        for item in self._addrList:
            ret.append(hex(item))
        return ret

    def set_frequency(self, freq, slaveAddr=0):
        if int(freq) > 2000:
            print('For now it is not possible to go higher than 2000kHz on this controller')
            freq = 2000
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        freq_register = 0x33
        # setting to page 0
        self._set_page(slaveAddr, page=0x00)
        # creating data for freq
        freq_data = [0, 0]
        frequency = freq / 2
        v2bytes = int(frequency).to_bytes(2, 'little')
        freq_data[0] = v2bytes[0]
        freq_data[1] = (v2bytes[1] | 0b00001000)
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, freq_register, freq_data)
        self.i2c.MrwExecute(True)

    def set_vout(self, voltage, slaveAddr=0):
        print(f'mckinley set_vout called. Voltage={voltage}')
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        vout_register = 0x21
        # setting to page 0
        self._set_page(slaveAddr, page=0x00)
        # creating data for vout
        volt_data = [0, 0]
        # voltage = (1 + (voltage - 0.5) / 0.01)
        voltage = voltage / 0.00195313725490196078431372549
        v2bytes = int(voltage).to_bytes(2, 'little')
        volt_data[0] = v2bytes[0]
        volt_data[1] = v2bytes[1]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(slaveAddr, vout_register, volt_data)
        self.i2c.MrwExecute(True)

    def pwm_on_off(self, state='ON', slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        reg_0x200585AC = self.i2c.AHBRead(slaveAddr, 0xCE, 0xDF, 0x200585AC)
        if state.upper() == 'ON':
            pmbusByteArray = [0x01, reg_0x200585AC[1], reg_0x200585AC[2], reg_0x200585AC[3]]
            self.i2c.AHBWrite(slaveAddr, 0xCE, 0xDE, 0x200585AC, pmbusByteArray)
        else:
            pmbusByteArray = [0x11, reg_0x200585AC[1], reg_0x200585AC[2], reg_0x200585AC[3]]
            self.i2c.AHBWrite(slaveAddr, 0xCE, 0xDE, 0x200585AC, pmbusByteArray)
        # self.i2c.MrwInitialize()
        # self.i2c.MrwWrite(slaveAddr, 0xFE, [0x1D])
        # exec_ret = self.i2c.MrwExecute(True)
        self._set_page(slaveAddr, 0x00)
        self.i2c.WriteRegister(slaveAddr, 0xFE, 0x1D)
        read = self.i2c.ReadRegister(slaveAddr, 0xFE)
        print(read)

    def check_status(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        # get reg0x79 value, read Status word
        reg = self._read2bytes(0x79, slaveAddr)
        status_L = reg[0]
        status_H = reg[1]
        fault = 0
        if status_H & 128 == 128:
            print("Vout fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7A)
            if (reg2 & 128) == 128:
                print('OV Fault')
            if reg2 & 64 == 64:
                print('OV Warning')
            if reg2 & 32 == 32:
                print('UV Warning')
            if reg2 & 16 == 16:
                print("UV Fault")
            if reg2 & 8 == 8:
                print('VOUT MAX WARNING')
            if reg2 & 4 == 4:
                print('TON MAX FAULT')
            fault += 1
        if status_H & 64 == 64:
            print("Iout fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7B)
            if reg2 & 128 == 128:
                print('OC Fault')
            if reg2 & 32 == 32:
                print('OC Warning')
            if reg2 & 8 == 8:
                print('IOUT Current Share')
            fault += 2
        if status_H & 32 == 32:
            print("Vin fault/warning")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7C)
            if reg2 & 128 == 128:
                print('VIN OV Fault')
            if reg2 & 32 == 32:
                print('VIN UV Warning')
            if reg2 & 8 == 8:
                print('VIN UV Fault')
            if reg2 & 2 == 2:
                print('IIN OC Warning')
            fault += 4
        if status_H & 16 == 16:
            print("MFR Fault, possible driver fault")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x80)
            if reg2 & 128 == 128:
                print('Phase Fault')
            if reg2 & 8 == 8:
                print('IOUT phase current imbalance')
            if reg2 & 4 == 4:
                print('VAUX UV Fault')
            if reg2 & 2 == 2:
                print('TSEN Fault')
            if reg2 & 1 == 1:
                print('Phase Fault')
            fault += 8
        if status_H & 8 == 8:
            print("Negated POWER_GOOD")
            fault += 16
        if status_L & 64 == 64:
            print("No Power to Output.")
            fault += 32
        if status_L & 32 == 32:
            print("Vout OVP fault")
            fault += 64
        if status_L & 16 == 16:
            print("Iout OCP fault")
            fault += 128
        if status_L & 8 == 8:
            print("IUVP fault")
            fault += 256
        if status_L & 4 == 4:
            print("Temperature fault OTP")
            fault += 512
        if status_L & 2 == 2:
            print("A Dongle communication, memory, or logic warning.")
            reg2 = self.i2c.ReadRegister(slaveAddr, 0x7E)
            if reg2 & 128 == 128:
                print('Invalid / Unsupported Command')
            if reg2 & 64 == 64:
                print('Invalid / Unsupported Data')
            if reg2 & 32 == 32:
                print('Packet Error Check Failed')
            if reg2 & 2 == 2:
                print('Other Communication Fault')
            fault += 1024
        if status_L & 1 == 1:
            print("Status not listed")
            fault += 2048

        return fault

    def get_temp(self, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self._set_page(slaveAddr)
        toutBytes = self._read2bytes(0x8D, slaveAddr)
        tout_c = toutBytes[1] | ((toutBytes[0] & 0b00000111) << 8)
        print(tout_c)
        return tout_c

    def set_pid_kp(self, value, i2cAddr=0):
        if i2cAddr == 0:
            i2cAddr = self._i2cAddr
        mask = 0b11000000
        self._set_page(i2cAddr, page=0x20)
        data = self._read2bytes(0x25, i2cAddr)
        data[1] = (data[1] & mask) | value
        dataW = [data[1], data[0]]
        self.i2c.MrwInitialize()
        self.i2c.MrwWrite(i2cAddr, 0x25, dataW)
        self.i2c.MrwExecute(True)

    def enable_8_phases_control(self, slaveAddr=0):
        pass
        # McKenley has a way to enable all 8 phases, but for the purpose of testing each phase individually this is not
        #   necessary
        return

    def select_phase(self, Phase=1, slaveAddr=0):
        if slaveAddr == 0:
            slaveAddr = self._slaveAddr
        self.pwm_on_off(state='OFF')
        time.sleep(1)
        # set to Page 0x30
        if Phase < 1:
            Phase = 1
            phase_data = 1
        elif Phase > 8:
            Phase = 8
            phase_data = 2 ** (Phase-1)
        else:
            phase_data = 2 ** (Phase-1)
        phase_data_bytes = int(phase_data).to_bytes(4, 'little')
        phase_data_bytes_array = [phase_data_bytes[0], phase_data_bytes[1], phase_data_bytes[2], phase_data_bytes[3]]
        self.i2c.AHBWrite(slaveAddr, 0xCE, 0xDE, 0x70000C0C, phase_data_bytes_array)
        time.sleep(0.1)
        self.pwm_on_off(state='ON')
        time.sleep(0.5)
        return

    def diode_emulation(self, state='OFF', cutoff=8, slaveAddr=None):
        pass
        # not fully working. Need to understand better how McKinley controls diode emulation
        # the code below is for McKinley, but it is only changing the threshold
        return
        if slaveAddr is None:
            slaveAddr = self._slaveAddr
        if state.upper() == 'ON':
            cutoff = 4 * float(cutoff)
            cutoffBytes = int(cutoff).to_bytes(4, 'little')
            cutoffBytesArray = [cutoffBytes[0], cutoffBytes[1], cutoffBytes[2], cutoffBytes[3],]
            self.i2c.AHBWrite(slaveAddr, 0xCE, 0xDE, 0x70000C58, cutoffBytesArray)
            time.sleep(0.1)
        else:
            cutoffBytesArray = [0,0,0,0]
            self.i2c.AHBWrite(slaveAddr, 0xCE, 0xDE, 0x70000C58, cutoffBytesArray)
            time.sleep(0.1)
        return

    def clear_faults(self, slaveAddr=0):
        pass
        # Not working.
        return

    def close(self):
        self.i2c.Close()


if __name__ == '__main__':
    myd = McKinley()
    # vout_reg_val = myd._read2bytes(reg=0x21)
    # print(vout_reg_val)
    myd.set_vout(1.2)
    myd.set_frequency(800)
    myd.pwm_on_off(state='OFF')
    # time.sleep(1)
    # myd.pwm_on_off(state='ON')
    # myd.get_temp()
    # print(myd.check_status())
    # myd.set_pid_kp(27)
    # myd.clear_faults()
    # myd.enable_8_phases_control()
    # myd.select_phase(Phase=1)
    # time.sleep(10)
    # myd.select_phase(Phase=1)
    # myd._set_pmbus()
