
import maya.cmds as cmds


def blocker_create(self):
    light = cmds.ls(sl=1)
    a = cmds.createNode('aiLightBlocker')
    cmds.setAttr('%s.density' % a, 1)
    cmds.setAttr('%s.geometryType' % a, 1)
    blk = cmds.listTransforms(a)


