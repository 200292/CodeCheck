from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

from CodeEditorWidget import CodeEditor
from GlobalData import GlobalData

CodeWidgetForm, CodeWidgetBase = uic.loadUiType("UI_CodeTabWidget.ui")

#
class MyCodeWidget(CodeWidgetBase,CodeWidgetForm):
    child_data_signal = pyqtSignal(str, int, int, str)
    invoke_data_signal = pyqtSignal(str, int, int, str)

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.global_data = GlobalData.get_instance()
        self.init_widgets = {}

        self.tabCloseRequested.connect(self.close_handler)
    def handle_sub_child_data(self, selected_text, start_line_column, start_column, file_path):
        self.child_data_signal.emit(selected_text,start_line_column, start_column, file_path)

    def handle_invoke_child_data(self, selected_text, start_line_column, start_column, file_path):
        self.invoke_data_signal.emit(selected_text,start_line_column, start_column, file_path)

    def init_widget(self):
        for file_path, node in self.global_data.orig_data.items():
            node = self.global_data.get_node(file_path)
            code_editor = CodeEditor(node, file_path)

            self.init_widgets[file_path] = code_editor

    def add_codewidget(self, file_path):
        node = self.global_data.get_node(file_path)
        code_editor = CodeEditor(node, file_path)

        self.init_widgets[file_path] = code_editor

    def show_codewidget(self, filepath):
        if self.count() == 0:
            if filepath in self.init_widgets:
                self.addTab(self.init_widgets[filepath], filepath)
                self.setCurrentIndex(self.count() - 1)

            else:
                self.add_codewidget(filepath)
                self.addTab(self.init_widgets[filepath], filepath)
                self.setCurrentIndex(self.count() - 1)


        elif filepath != self.tabText(self.currentIndex()):
            res = self.ensure_unique_tabs(filepath)

            if res != None:
                self.setCurrentIndex(res)

            else:
                if self.init_widgets[filepath] != None:
                    self.addTab(self.init_widgets[filepath], filepath)
                    self.setCurrentIndex(self.count() - 1)

                else:
                    self.add_codewidget(filepath)
                    self.addTab(self.init_widgets[filepath], filepath)
                    self.setCurrentIndex(self.count() - 1)

        else:
             pass

        self.currentWidget().sub_child_data_signal.connect(self.handle_sub_child_data)
        self.currentWidget().sub_invoke_data_signal.connect(self.handle_invoke_child_data)

    def set_position(self, pos):
        cursor = self.currentWidget().textCursor()
        cursor.movePosition(cursor.Start)
        cursor.movePosition(cursor.Down, cursor.MoveAnchor, n = pos[0])
        cursor.movePosition(cursor.Right, cursor.MoveAnchor, n = pos[1])
        self.currentWidget().setTextCursor(cursor)

    def ensure_unique_tabs(self, file_path):
                # 获取当前选项卡的数量
        tab_count = self.count()

        for i in range(tab_count):
            if file_path == self.tabText(i):
                return i
        return None

    def close_handler(self, index):
        self.removeTab(index)


