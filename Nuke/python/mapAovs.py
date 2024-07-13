#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import nuke


class MapAovs(object):

    def iter_pairs(self, array, continuous = True):
        if continuous:
            # "ABCDEF" ---> AB BC CD DE EF
            for n in range(len(array)-1):
                yield array[n:(n+2)]
        else:
            # "ABCDEF" ---> AB CD EF
            for n in range(len(array)//2):
                yield array[n*2:(n+1)*2]

    # def fetch_all_layers(self):
    #     self.dot_array = []
    #     self.start_node = nuke.selectedNode()

    #     self.start_xpos = self.start_node.xpos()
    #     self.start_ypos = self.start_node.ypos()
    #     all_channels = list({
    #         channel_node.split('.')[0] for channel_node in self.start_node.channels()
    #         if channel_node.split('_')[0] in ['RGBA', 'Beauty'] and 'default' not in channel_node.split('_')[1]
    #     })
        
    #     self.dot_array = []
    #     prefix_set = list(set([i.split('_')[0] for i in all_channels]))
    #     for prefix in prefix_set:
    #         prfix_channel = [i for i in all_channels if i.split('_')[0] == prefix]
    #         prfix_channel.sort()
    #         self.create_channels_node(prfix_channel)

    def create_channels_node(self, channel_array):
        dot_nodes, remove_nodes, shuffle_nodes, merge_nodes = [], [], [], []

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
            plug_suffle.knob('postage_stamp').setValue(True)
            plug_suffle.setInput(0, plug_remove)
            shuffle_nodes.append(plug_suffle)

            if index == 0:
                dot_node = nuke.nodes.Dot()
                dot_node.setInput(0, plug_suffle)
                merge_nodes.append(dot_node)
            else:
                merge_node = nuke.nodes.Merge2(name='Merge_' + layer)
                merge_node.knob("operation").setValue("plus")
                merge_node.knob("Achannels").setValue("rgb")
                merge_node.knob("also_merge").setValue("all")
                merge_node.setInput(1, plug_suffle)
                merge_nodes.append(merge_node)

        for src_merge_node, dst_merge_node in self.iter_pairs(merge_nodes, continuous=True):
            dst_merge_node.setInput(0, src_merge_node)

        for index, (dot_node, remove_node, shuffle_node, merge_node) in enumerate(zip(dot_nodes, remove_nodes, shuffle_nodes, merge_nodes)):
            dot_node.setXYpos(self.start_xpos + 125 * (index + 1) - dot_node.screenWidth() // 2, self.start_ypos + 0 - self.start_node.screenHeight() // 2)
            remove_node.setXYpos(self.start_xpos + 125 * (index + 1) - remove_node.screenWidth() // 2, self.start_ypos + 60 - self.start_node.screenHeight() // 2)
            shuffle_node.setXYpos(self.start_xpos + 125 * (index + 1) - shuffle_node.screenWidth() // 2, self.start_ypos + 120 - self.start_node.screenHeight() // 2)
            merge_node.setXYpos(self.start_xpos + 125 * (index + 1) - merge_node.screenWidth() // 2, self.start_ypos + 240 - self.start_node.screenHeight() // 2)


def main():
    doit = MapAovs()
    doit.fetch_all_layers()


if __name__ == '__main__':
    main()

