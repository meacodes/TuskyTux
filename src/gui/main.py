import sys
import json
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import webbrowser

CONFIG_PATH = os.path.expanduser("~/.config/tuskydrive/settings.json")

class SettingsGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_settings()

    def initUI(self):
        self.setWindowTitle("TuskyDrive Settings")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.api_key_label = QLabel("Enter your API Key:")
        self.api_key_input = QLineEdit()
        self.save_button = QPushButton("Save API Key")
        self.login_button = QPushButton("Login to Tusky")

        self.save_button.clicked.connect(self.save_api_key)
        self.login_button.clicked.connect(self.open_login_page)

        layout.addWidget(self.api_key_label)
        layout.addWidget(self.api_key_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def save_api_key(self):
        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Warning", "API Key cannot be empty!")
            return

        settings = {"api_key": api_key}
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as file:
            json.dump(settings, file)

        QMessageBox.information(self, "Success", "API Key saved successfully!")

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as file:
                settings = json.load(file)
                api_key = settings.get("api_key", "")
                self.api_key_input.setText(api_key)

    def open_login_page(self):
        login_url = "https://app.tusky.io/connect"  # Login in Tusky
        webbrowser.open(login_url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsGUI()
    window.show()
    sys.exit(app.exec())
