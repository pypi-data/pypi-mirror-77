# -*- coding: utf-8 -*-

# File generated according to WHoleMag.ui
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WHoleMag(object):
    def setupUi(self, WHoleMag):
        WHoleMag.setObjectName("WHoleMag")
        WHoleMag.resize(760, 490)
        WHoleMag.setMinimumSize(QtCore.QSize(760, 490))
        self.main_layout = QtWidgets.QVBoxLayout(WHoleMag)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(4)
        self.main_layout.setObjectName("main_layout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.c_hole_type = QtWidgets.QComboBox(WHoleMag)
        self.c_hole_type.setObjectName("c_hole_type")
        self.c_hole_type.addItem("")
        self.c_hole_type.addItem("")
        self.c_hole_type.addItem("")
        self.c_hole_type.addItem("")
        self.c_hole_type.addItem("")
        self.c_hole_type.addItem("")
        self.c_hole_type.addItem("")
        self.horizontalLayout.addWidget(self.c_hole_type)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.main_layout.addLayout(self.horizontalLayout)
        self.w_hole = QtWidgets.QWidget(WHoleMag)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_hole.sizePolicy().hasHeightForWidth())
        self.w_hole.setSizePolicy(sizePolicy)
        self.w_hole.setMinimumSize(QtCore.QSize(750, 450))
        self.w_hole.setObjectName("w_hole")
        self.main_layout.addWidget(self.w_hole)

        self.retranslateUi(WHoleMag)
        QtCore.QMetaObject.connectSlotsByName(WHoleMag)

    def retranslateUi(self, WHoleMag):
        _translate = QtCore.QCoreApplication.translate
        WHoleMag.setWindowTitle(_translate("WHoleMag", "Form"))
        self.c_hole_type.setItemText(0, _translate("WHoleMag", "Slot Type 50"))
        self.c_hole_type.setItemText(1, _translate("WHoleMag", "Slot Type 51"))
        self.c_hole_type.setItemText(2, _translate("WHoleMag", "Slot Type 52"))
        self.c_hole_type.setItemText(3, _translate("WHoleMag", "Slot Type 53"))
        self.c_hole_type.setItemText(4, _translate("WHoleMag", "Slot Type 54"))
        self.c_hole_type.setItemText(5, _translate("WHoleMag", "Slot Type 55"))
        self.c_hole_type.setItemText(6, _translate("WHoleMag", "Slot Type 56"))
