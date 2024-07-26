import maya.cmds as cmds
import mtoa.aovs as aovs

selected_lights = cmds.ls(selection=True)
light_group_list = []

# 获取每个灯光对象的aiAov属性作为AOV名称
for light in selected_lights:
    aov_name = cmds.getAttr(light + '.aiAov')
    light_group_list.append(aov_name)

# 去除重复的AOV名称
lightGroup_aov_list = list(dict.fromkeys(light_group_list))

# 针对每个AOV名称创建对应的AOV
for name in lightGroup_aov_list:
    # 创建AOV
    aov_name = 'RGBA_' + name
    aov = aovs.AOVInterface().addAOV(aov_name)
    
    # 填写LightPathExpression
    aov_node = aovs.AOVInterface().getAOVNode(aov_name)
    cmds.setAttr(aov_node + '.lightPathExpression', "C.*<L.'" + name + "'>", type='string')