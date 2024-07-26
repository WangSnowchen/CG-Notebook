import maya.cmds as cmds
import mtoa.aovs as aovs

def connect_light_to_aov():
    selected_lights = cmds.ls(selection=True)
    if not selected_lights:
        cmds.warning("请先选择灯光对象！")
        return

    light_group_list = []

    try:
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

    except Exception as e:
        cmds.warning("连接灯光到AOV时出现错误：{}".format(str(e)))

# 调用函数连接灯光到对应的AOV
connect_light_to_aov()