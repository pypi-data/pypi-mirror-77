# -*- coding: utf-8 -*-

# File generated according to PCondType22.ui
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PCondType22(object):
    def setupUi(self, PCondType22):
        PCondType22.setObjectName("PCondType22")
        PCondType22.resize(460, 124)
        self.horizontalLayout = QtWidgets.QHBoxLayout(PCondType22)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.w_mat = WMatSelect(PCondType22)
        self.w_mat.setObjectName("w_mat")
        self.horizontalLayout.addWidget(self.w_mat)
        self.w_out = WBarOut(PCondType22)
        self.w_out.setObjectName("w_out")
        self.horizontalLayout.addWidget(self.w_out)

        self.retranslateUi(PCondType22)
        QtCore.QMetaObject.connectSlotsByName(PCondType22)

    def retranslateUi(self, PCondType22):
        _translate = QtCore.QCoreApplication.translate
        PCondType22.setWindowTitle(_translate("PCondType22", "Form"))


from ......GUI.Dialog.DMachineSetup.SBar.WBarOut.WBarOut import WBarOut
from ......GUI.Dialog.DMatLib.WMatSelect.WMatSelect import WMatSelect
