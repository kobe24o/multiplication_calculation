# _*_ coding: utf-8 _*_
# @Time : 2023/8/6 9:07
# @Author : Michael
# @File : main.py.py
# @desc :
import gc
from multiply_movie import show_multiple
import sys
import os
import random
from PyQt5.QtGui import QDesktopServices, QPixmap, QIcon
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QAction, \
    QMenuBar, QDialog


# 生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 判断sys中是否存在frozen变量,即是否是打包程序
        base_path = sys._MEIPASS  # sys._MEIPASS在一些编辑器中会报错，不用理会
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class TurtleDrawingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.version = 'v0.1'
        self.title = "乘法计算过程动画演示"
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 400, 200)
        self.setWindowIcon(QIcon(resource_path('xlogo.ico')))

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_drawing)

        self._min_input = 10
        self._max_input = 9999
        self.title_label = QLabel(f"欢迎使用{self.title}程序！", self)
        self.input_label1 = QLabel(f"请输入第一个整数（{self._min_input} ~ {self._max_input}）：", self)
        self.input_label2 = QLabel(f"请输入第二个整数（{self._min_input} ~ {self._max_input}）：", self)

        self.input_edit1 = QLineEdit(self)
        self.input_edit2 = QLineEdit(self)

        self.random_button = QPushButton("随机两个数字", self)
        self.start_button = QPushButton("开始计算", self)

        # 添加菜单栏
        self.menubar = QMenuBar(self)

        layout = QVBoxLayout()
        layout.addWidget(self.menubar)
        layout.addWidget(self.title_label)
        layout.addWidget(self.input_label1)
        layout.addWidget(self.input_edit1)
        layout.addWidget(self.input_label2)
        layout.addWidget(self.input_edit2)
        layout.addWidget(self.random_button)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        self.random_button.clicked.connect(self.random_numbers)
        self.start_button.clicked.connect(self.start_drawing)

        self.is_drawing = False
        self.drawing_worker = None

        help_menu = self.menubar.addMenu('帮助')
        # 添加关于菜单项
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.showAboutDialog)
        help_menu.addAction(about_action)

        link = QAction('作者博客', self)
        link.triggered.connect(self.openLink)
        help_menu.addAction(link)

        wechat = QAction('公众号', self)
        wechat.triggered.connect(self.openWechat)
        help_menu.addAction(wechat)

    def openWechat(self):
        img_dialog = QDialog(self)
        img_dialog.setWindowTitle("热烈欢迎关注作者公众号！")
        img_dialog.resize(280, 280)
        img_dialog.move(self.width() // 2, self.height() // 2)
        img_dialog.setWindowFlags(img_dialog.windowFlags())
        lbl = QLabel(img_dialog)
        lbl.setPixmap(QPixmap(resource_path("qrcode_for_michael.jpg")))
        img_dialog.exec_()

    # 打开链接的方法
    def openLink(self):
        QDesktopServices.openUrl(QUrl('https://michael.blog.csdn.net/'))

    def showAboutDialog(self):
        about_text = f"""
        {self.title_label}
        版本: {self.version}
        作者: Michael阿明
        网址: https://michael.blog.csdn.net
        """

        QMessageBox.about(self, '关于', about_text)

    def random_numbers(self):
        self.input_edit1.setText(str(random.randint(self._min_input, self._max_input)))
        self.input_edit2.setText(str(random.randint(self._min_input, self._max_input)))

    def start_drawing(self):
        if not self.is_drawing:
            self.num1 = self.validate_input(self.input_edit1.text(), self._min_input, self._max_input)
            self.num2 = self.validate_input(self.input_edit2.text(), self._min_input, self._max_input)
            if not self.num1 or not self.num2:
                return
            self.is_drawing = True
            self.start_button.setEnabled(False)  # 禁用开始绘图按钮

            self.update_timer.start(100)  # Adjust the interval as needed

    def update_drawing(self):
        self.update_timer.stop()
        try:
            show_multiple(self.num1, self.num2, 100, 100, 100, 0)
        except Exception as e:
            print(e)
        gc.collect()
        self.drawing_finished()

    def drawing_finished(self):
        self.is_drawing = False
        self.start_button.setEnabled(True)  # 启用开始绘图按钮

    def validate_input(self, text, min_val, max_val):
        try:
            num = int(text)
            if min_val <= num <= max_val:
                return num
            else:
                QMessageBox.warning(self, "输入错误", f"请输入{min_val} ~ {max_val}之间的整数！")
                return None
        except ValueError:
            try:
                float_num = float(text)
                QMessageBox.warning(self, "输入错误", "请输入整数！")
                return None
            except ValueError:
                QMessageBox.warning(self, "输入错误", "请输入有效的整数！")
                return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TurtleDrawingApp()
    window.show()
    sys.exit(app.exec_())
