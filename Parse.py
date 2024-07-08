from GlobalData import GlobalData

class Parse():
    def __init__(self):
        self.global_data = GlobalData.get_instance()
    def scan_project(self): #对整个项目源文件经行扫描
        for path, node in self.global_data.orig_data.items():

            function_definitions = [] #函数定义表
            function_calls = [] #函数调用表

            self.scan_node(function_definitions, function_calls, node)
            if len(function_definitions) != 0:
                self.global_data.add_def_func(path, function_definitions)
            if len(function_calls) != 0:
                self.global_data.add_inv_func(path, function_calls)
    def scan_node(self, function_definitions, function_calls, node): #扫描递归的节点 将不同类型的节点添加到不同的数组
        if node.type == 'function_definition':

            function_definitions.append(node)

        elif node.type == 'call_expression':
            function_calls.append(node)

        for child in node.children:
            self.scan_node(function_definitions, function_calls, child)
    def func_check(self): #对整个项目源文件进行筛查 找到所有引用的库函数
        func = []
        for file, nodelist in self.global_data.inv_func.items():
            for inv_node in nodelist:
                checked = False
                invname, argus = self.funcinv_parse(inv_node)
                for def_node in self.global_data.def_func[file]:
                    defname, params, retype = self.funcdef_parse(def_node)

                    if invname == defname:
                        checked = True
                        break

                if checked == False:

                    lib_func = {}
                    lib_func['name'] = invname
                    lib_func['start'] = inv_node.start_point
                    lib_func['end'] = inv_node.end_point
                    lib_func['file'] = file

                    func.append(lib_func)

                    print(invname, file, inv_node.start_point, inv_node.end_point)
        print(func)
        return func
    def scan_defvar(self, node):
        def_var = []
        self.traverse_node(node, def_var)
        return def_var
    def traverse_node(self, node, def_var):
        # 处理当前节点
        if node.type in ("variable_declaration", "parameter_declaration", "declaration"):
            def_var.append(node)
        for child in node.children:
            self.traverse_node(child, def_var)
    def get_node(self, value, line, colum, file_path):
        for node in self.global_data.def_func[file_path]: #在对应原文件中查找
            if node.start_point[0] < line and node.start_point[1] < colum \
                    and node.end_point[0] > line and node.end_point[1] >colum:
                get_node = self.traverse_node(node, line, colum, value)
                if get_node:
                    print("Node Found: Type -", get_node.type, "Text -", get_node.text())
    def funcdef_search(self, tar_name, file_path): #查找函数定义

        for node in self.global_data.def_func[file_path]: #在对应原文件中查找函数
            name, parameters, return_type = self.funcdef_parse(node)

            if name == tar_name:
                dirt = {}
                dirt[name] = node
                return dirt
        return None
    def funcinv_search(self, tar_name, file_path):
        list = []
        for node in self.global_data.inv_func[file_path]:
            name, paralist = self.funcinv_parse(node)

            if name == tar_name:
                list.append(node)
        return list
    def funcinv_parse(self, node):
        function_name = ""
        arguments = []

        for i in range(node.child_count):
            child_node = node.children[i]

            if child_node.type == "identifier":
                function_name = child_node.text.decode('utf-8')

            if child_node.type == "argument_list":
                for j in range(child_node.child_count):
                    argument_node = child_node.children[j]
                    if argument_node.type == "identifier":
                        arguments.append(argument_node.text.decode('utf-8'))

        return function_name, arguments
    def funcdef_parse(self, node):

        return_type_node = node.children[0]
        name_node = node.children[1].children[0]
        parameter_node = node.children[1].children[1]

        name = name_node.text.decode('utf-8') if name_node else ""
        parameters = [child.text.decode('utf-8') for child in parameter_node.children] if parameter_node else []
        return_type = return_type_node.text.decode('utf-8') if return_type_node else ""

        return name, parameters, return_type

    def vardef_parse(self, node):
        variables = {}
        type = []
        name = None
        self.varpas_node(node, type)

        paras = ' '.join(map(str, type))
        variables[paras] = name
        return variables
    def varpas_node(self, node, type):
        if node.type == "identifier":
            name = node.text.decode('utf-8')
            return

        else:
            if node.children == None:
                type.append(node.text.decode('utf-8'))

            else :
                for child in node.children:
                    self.varpas_node(child, type)
    def vardef_search(self, tar_name, ln, col):
        var_dict = self.global_data.ret_varaera(ln, col)
        if var_dict != None:
            for key, value in var_dict.items():
                if tar_name == key:
                    dirt = {}
                    dirt[key] = value
                    return dirt

        return None
    def varinv_search(self, tar_name, ln, col, file_path):
        list = []
        for node in self.global_data.inv_func[file_path]:
            if ln > node.start_point[0] and col > node.start_point[1] and \
                    ln < node.start_point[0] and col < node.start_point[1]:
                self.traverse_node_varinv(node, tar_name, list)
                return list
        return None
    def traverse_node_varinv(self, node, name, list):
        # 处理当前节点
        if node.type == 'name' and node.parent.type == 'assignment':
            if node.text.enconde('utf-8') == name:
                list.append({node.parent.text.enconde('utf-8'):node})
        for child in node.children:
            self.traverse_node(child, name, list)








