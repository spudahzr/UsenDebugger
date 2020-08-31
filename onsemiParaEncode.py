# -*- coding: utf-8 -*-


class OnsemiParaEncode(object):
    def __init__(self):
        self.__Tdata_Def = {'Onsemi_CmdPluse_Def': 'TDATA_L', 'Onsemi_CmdSep_Def': 'TDATA_SEP_H',
                            'Onsemi_Tbit0_Def': 'UNION_TBIT0', 'Onsemi_Tbit1_Def': 'UNION_TBIT1'}

    def onsemi_set_settingdef(self, defined):
        for key, value in defined.items():
            if key in self.__Tdata_Def:
                self.__Tdata_Def[key] = value

    def onsemi_get_settingdef(self):
        return self.__Tdata_Def

    def onsemi_conver_byte(self, byte, bits_len):
        conver_data = [self.__Tdata_Def['Onsemi_Tbit1_Def'] if (byte >> idx) & 0x01
                       else self.__Tdata_Def['Onsemi_Tbit0_Def']
                       for idx in range(bits_len)]
        return conver_data

    @staticmethod
    def onsemi_calc_checksum(rw_bit, addr, data):
        checksum = ((rw_bit & 0x01) << 7) + ((addr & 0x0f) << 3)
        for byte in data:
            checksum += byte
            if checksum > 0xff:
                checksum -= 0xff
        checksum ^= 0xff
        return checksum

    def encode_carrier_period(self, period):
        write_bit = 0
        reg_addr = 2
        encode_data = [self.__Tdata_Def['Onsemi_CmdPluse_Def'], self.__Tdata_Def['Onsemi_CmdSep_Def']]
        conver_byte = [period & 0x00ff, (period >> 8) & 0x0007]
        checksum = self.onsemi_calc_checksum(write_bit, reg_addr, conver_byte)
        encode_data.extend(self.onsemi_conver_byte(write_bit, 1))
        encode_data.extend(self.onsemi_conver_byte(reg_addr, 4))
        encode_data.extend(self.onsemi_conver_byte(period, 11))
        encode_data.extend(self.onsemi_conver_byte(checksum, 8))
        return encode_data

    def encode_detal_period(self, dt_tx_per, dt_rx_per):
        write_bit = 0
        reg_addr = 2
        encode_data = [self.__Tdata_Def['Onsemi_CmdPluse_Def'], self.__Tdata_Def['Onsemi_CmdSep_Def']]
        conver_byte = [dt_tx_per, dt_rx_per]
        checksum = self.onsemi_calc_checksum(write_bit, reg_addr, conver_byte)
        encode_data.extend(self.onsemi_conver_byte(write_bit, 1))
        encode_data.extend(self.onsemi_conver_byte(reg_addr, 4))
        encode_data.extend(self.onsemi_conver_byte(dt_tx_per, 8))
        encode_data.extend(self.onsemi_conver_byte(dt_rx_per, 8))
        encode_data.extend(self.onsemi_conver_byte(checksum, 8))
        return encode_data

    def encode_txburst_pulsecnt(self, tx_burst):
        write_bit = 0
        reg_addr = 3
        encode_data = [self.__Tdata_Def['Onsemi_CmdPluse_Def'], self.__Tdata_Def['Onsemi_CmdSep_Def']]
        conver_byte = [tx_burst]
        checksum = self.onsemi_calc_checksum(write_bit, reg_addr, conver_byte)
        encode_data.extend(self.onsemi_conver_byte(write_bit, 1))
        encode_data.extend(self.onsemi_conver_byte(reg_addr, 4))
        encode_data.extend(self.onsemi_conver_byte(tx_burst, 5))
        encode_data.extend(self.onsemi_conver_byte(checksum, 8))
        return encode_data

    def encode_meas_duration(self, mesa_dura):
        write_bit = 0
        reg_addr = 4
        encode_data = [self.__Tdata_Def['Onsemi_CmdPluse_Def'], self.__Tdata_Def['Onsemi_CmdSep_Def']]
        conver_byte = [mesa_dura]
        checksum = self.onsemi_calc_checksum(write_bit, reg_addr, conver_byte)
        encode_data.extend(self.onsemi_conver_byte(write_bit, 1))
        encode_data.extend(self.onsemi_conver_byte(reg_addr, 4))
        encode_data.extend(self.onsemi_conver_byte(mesa_dura, 4))
        encode_data.extend(self.onsemi_conver_byte(checksum, 8))
        return encode_data

    def encode_thr(self, thr_num, lvl, dt):
        write_bit = 0
        if thr_num == 1:
            reg_addr = 5
        else:
            reg_addr = 6
        encode_data = [self.__Tdata_Def['Onsemi_CmdPluse_Def'], self.__Tdata_Def['Onsemi_CmdSep_Def']]
        if len(lvl) == 12 and len(dt) == 12:
            lvl_bytes = [(lvl[idx_1 * 4 + idx_2] & 0x3f) + (((lvl[idx_1 * 4 + 3] >> idx_2 * 2) & 0x03) << 6)
                         for idx_1 in range(3)
                         for idx_2 in range(3)]
            dt_bytes = [(dt[idx * 2] & 0x0f) + ((dt[idx * 2 + 1] & 0x0f) << 4)
                        for idx in range(6)]
            conver_byte = []
            conver_byte.extend(lvl_bytes)
            conver_byte.extend(dt_bytes)
            checksum = self.onsemi_calc_checksum(write_bit, reg_addr, conver_byte)
            conver_byte.append(checksum)
            encode_data.extend(self.onsemi_conver_byte(write_bit, 1))
            encode_data.extend(self.onsemi_conver_byte(reg_addr, 4))
            for byte in conver_byte:
                encode_data.extend((self.onsemi_conver_byte(byte, 8)))
        return encode_data
