from PyQt5 import uic
from PyQt5.QtWidgets import QListWidgetItem
from Parse import Parse
CodeWidgetForm, CodeWidgetBase = uic.loadUiType("UI_InfoWidget.ui")

class InfoItem(QListWidgetItem):
    def __init__(self, node):
        super().__init__()
        self.node = node
class MyInfoWidget(CodeWidgetBase,CodeWidgetForm):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parse = Parse()

    def init_list(self, list, type):
        for dirt in list:
            for key, value in dirt.items():
                item = InfoItem(value)
                line = value.start_point[0]
                col = value.start_point[1]
                pos = "<" + str(line) +","+ str(col) +">"

                if type == 'FUNC':
                    name, parameters, return_type = self.parse.funcdef_parse(value)

                    if parameters:
                        paras = ' '.join(map(str, parameters))
                    else:
                        paras = '()'

                    text = return_type + ' ' + name + ' ' + paras

                elif type == 'VAR':
                    text = value.text.decode('utf-8')

                item.setText(text + pos)
                self.itemlist.addItem(item)

    def get_item_node(self, item):
        if isinstance(item, InfoItem):
            return item.node



