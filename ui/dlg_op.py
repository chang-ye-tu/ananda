# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/ananda/designer/dlg_op.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlg_op(object):
    def setupUi(self, dlg_op):
        dlg_op.setObjectName("dlg_op")
        dlg_op.resize(407, 292)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(12)
        dlg_op.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/img/tex.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlg_op.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(dlg_op)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(dlg_op)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chk_tkd = QtWidgets.QCheckBox(self.groupBox)
        self.chk_tkd.setObjectName("chk_tkd")
        self.horizontalLayout.addWidget(self.chk_tkd)
        self.led_tkd = QtWidgets.QLineEdit(self.groupBox)
        self.led_tkd.setObjectName("led_tkd")
        self.horizontalLayout.addWidget(self.led_tkd)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.chk_bxd = QtWidgets.QCheckBox(self.groupBox)
        self.chk_bxd.setObjectName("chk_bxd")
        self.horizontalLayout_3.addWidget(self.chk_bxd)
        self.led_bxd = QtWidgets.QLineEdit(self.groupBox)
        self.led_bxd.setObjectName("led_bxd")
        self.horizontalLayout_3.addWidget(self.led_bxd)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.led_bxd_morph = QtWidgets.QLineEdit(self.groupBox)
        self.led_bxd_morph.setObjectName("led_bxd_morph")
        self.horizontalLayout_3.addWidget(self.led_bxd_morph)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chk_yd = QtWidgets.QCheckBox(self.groupBox)
        self.chk_yd.setObjectName("chk_yd")
        self.horizontalLayout_2.addWidget(self.chk_yd)
        self.led_yd = QtWidgets.QLineEdit(self.groupBox)
        self.led_yd.setObjectName("led_yd")
        self.horizontalLayout_2.addWidget(self.led_yd)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.chk_sep = QtWidgets.QCheckBox(self.groupBox)
        self.chk_sep.setObjectName("chk_sep")
        self.horizontalLayout_4.addWidget(self.chk_sep)
        self.led_sep = QtWidgets.QLineEdit(self.groupBox)
        self.led_sep.setObjectName("led_sep")
        self.horizontalLayout_4.addWidget(self.led_sep)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.chk_man = QtWidgets.QCheckBox(dlg_op)
        self.chk_man.setObjectName("chk_man")
        self.horizontalLayout_5.addWidget(self.chk_man)
        self.led_man = QtWidgets.QLineEdit(dlg_op)
        self.led_man.setObjectName("led_man")
        self.horizontalLayout_5.addWidget(self.led_man)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.bbx = QtWidgets.QDialogButtonBox(dlg_op)
        self.bbx.setOrientation(QtCore.Qt.Horizontal)
        self.bbx.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bbx.setObjectName("bbx")
        self.verticalLayout_2.addWidget(self.bbx)

        self.retranslateUi(dlg_op)
        self.bbx.accepted.connect(dlg_op.accept)
        self.bbx.rejected.connect(dlg_op.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_op)

    def retranslateUi(self, dlg_op):
        _translate = QtCore.QCoreApplication.translate
        dlg_op.setWindowTitle(_translate("dlg_op", "Operations"))
        self.groupBox.setTitle(_translate("dlg_op", "Processing"))
        self.chk_tkd.setText(_translate("dlg_op", "tkd"))
        self.chk_bxd.setText(_translate("dlg_op", "bxd"))
        self.label.setText(_translate("dlg_op", "morph"))
        self.chk_yd.setText(_translate("dlg_op", "yd"))
        self.chk_sep.setText(_translate("dlg_op", "sep"))
        self.chk_man.setText(_translate("dlg_op", "clean manual data"))
from . import ananda_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg_op = QtWidgets.QDialog()
    ui = Ui_dlg_op()
    ui.setupUi(dlg_op)
    dlg_op.show()
    sys.exit(app.exec_())
