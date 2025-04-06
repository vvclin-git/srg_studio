import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout
)
from system_parameters_widget import SystemParametersWidget

class DemoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Parameters Demo")

        self.params_widget = SystemParametersWidget("sys_params.json")
        self.print_button = QPushButton("Print")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.params_widget)
        layout.addWidget(self.print_button)
        layout.addWidget(self.output_text)
        self.setLayout(layout)

        self.print_button.clicked.connect(self.print_values)

    def print_values(self):
        self.output_text.clear()
        for label, line_edit in self.params_widget.inputs.items():
            self.output_text.append(f"{label}: {line_edit.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = DemoApp()
    demo.show()
    sys.exit(app.exec())
