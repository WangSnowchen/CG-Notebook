from PySide2 import QtWidgets, QtCore  
import re  
import maya.cmds as cmds  

class MyWindow(QtWidgets.QWidget):  
    def __init__(self):  
        super(MyWindow, self).__init__()  
        self.setWindowTitle('convert_nuke_to_maya')  
        self.setFixedSize(300, 200)  
        self.create_layout()  

        # self.timer = QtCore.QTimer(self)  # 创建一个定时器
        # self.timer.timeout.connect(self.update_color)
        # self.timer.start(100)

    def create_layout(self):  
        self.main_layout = QtWidgets.QVBoxLayout()  

        self.tip_label = QtWidgets.QLabel('选择物体以查看颜色属性')  
        self.main_layout.addWidget(self.tip_label)  

        self.text_field = QtWidgets.QTextEdit()  
        self.text_field.setFixedSize(280, 100)  
        self.text_field.setPlaceholderText('在此输入...')  
        self.main_layout.addWidget(self.text_field)  

        self.color_label =  QtWidgets.QLabel()  
        self.main_layout.addWidget(self.color_label)  

        self.my_button = QtWidgets.QPushButton('convert')  
        self.main_layout.addWidget(self.my_button)  

        self.setLayout(self.main_layout)  

        self.my_button.clicked.connect(self.button_clicked)  

    # def update_color(self):
    #         selected_objects = cmds.ls(selection=True)  # 获取当前选中对象
    #         if selected_objects: 
    #             shape = cmds.listRelatives(selected_objects[0], shapes=True)  # 获取所选对象的形状节点
    #             if shape:
    #                 color = cmds.getAttr(shape[0] + '.color')  # 获取颜色属性
    #                 self.color_label.setText('Color: {}'.format(color))
    #             else:
    #                 self.color_label.setText('所选对象没有颜色属性')
    #                 color = cmds.getAttr(selected_objects[0] + '.color')
    #                 self.color_label.setText('Color: {}'.format(color))
    #         else:
    #             self.color_label.setText('没有选中对象')

    def button_clicked(self):  
        user_text = self.text_field.toPlainText()  
        txt = user_text  
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

my_window = MyWindow()  
my_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  
my_window.show()  