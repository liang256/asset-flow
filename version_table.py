from PySide6.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem, QComboBox, QVBoxLayout, 
    QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
)
import sys

class VersionTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Sample versions to populate the dropdown menus
        self.versions = ["v1.0", "v2.0", "v3.0"]

        # Create the table widget
        self.table = QTableWidget()
        self.table.setRowCount(3)  # Set the number of rows
        self.table.setColumnCount(2)  # Set the number of columns
        self.table.setHorizontalHeaderLabels(["Row", "Version"])

        # Populate the table
        for row in range(3):
            # Set the row number
            item = QTableWidgetItem(str(row + 1))
            self.table.setItem(row, 0, item)

            # Create a QComboBox for version selection
            combo_box = QComboBox()
            combo_box.addItems(self.versions)

            # Set the QComboBox as the cell widget
            self.table.setCellWidget(row, 1, combo_box)

        # Add command label and text input
        self.command_label = QLabel("Command:")
        self.command_input = QLineEdit()

        # Add preview and execute buttons
        self.preview_button = QPushButton("Preview")
        self.execute_button = QPushButton("Execute")

        # Connect buttons to their actions
        self.preview_button.clicked.connect(self.preview_command)
        self.execute_button.clicked.connect(self.execute_command)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.execute_button)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.command_label)
        layout.addWidget(self.command_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setWindowTitle("Table with Dropdown Menus and Commands")

    def preview_command(self):
        # Generate a command from the selected versions
        commands = []
        for row in range(self.table.rowCount()):
            combo_box = self.table.cellWidget(row, 1)
            selected_version = combo_box.currentText()
            commands.append(f"Row {row + 1}: {selected_version}")
        self.command_input.setText("; ".join(commands))

    def execute_command(self):
        # Clear the command text input
        self.command_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VersionTableWidget()
    window.show()
    sys.exit(app.exec())
