from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox, QFormLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QRegularExpressionValidator, QIcon, QPixmap

from src.api.calculation import normalised_deviation
from src.api.settings import get_default_analysis_settings, set_default_analysis_settings


# noinspection PyAttributeOutsideInit
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(" ")
        self.setup_ui()

    def setup_ui(self):
        """Setting up the ui"""

        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.cbx_analysis = QComboBox()
        self.la_value1 = QLabel("")
        self.le_shocks1 = QLineEdit()
        self.la_value2 = QLabel("")
        self.le_shocks2 = QLineEdit()
        self.la_result = QLabel("")

    def modify_widgets(self):
        self.cbx_analysis.addItem("Alpha-Bêta")
        self.cbx_analysis.addItem("Tritium")

        self.display_settings()

        self.le_shocks1.setAlignment(Qt.AlignCenter)
        self.le_shocks2.setAlignment(Qt.AlignCenter)

        self.la_result.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        self.la_result.setFont(font)

    def create_layouts(self):
        self.layout_time = QHBoxLayout()
        self.form_layout = QFormLayout(self)

    def add_widgets_to_layouts(self):
        self.form_layout.addRow(QLabel("Analyse :"), self.cbx_analysis)
        self.form_layout.addRow(self.la_value1, self.le_shocks1)
        self.form_layout.addRow(self.la_value2, self.le_shocks2)
        self.form_layout.addRow(QLabel(""), self.la_result)

    def setup_connections(self):
        self.cbx_analysis.currentIndexChanged.connect(self.analysis_changed)
        self.le_shocks1.textChanged.connect(self.calculation_deviation)
        self.le_shocks2.textChanged.connect(self.calculation_deviation)

    def display_settings(self):
        """Retrieves and displays the parameters associated with the selected analysis in the combobox"""
        settings_of_analysis = get_default_analysis_settings()

        self.cbx_analysis.setCurrentText(settings_of_analysis["analysis"])

        input_validator = QRegularExpressionValidator()
        input_validator.setRegularExpression(settings_of_analysis["regex"])
        self.le_shocks1.setValidator(input_validator)
        self.le_shocks2.setValidator(input_validator)

        self.la_value1.setText(settings_of_analysis["label1"])
        self.la_value2.setText(settings_of_analysis["label2"])

    def calculation_deviation(self):
        """If data present, calculation and display of the result of the normalized deviation"""

        if not self.verification_widget_filling():
            self.display_result(-1.0)
            return

        deviation = normalised_deviation(**self.data_transformation())
        self.display_result(deviation)

    def data_transformation(self) -> dict:
        """Transforms the data according to the selected analysis to be compatible
        with the calculation of the normalized deviation"""

        shocks1 = float(self.le_shocks1.text().replace(',', '.'))
        shocks2 = float(self.le_shocks2.text().replace(',', '.'))
        if self.cbx_analysis.currentText() == "Tritium":
            shocks1 *= 60
            shocks2 *= 60

        return {"shocks1": shocks1, "shocks2": shocks2}

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

    def analysis_changed(self):
        """Changes the default analysis in the settings, deletes user entries and the result.
        Displays the settings for the selected analysis."""

        set_default_analysis_settings(str(self.cbx_analysis.currentIndex()))
        self.le_shocks1.setText("")
        self.le_shocks2.setText("")
        self.la_result.setText("")
        self.display_settings()

    def verification_widget_filling(self) -> bool:
        """Checking the presence of data for the calculation"""

        return bool(self.le_shocks1.text() and self.le_shocks2.text())


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from src.api.settings import BASE_DIR

    app = QApplication()
    app.setWindowIcon(QIcon(QPixmap(BASE_DIR / 'icon.ico')))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
