import sys

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication

from src.api.settings import SETTING_JSON, write_json_settings, DEFAULT_SETTING, RESSOURCE_DIR
from src.windows.main_window import MainWindow


def check_start():
    if not SETTING_JSON.exists():
        write_json_settings(DEFAULT_SETTING)

def launch_app():
    app = QApplication()
    app.setWindowIcon(QIcon(QPixmap(RESSOURCE_DIR / 'icon.ico')))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

def main():
    check_start()
    launch_app()


if __name__ == '__main__':
    main()
