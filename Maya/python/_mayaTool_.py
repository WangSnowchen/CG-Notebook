import maya.cmds as cmds



def creat_light_in_different_positions(lightType:str):
    
    selected_objects = cmds.ls(selection=True)
    for obj in selected_objects:
        obj_center = cmds.objectCenter(obj, gl=True)
        area_light = cmds.shadingNode(lightType, asLight=True)
        cmds.move(obj_center[0], obj_center[1], obj_center[2], area_light)


def connect_light_to_selected_lightFilter(lightfilterType:str):
    selected_lights = cmds.ls(selection=True)
    light_filter = cmds.createNode(lightfilterType)

    for light in selected_lights:
        cmds.connectAttr(light_filter + '.message', light + '.aiFilters[0]', force=True)