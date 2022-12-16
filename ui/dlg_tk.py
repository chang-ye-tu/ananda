# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/ananda/designer/dlg_tk.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlg_tk(object):
    def setupUi(self, dlg_tk):
        dlg_tk.setObjectName("dlg_tk")
        dlg_tk.resize(400, 215)
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei")
        font.setPointSize(12)
        dlg_tk.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/img/tex.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlg_tk.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(dlg_tk)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(dlg_tk)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.cbo_tk = QtWidgets.QComboBox(dlg_tk)
        self.cbo_tk.setObjectName("cbo_tk")
        self.horizontalLayout_3.addWidget(self.cbo_tk)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.lbl_ocr = QtWidgets.QLabel(dlg_tk)
        self.lbl_ocr.setText("")
        self.lbl_ocr.setObjectName("lbl_ocr")
        self.verticalLayout.addWidget(self.lbl_ocr)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(dlg_tk)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.led_tk = QtWidgets.QLineEdit(dlg_tk)
        self.led_tk.setObjectName("led_tk")
        self.horizontalLayout_2.addWidget(self.led_tk)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(dlg_tk)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.led_key = QtWidgets.QLineEdit(dlg_tk)
        self.led_key.setObjectName("led_key")
        self.horizontalLayout.addWidget(self.led_key)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.btb = QtWidgets.QDialogButtonBox(dlg_tk)
        self.btb.setOrientation(QtCore.Qt.Horizontal)
        self.btb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btb.setObjectName("btb")
        self.gridLayout.addWidget(self.btb, 1, 0, 1, 1)

        self.retranslateUi(dlg_tk)
        self.btb.accepted.connect(dlg_tk.accept)
        self.btb.rejected.connect(dlg_tk.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_tk)
        dlg_tk.setTabOrder(self.led_tk, self.cbo_tk)
        dlg_tk.setTabOrder(self.cbo_tk, self.btb)
        dlg_tk.setTabOrder(self.btb, self.led_key)

    def retranslateUi(self, dlg_tk):
        _translate = QtCore.QCoreApplication.translate
        dlg_tk.setWindowTitle(_translate("dlg_tk", "Edit Token"))
        self.label_3.setText(_translate("dlg_tk", "item type"))
        self.label_2.setText(_translate("dlg_tk", "ocr\'d text"))
        self.label.setText(_translate("dlg_tk", "extra key"))
from . import ananda_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg_tk = QtWidgets.QDialog()
    ui = Ui_dlg_tk()
    ui.setupUi(dlg_tk)
    dlg_tk.show()
    sys.exit(app.exec_())
