# -*- coding: utf-8 -*-
from ui.mainWindow import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from onsemiParaEncode import OnsemiParaEncode


class UsenMainWindow(QMainWindow, Ui_MainWindow, OnsemiParaEncode):
    def __init__(self):
        super(UsenMainWindow, self).__init__()
        OnsemiParaEncode.__init__(self)
        self.setupUi(self)
        self.comp_onsemiThr1_Lvlx = (
            self.OnsemiThrTab1_Lvl0, self.OnsemiThrTab1_Lvl1, self.OnsemiThrTab1_Lvl2, self.OnsemiThrTab1_Lvl3,
            self.OnsemiThrTab1_Lvl4, self.OnsemiThrTab1_Lvl5, self.OnsemiThrTab1_Lvl6, self.OnsemiThrTab1_Lvl7,
            self.OnsemiThrTab1_Lvl8, self.OnsemiThrTab1_Lvl9, self.OnsemiThrTab1_Lvl10, self.OnsemiThrTab1_Lvl11)
        self.comp_onsemiThr1_Dtx = (
            self.OnsemiThrTab1_DT0, self.OnsemiThrTab1_DT1, self.OnsemiThrTab1_DT2, self.OnsemiThrTab1_DT3,
            self.OnsemiThrTab1_DT4, self.OnsemiThrTab1_DT5, self.OnsemiThrTab1_DT6, self.OnsemiThrTab1_DT7,
            self.OnsemiThrTab1_DT8, self.OnsemiThrTab1_DT9, self.OnsemiThrTab1_DT10, self.OnsemiThrTab1_DT11)
        self.comp_onsemiThr2_Lvlx = (
            self.OnsemiThrTab2_Lvl0, self.OnsemiThrTab2_Lvl1, self.OnsemiThrTab2_Lvl2, self.OnsemiThrTab2_Lvl3,
            self.OnsemiThrTab2_Lvl4, self.OnsemiThrTab2_Lvl5, self.OnsemiThrTab2_Lvl6, self.OnsemiThrTab2_Lvl7,
            self.OnsemiThrTab2_Lvl8, self.OnsemiThrTab2_Lvl9, self.OnsemiThrTab2_Lvl10, self.OnsemiThrTab2_Lvl11)
        self.comp_onsemiThr2_Dtx = (
            self.OnsemiThrTab2_DT0, self.OnsemiThrTab2_DT1, self.OnsemiThrTab2_DT2, self.OnsemiThrTab2_DT3,
            self.OnsemiThrTab2_DT4, self.OnsemiThrTab2_DT5, self.OnsemiThrTab2_DT6, self.OnsemiThrTab2_DT7,
            self.OnsemiThrTab2_DT8, self.OnsemiThrTab2_DT9, self.OnsemiThrTab2_DT10, self.OnsemiThrTab2_DT11)

        self.onsemiSetDefine_Button.clicked.connect(self.setting_onsemi_defined)
        self.OnsemiCarrierPer_GenerateButton.clicked.connect(self.generate_onsemi_carrier_period)
        self.OnsemiDeltaPer_GenerateButton.clicked.connect(self.generate_onsemi_delta_period)
        self.OnsemiTxBurstPulse_GenerateButton.clicked.connect(self.generate_onsemi_txBurstPulse)
        self.OnsemiMeasDura_GenerateButton.clicked.connect(self.generate_onsemi_meas_duration)
        self.OnsemiThr1_GenerateButton.clicked.connect(lambda: self.generate_onsemi_thres(1))
        self.OnsemiThr2_GenerateButton.clicked.connect(lambda: self.generate_onsemi_thres(2))

    def setting_onsemi_defined(self):
        defined = self.onsemi_get_settingdef()
        defined['Onsemi_CmdPluse_Def'] = self.onsemiTCmdPulse_Def.text()
        defined['Onsemi_CmdSep_Def'] = self.onsemiTCmdSepPulse_Def.text()
        defined['Onsemi_Tbit0_Def'] = self.onsemiTbit0_Def.text()
        defined['Onsemi_Tbit1_Def'] = self.onsemiTbit1_Def.text()
        self.onsemi_set_settingdef(defined)

    def generate_onsemi_carrier_period(self):
        period = self.OnsemiCarrierPer.value()
        period_encode = self.encode_carrier_period(period)
        self.OnsemiCarrierPer_CodeText.setText(', '.join(period_encode))

    def generate_onsemi_delta_period(self):
        dt_tx_per = self.OnsemiDtx_Per.value()
        dt_rx_per = self.OnsemiDrx_Per.value()
        dt_per_encode = self.encode_detal_period(dt_tx_per, dt_rx_per)
        self.OnsemiDtCarrierPer_CodeText.setText(', '.join(dt_per_encode))

    def generate_onsemi_txBurstPulse(self):
        txBurst_PulseCnt = self.OnsemiTxBurstPulseCnt.value()
        txBurst_encode = self.encode_txburst_pulsecnt(txBurst_PulseCnt)
        self.OnsemiTxBurstPulse_CodeText.setText(', '.join(txBurst_encode))

    def generate_onsemi_meas_duration(self):
        meas_dura = self.OnsemiMeasDura.value()
        meas_dura_encode = self.encode_meas_duration(meas_dura)
        self.OnsemiMeasDura_CodeText.setText(', '.join(meas_dura_encode))

    def generate_onsemi_thres(self, thr_num):
        # thr_lvl = [lvl.value() for lvl in self.comp_onsemiThr1_Lvlx]
        thr_lvl = [self.comp_onsemiThr1_Lvlx[idx].value() if thr_num == 1
                   else self.comp_onsemiThr2_Lvlx[idx].value()
                   for idx in range(12)]
        # thr_dt = [dt.value() for dt in self.comp_onsemiThr1_Dtx]
        thr_dt = [self.comp_onsemiThr1_Dtx[idx].value() if thr_num == 1
                  else self.comp_onsemiThr2_Dtx[idx].value()
                  for idx in range(12)]
        thr_encode = self.encode_thr(thr_num, thr_lvl, thr_dt)
        # self.textBrowser.setText(str(thr_encode).replace('[', '{').replace(']', '}'))
        if thr_num == 1:
            self.OnsemiThrTab1_CodeText.setText(', '.join(thr_encode))
        else:
            self.OnsemiThrTab2_CodeText.setText(', '.join(thr_encode))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWin = UsenMainWindow()
    mainWin.show()
    sys.exit(app.exec_())
