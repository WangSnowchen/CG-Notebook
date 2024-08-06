#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import nuke


class MapAovs(object):
    """
    处理AOV（Arbitrary Output Variables）映射的类
    """

    def iter_pairs(self, array, continuous=True):
        """
        生成数组中相邻元素对或间隔元素对的迭代器
        :param array: 输入数组
        :param continuous: 是否生成连续对
        :return: 生成器，生成相邻或间隔元素对
        """
        # 如果需要连续的子数组
        if continuous:
            for n in range(len(array)-1):
                yield array[n:(n+2)]
        else:
            # 如果需要非连续的子数组
            for n in range(len(array)//2):
                yield array[n*2:(n+1)*2]

    def fetch_all_layers(self):
        """
        获取所有图层并创建相应的通道节点
        """
        # 初始化点的数组
        self.dot_array = []
        # 获取选中的起始节点
        self.start_node = nuke.selectedNode()

        # 获取起始节点的x和y坐标
        self.start_xpos = self.start_node.xpos()
        self.start_ypos = self.start_node.ypos()
    
        # 获取所有符合条件的通道
        all_channels = list({
            channel_node.split('.')[0] for channel_node in self.start_node.channels()
            if channel_node.startswith('RGBA') or channel_node.startswith('emission')
        })
    
        # 重新初始化点的数组
        self.dot_array = []
        # 初始化组合通道的列表
        combined_channels = []
        # 根据前缀组合通道
        # 遍历指定的前缀列表，筛选出符合条件的通道并添加到 combined_channels 列表中
        for prefix in ['RGBA', 'emission']:
            combined_channels.extend([i for i in all_channels if i.startswith(prefix) and i != 'RGBA_default'])
        # 对 combined_channels 列表进行排序
        combined_channels.sort()
        # 创建通道节点
        self.create_channels_node(combined_channels)
    def create_channels_node(self, channel_array):
        """
        创建通道节点，包括Dot、Remove、Shuffle和Merge节点
        :param channel_array: 通道数组
        """
        dot_nodes, remove_nodes, shuffle_nodes, merge_nodes = [], [], [], []

        # 修改节点的x和y坐标
        all_node_x = 330
        merge_node_y = 1100

        # 遍历通道数组，为每个通道创建节点
        # 遍历通道数组中的每一层
        for index, layer in enumerate(channel_array):
            # 创建一个Dot节点
            plug_dot = nuke.nodes.Dot()
            # 如果dot_array为空，将Dot节点的输入设置为start_node
            if self.dot_array == []:
                plug_dot.setInput(0, self.start_node)
            # 否则，将Dot节点的输入设置为dot_array中的最后一个节点
            else:
                plug_dot.setInput(0, self.dot_array[-1])
        
            # 将创建的Dot节点添加到dot_array中
            self.dot_array.append(plug_dot)
            # 将创建的Dot节点添加到dot_nodes列表中
            dot_nodes.append(plug_dot)
        
            # 创建一个Remove节点，并命名为'Remove_' + 当前层
            plug_remove = nuke.nodes.Remove(name='Remove_' + layer)
            # 将Remove节点的输入设置为创建的Dot节点
            plug_remove.setInput(0, plug_dot)
            # 设置Remove节点的操作模式为'keep'
            plug_remove.knob('operation').setValue('keep')
            # 设置Remove节点要处理的通道为当前层
            plug_remove.knob('channels').setValue(layer)
            # 将创建的Remove节点添加到remove_nodes列表中
            remove_nodes.append(plug_remove)
        
            # 创建一个Shuffle节点，并命名为'Shuffle_' + 当前层
            plug_suffle = nuke.nodes.Shuffle(name='Shuffle_' + layer)
            # 设置Shuffle节点的输入通道为当前层
            plug_suffle.knob('in').setValue(layer)
            # 启用Shuffle节点的邮票预览功能
            plug_suffle.knob('postage_stamp').setValue(True)
            # 将Shuffle节点的输入设置为创建的Remove节点
            plug_suffle.setInput(0, plug_remove)
            # 将创建的Shuffle节点添加到shuffle_nodes列表中
            shuffle_nodes.append(plug_suffle)

            # 如果索引为0，创建一个Dot节点并将其输入设置为plug_suffle，然后将Dot节点添加到merge_nodes列表中
            if index == 0:
                dot_node = nuke.nodes.Dot()
                dot_node.setInput(0, plug_suffle)
                merge_nodes.append(dot_node)
            else:
                # 否则，创建一个Merge2节点，设置其操作、通道和合并选项，并将其输入设置为plug_suffle，然后将Merge2节点添加到merge_nodes列表中
                # 创建一个名为 'Merge_' + layer 的 Merge2 节点
                merge_node = nuke.nodes.Merge2(name='Merge_' + layer)
                # 设置 Merge2 节点的操作模式为 "plus"
                merge_node.knob("operation").setValue("plus")
                # 设置 Merge2 节点的 A 通道为 "rgb"
                merge_node.knob("Achannels").setValue("rgb")
                # 设置 Merge2 节点同时合并所有通道
                merge_node.knob("also_merge").setValue("all")
                # 将 plug_suffle 节点连接到 Merge2 节点的输入 1
                merge_node.setInput(1, plug_suffle)
                # 将 Merge2 节点添加到 merge_nodes 列表中
                merge_nodes.append(merge_node)
        # 设置合并节点的输入
        # 遍历合并节点对，并将每个目标合并节点的输入设置为源合并节点
        for src_merge_node, dst_merge_node in self.iter_pairs(merge_nodes, continuous=True):
            dst_merge_node.setInput(0, src_merge_node)
        
        # 如果存在合并节点
        if merge_nodes:
            # 获取最后一个合并节点
            last_merge_node = merge_nodes[-1]
            # 如果合并节点数量大于1，将最后一个合并节点的输入设置为倒数第二个合并节点
            if len(merge_nodes) > 1:
                last_merge_node.setInput(0, merge_nodes[-2])
            # 否则，将最后一个合并节点的输入设置为第一个shuffle节点
            else:
                last_merge_node.setInput(0, shuffle_nodes[0])

        # 设置节点的位置
        # 遍历每个节点组，设置每个节点的位置
        for index, (dot_node, remove_node, shuffle_node, merge_node) in enumerate(zip(dot_nodes, remove_nodes, shuffle_nodes, merge_nodes)):
            dot_node.setXYpos(self.start_xpos + all_node_x * (index + 1) - dot_node.screenWidth() // 2, self.start_ypos + 0 - self.start_node.screenHeight() // 2)
            remove_node.setXYpos(self.start_xpos + all_node_x * (index + 1) - remove_node.screenWidth() // 2, self.start_ypos + 60 - self.start_node.screenHeight() // 2)
            shuffle_node.setXYpos(self.start_xpos + all_node_x * (index + 1) - shuffle_node.screenWidth() // 2, self.start_ypos + 120 - self.start_node.screenHeight() // 2)
            merge_node.setXYpos(self.start_xpos + all_node_x * (index + 1) - merge_node.screenWidth() // 2, self.start_ypos + merge_node_y - self.start_node.screenHeight() // 2)


def main():
    """
    主函数，实例化MapAovs类并调用fetch_all_layers方法
    """
    doit = MapAovs()
    doit.fetch_all_layers()


if __name__ == '__main__':
    main()