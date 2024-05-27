from PySide2 import QtWidgets, QtCore  # 导入PySide2的控件和核心模块
import re  # 导入正则表达式模块
import maya.cmds as cmds  # 导入Maya的命令模块

class MyWindow(QtWidgets.QWidget):  # 定义自定义窗口类
    def __init__(self):  # 初始化方法
        super(MyWindow, self).__init__()  # 调用父类的初始化方法
        self.setWindowTitle('convert_nuke_to_maya')  # 设置窗口标题
        self.setFixedSize(300, 200)  # 锁定窗口大小
        self.create_layout()  # 调用创建布局的方法

    def create_layout(self):  # 定义创建布局的方法
        self.main_layout = QtWidgets.QVBoxLayout()  # 创建垂直布局

        self.tip_label = QtWidgets.QLabel('选择物体以查看颜色属性')  # 创建提示标签
        self.main_layout.addWidget(self.tip_label)  # 将提示标签添加到主布局中

        self.text_field = QtWidgets.QTextEdit()  # 创建文本输入框
        self.text_field.setFixedSize(280, 100)  # 锁定文本框大小
        self.text_field.setPlaceholderText('在此输入...')  # 设置文本框的占位符文本
        self.main_layout.addWidget(self.text_field)  # 将文本输入框添加到主布局中

        self.color_label =  QtWidgets.QLabel()  # 创建颜色标签
        self.main_layout.addWidget(self.color_label)  # 将颜色标签添加到主布局中

        self.my_button = QtWidgets.QPushButton('convert')  # 创建按钮
        self.main_layout.addWidget(self.my_button)  # 将按钮添加到主布局中

        self.setLayout(self.main_layout)  # 将主布局设置为窗口的布局

        self.my_button.clicked.connect(self.button_clicked)  # 将按钮的点击事件连接到相应方法上

    def button_clicked(self):  # 定义按钮点击事件的方法
        user_text = self.text_field.toPlainText()  # 获取文本输入框中的内容
        txt = user_text  # 使用文本框输入的内容替换txt的内容
        selected_lights = cmds.ls(selection=True)  # 获取当前选中的灯光

        white_match = re.search(r'white\s+([\d.]+)', txt)  # 在输入文本中匹配白色属性
        multiply_match = re.search(r'multiply\s+{([\d.\s]+)}', txt)  # 在输入文本中匹配乘法属性

        if white_match != None:  # 如果匹配到白色属性
            white = float(white_match.group(1))  # 获取白色属性的值
            for light in selected_lights:  # 遍历选中的灯光
                light_intensity = cmds.getAttr(light + ".intensity")  # 获取灯光的强度属性
                new_intensity = white * light_intensity  # 计算新的强度值

                cmds.setAttr(light + ".intensity", new_intensity)  # 设置灯光的强度属性为新值

        if multiply_match != None:  # 如果匹配到乘法属性
            multiply = [float(num) for num in multiply_match.group(1).split()]  # 将匹配到的值转换为列表
            for light in selected_lights:  # 遍历选中的灯光
                light_color = cmds.getAttr(light + ".color")[0]  # 获取灯光的颜色属性
                new_color = [color * factor for color, factor in zip(light_color, multiply)]  # 计算新的颜色值

                cmds.setAttr(light + ".color", new_color[0], new_color[1], new_color[2], type="double3")  # 设置灯光的颜色属性为新值

# 创建窗口实例并显示
my_window = MyWindow()  # 创建自定义窗口实例
my_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 窗口一直在最上层
my_window.show()  # 显示窗口