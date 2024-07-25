# -*- coding: utf-8 -*-
import sys

plat = sys.platform

if plat == 'win32':
	tl_path = '//storage1.of3d.com/tankprojects/ofLibrary/lgtLib/tools&plugins/hq_yongzhicheng_movie/light_tools/light_tools_WIZ'
else:
	tl_path =  '/mnt/ofLibrary/lgtLib/tools&plugins/hq_yongzhicheng_movie/light_tools/light_tools_WIZ'

if tl_path not in sys.path:
    sys.path.append(tl_path)

from PySide2 import QtCore, QtGui, QtWidgets
import maya.OpenMayaUI as mui
import shiboken2
import pymel.core as pm
import mtoa.aovs as aov
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

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(399, 191)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 20, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 60, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 100, 91, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        #self.pushButton_4 = QtWidgets.QPushButton(Form)
        #self.pushButton_4.setGeometry(QtCore.QRect(30, 140, 91, 31))
        #self.pushButton_4.setObjectName("pushButton_4")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(140, 20, 241, 151))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        self.button_connetion()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Form", "Add Lights", None, -1))
        self.pushButton_2.setText("Opt current aov")
        self.pushButton_3.setText(QtWidgets.QApplication.translate("Form", "Opt all aov", None, -1))
        #self.pushButton_4.setText(QtWidgets.QApplication.translate("Form", "Create Pref", None, -1))
        self.textBrowser.setText('''Add Lights:  将所选灯光加入可见层\n
Opt current aov: 优化当前层的灯光AOV，去除当前层无用的灯光AOV\n
Opt all aov: Optimize all aov''')

    def button_connetion(self):
        self.pushButton.clicked.connect(self.addLight)
        self.pushButton_2.clicked.connect(self.optimise_current_aov)
        self.pushButton_3.clicked.connect(self.optimise_all_aov)


    def addLight(self):
        cmds.optionVar(q="renderSetupEnable")
        import maya.app.renderSetup.model.renderSetup as renderSetupModel

        renderSetup = renderSetupModel.instance()
        visi_renderlayer = renderSetup.getVisibleRenderLayer()
        lights = visi_renderlayer.lightsCollectionInstance()
        lights.setSelfEnabled(0)

        a = visi_renderlayer.getChildren()

        lightCollection = []
        for i in a:
            if 'visilight' in i.name():
                lightCollection = i
                break

        if lightCollection == []:
            lightCollection = visi_renderlayer.createCollection('visilights')

        sl_light = newom.MGlobal.getActiveSelectionList()
        for i in sl_light.getSelectionStrings():
            try:
                if pm.PyNode(i).getShape().type() not in via.light_type_list:
                    pm.error('Must be Light')
            except:
                pm.error('Must be Light')

        if 'visilights' in lightCollection.name():
            lightCollection.getSelector().staticSelection.add(sl_light)

    def optimiseAov(self,Layer):

        LightList_Col = None
        for i in Layer.getChildren():
            if 'visilights' in i.name():
                LightList_Col = i.getSelector().staticSelection.asList()

        for i in LightList_Col:
            if pm.PyNode(i).type() == 'transform':
                if pm.PyNode(i).getShape() == None:
                    pm.error('Must be all light')
                elif pm.PyNode(i).getShape().type() not in via.light_type_list:
                    pm.error('Must be all light')
            elif pm.PyNode(i).type() != 'transform':
                pm.error('Must be all light')

        if LightList_Col != None:
            LightAov = []
            for ii in aov.getAOVs():
                if 'RGBA_lgt_' in ii.name:
                    LightAov.append(ii.name)
                else:
                    continue

        LightPath = []

        for iii in LightList_Col:
            light = pm.PyNode(iii).getShape()
            aiAov = pm.getAttr('%s.aiAov' % light)
            if (aiAov not in LightPath) and (aiAov != 'default'):
                LightPath.append(aiAov)

        if Layer.hasAOVCollectionInstance():
            s = Layer.aovCollectionInstance()
            collection.delete(s)

        for i in LightAov:
            if i in LightPath:
                Layer.createAbsoluteOverride('aiAOV_%s' % i, 'enabled').setAttrValue(1)
            elif i not in LightPath:
                Layer.createAbsoluteOverride('aiAOV_%s' % i, 'enabled').setAttrValue(0)


    def optimise_all_aov(self):
        Rs = RenderSetup.instance()
        for Layer in Rs.getRenderLayers():
            self.optimiseAov(Layer)

    def optimise_current_aov(self):
        Rs = RenderSetup.instance()
        Layer = Rs.getVisibleRenderLayer()
        self.optimiseAov(Layer)


    def checkLight(self):
        import pymel.core as pm
        lightLists = []
        for i in light_type_list:
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
