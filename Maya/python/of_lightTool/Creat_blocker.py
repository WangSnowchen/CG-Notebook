import maya.cmds as cmds

light_type_list = ['directionalLight','spotLight','pointLight', 'areaLight','aiAreaLight','aiSkyDomeLight','aiMeshLight','aiPhotometricLight','aiLightPortal']
light_filter = ['aiBarndoor','aiGobo','aiLightBlocker','aiLightDecay']

def blocker_create():
    blocker = cmds.createNode('aiLightBlocker')
    cmds.setAttr(f'{blocker}.density', 1)
    cmds.setAttr(f'{blocker}.geometryType', 1)

def blocker_connection():
    selected_all = cmds.listRelatives(cmds.ls(selection=True))

    light_list = []
    light_filters_list = []

    for i in selected_all:
        if cmds.nodeType(str(i)) in light_type_list:
            light_list.append(i)
        elif cmds.nodeType(str(i)) in light_filter:
            light_filters_list.append(i)
    
    filter_index = len(light_filters_list) + 1

    for light in light_list:
        light_filters_index = cmds.getAttr(light + '.aiFilters',mi=1)
        light_filters_index = light_filters_index[-1] + 1
        #return light_filters_index
    r = range(light_filters_index,filter_index)
    iterator = iter(r)

    while True:
        try:
            i = next(iterator)
            for light in light_list:
                for filter in light_filters_list:
                    cmds.connectAttr(f'{filter}.message', f'{light}.aiFilters[{i}]')
        except StopIteration:
            break
