import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeView, QFileSystemModel, QVBoxLayout, QWidget

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('File Explorer')
        self.setGeometry(300, 300, 800, 600)

        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath('')

        self.tree = QTreeView()
        self.tree.setModel(self.file_system_model)
        self.tree.setRootIndex(self.file_system_model.index(''))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tree)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.open_file()

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            directory = file_name.rsplit('/', 1)[0]
            self.tree.setRootIndex(self.file_system_model.index(directory))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileExplorer()
    ex.show()
    sys.exit(app.exec_())
