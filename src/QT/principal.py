from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.WindowModal)
        Form.resize(1085, 695)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(1085, 695))
        Form.setSizeIncrement(QtCore.QSize(1, 1))
        Form.setBaseSize(QtCore.QSize(1085, 695))
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(860, 40, 211, 651))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.expedienteG = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.expedienteG.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.expedienteG.setContentsMargins(0, 0, 0, 0)
        self.expedienteG.setObjectName("expedienteG")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 40, 2, 2))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.expedienteI = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.expedienteI.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.expedienteI.setContentsMargins(0, 0, 0, 0)
        self.expedienteI.setObjectName("expedienteI")

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

