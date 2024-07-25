# -*- coding: utf-8 -*-
import sys

plat = sys.platform

if plat == 'win32':
    tl_path = '//storage1.of3d.com/tankprojects/ofLibrary/lgtLib/tools&plugins/hq_yongzhicheng_movie/light_tools/light_tools_WIZ'
else:
    tl_path = '/mnt/ofLibrary/lgtLib/tools&plugins/hq_yongzhicheng_movie/light_tools/light_tools_WIZ'

if tl_path not in sys.path:
    sys.path.append(tl_path)

from PySide2 import QtCore, QtGui, QtWidgets
import maya.OpenMayaUI as mui
import shiboken2
import pymel.core as pm
import mtoa.aovs as aovs
import maya.cmds as cmds
import maya.app.renderSetup.model.renderSetup as RenderSetup
import maya.app.renderSetup.model.collection as collection
import maya.api.OpenMaya as newom
import via


def getMayaWindow():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__(parent=getMayaWindow())
        self.setWindowFlags(QtCore.Qt.Window)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(247, 297)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(10, 30, 141, 241))
        self.listWidget.setObjectName("listWidget")
        QtWidgets.QListWidgetItem(self.listWidget)
        QtWidgets.QListWidgetItem(self.listWidget)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 30, 75, 26))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 60, 75, 26))
        self.pushButton_2.setObjectName("pushButton_3")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 90, 75, 26))
        self.pushButton_3.setObjectName("pushButton_3")

        self.init_items()
        self.button_connetion()
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Select Light by aov", None, -1))
        __sortingEnabled = self.listWidget.isSortingEnabled()

        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(QtWidgets.QApplication.translate("Dialog", "Refresh", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("Dialog", "Select Light", None, -1))
        self.pushButton_3.setText(QtWidgets.QApplication.translate("Dialog", "No aov Light", None, -1))

    def button_connetion(self):
        self.pushButton.clicked.connect(self.init_items)
        self.pushButton_2.clicked.connect(self.select_light)
        self.pushButton_3.clicked.connect(self.checkLight)

    def select_light(self):
        pm.select(cl=1)
        a = self.listWidget
        text_list = a.selectedItems()
        if len(text_list) == 1:
            light_list = []
            for i in via.light_type_list:
                lights = pm.ls(type=i)
                if lights != []:
                    for ii in lights:
                        light_list.append(ii)

            bingo_light = []
            for i in light_list:
                aovpath = pm.PyNode(i).getAttr('aiAov')
                if aovpath == text_list[0].text():
                    bingo_light.append(i.getTransform())

            pm.select(bingo_light)

    def aov_edit(self):
        print('b')


    def init_items(self):
        a = self.listWidget
        a.clear()
        aovlist = [i.name for i in aovs.getAOVs()]
        if aovlist is not None and len(aovlist):
            a.addItems(aovlist)

    def checkLight(self):
        pm.select(cl=1)
        lightLists = []
        for i in via.light_type_list:
            lsLight = pm.ls(type=i, dag=1)
            if lsLight != []:
                for x in lsLight:
                    lightLists.append(x)
        selectlist = []
        for i in lightLists:
            lightGroup = pm.getAttr('%s.aiAov' % i)
            if lightGroup == 'default' or lightGroup == '':
                selectlist.append(i)

        for i in selectlist:
            pm.select(pm.listTransforms(i)[0], add=1)








if __name__ == '__main__':
    try:
        my.close()

    except:
        pass
    my = Ui_Form()
    my.show()