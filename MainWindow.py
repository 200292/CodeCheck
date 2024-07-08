import os

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
from Parse import Parse
from GlobalData import GlobalData
from RiskFunctionAnalysis import RiskFunctionAnalysis
from StackWidget import MyStackedWidget
from CodeWidget import MyCodeWidget
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QSplitter, QTabWidget, QHBoxLayout, QSizePolicy, QApplication
from sqlcontrol import App
from InfoWidget import MyInfoWidget

MainWindowForm, MainWindowBase  = uic.loadUiType("./UI_MainWindow.ui")

class MyWindow(MainWindowBase, MainWindowForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()
        self.parse = Parse()
        self.currentfile = None

        #打开文件按钮,会调用load_file函数
        self.actionOpen.triggered.connect(self.load_file)
        self.actionSQL.triggered.connect(self.load_sqlwidget)
        #生成报告按钮
        self.actionRep.triggered.connect(self.make_report)
        self.code_widget.currentChanged.connect(self.rebuild_con)
        self.dir_but.clicked.connect(self.load_dir)
        self.con_but.clicked.connect(self.load_con)
        self.stack_widget.currentChanged.connect(self.change_but)
        self.stack_widget.dir_tree.itemClicked.connect(self.file_clicked)
        self.stack_widget.con_tree.itemClicked.connect(self.con_clicked)
        self.info_widget.itemlist.itemClicked.connect(self.info_clicked)
        self.global_data = GlobalData.get_instance()
        self.code_widget.child_data_signal.connect(self.handle_child_data)
        self.code_widget.invoke_data_signal.connect(self.invoke_child_data)

    def init_ui(self):
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        self.stack_widget = MyStackedWidget(self)
        self.code_widget = MyCodeWidget(self)
        self.info_widget = MyInfoWidget(self)

        self.hor_splitter = QSplitter(self)
        self.hor_splitter.setHandleWidth(0)
        self.hor_splitter.addWidget(self.stack_widget)
        self.hor_splitter.addWidget(self.code_widget)
        self.hor_splitter.setSizes([1600, 10000])

        self.ver_splitter = QSplitter(self)
        self.ver_splitter.setOrientation(Qt.Vertical)
        self.ver_splitter.setHandleWidth(0)
        self.ver_splitter.addWidget(self.hor_splitter)
        self.ver_splitter.addWidget(self.info_widget)
        self.ver_splitter.setSizes([10000, 0])

        hbox.addWidget(self.ver_splitter)
        self.content_frame.setLayout(hbox)
    def load_file(self):
        # 使用QtWidgets模块中的QFileDialog.getExistingDirectory函数弹出一个文件夹选择对话框，
        # 允许用户选择一个现有的目录。初始显示的目录路径为"C:/Users/liudingyu/Desktop/"。
        # 若用户成功选择了目录，将路径赋值给变量path；否则，path保持为None。
        if path := QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/Users/liudingyu/Desktop/"):# 起始路径
            self.stack_widget.dir_tree.clear()
            self.global_data.clean_data()
            self.code_widget.init_widgets.clear()
            self.code_widget.clear()
            self.info_widget.itemlist.clear()

            self.hor_splitter.setSizes([1600, 10000])
            #针对路径遍历该路径下的文件和文件夹,生成ast树以及展示目录结构
            self.stack_widget.init_tree(path)

            self.code_widget.init_widget()
            self.parse.scan_project()
    def load_dir(self):
        self.stack_widget.setCurrentIndex(0)
        if self.hor_splitter.isCollapsible(0):
            self.hor_splitter.setSizes([1600,10000])
    def load_con(self):
        self.stack_widget.setCurrentIndex(1)

        if self.hor_splitter.isCollapsible(0):
            self.hor_splitter.setSizes([1600, 10000])
    def change_but(self, index):
        if index == 0:
            self.dir_but.setStyleSheet("QPushButton"
                                   "{"
                                   "background-color : lightgreen"
                                   "}")
            self.con_but.setStyleSheet("QPushButton"
                                   "{"
                                   "background-color : transparent"
                                   "}")

        if index == 1:
            self.con_but.setStyleSheet("QPushButton"
                                       "{"
                                       "background-color : lightgreen"
                                       "}")
            self.dir_but.setStyleSheet("QPushButton"
                                       "{"
                                       "background-color : transparent"
                                       "}")
    def file_clicked(self, item, column):

        file_path = self.stack_widget.get_item_path(item)
        self.currentfile = file_path
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            file_name, file_ext = os.path.splitext(file_name)
            if file_ext in {'.c', '.h'}:
                self.code_widget.show_codewidget(file_path)
    def con_clicked(self, item, column):
        node = self.stack_widget.get_item_node(item)
        self.code_widget.set_position(node.start_point)

    def info_clicked(self, item):
        node = self.info_widget.get_item_node(item)
        self.code_widget.set_position(node.start_point)
    def load_sqlwidget(self):
        self.ex = App(self.currentfile)
        self.ex.show()
    def make_report(self):
        list = self.parse.func_check()
        risk = RiskFunctionAnalysis(list)
        risk.Generatereport()
    def rebuild_con(self):
        self.stack_widget.con_tree.clear()
        self.info_widget.itemlist.clear()
        index = self.code_widget.currentIndex()
        if index != -1:
            file_path = self.code_widget.tabText(self.code_widget.currentIndex())
            self.stack_widget.init_con(file_path)

    def handle_child_data(self, selected_text,start_line_column, start_column, file_path):
        self.parse.get_node(selected_text,start_line_column, start_column, file_path)
        deffunc = self.parse.funcdef_search(selected_text,file_path) #进行函数查找
        if deffunc != None:
            func = [deffunc]
            self.info_widget.init_list(func, 'FUNC')

        else:
            defvar = self.parse.vardef_search(selected_text,start_line_column,start_column)
            if defvar != None:
                var = [defvar]
                self.info_widget.init_list(var, 'VAR')

    def invoke_child_data(self, selected_text,start_line_column, start_column, file_path):
        self.parse.get_node(selected_text, start_line_column, start_column, file_path)
        deffunc = self.parse.funcdef_search(selected_text, file_path)  # 进行函数查找

        list =  self.parse.funcinv_search(selected_text, file_path)
        if list != None:
            func = [deffunc]
            self.info_widget.init_list(func, 'FUNC')

        else:
            defvar = self.parse.varinv_search(selected_text, start_line_column, start_column)
            if defvar != None:
                var = [defvar]
                self.info_widget.init_list(var, 'VAR')


