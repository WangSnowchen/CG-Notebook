from PySide2 import QtCore, QtGui, QtWidgets
import maya.OpenMayaUI as mui
import shiboken2
import pymel.core as pm



def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__(parent=getMayaWindow())
        self.setWindowFlags(QtCore.Qt.Window)
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(214, 120)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 44, 71, 31))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(90, 50, 101, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(120, 80, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 30, 221, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 191, 21))
        self.label_2.setObjectName("label_2")
        self.button_connetion()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "RGBA_lgt_", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "RGBA_lgt_", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Form", "confirm", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form",
                                                              "<html><head/><body><p><span style=\" font-weight:1000;\">Select lights and confirm</span></p></body></html>",
                                                              None, -1))

    def button_connetion(self):
        self.pushButton.clicked.connect(self.LightGroup)

    def LightGroup(self):
        lt_group = 'RGBA_lgt_' + self.lineEdit.text()
        sl = pm.ls(sl=True)
        for i in sl:
            light = i.getShape()
            try:
                pm.setAttr('%s.aiAov' % light, lt_group)
                # self.lineEdit.clear()
            except:
                pass
		

		
if __name__ == '__main__':
    try:
        my.close()

    except:
        pass
    my = Ui_Form()
    my.show()