import string

from AnalyCode import get_node
from tree_sitter import Node

class GlobalData:
    __instance = None

    @staticmethod
    def get_instance():
        if not GlobalData.__instance:
            GlobalData()
        return GlobalData.__instance

    def __init__(self):
        if GlobalData.__instance:
            raise Exception("This class is a singleton!")
        else:
            GlobalData.__instance = self

        self.def_func = {} #存储定义的函数
        self.inv_func = {}  #存储程序项目调用函数
        self.orig_data = {}  # 存储程序项目源文件
        self.other_data = {}  # 存储程序项目库文件或其他文件
        self.currentvar = []  #

    def add_orig_node(self, file_path):
        node = get_node(file_path)
        self.orig_data[file_path] = node
    def add_other_node(self, file_path):
        node = get_node(file_path)
        self.other_data[file_path] = node
    def get_node(self, file_path) -> Node:
        if self.orig_data.get(file_path) != None:
            return self.orig_data.get(file_path)
        else:
            if self.other_data.get(file_path) != None:
                return self.other_data.get(file_path)
            else:
                self.add_other_node(file_path)
                return self.other_data.get(file_path)
    def clean_data(self):
        self.orig_data.clear()
        self.other_data.clear()
        self.currentvar.clear()
        self.def_func.clear()
        self.inv_func.clear()
    def add_def_func(self, path, list):
        if self.def_func.get(path) == None:
            self.def_func[path] = list
    def add_inv_func(self, path, list):
        if self.inv_func.get(path) == None:
            self.inv_func[path] = list
    def add_currentvar(self, dirc):
        self.currentvar.append(dirc)
    def ret_varaera(self, ln ,col): #确定定义变量作用域 返回
        for dir in self.currentvar:
            begin = dir['begin']
            end = dir['end']
            if ln > begin[0] and ln < end[0]:
                var = dir['var'] #返回定义函数字典
                return var
            elif ln == begin[0] and col > begin[1]:
                var = dir['var'] #返回定义函数字典
                return var
            elif ln == end[0] and col < end[1]:
                var = dir['var'] #返回定义函数字典
                return var

        return None

