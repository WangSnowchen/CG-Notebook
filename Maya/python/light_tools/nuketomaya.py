# -*- coding: utf-8 -*-

import re
from PySide2 import QtCore, QtGui, QtWidgets
import maya.OpenMayaUI as mui
import shiboken2
import pymel.core as pm

def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__(parent=getMayaWindow())
        self.setWindowFlags(QtCore.Qt.Window)
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(216, 227)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(130, 190, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 90, 221, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 191, 81))
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 110, 191, 71))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setPlainText('gain-Intensity\nmultiply-Color')

        self.button_connetion()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Nuke to Maya", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Form", "modify", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form",
                                                              "<html><head/><body><p><span style=\" font-size:10pt;\">1.复制Nuke\\Grade节点</span></p><p><span style=\" font-size:10pt;\">2.粘贴到输入框</span></p><p><span style=\" font-size:10pt;\">3.选择灯光后modify</span></p></body></html>",
                                                              None, -1))

    def button_connetion(self):
        self.pushButton.clicked.connect(self.modifylight)

    def modifylight(self):
        intensity_all = None
        multiply_all = None
        intensity = 1
        multiply = [1, 1, 1, 1]

        a = self.textEdit.toPlainText()
        c = a.split('\n')
        for i in c:
            if 'white' in i:
                intensity_all = i
            elif 'multiply {' in i:
                multiply_all = i

        if intensity_all:
            intensity = re.findall('(\d+(\.\d+)?)', intensity_all)[0][0]
        if multiply_all:
            multiply = re.findall('\{(.*)\}', multiply_all)[0].split()

        light_list = pm.ls(selection=True)
        for i in light_list:
            light = i.getShape()
            ori_intensity = float(pm.getAttr('%s.intensity' % light))
            modify_intensity = ori_intensity * float(intensity)
            ori_color = [1, 1, 1]
            ori_color[0] = pm.getAttr('%s.colorR' % light)
            ori_color[1] = pm.getAttr('%s.colorG' % light)
            ori_color[2] = pm.getAttr('%s.colorB' % light)

            a = [1.0, 1.0, 1.0]
            for i in range(3):
                a[i] = float(multiply[i]) * ori_color[i]

            try:
                pm.setAttr('%s.intensity' % light, modify_intensity)
                pm.setAttr('%s.colorR' % light, a[0])
                pm.setAttr('%s.colorG' % light, a[1])
                pm.setAttr('%s.colorB' % light, a[2])
            except:
                pass


if __name__ == '__main__':
    try:
        my.close()

    except:
        pass
    my = Ui_Form()
    my.show()
