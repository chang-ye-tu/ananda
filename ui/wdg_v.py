# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cytu/usr/src/py/ananda/designer/wdg_v.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdg_v(object):
    def setupUi(self, wdg_v):
        wdg_v.setObjectName("wdg_v")
        wdg_v.resize(582, 558)
        self.gridLayout = QtWidgets.QGridLayout(wdg_v)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.hlo = QtWidgets.QHBoxLayout()
        self.hlo.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.hlo.setSpacing(0)
        self.hlo.setObjectName("hlo")
        self.vw = QVideoWidget(wdg_v)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vw.sizePolicy().hasHeightForWidth())
        self.vw.setSizePolicy(sizePolicy)
        self.vw.setObjectName("vw")
        self.hlo.addWidget(self.vw)
        self.verticalLayout.addLayout(self.hlo)
        self.vlo = QtWidgets.QVBoxLayout()
        self.vlo.setSpacing(0)
        self.vlo.setObjectName("vlo")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_play = QtWidgets.QPushButton(wdg_v)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_play.sizePolicy().hasHeightForWidth())
        self.btn_play.setSizePolicy(sizePolicy)
        self.btn_play.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_play.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_play.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/img/media_playback_start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_play.setIcon(icon)
        self.btn_play.setIconSize(QtCore.QSize(24, 24))
        self.btn_play.setAutoDefault(False)
        self.btn_play.setDefault(False)
        self.btn_play.setFlat(True)
        self.btn_play.setObjectName("btn_play")
        self.horizontalLayout.addWidget(self.btn_play)
        self.btn_stop = QtWidgets.QPushButton(wdg_v)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_stop.sizePolicy().hasHeightForWidth())
        self.btn_stop.setSizePolicy(sizePolicy)
        self.btn_stop.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_stop.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_stop.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/res/img/media_playback_stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_stop.setIcon(icon1)
        self.btn_stop.setIconSize(QtCore.QSize(24, 24))
        self.btn_stop.setFlat(True)
        self.btn_stop.setObjectName("btn_stop")
        self.horizontalLayout.addWidget(self.btn_stop)
        self.btn_rec = QtWidgets.QPushButton(wdg_v)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_rec.sizePolicy().hasHeightForWidth())
        self.btn_rec.setSizePolicy(sizePolicy)
        self.btn_rec.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_rec.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_rec.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/res/img/media_record.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_rec.setIcon(icon2)
        self.btn_rec.setIconSize(QtCore.QSize(24, 24))
        self.btn_rec.setCheckable(True)
        self.btn_rec.setFlat(True)
        self.btn_rec.setObjectName("btn_rec")
        self.horizontalLayout.addWidget(self.btn_rec)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lbl_s = QtWidgets.QLabel(wdg_v)
        self.lbl_s.setText("")
        self.lbl_s.setObjectName("lbl_s")
        self.horizontalLayout.addWidget(self.lbl_s)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.lbl_t = QtWidgets.QLabel(wdg_v)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_t.sizePolicy().hasHeightForWidth())
        self.lbl_t.setSizePolicy(sizePolicy)
        self.lbl_t.setObjectName("lbl_t")
        self.horizontalLayout.addWidget(self.lbl_t)
        self.vlo.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.sld = QtWidgets.QSlider(wdg_v)
        self.sld.setOrientation(QtCore.Qt.Horizontal)
        self.sld.setObjectName("sld")
        self.horizontalLayout_2.addWidget(self.sld)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.btn_file = QtWidgets.QPushButton(wdg_v)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/res/img/document_save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_file.setIcon(icon3)
        self.btn_file.setObjectName("btn_file")
        self.horizontalLayout_2.addWidget(self.btn_file)
        self.vlo.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.vlo)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(wdg_v)
        QtCore.QMetaObject.connectSlotsByName(wdg_v)

    def retranslateUi(self, wdg_v):
        _translate = QtCore.QCoreApplication.translate
        wdg_v.setWindowTitle(_translate("wdg_v", "Form"))
        self.lbl_t.setText(_translate("wdg_v", "59:59:59"))
        self.btn_file.setText(_translate("wdg_v", "load"))
from PyQt5.QtMultimediaWidgets import QVideoWidget
from . import ananda_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wdg_v = QtWidgets.QWidget()
    ui = Ui_wdg_v()
    ui.setupUi(wdg_v)
    wdg_v.show()
    sys.exit(app.exec_())
