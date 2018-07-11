# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'principal_imagenes.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1109, 606)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 460, 2, 2))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.scanL = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.scanL.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.scanL.setContentsMargins(0, 0, 0, 0)
        self.scanL.setObjectName("scanL")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 9, 2, 2))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.canvasL = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.canvasL.setContentsMargins(0, 0, 0, 0)
        self.canvasL.setObjectName("canvasL")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

