import maya.cmds as cmds
import mtoa.aovs as aovs

class LightGroupManager:
    def __init__(self, light_type_list):
        self.light_type_list = light_type_list

    def connect_lightGroup_to_aov():
        selected_lights = cmds.ls(selection=True)
        if not selected_lights:
            cmds.warning("请先选择灯光对象！")
            return

        light_group_name_list = []

        try:
            # 获取每个灯光对象的aiAov属性作为AOV名称
            for light in selected_lights:
                aov_name = cmds.getAttr(light + '.aiAov')
                if aov_name:  # 确保aov_name不为空
                    light_group_name_list.append(aov_name)

            # 去除重复的AOV名称
            lightGroup_aov_list = list(dict.fromkeys(light_group_name_list))

            # 针对每个AOV名称创建对应的AOV
            for name in lightGroup_aov_list:
                aov_name = 'RGBA_' + name
                aov = aovs.AOVInterface().addAOV(aov_name)

                # 填写LightPathExpression
                aov_node = aovs.AOVInterface().getAOVNode(aov_name)
                if aov_node:  # 确保aov_node不为空
                    cmds.setAttr(aov_node + '.lightPathExpression', f"C.*<L.'{name}'>", type='string')

        except Exception as e:
            cmds.warning(f"连接灯光到AOV时出现错误：{str(e)}")

    def select_lights_by_aov(self, aov_name):
        # 获取场景里所有指定类型的灯光对象
        light_list = cmds.ls(type=self.light_type_list)
        if not light_list:
            cmds.warning("场景里没有指定类型的灯光对象！")
            return

        selected_lights = []
        # 遍历灯光对象，查找aiAov属性值与输入的AOV名称相同的灯光对象
        for light in light_list:
            if cmds.attributeQuery('aiAov', node=light, exists=True):  # 检查属性是否存在
                if cmds.getAttr(light + '.aiAov') == aov_name:
                    selected_lights.append(light)
            else:
                cmds.warning(f"{light} 没有 aiAov 属性。")

        if selected_lights:
            # 选中符合条件的灯光对象
            cmds.select(selected_lights)
        else:
            cmds.warning(f"没有找到 aiAov 属性值为 {aov_name} 的灯光对象。")

# 示例调用
# light_type_list = ['directionalLight', 'spotLight', 'pointLight', 'areaLight', 'aiAreaLight', 'aiSkyDomeLight', 'aiMeshLight', 'aiPhotometricLight', 'aiLightPortal']
# manager = LightGroupManager(light_type_list)
# aov_name = "your_aov_name_here"  # 替换为实际的AOV名称
# manager.select_lights_by_aov(aov_name)
