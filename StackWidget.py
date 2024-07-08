import os
import re

from PyQt5 import uic
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileIconProvider, QTreeWidgetItem, QApplication, QListWidgetItem
from GlobalData import GlobalData
from Parse import Parse
StackedWidgetForm, StackedWidgetBase = uic.loadUiType("UI_StackedWidget.ui")

#表示文件或目录的视图组件，包含一个文件路径属性file_path。
class FileItem(QTreeWidgetItem):
    def __init__(self, parent, file_path):
        super().__init__(parent)
        self.file_path = file_path

class ConItem(QTreeWidgetItem):
    def __init__(self, parent, node):
        super().__init__(parent)
        self.node = node
class MyStackedWidget(StackedWidgetBase,StackedWidgetForm):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parse = Parse()
        self.global_data = GlobalData.get_instance()

    #用于初始化ast树。它通过给定的路径，遍历该路径下的文件和文件夹，在ast树中创建相应的节点
    def init_tree(self, path):
        #获取路径下的文件和文件夹
        dirs =  os.listdir(path)

        file_Info = QFileInfo(path)
        file_Icon = QFileIconProvider()
        icon = QIcon(file_Icon.icon(file_Info))
        #dir_tree是展示文件夹的树结构的组件
        root = FileItem(self.dir_tree, path)
        root.setText(0, path.split('/')[-1])
        root.setIcon(0, QIcon(icon))
        self._create_tree(dirs, root, path)
        QApplication.processEvents()

    #该函数用于创建一个树结构，表示给定路径下的文件夹和文件
    def _create_tree(self, dirs, root, path):
        for i in dirs:
            path_new = path + '/' + i
            if os.path.isdir(path_new):
                fileInfo = QFileInfo(path_new)
                fileIcon = QFileIconProvider()
                icon = QIcon(fileIcon.icon(fileInfo))
                child = FileItem(root, path_new)
                child.setText(0, i)
                child.setIcon(0, QIcon(icon))

                dirs_new = os.listdir(path_new)
                self._create_tree(dirs_new, child, path_new)
            else:
                fileInfo = QFileInfo(path_new)
                fileIcon = QFileIconProvider()
                icon = QIcon(fileIcon.icon(fileInfo))
                child = FileItem(root, path_new)
                child.setText(0, i)
                child.setIcon(0, QIcon(icon))

                file_name, file_ext = os.path.splitext(i)
                if file_ext in {'.c', '.h'}:
                    self.global_data.add_orig_node(path_new)
    def get_item_path(self, item):
        if isinstance(item, FileItem):
            return item.file_path
    def get_item_node(self, item):
        if isinstance(item, ConItem):
            return item.node
    def init_con(self, file_path):
        self.global_data.currentvar.clear()
        for fun_node in self.global_data.def_func[file_path]:
            name, parameters, return_type = self.parse.funcdef_parse(fun_node)
            all_var = {}

            if parameters:
                paras = ' '.join(map(str, parameters))
            else:
                paras = '()'

            text = return_type + ' ' + name + ' ' + paras
            root = ConItem(self.con_tree, fun_node)
            root.setText(0, text)

            list = self.parse.scan_defvar(fun_node)

            var_list = {}

            if list!= None:
                for var_node in list:
                    text = var_node.text.decode('utf-8')
                    new_text = re.sub(r'[=;].*', '', text)

                    last_space_index = text.rfind(' ')
                    #
                    # if last_space_index != -1:
                    #     # 使用切片将字符串分为两部分
                    #     part1 = new_text[:last_space_index]
                    #     part2 = new_text[last_space_index + 1:]
                    # else:
                    #     # 如果找不到空格，则将整个字符串作为第一部分
                    #     part1 = new_text
                    #     part2 = ''
                    #
                    # string = re.sub(r'\[.*?\]', '', part2)
                    # string = re.sub(r'[*&]', '', string)
                    # new_text = self.extract_variable_name(text)
                    var_list[new_text] = var_node

                    child = ConItem(root, var_node)
                    child.setText(0, new_text)


            all_var['begin'] = fun_node.start_point
            all_var['var'] = var_list
            all_var['end'] = fun_node.end_point

            self.global_data.add_currentvar(all_var)

            print(all_var)

    def extract_variable_name(self, string):
        pattern = r"[\w\[\];*=]+"
        match = re.search(pattern, string)
        if match:
            return match.group()
        else:
            return None










