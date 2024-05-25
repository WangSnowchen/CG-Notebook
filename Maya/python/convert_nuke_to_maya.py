from PySide2 import QtWidgets, QtCore
import maya.cmds as cmds

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('convert_nuke_to_maya')
        self.setFixedSize(300, 200)  # 锁定窗口大小
        self.create_layout()

        self.timer = QtCore.QTimer(self)  # 创建一个定时器
        self.timer.timeout.connect(self.update_color)
        self.timer.start(100)  # 每100毫秒刷新一次颜色

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

    def update_color(self):
        selected_objects = cmds.ls(selection=True)  # 获取当前选中对象
        if selected_objects:
            shape = cmds.listRelatives(selected_objects[0], shapes=True)  # 获取所选对象的形状节点
            if shape:
                color = cmds.getAttr(shape[0] + '.color')  # 获取颜色属性
                self.color_label.setText('Color: {}'.format(color))
            else:
                self.color_label.setText('所选对象没有颜色属性')
        else:
            self.color_label.setText('没有选中对象')

    def button_clicked(self):
        user_text = self.text_field.toPlainText()
        cmds.confirmDialog(title='User Input', message='You entered: {}'.format(user_text))

# 创建窗口实例并显示
my_window = MyWindow()
my_window.show()
