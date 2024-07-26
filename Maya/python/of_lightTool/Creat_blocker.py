import maya.cmds as cmds
import via as light_type_list
import via as light_filter

#light_type_list = ['directionalLight','spotLight','pointLight', 'areaLight','aiAreaLight','aiSkyDomeLight','aiMeshLight','aiPhotometricLight','aiLightPortal']
#light_filter = ['aiBarndoor','aiGobo','aiLightBlocker','aiLightDecay']

class BlockerTool:
    def __init__(self):
        pass

    def create_blocker(self):
        try:
            blocker = cmds.createNode('aiLightBlocker')
            cmds.setAttr(f'{blocker}.density', 1)
            cmds.setAttr(f'{blocker}.geometryType', 1)
        except Exception as e:
            print(f"Error creating blocker: {e}")

    def connect_blockers(self):
        try:
            selected = cmds.ls(selection=True)
            if not selected:
                print("No objects selected.")
                return
            
            selected_all = cmds.listRelatives(selected, fullPath=True) or []

            light_list = [node for node in selected_all if cmds.nodeType(node) in light_type_list]
            light_filters_list = [node for node in selected_all if cmds.nodeType(node) in light_filter]

            if not light_list or not light_filters_list:
                print("No lights or filters selected.")
                return

            for light in light_list:
                light_filters_index = cmds.getAttr(f'{light}.aiFilters', mi=True) or []
                next_index = max(light_filters_index, default=-1) + 1

                for filter in light_filters_list:
                    cmds.connectAttr(f'{filter}.message', f'{light}.aiFilters[{next_index}]')
                    next_index += 1
        except Exception as e:
            print(f"Error connecting blockers: {e}")

    def show_related_filters(self):
        try:
            selected = cmds.ls(selection=True)
            if not selected:
                print("No objects selected.")
                return
            
            selected_all = cmds.listRelatives(selected, fullPath=True) or []

            light_list = [node for node in selected_all if cmds.nodeType(node) in light_type_list]

            if not light_list:
                print("No lights selected.")
                return

            filters_to_select = []
            for light in light_list:
                light_filters_index = cmds.getAttr(f'{light}.aiFilters', mi=True) or []
                for index in light_filters_index:
                    filter_node = cmds.listConnections(f'{light}.aiFilters[{index}]', s=True, d=False) or []
                    if filter_node:
                        print(f"{light} related filter: {filter_node[0]}")
                        filters_to_select.append(filter_node[0])
            
            # 选中所有相关的过滤器节点
            cmds.select(filters_to_select)
        except Exception as e:
            print(f"Error showing related filters: {e}")



# 示例使用
# blocker_tool = BlockerTool()
# blocker_tool.create_blocker()
# blocker_tool.connect_blockers()
# blocker_tool.show_related_filters()
