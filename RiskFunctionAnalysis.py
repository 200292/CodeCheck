import os

import pymysql
from collections import Counter
import matplotlib.pyplot as plt


def Pie(datas_method, datas_level):
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    pie = plt.figure(figsize=(8, 8))
    pie_name = pie.add_subplot(2, 1, 1)
    pie_level = pie.add_subplot(2, 1, 2)
    data_name = list(datas_method.values())
    labels_name = list(datas_method.keys())
    data_level = list(datas_level.values())
    labels_level = list(datas_level.keys())
    plt.sca(pie_name)
    plt.title('风险函数', size=12)
    plt.pie(data_name, labels=labels_name, autopct='%1.2f%%')
    plt.legend(labels=data_name, loc='best', title="函数个数", fontsize=10, bbox_to_anchor=(1.1, 1.05),
               borderaxespad=0.3)
    plt.axis('equal')

    plt.sca(pie_level)
    plt.title('风险函数等级', size=12)
    plt.pie(data_level, labels=labels_level, autopct='%1.2f%%')
    plt.legend(labels=data_level, loc='best', title="函数个数", fontsize=10, bbox_to_anchor=(1.1, 1.05),
               borderaxespad=0.3)
    plt.axis('equal')

    plt.savefig('Risk Report.jpg')
    plt.close()



class RiskFunctionAnalysis:
    def __init__(self, list):
        self.method_list = list # 检测到的函数列表

        for dirc in list:
            dirc['name'] #函数名子 str
            dirc['file'] #文件路径 str
            dirc['start']  #该函数的开始索引 list [line, column]
            dirc['end'] #同上
    def Generatereport(self):
        if self.method_list:
            risk_method_list = []
            risk_method_level = []
            risk_method_advice = []
            dbconn = pymysql.connect(
                host="localhost",
                database="riskfunction",
                user="root",
                password="cyc24826...",  # 密码 需自行修改
                port=3306,
                charset='utf8'
            )

            cur = dbconn.cursor()
            for dirc in self.method_list:
                method_name = dirc['name']
                sql = "SELECT * FROM functions WHERE func_name = '" + method_name + "'"
                cur.execute(sql)
                data = cur.fetchall()
                if data:  # 如果检测到风险函数
                    risk_method_list.append(data[0][0])  # 将其添加到风险函数列表中
                    risk_method_level.append(data[0][1])  # 风险函数等级
                    risk_method_advice.append(data[0][2])
            datas_method = Counter(risk_method_list)  # 将风险函数列表按出现次数转换为字典
            datas_level = Counter(risk_method_level)
            datas_advice = dict(zip(risk_method_list, risk_method_advice))
            message = ""
            file_name = os.path.basename(dirc['file']) #获得文件名
            for name, advice in datas_advice.items():
                message +=  "在文件" + file_name + "中检测到风险函数：" + name +  "位于第" + str(dirc['start'][0] + 1) + "行" + ",第" + str(dirc['start'][1] + 1) + "列"
                message += "\n建议：" + advice + "\n"
            file = open("Report.txt", 'w')
            file.write(message)
            file.close()
            Pie(datas_method, datas_level)  # 转换为饼图
