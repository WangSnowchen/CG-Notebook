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
        if continuous:
            for n in range(len(array)-1):
                yield array[n:(n+2)]
        else:
            for n in range(len(array)//2):
                yield array[n*2:(n+1)*2]

    def fetch_all_layers(self):
        """
        获取所有图层并创建相应的通道节点
        """
        self.dot_array = []
        self.start_node = nuke.selectedNode()

        self.start_xpos = self.start_node.xpos()
        self.start_ypos = self.start_node.ypos()
    
        all_channels = list({
            channel_node.split('.')[0] for channel_node in self.start_node.channels()
            if channel_node.startswith('RGBA') or channel_node.startswith('emission')
        })
    
        self.dot_array = []
        combined_channels = []
        for prefix in ['RGBA', 'emission']:
            combined_channels.extend([i for i in all_channels if i.startswith(prefix)])

        self.create_channels_node(combined_channels)

    def create_channels_node(self, channel_array):
        """
        创建通道节点，包括Dot、Remove、Shuffle和Merge节点
        :param channel_array: 通道数组
        """
        dot_nodes, remove_nodes, shuffle_nodes, merge_nodes = [], [], [], []

        # 遍历通道数组，为每个通道创建节点
        for index, layer in enumerate(channel_array):
            plug_dot = nuke.nodes.Dot()
            if self.dot_array == []:
                plug_dot.setInput(0, self.start_node)
            else:
                plug_dot.setInput(0, self.dot_array[-1])

            self.dot_array.append(plug_dot)
            dot_nodes.append(plug_dot)

            plug_remove = nuke.nodes.Remove(name='Remove_' + layer)
            plug_remove.setInput(0, plug_dot)
            plug_remove.knob('operation').setValue('keep')
            plug_remove.knob('channels').setValue(layer)
            remove_nodes.append(plug_remove)

            plug_suffle = nuke.nodes.Shuffle(name='Shuffle_' + layer)
            plug_suffle.knob('in').setValue(layer)
            #plug_suffle.knob('in2').setValue('alpha')
            plug_suffle.knob('postage_stamp').setValue(True)
            plug_suffle.setInput(0, plug_remove)
            shuffle_nodes.append(plug_suffle)

            # 如果索引为0，创建一个Dot节点并将其输入设置为plug_suffle，然后将Dot节点添加到merge_nodes列表中
            if index == 0:
                dot_node = nuke.nodes.Dot()
                dot_node.setInput(0, plug_suffle)
                merge_nodes.append(dot_node)
            else:
                # 否则，创建一个Merge2节点，设置其操作、通道和合并选项，并将其输入设置为plug_suffle，然后将Merge2节点添加到merge_nodes列表中
                merge_node = nuke.nodes.Merge2(name='Merge_' + layer)
                merge_node.knob("operation").setValue("plus")
                merge_node.knob("Achannels").setValue("rgb")
                merge_node.knob("also_merge").setValue("all")
                merge_node.setInput(1, plug_suffle)
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
        for index, (dot_node, remove_node, shuffle_node, merge_node) in enumerate(zip(dot_nodes, remove_nodes, shuffle_nodes, merge_nodes)):
            dot_node.setXYpos(self.start_xpos + 125 * (index + 1) - dot_node.screenWidth() // 2, self.start_ypos + 0 - self.start_node.screenHeight() // 2)
            remove_node.setXYpos(self.start_xpos + 125 * (index + 1) - remove_node.screenWidth() // 2, self.start_ypos + 60 - self.start_node.screenHeight() // 2)
            shuffle_node.setXYpos(self.start_xpos + 125 * (index + 1) - shuffle_node.screenWidth() // 2, self.start_ypos + 120 - self.start_node.screenHeight() // 2)
            merge_node.setXYpos(self.start_xpos + 125 * (index + 1) - merge_node.screenWidth() // 2, self.start_ypos + 240 - self.start_node.screenHeight() // 2)


def main():
    """
    主函数，实例化MapAovs类并调用fetch_all_layers方法
    """
    doit = MapAovs()
    doit.fetch_all_layers()


if __name__ == '__main__':
    main()