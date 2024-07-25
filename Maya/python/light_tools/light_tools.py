# -*- coding: utf-8 -*-
# Author:WangZhiChao   2018.8.24
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
import re
import lightgroup as lg
import nuketomaya as ntm
import getdir
import lightinvert
import Light_RenderSetup
from via import light_type_list, aov_list


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

        Form.resize(156, 700)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 40, 111, 21))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 70, 111, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 100, 111, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(100, 195, 71, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(55, 195, 54, 12))
        self.label.setObjectName("label")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(-20, 195, 71, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(64, 10, 54, 12))
        self.label_2.setObjectName("label_2")
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setGeometry(QtCore.QRect(90, 10, 81, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setGeometry(QtCore.QRect(-20, 10, 81, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 225, 111, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 255, 111, 21))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(20, 285, 111, 21))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(20, 315, 111, 21))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(20, 130, 111, 21))
        self.pushButton_8.setObjectName("pushButton_8")
        # ________________count__________________________________
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 147, 100, 50))
        self.label_3.setObjectName("label_3")
        # _______________Cryptomatte____________________________
        self.line_5 = QtWidgets.QFrame(Form)
        self.line_5.setGeometry(QtCore.QRect(0, 350, 160, 20))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setGeometry(QtCore.QRect(20, 375, 70, 21))
        self.pushButton_9.setObjectName("pushButton_9")

        self.pushButton_15 = QtWidgets.QPushButton(Form)
        self.pushButton_15.setGeometry(QtCore.QRect(100, 375, 30, 21))
        self.pushButton_15.setObjectName("pushButton_15")

        # _____lightgroup_______________________________________
        self.line_7 = QtWidgets.QFrame(Form)
        self.line_7.setGeometry(QtCore.QRect(0, 406, 160, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setGeometry(QtCore.QRect(20, 435, 111, 21))
        self.pushButton_10.setObjectName("pushButton_10")
        # _____nuketomaya________________________________________
        self.line_9 = QtWidgets.QFrame(Form)
        self.line_9.setGeometry(QtCore.QRect(0, 466, 160, 20))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.pushButton_11 = QtWidgets.QPushButton(Form)
        self.pushButton_11.setGeometry(QtCore.QRect(20, 495, 111, 21))
        self.pushButton_11.setObjectName("pushButton_11")
        # _____renderimage________________________________________
        self.line_11 = QtWidgets.QFrame(Form)
        self.line_11.setGeometry(QtCore.QRect(0, 526, 160, 20))
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_8")

        self.pushButton_12 = QtWidgets.QPushButton(Form)
        self.pushButton_12.setGeometry(QtCore.QRect(20, 555, 111, 21))
        self.pushButton_12.setObjectName("pushButton_12")
        # _____light_invert________________________________________
        self.line_13 = QtWidgets.QFrame(Form)
        self.line_13.setGeometry(QtCore.QRect(0, 586, 160, 20))
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")

        self.pushButton_13 = QtWidgets.QPushButton(Form)
        self.pushButton_13.setGeometry(QtCore.QRect(20, 615, 111, 21))
        self.pushButton_13.setObjectName("pushButton_13")
        # _____recount________________________________________
        self.pushButton_14 = QtWidgets.QPushButton(Form)
        self.pushButton_14.setGeometry(QtCore.QRect(70, 161, 60, 21))
        self.pushButton_14.setObjectName("pushButton_14")

        self.count()
        self.retranslateUi(Form)
        self.button_connetion()

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Arnold_LTs", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Form", "AOV building", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("Form", "Auto Light Group", None, -1))
        self.pushButton_3.setText(QtWidgets.QApplication.translate("Form", "Light AOV", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "BLOKER", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "AOV", None, -1))
        self.pushButton_4.setText(QtWidgets.QApplication.translate("Form", "select", None, -1))
        self.pushButton_5.setText(QtWidgets.QApplication.translate("Form", "connect", None, -1))
        self.pushButton_6.setText(QtWidgets.QApplication.translate("Form", "break", None, -1))
        self.pushButton_7.setText(QtWidgets.QApplication.translate("Form", "create", None, -1))
        self.pushButton_8.setText(QtWidgets.QApplication.translate("Form", "LightRenderSetup", None, -1))
        # _______________Cryptomatte____________________________

        self.pushButton_9.setText(QtWidgets.QApplication.translate("Form", "CrypteMatte", None, -1))
        self.pushButton_15.setText(QtWidgets.QApplication.translate("Form", "ID", None, -1))
        # _______________Cryptomatte____________________________

        self.pushButton_10.setText(QtWidgets.QApplication.translate("Form", "check", None, -1))
        # ________________nuketomaya_____________________________

        self.pushButton_11.setText(QtWidgets.QApplication.translate("Form", "Nuke to Maya", None, -1))
        # ________________renderimage_____________________________
        self.pushButton_12.setText(QtWidgets.QApplication.translate("Form", "Pref ", None, -1))
        # ________________selectlight_____________________________

        self.pushButton_13.setText(QtWidgets.QApplication.translate("Form", "Select Light by aov", None, -1))
        # ________________recount_________________________________
        self.pushButton_14.setText(QtWidgets.QApplication.translate("Form", "Refresh", None, -1))

    def button_connetion(self):
        self.pushButton.clicked.connect(self.AOV_building)
        self.pushButton_2.clicked.connect(self.lt_group)
        self.pushButton_3.clicked.connect(self.AOV_light)
        self.pushButton_4.clicked.connect(self.blocker_selection)
        self.pushButton_5.clicked.connect(self.blocker_connection)
        self.pushButton_6.clicked.connect(self.blocker_disconnection)
        self.pushButton_7.clicked.connect(self.blocker_create)
        self.pushButton_8.clicked.connect(self.Rs_light)
        self.pushButton_9.clicked.connect(self.Cryptomatte)
        self.pushButton_10.clicked.connect(self.Check)
        self.pushButton_11.clicked.connect(self.nuketomaya)
        self.pushButton_12.clicked.connect(self.Pref)
        self.pushButton_13.clicked.connect(self.select_light_by_aov)
        self.pushButton_14.clicked.connect(self.count)
        self.pushButton_15.clicked.connect(self.AOV_id)

    def count(self):
        light_aov_list = []
        current_light_list = self.selection_current_light()

        for i in current_light_list:
            c = pm.getAttr(i + '.aiAov')
            if c not in light_aov_list and c != 'default':
                light_aov_list.append(c)

        light_aov_display = str(len(light_aov_list)) + '/16'
        self.label_3.setText(light_aov_display)

        if len(light_aov_list) > 16:
            self.label_3.setStyleSheet('color:red')
        else:
            self.label_3.setStyleSheet('color:orange')

    def AOV_building(self):
        current_list = []
        for i in aovs.getAOVs():
            current_list.append(i.name)

        for i in aov_list:
            if i not in current_list:
                try:
                    aovs.AOVInterface().addAOV(i)
                except Exception:
                    pass

        aov_driver = pm.ls(type='aiAOVDriver')
        for i in aov_driver:
            pm.setAttr(i + '.mergeAOVs', 1)

        occ_shader = pm.createNode('aiAmbientOcclusion')
        pm.connectAttr('%s.outColor' % occ_shader, 'aiAOV_AO.defaultValue')

        a = pm.createNode('aiFacingRatio')
        b = pm.createNode('aiMultiply')
        c = pm.createNode('aiAdd')

        pm.setAttr('%s.bias' % a, 0.717)
        pm.setAttr('%s.gain' % a, 0)
        pm.setAttr('%s.invert' % a, 1)
        pm.setAttr('%s.input2' % b, (1, 0, 0))
        pm.setAttr('%s.input2' % c, (0, 0, 1))

        pm.connectAttr('%s.outValue' % a, '%s.input1.input1R' % b)
        pm.connectAttr('%s.outValue' % a, '%s.input1.input1G' % b)
        pm.connectAttr('%s.outValue' % a, '%s.input1.input1B' % b)
        pm.connectAttr('%s.outColor' % b, '%s.input1' % c)
        pm.connectAttr('%s.outColor' % c, 'aiAOV_Rim.defaultValue')

        a = pm.createNode('aiUtility')
        pm.setAttr('%s.shadeMode' % a, 2)
        pm.setAttr('%s.colorMode' % a, 5)
        pm.connectAttr('%s.outColor' % a, '%s.defaultValue' % 'aiAOV_UV')

        self.newdriver('P')
        self.newdriver('N')
        self.newdriver('Z')

        pm.setAttr('aiAOV_specular_direct.lightGroups', 1)
        pm.setAttr('aiAOV_specular_indirect.lightGroups', 1)
        pm.setAttr('aiAOV_indirect.globalAov', 0)
        pm.setAttr('aiAOV_indirect.lightGroupsList', 'default')

    def newdriver(slef, aovname):
        i = aovname
        if i not in aovs.getAOVs():
            try:
                aovs.AOVInterface().addAOV(i)
            except Exception:
                pass
        myaov = pm.PyNode(aovs.AOVInterface().getAOVNode(i))
        mydriver = pm.createNode('aiAOVDriver', name='aiAOVDriver_%s' % i)
        mydriver.attr('prefix').set('<RenderLayer>/<Version>/<RenderLayer>.%s' % i)
        if i == 'Z':
            mydriver.attr('exrTiled').set(0)
        pm.connectAttr(mydriver.message, myaov.attr('outputs[0]').driver, f=1)

    def AOV_id(self):
        current_list = []
        mask_list = []
        sg_list = pm.ls(type='shadingEngine')
        for sg in sg_list:
            for aov in sg.aiCustomAOVs:
                mask = aov.aovName.get()
                if mask.startswith('id'):
                    mask_list.append(aov.aovName.get())

        mask_list = list(set(mask_list))

        for i in aovs.getAOVs():
            current_list.append(i.name)

        for i in mask_list:
            if i not in current_list:
                try:
                    aovs.AOVInterface().addAOV(i)
                except Exception:
                    pass

    def selection_current_light(self):
        current_light_list = []

        for element_light in light_type_list:
            sl = pm.ls(type=element_light)
            for element_sl in sl:
                current_light_list.append(element_sl)
        return current_light_list

    def Light_reset(self):
        current_light_list = self.selection_current_light()

        for i in current_light_list:
            light_name = re.sub('Shape', '', i.name())
            aov_name = pm.getAttr(i + '.aiAov')
            if aov_name == 'default' or aov_name != 'Light_' + light_name:
                pm.setAttr(i + '.aiAov', 'Light_' + light_name)
        self.count()

    def AOV_light(self):
        if pm.ls(type='aiAOVDriver') == None:
            pm.createNode('aiAOVDriver')
        current_light_list = self.selection_current_light()
        light_aov_list = []

        for element_current in current_light_list:
            aov = pm.getAttr(element_current + '.aiAov')
            if aov not in light_aov_list and aov != 'default':
                light_aov_list.append(aov)

        current_aov_list = []
        for aov in aovs.getAOVs():
            current_aov_list.append(aov.name)

        for light_aov in light_aov_list:
            # if ('diff_' + light_aov) not in current_aov_list:
            #     aovs.AOVInterface().addAOV('diff_' + light_aov)
            #     pm.setAttr('aiAOV_diff_' + light_aov + '.lightPathExpression', "C<RD><L.'" + light_aov + "'>")
            # if ('sss_' + light_aov) not in current_aov_list:
            #     aovs.AOVInterface().addAOV('sss_' + light_aov)
            #     pm.setAttr('aiAOV_sss_' + light_aov + '.lightPathExpression', "C<TD><L.'" + light_aov + "'>")
            if light_aov not in current_aov_list:
                try:
                    aovs.AOVInterface().addAOV(light_aov)
                except Exception:
                    pass
                pm.setAttr('aiAOV_' + light_aov + '.lightPathExpression', "C.*<L.'" + light_aov + "'>")

            aov_driver = pm.ls(type='aiAOVDriver')
            for i in aov_driver:
                pm.setAttr(i + '.mergeAOVs', 1)
        for aov in current_aov_list:
            if aov not in light_aov_list and 'Light' in aov:
                aovs.AOVInterface().removeAOV(aov)

    def blocker_create(self):
        light = pm.ls(sl=1)
        a = pm.createNode('aiLightBlocker')
        pm.setAttr('%s.density' % a, 1)
        pm.setAttr('%s.geometryType' % a, 1)
        blk = pm.listTransforms(a)
        if light != None:
            pm.select(light, blk)
            Ui_Form.blocker_connection(self)
            pm.select(light, deselect=1)

    def blocker_selection(self):
        current_selection = pm.listRelatives(pm.ls(selection=True))
        for i in current_selection:
            a = pm.listConnections(i)
            pm.select(a)

    def blocker_connection(self):
        current_selection = pm.listRelatives(pm.ls(selection=True))
        light_list = []
        bloker_list = []
        for i in current_selection:
            if pm.nodeType(str(i)) in light_type_list:
                light_list.append(i)
            elif pm.nodeType(str(i)) == 'aiLightBlocker':
                bloker_list.append(i)

        for light_element in light_list:
            for bloker_element in bloker_list:
                if bloker_element not in pm.listRelatives(pm.getAttr('%s.aiFilters' % light_element)):
                    filter_index = 0
                    while pm.getAttr('%s.aiFilters[%s]' % (light_element, filter_index)) != None:
                        filter_index += 1
                    pm.connectAttr('%s.message' % bloker_element, '%s.aiFilters[%s]' % (light_element, filter_index))

    def blocker_disconnection(self):
        current_selection = pm.listRelatives(pm.ls(selection=True))
        light_list = []
        bloker_list = []
        for i in current_selection:
            if pm.nodeType(str(i)) in light_type_list:
                light_list.append(i)
            elif pm.nodeType(str(i)) == 'aiLightBlocker':
                bloker_list.append(i)

        for light_element in light_list:
            filters = pm.listRelatives(pm.listConnections('%s.aiFilters' % light_element))
            for bloker_element in bloker_list:
                if bloker_element in filters:
                    filter_index = pm.listConnections('%s.message' % bloker_element, p=True)
                    for filter_index_element in filter_index:
                        if str(light_element) in str(filter_index_element):
                            try:
                                pm.disconnectAttr('%s.message' % bloker_element, filter_index_element)
                            except:
                                pass

    def Cryptomatte(self):
        cry_list = ['crypto_asset', 'crypto_material', 'crypto_object']
        current_list = []
        for i in aovs.getAOVs():
            current_list.append(i.name)

        for i in cry_list:
            if i not in current_list:
                try:
                    newaov = aovs.AOVInterface().addAOV(i)
                except Exception:
                    pass
                driver = pm.createNode('aiAOVDriver', name='AronldDriver_%s' % i)
                pm.setAttr('%s.prefix' % driver, '<RenderLayer>/<Version>/<RenderLayer>.%s' % i)
                pm.disconnectAttr('%s.outputs[0].driver' % ('aiAOV_' + i))
                pm.connectAttr('%s.message' % driver, '%s.outputs[0].driver' % ('aiAOV_' + i))

        cry_shader = pm.createNode('cryptomatte')
        pm.connectAttr('%s.outColor' % cry_shader, 'aiAOV_crypto_asset.defaultValue')
        pm.connectAttr('%s.outColor' % cry_shader, 'aiAOV_crypto_material.defaultValue')
        pm.connectAttr('%s.outColor' % cry_shader, 'aiAOV_crypto_object.defaultValue')

    def getimagedir(self):
        getdir.getdir()

    def lt_group(self):
        try:
            lg.my.close()

        except:
            pass
        lg.my = lg.Ui_Form()
        lg.my.show()

    def nuketomaya(self):
        try:
            ntm.my.close()

        except:
            pass
        ntm.my = ntm.Ui_Form()
        ntm.my.show()

    def aov_building(self):
        import ofArnoldOptions.ofArnoldAovSetting as aovsetup
        aovsetup.setup_aovs_main()

    def lightinvert(self):
        lightinvert.light_invert()

    def Rs_light(self):
        try:
            Light_RenderSetup.my.close()

        except:
            pass
        Light_RenderSetup.my = Light_RenderSetup.Ui_Form()
        Light_RenderSetup.my.show()

    def Check(self):
        import mayacheck as mc
        try:
            mc.my.close()

        except:
            pass
        mc.my = mc.Ui_Form()
        mc.my.show()

    def select_light_by_aov(self):
        import aov_select as aov_sl
        try:
            aov_sl.my.close()

        except:
            pass
        aov_sl.my = aov_sl.Ui_Form()
        aov_sl.my.show()

    def Pref(self):
        import pymel.core as pm
        import mtoa.aovs as aovs
        import lightingToolset.createPrefReference as pf

        def newdriver(aovname):
            i = aovname
            if i not in aovs.getAOVs():
                try:
                    aovs.AOVInterface().addAOV(i)
                except Exception:
                    pass
            myaov = pm.PyNode(aovs.AOVInterface().getAOVNode(i))
            mydriver = pm.createNode('aiAOVDriver', name='aiAOVDriver_%s' % i)
            mydriver.attr('prefix').set('<RenderLayer>/<Version>/<RenderLayer>.%s' % i)
            pm.connectAttr(mydriver.message, myaov.attr('outputs[0]').driver, f=1)

        if pm.selected() == []:
            ls = pm.ls('char_grp', 'prop_grp')
            if ls != []:
                pm.select(ls)
                pf.main()
                newdriver('Pref')
        elif pm.selected() != []:
            pf.main()
            newdriver('Pref')

if __name__ == '__main__':
    try:
        my.close()

    except:
        pass
    my = Ui_Form()
    my.show()





