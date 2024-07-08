from PyQt5.QtCore import QRect, pyqtSignal
from PyQt5.QtGui import QFont, QTextFormat, QTextCharFormat, QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit, QMenu, QAction
from LineNumberArea import *
from tree_sitter import Node
from Parse import Parse

SYNTAX_COLORS = {
    'comment': QColor(0, 128, 0),     # 绿色
    'string': QColor(230, 57, 70),    # 红色
    'number': QColor(255, 165, 0),    # 橙色
    'keyword': QColor(0, 0, 255),     # 蓝色
    'type': QColor(176, 48, 96),      # 紫色
    'identifier': QColor(0, 0, 0),    # 黑色
}

class SyntaxHighlighter:
    def __init__(self, text_edit, document, root_node):
        self.document = document
        self.text_edit = text_edit
        self.format = QTextCharFormat()
        self.format.setForeground(QColor("#000000"))
        self.formats = {}
        self.node = root_node

    def create_format(self, color, style='Normal', weight='Normal'):
        char_format = QTextCharFormat()
        char_format.setForeground(color)
        char_format.setFontWeight(getattr(QFont, weight))
        char_format.setFontItalic(style == 'italic')
        return char_format

    def highlight_syntax(self, node, code_text):

        syntax_formats = {
            "function_definition": QColor("#800000"),  # 红色
            "preproc": QColor("#808080"),  # 灰色
            "comment": QColor("#008000"),  # 绿色
            # 可以继续添加其他语法元素的着色格式
        }
        if node.is_named:
            start_line, start_column = node.start_point
            end_line, end_column = node.end_point
            length = end_column - start_column

            if node.type in self.highlight_formats:
                format_style = self.highlight_formats[node.type]
                code_text.setFormat(start_column, length, format_style)

        for child in node.children:
            self.highlight_node(child, code_text)
class CodeEditor(QPlainTextEdit):
    sub_child_data_signal = pyqtSignal(str, int, int ,str)

    sub_invoke_data_signal = pyqtSignal(str, int, int, str)

    def __init__(self, root_node, file_path):
        super(CodeEditor, self).__init__()
        self.parse = Parse()
        self.file_path = file_path

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        self.setPlainText(content)

        self.setFont(QFont("Microsoft YaHei UI Light", 11))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.number_bar = LineNumberArea(self)
        self.highlighter = SyntaxHighlighter(self, self.document(), root_node)

        self.currentLineNumber = None
        self.currentLineColor = self.palette().alternateBase()
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.customContextMenuRequested.connect(self.show_context_menu)
        self.cursorPositionChanged.connect(self.highlight_current_line)

    def resizeEvent(self, *e):
        cr = self.contentsRect()
        rec = QRect(cr.left(), cr.top(), self.number_bar.get_width(), cr.height())
        self.number_bar.setGeometry(rec)

        QPlainTextEdit.resizeEvent(self, *e)

    def highlight_current_line(self):
        new_current_line_number = self.textCursor().blockNumber()
        if new_current_line_number != self.currentLineNumber:
            self.currentLineNumber = new_current_line_number
            hi_selection = QTextEdit.ExtraSelection()
            hi_selection.format.setBackground(self.currentLineColor)
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()
            self.setExtraSelections([hi_selection])

    def show_context_menu(self, event):
        context_menu = QMenu(self)

        copy_action = QAction("复制", self)
        define_action = QAction("查看定义", self)
        # invoke_action = QAction("查看引用", self)

        context_menu.addAction(copy_action)
        context_menu.addAction(define_action)
        # context_menu.addAction(invoke_action)

        selected_text = self.textCursor().selectedText()
        if selected_text:
            copy_action.setEnabled(True)
        else:
            copy_action.setEnabled(False)

        action = context_menu.exec_(self.mapToGlobal(event))

        if action == copy_action:
            self.copy()

        if action == define_action:
            cursor = self.textCursor()
            selected_text = cursor.selectedText()
            start_column = cursor.columnNumber()

            start_position = cursor.selectionStart()
            start_line_column = self.toPlainText().count("\n", 0, start_position)

            self.sub_child_data_signal.emit(selected_text,start_line_column, start_column, self.file_path)

        # if action == invoke_action:
        #     cursor = self.textCursor()
        #     selected_text = cursor.selectedText()
        #     start_column = cursor.columnNumber()
        #
        #     start_position = cursor.selectionStart()
        #     start_line_column = self.toPlainText().count("\n", 0, start_position)
        #
        #     self.sub_invoke_data_signal.emit(selected_text,start_line_column, start_column, self.file_path)




