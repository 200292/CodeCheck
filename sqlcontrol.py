import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QPushButton, QTextBrowser, QInputDialog
from sqlconnect import SQLCONNECT


class App(QWidget):
    def __init__(self, filename):
        super().__init__()
        self.sqlconnect = SQLCONNECT()
        self.initUI()
        self.filename = filename

    def initUI(self):
        self.setWindowTitle("风险函数管理")
        self.showMaximized()  # 设置窗口全屏
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 显示结果的文本框
        self.result_text = QTextBrowser()
        main_layout.addWidget(self.result_text)

        # 选择操作的按钮
        button_group = QGroupBox("选择操作")
        button_group_layout = QVBoxLayout()
        button_group.setLayout(button_group_layout)
        main_layout.addWidget(button_group)

        show_button = QPushButton("显示所有风险函数")
        show_button.clicked.connect(self.show_data)
        button_group_layout.addWidget(show_button)

        search_button = QPushButton("在.c文件中搜索风险函数")
        search_button.clicked.connect(self.search_and_match)
        button_group_layout.addWidget(search_button)

        add_button = QPushButton("添加风险函数")
        add_button.clicked.connect(self.add)
        button_group_layout.addWidget(add_button)

        delete_button = QPushButton("删除风险函数")
        delete_button.clicked.connect(self.delete)
        button_group_layout.addWidget(delete_button)

        modify_button = QPushButton("修改风险函数")
        modify_button.clicked.connect(self.modify)
        button_group_layout.addWidget(modify_button)

        search_file_button = QPushButton("在.c文件中搜索函数")
        search_file_button.clicked.connect(self.regex_search)
        button_group_layout.addWidget(search_file_button)

        exit_button = QPushButton("退出")
        exit_button.clicked.connect(self.exit_program)
        button_group_layout.addWidget(exit_button)

    def show_data(self):
        self.result_text.clear()
        self.sqlconnect.cur.execute("SELECT * FROM functions")
        data = self.sqlconnect.cur.fetchall()
        for row in data:
            self.result_text.append(str(row))

    def search_and_match(self):
        #
        # self.result_text.clear()
        # filename, ok = QInputDialog.getText(self, '文件名', '请输入要搜索的 .c 文件名:')
        # if ok:
        #     try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    risk_functions = ["realpath", "scanf", "snprintf", "sprintf", "sscanf", "strcadd", "strcat",
                                      "strccpy", "strcpy", "streadd", "strecpy", "strncpy", "strtrns", "syslog",
                                      "vfscanf", "vscanf", "vsnprintf", "vsprintf", "vsscanf"]  # 使用你的风险函数列表
                    matched_functions = []  # 存储匹配到的风险函数
                    for risk_function in risk_functions:
                        regex = rf'\b{risk_function}\b'
                        match = re.search(regex, content)
                        if match:
                            matched_functions.append(risk_function)
                            sql = "SELECT func_name, level, suggestion FROM functions WHERE func_name = %s"
                            self.sqlconnect.cur.execute(sql, (risk_function,))
                            data = self.sqlconnect.cur.fetchall()
                            self.result_text.append(f"风险函数: {risk_function}")
                            for row in data:
                                self.result_text.append(str(row))
                    if not matched_functions:
                        self.result_text.append("该C代码不存在风险函数。")
                    else:
                        self.result_text.append(f"共匹配到 {len(matched_functions)} 个风险函数。")
            # except FileNotFoundError:
            #     self.result_text.append("文件未找到。")

    def add(self):
        self.result_text.clear()
        func_name, ok = QInputDialog.getText(self, '函数名称', '请输入函数名称:')
        if ok:
            self.sqlconnect.cur.execute("SELECT COUNT(*) FROM functions WHERE func_name = %s", (func_name,))
            count = self.sqlconnect.cur.fetchone()[0]
            if count > 0:
                self.result_text.append("函数名称已存在，请输入其他名称。")
                return
            level, ok = QInputDialog.getText(self, '函数风险等级', '请输入函数风险等级:')
            suggestion, ok = QInputDialog.getText(self, '函数建议', '请输入函数建议:')

            sql = 'INSERT INTO functions (func_name, level, suggestion) VALUES (%s, %s, %s)'
            val = (func_name, level, suggestion)
            self.sqlconnect.cur.execute(sql, val)
            self.sqlconnect.dbconn.commit()
            self.result_text.append("风险函数添加成功。")

    def delete(self):
        self.result_text.clear()
        func_name, ok = QInputDialog.getText(self, '函数名称', '请输入要删除的函数名称:')
        if ok:
            self.sqlconnect.cur.execute("SELECT COUNT(*) FROM functions WHERE func_name = %s", (func_name,))
            count = self.sqlconnect.cur.fetchone()[0]
            if count == 0:
                self.result_text.append("函数名称不存在。")
                return
            sql = "DELETE FROM functions WHERE func_name = %s"
            self.sqlconnect.cur.execute(sql, (func_name,))
            self.sqlconnect.dbconn.commit()
            self.result_text.append("风险函数删除成功。")

    def modify(self):
        self.result_text.clear()
        func_name, ok = QInputDialog.getText(self, '函数名称', '请输入要修改的函数名称:')
        if ok:
            self.sqlconnect.cur.execute("SELECT COUNT(*) FROM functions WHERE func_name = %s", (func_name,))
            count = self.sqlconnect.cur.fetchone()[0]
            if count == 0:
                self.result_text.append("函数名称不存在。")
                return
            level, ok = QInputDialog.getText(self, '函数风险等级', '请输入新的函数风险等级:')
            suggestion, ok = QInputDialog.getText(self, '函数建议', '请输入新的函数建议:')
            sql = "UPDATE functions SET level = %s, suggestion = %s WHERE func_name = %s"
            val = (level, suggestion, func_name)
            self.sqlconnect.cur.execute(sql, val)
            self.sqlconnect.dbconn.commit()
            self.result_text.append("风险函数修改成功。")

    def regex_search(self):
        # self.result_text.clear()
        # filename, ok = QInputDialog.getText(self, '文件名', '请输入要搜索的 .c 文件名:')
        # if ok:
            with open(self.filename, "r") as file:
                content = file.readlines()
            function_name, ok = QInputDialog.getText(self, '函数名', '请输入要搜索的函数名:')
            if ok:
                function_start = None
                function_end = None
                for i, line in enumerate(content, start=1):
                    match = re.search(r"\b" + re.escape(function_name) + r"\b", line)
                    if match:
                        function_start = (i, match.start() + 1)
                        break
                if function_start:
                    brace_count = 0
                    for i in range(function_start[0] - 1, len(content)):
                        line = content[i]
                        brace_count += line.count("{") - line.count("}")
                        if brace_count == 0:
                            function_end = (i + 1, len(line))
                            break
                if function_start and function_end:
                    self.result_text.append(
                        f"在文件中找到函数 {function_name}，起始位置：第 {function_start[0]} 行，第 {function_start[1]} 个字符；结束位置：第 {function_end[0]} 行，第 {function_end[1]} 个字符")
                else:
                    self.result_text.append(f"未在文件中找到函数 {function_name}")

    def exit_program(self):
        sys.exit(0)

    def closeEvent(self, event):
        self.sqlconnect.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
