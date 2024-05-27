from PySide2 import QtWidgets, QtCore
import re
import maya.cmds as cmds

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('convert_nuke_to_maya')
        self.setFixedSize(300, 200)  # 锁定窗口大小
        self.create_layout()

    def create_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()

        self.tip_label = QtWidgets.QLabel('选择物体以查看颜色属性')
        self.main_layout.addWidget(self.tip_label)

        self.text_field = QtWidgets.QTextEdit()
        self.text_field.setFixedSize(280, 100)  # 锁定文本框大小
        self.text_field.setPlaceholderText('在此输入...')
        self.main_layout.addWidget(self.text_field)

        self.color_label =  QtWidgets.QLabel()
        self.main_layout.addWidget(self.color_label)

        self.my_button = QtWidgets.QPushButton('convert')
        self.main_layout.addWidget(self.my_button)

        self.setLayout(self.main_layout)

        self.my_button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        user_text = self.text_field.toPlainText()
        txt = user_text  # 使用文本框输入的内容替换txt的内容
        selected_lights = cmds.ls(selection=True)
    
        white_match = re.search(r'white\s+([\d.]+)', txt)
        multiply_match = re.search(r'multiply\s+{([\d.\s]+)}', txt)

        if white_match != None:
            white = float(white_match.group(1))
            for light in selected_lights:
                light_intensity = cmds.getAttr(light + ".intensity")
                new_intensity = white * light_intensity

                cmds.setAttr(light + ".intensity", new_intensity)
        if multiply_match != None:
            multiply = [float(num) for num in multiply_match.group(1).split()]
            for light in selected_lights:
                light_color = cmds.getAttr(light + ".color")[0]
                new_color = [color * factor for color, factor in zip(light_color, multiply)]

                cmds.setAttr(light + ".color", new_color[0], new_color[1], new_color[2], type="double3")

# 创建窗口实例并显示
my_window = MyWindow()
my_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 窗口一直在最上层
my_window.show()