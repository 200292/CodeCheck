import pymysql


class SQLCONNECT:
    def __init__(self):
        self.dbconn = pymysql.connect(
            host="localhost",
            database="riskfunction",
            user="root",
            password="l518020",
            port=3306,
        )

        self.cur = self.dbconn.cursor()

#     def show_data(self):
#         sql = "SELECT * FROM functions"
#         self.cur.execute(sql)
#         data = self.cur.fetchall()
#         for row in data:
#             print(row)
#
#     def search_and_match(self):
#         filename = input("请输入要搜索的 .c 文件名: ")
#         try:
#             with open(filename, 'r') as file:
#                 content = file.read()
#                 risk_functions = ["realpath", "scanf", "snprintf", "sprintf", "sscanf", "strcadd", "strcat",
#                                   "strccpy", "strcpy", "streadd", "strecpy", "strncpy", "strtrns", "syslog",
#                                   "vfscanf", "vscanf", "vsnprintf", "vsprintf", "vsscanf"]
#                 # 遍历函数列表，匹配与文件中的函数
#                 for risk_function in risk_functions:
#                     # 构建匹配函数的正则表达式
#                     regex = rf'\b{risk_function}\b'
#                     # 使用正则表达式搜索匹配
#                     match = re.search(regex, content)
#                     # 如果找到匹配则执行数据库查询
#                     if match:
#                         # 查询数据库表中的函数
#                         self.cur.execute("SELECT func_name FROM functions WHERE func_name=%s", (risk_function,))
#                         result = self.cur.fetchone()
#                         # 如果结果存在则输出匹配的函数及对应的数据库列
#                         if result:
#                             print("风险函数: ", risk_function)
#                             sql = "SELECT func_name, level, suggestion FROM functions WHERE func_name = %s"
#                             self.cur.execute(sql, (risk_function,))
#                             data = self.cur.fetchall()
#                             print(data)
#                         else:
#                             print("该C代码不存在风险函数。")
#         except FileNotFoundError:
#             print("文件未找到。")
#
#     def add(self):
#         func_name = input("请输入函数名称: ")
#         level = input("请输入函数风险等级: ")
#         suggestion = input("请输入函数建议: ")
#
#         # Check if func_name already exists
#         check_sql = "SELECT COUNT(*) FROM functions WHERE func_name = %s"
#         self.cur.execute(check_sql, (func_name,))
#         count = self.cur.fetchone()[0]
#         if count > 0:
#             print("函数名称已存在，请输入其他名称。\n")
#             return
#
#         sql = 'INSERT INTO functions (func_name, level, suggestion) VALUES (%s, %s, %s)'
#         val = (func_name, level, suggestion)
#         self.cur.execute(sql, val)
#         self.dbconn.commit()
#         print("风险函数添加成功。")
#
#     def delete(self):
#         func_name = input("请输入要删除的函数名称: ")
#
#         # Check if func_name exists
#         check_sql = "SELECT COUNT(*) FROM functions WHERE func_name = %s"
#         self.cur.execute(check_sql, (func_name,))
#         count = self.cur.fetchone()[0]
#         if count == 0:
#             print("函数名称不存在。\n")
#             return
#
#         sql = "DELETE FROM functions WHERE func_name = %s"
#         self.cur.execute(sql, (func_name,))
#         self.dbconn.commit()
#         print("风险函数删除成功。")
#
#     def modify(self):
#         func_name = input("请输入要修改的函数名称: ")
#
#         # Check if func_name exists
#         check_sql = "SELECT COUNT(*) FROM functions WHERE func_name = %s"
#         self.cur.execute(check_sql, (func_name,))
#         count = self.cur.fetchone()[0]
#         if count == 0:
#             print("函数名称不存在。\n")
#             return
#
#         level = input("请输入新的函数风险等级: ")
#         suggestion = input("请输入新的函数建议: ")
#
#         sql = "UPDATE functions SET level = %s, suggestion = %s WHERE func_name = %s"
#         val = (level, suggestion, func_name)
#         self.cur.execute(sql, val)
#         self.dbconn.commit()
#         print("风险函数修改成功。")
#
#     def close(self):
#         self.cur.close()
#         self.dbconn.close()
#
#     def regex_search(self):
#         filename = input("请输入要搜索的 .c 文件名: ")
#
#         with open(filename, "r") as file:
#             content = file.readlines()
#
#         function_name = input("请输入要搜索的函数名：")
#
#         function_start = None
#         function_end = None
#
#         # 遍历每一行的内容
#         for i, line in enumerate(content, start=1):
#             # 使用正则表达式从行中匹配函数名
#             match = re.search(r"\b" + re.escape(function_name) + r"\b", line)
#             if match:
#                 function_start = (i, match.start() + 1)
#                 break
#
#         if function_start:
#             brace_count = 0
#             for i in range(function_start[0] - 1, len(content)):
#                 line = content[i]
#                 brace_count += line.count("{") - line.count("}")
#                 if brace_count == 0:
#                     function_end = (i + 1, len(line))
#                     break
#
#         if function_start and function_end:
#             print(
#                 f"在文件中找到函数 {function_name}，起始位置：第 {function_start[0]} 行，第 {function_start[1]} 个字符；结束位置：第 {function_end[0]} 行，第 {function_end[1]} 个字符")
#         else:
#             print(f"未在文件中找到函数 {function_name}")
#
#
# def main():
#     sql_control = SQLCONTROL()
#
#     while True:
#         print("1. 显示所有风险函数")
#         print("2. 查找.c文件中的风险函数")
#         print("3. 添加风险函数")
#         print("4. 删除风险函数")
#         print("5. 修改风险函数")
#         print("6. 在.c文件中搜索函数")
#         print("7. 退出")
#
#         choice = input("请输入您的选择: ")
#
#         if choice == '1':
#             sql_control.show_data()
#         elif choice == '2':
#             sql_control.search_and_match()
#         elif choice == '3':
#             sql_control.add()
#         elif choice == '4':
#             sql_control.delete()
#         elif choice == '5':
#             sql_control.modify()
#         elif choice == '6':
#             sql_control.regex_search()
#         elif choice == '7':
#             break
#         else:
#             print("无效选择，请重试。\n")
#
#
# if __name__ == "__main__":
#     main()
