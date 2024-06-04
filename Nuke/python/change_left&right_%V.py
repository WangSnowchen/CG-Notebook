import nuke

# 获取所有 Read 节点
read_nodes = [node for node in nuke.allNodes() if node.Class() == 'Read']
#print(read_nodes)
# 遍历所有 Read 节点
for node in read_nodes:
    file_path = node['file'].value()
    new_file_path = file_path.replace('left', '%V').replace('right', '%V')
    node['file'].setValue(new_file_path)