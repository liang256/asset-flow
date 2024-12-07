from PySide6.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem, QComboBox, QVBoxLayout, QWidget
)
import sys

class VersionTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Sample versions to populate the dropdown menus
        versions = ["v1.0", "v2.0", "v3.0"]

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
            combo_box.addItems(versions)

            # Set the QComboBox as the cell widget
            self.table.setCellWidget(row, 1, combo_box)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle("Table with Dropdown Menus")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VersionTableWidget()
    window.show()
    sys.exit(app.exec())
