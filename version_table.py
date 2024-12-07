import sys
import model
from PySide6.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem, QComboBox, QVBoxLayout,
    QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
)


class AssetManager(QWidget):
    def __init__(self, packages):
        super().__init__()
        self.packages = packages

        # Create the table widget
        self.table = QTableWidget()
        self.table.setRowCount(len(packages))
        self.table.setColumnCount(3)  # ['cameraPkg', 'rig', 'animation']
        self.table.setHorizontalHeaderLabels(["cameraPkg", "rig", "animation"])

        # Populate the table
        self.populate_table()

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
        self.setWindowTitle("Asset Manager")

    def populate_table(self):
        for row, package in enumerate(self.packages):
            root_asset_key = package.root_asset_key

            # Set root asset
            root_combo = QComboBox()
            root_asset = package[root_asset_key]

            # Add available versions + None (for UI only)
            root_combo.addItems(list(root_asset.available_versions) + ["None"])
            root_combo.setCurrentText(root_asset.get_version() or "None")
            root_combo.currentTextChanged.connect(
                lambda version, asset=root_asset: asset.set_version(None if version == "None" else version)
            )
            self.table.setCellWidget(row, 0, root_combo)

            # Set child assets
            for col, (asset_type, asset) in enumerate(package.child_assets.items(), start=1):
                combo = QComboBox()

                # Add available versions + None
                combo.addItems(list(asset.available_versions) + ["None"])
                combo.setCurrentText(asset.get_version() or "None")
                combo.currentTextChanged.connect(
                    lambda version, asset=asset: asset.set_version(None if version == "None" else version)
                )
                self.table.setCellWidget(row, col, combo)


    def preview_command(self):
        commands = model.generate_commands(self.packages)
        command_strings = [
            str(cmd) for cmd in commands
        ]
        self.command_input.setText("\n".join(command_strings))
        print("Previewed commands:")  # Replace with actual preview logic
        print(commands)

    def execute_command(self):
        self.command_input.clear()
        print("Executed commands.")  # Replace with actual execution logic


if __name__ == "__main__":
    # Sample data
    data = [
        model.AssetPackage(
            "camera_asset",
            assets={
                "camera_asset": model.TrackedAsset(["v1", "v2"]),
                "camera_rig": model.TrackedAsset(["rig_v1", "rig_v2"]),
                "animation_curves": model.TrackedAsset(["anim_v1"]),
            },
        ),
        model.AssetPackage(
            "character_asset",
            assets={
                "character_asset": model.TrackedAsset(["v1", "v2", "v3"]),
                "rig_puppet": model.TrackedAsset(["rig_v1", "rig_v2"]),
            },
        ),
    ]

    app = QApplication(sys.argv)
    window = AssetManager(data)
    window.show()
    sys.exit(app.exec())
