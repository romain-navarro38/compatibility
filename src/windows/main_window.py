from functools import partial

from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QFormLayout
from PySide6.QtGui import QFont, QRegularExpressionValidator, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize

from src.api.calculation import normalised_deviation
from src.api.settings import get_settings, set_default_settings


# noinspection PyAttributeOutsideInit
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(" ")
        self.setMinimumSize(QSize(220, 0))
        self.setup_ui()

    def setup_ui(self):
        """Setting up the ui"""

        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.le_value1.setFocus()
        self.setup_connections()

    def create_widgets(self):
        self.cbx_unit = QComboBox()
        self.le_time = QLineEdit()
        self.la_value1 = QLabel("")
        self.le_value1 = QLineEdit()
        self.la_value2 = QLabel("")
        self.le_value2 = QLineEdit()
        self.la_result = QLabel("")

    def modify_widgets(self):
        settings = get_settings()

        for unit in settings["unit_list"]:
            self.cbx_unit.addItem(unit)

        self.cbx_unit.setCurrentText(settings["unit_default"])
        self.le_time.setText(str(settings["time_default"]))

        self.change_validator_lineedit_count()
        validator_time = QRegularExpressionValidator()
        validator_time.setRegularExpression(r"[1-9]\d*")
        self.le_time.setValidator(validator_time)

        font = QFont()
        font.setBold(True)
        self.la_result.setFont(font)
        self.la_result.setAlignment(Qt.AlignCenter)

    def create_layouts(self):
        self.form_layout = QFormLayout(self)

    def add_widgets_to_layouts(self):
        self.form_layout.addRow(QLabel("Temps (min) :"), self.le_time)
        self.form_layout.addRow(QLabel("Unité :"), self.cbx_unit)
        self.form_layout.addRow(QLabel("Comptage 1 :"), self.le_value1)
        self.form_layout.addRow(QLabel("Comptage 2 :"), self.le_value2)
        self.form_layout.addRow(QLabel(""), self.la_result)

    def setup_connections(self):
        self.cbx_unit.currentIndexChanged.connect(self.unit_changed)
        self.le_time.textChanged.connect(self.time_changed)
        self.le_value1.textChanged.connect(partial(self.check_value, self.le_value1))
        self.le_value2.textChanged.connect(partial(self.check_value, self.le_value2))

    def check_value(self, lineedit: QLineEdit, value: str):
        """Adds a 0 if the user input starts with a decimal separator"""

        if value.startswith(".") or value.startswith(","):
            lineedit.setText(f"0{value}")
        self.calculation_deviation()

    def calculation_deviation(self):
        """If data present, calculation and display of the result of the normalized deviation"""

        if not self.verification_widget_filling():
            self.display_result(-1.0)
            return

        deviation = normalised_deviation(**self.data_transformation())
        self.display_result(deviation)

    def data_transformation(self) -> dict:
        """Transforms the data according to the unit and counting time entered
        to be compatible with the calculation of the normalized deviation"""

        count1 = float(self.le_value1.text().replace(',', '.'))
        count2 = float(self.le_value2.text().replace(',', '.'))
        time = int(self.le_time.text())
        if self.cbx_unit.currentText() == "Coups/s":
            count1 *= 60 * time
            count2 *= 60 * time
        elif self.cbx_unit.currentText() == "Coups/min":
            count1 *= time
            count2 *= time

        return {"count1": count1, "count2": count2}

    def display_result(self, result: float):
        """Changes the interface according to the result of the normalized deviation"""

        if result == -1.0:
            self.la_result.setText("")
        elif result > 1:
            self.la_result.setStyleSheet("color: red")
            self.la_result.setText("INCOMPATIBLES")
        else:
            self.la_result.setStyleSheet("color: green")
            self.la_result.setText("OK")

    def change_validator_lineedit_count(self):
        """Changes the validator of the user inputs according to the selected unit"""

        validator = QRegularExpressionValidator()
        if self.cbx_unit.currentText() == "Coups":
            validator.setRegularExpression(r"[1-9]\d*")
        else:
            validator.setRegularExpression(r"([0](\.|,)|(\.|,)|[1-9]\d*(\.|,))\d*")

        self.le_value1.setValidator(validator)
        self.le_value2.setValidator(validator)

    def unit_changed(self):
        """Changes the default unit in the settings, deletes user entries and the result"""

        set_default_settings("unit_default", self.cbx_unit.currentText())
        self.le_value1.setText("")
        self.le_value2.setText("")
        self.la_result.setText("")
        self.change_validator_lineedit_count()

    def time_changed(self):
        """Change the default time in the settings, and start the calculation"""

        set_default_settings("time_default", self.le_time.text())
        self.calculation_deviation()

    def verification_widget_filling(self) -> bool:
        """Checking the presence of data for the calculation"""

        return bool(self.le_time.text()
                    and self.le_value1.text()
                    and self.le_value2.text())


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from src.api.settings import BASE_DIR

    app = QApplication()
    app.setWindowIcon(QIcon(QPixmap(BASE_DIR / 'icon.ico')))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
