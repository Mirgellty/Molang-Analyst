# -*- coding: utf-8 -*-
# @Time    : 2023/9/25 22:03
# @Author  : Emli / Mirgellty / deepseek / copilot
# @File    : uiloader.py
# @Software: VScode
from analyser import analyse,find_matching_parentheses,split_arguments,parse_expression
import sys
from PySide6.QtCore import QFile, QIODevice, Slot, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QPushButton,
    QWidget, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, QTextEdit
)
from PySide6.QtGui import QGuiApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("ui.ui")
        if not ui_file.open(QIODevice.ReadOnly):
            print("无法打开UI文件")
            sys.exit(-1)

        
        self.items = []
        self.functions = {}
        self.window = loader.load(ui_file)

        self.add_button = self.window.findChild(QPushButton, "add_button")
        self.add_button.clicked.connect(self.add_item)

        #self.test_button = self.window.findChild(QPushButton, "test_button")
        #self.test_button.clicked.connect(self.test_method)

        self.translate_button = self.window.findChild(QPushButton, "translate_button")
        self.translate_button.clicked.connect(self.translate_method)

        self.copy_button = self.window.findChild(QPushButton, "copy_button")
        self.copy_button.clicked.connect(self.copy_method)

        self.function_name = self.window.findChild(QTextEdit, "function_name")

        ui_file.close()

        scroll_area = self.window.findChild(QWidget, "scrollAreaWidgetContents_3")
        scroll_area.layout().setAlignment(Qt.AlignTop) 

    
    #@Slot()
    #def test_method(self):
        # print(self.functions)
        # analyse("f.1aa(a, f.2(b, c)) + f.3(d, e)", self.functions)

    
    @Slot()
    def copy_method(self):
        print("Copied.")
        translated_context = self.window.findChild(QTextEdit, "translated_context")
        QGuiApplication.clipboard().setText(translated_context.toPlainText())

    @Slot()
    def translate_method(self):
        translate_context = self.window.findChild(QTextEdit, "translate_context")
        translated_context = self.window.findChild(QTextEdit, "translated_context")
        text = analyse(translate_context.toPlainText(), self.functions)
        translated_context.setPlainText(text)

    @Slot()
    def on_add_button_clicked(self):
        print("Add button clicked")

    @Slot()
    def remove_item(self, widget_to_remove):
        scroll_area = self.window.findChild(QWidget, "scrollAreaWidgetContents_3")
        scroll_layout = scroll_area.layout()
        if widget_to_remove in self.items:
            scroll_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
            label = widget_to_remove.findChild(QLabel)
            if label:
                fname = label.text()
                print(fname)
                if fname in self.functions:
                    del self.functions[fname]
    
    @Slot()
    def add_item(self):
        add_fname = str(self.function_name.toPlainText())
        if not f"f.{add_fname}" in self.functions and add_fname != "":
            layoutWidget = QWidget()
            layoutWidget_layout = QHBoxLayout(layoutWidget)
            layoutWidget_layout.setContentsMargins(3, 3, 3, 3)
            layoutWidget_layout.setSpacing(5)

            label = QLabel(f"f.{add_fname}")

            text_edit = QLineEdit()
            text_edit.setMaximumHeight(25)
            self.functions[f"f.{add_fname}"] = text_edit.text()

            text_edit.textChanged.connect(lambda: self.functions.update({f"f.{add_fname}": text_edit.text()}))

            delete_button = QPushButton("删除")
            delete_button.setFixedSize(60, 25)

            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            layoutWidget_layout.addWidget(label)
            layoutWidget_layout.addWidget(text_edit)
            layoutWidget_layout.addWidget(delete_button)

            scroll_area = self.window.findChild(QWidget, "scrollAreaWidgetContents_3")
            scroll_layout = scroll_area.layout()
            if scroll_layout is None or not isinstance(scroll_layout, QVBoxLayout):
                scroll_layout = QVBoxLayout(scroll_area)
                scroll_area.setLayout(scroll_layout)
            scroll_layout.setAlignment(Qt.AlignTop) 
            scroll_layout.addWidget(layoutWidget)

            self.items.append(layoutWidget)

            delete_button.clicked.connect(lambda: self.remove_item(layoutWidget))
        else:
            print("警告:", "函数名已存在或为空！")




if __name__ == "__main__":
    
    app = QApplication([])
    main_window = MainWindow()
    main_window.window.show()
    translated_context = main_window.window.findChild(QTextEdit, "translated_context")
    translated_context.setPlainText('左上角输入函数名点击\'+\'新增函数，不能重复或为空。\n变量以{x}和{y}键入。原始表达式处相关函数格式为f.xxx(a,b)，必须有两个变量。\n函数默认为二元，若需要一元函数，不引用{y}，原始表达式f.xxx函数第二个变量随便填即可。\n不要出现未在左侧定义的f.函数。\n点击translate解析表达式，该段文本自动消失。')
    app.exec()
