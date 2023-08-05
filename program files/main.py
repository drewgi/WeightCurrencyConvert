from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QDoubleValidator
from qt_material import apply_stylesheet
from price_currency_weight_row import Ui_price_currency_weight_row
from currency_api import get_currencies, get_currency_conversion
from weight_units import get_weight_units

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.currency_symbols = get_currencies()
        self.valid_currency_dict = get_currency_conversion(self.currency_symbols)
        self.weight_units = get_weight_units()

        # Set up central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Set up buttons
        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")
        self.add_button.clicked.connect(self.add_widget)
        self.remove_button.clicked.connect(self.remove_widget)

        # Add initial widgets
        for _ in range(2):
            self.add_widget()

        # Add buttons to layout
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.remove_button)

        # Set window width
        single_widget_width = self.layout.itemAt(0).widget().width()
        self.setFixedWidth(single_widget_width)

        # Update window height after the main event loop starts
        QTimer.singleShot(0, self.update_height)

    def add_widget(self):
        # Create new widget and add to layout
        widget = QWidget()
        ui = Ui_price_currency_weight_row()
        ui.setupUi(widget)
        ui.lineEdit.setValidator(QDoubleValidator(0, 9999999.99, 2))
        
        
        for currency_code, currency_data in self.currency_symbols.items():
            ui.comboBox.addItem(currency_code)
            ui.comboBox.setItemData(ui.comboBox.count() - 1, currency_data['description'], Qt.ToolTipRole)

        for weight_unit, weight_data in self.weight_units.items():
            ui.comboBox_2.addItem(weight_unit)
            ui.comboBox_2.setItemData(ui.comboBox_2.count() - 1, weight_data['description'], Qt.ToolTipRole)
        
        widget.setFixedSize(ui.get_width(), ui.get_height())
        self.layout.insertWidget(self.layout.count() - 2, widget)
        self.update_height()

    def remove_widget(self):
        # Remove widget from layout
        if self.layout.count() > 4: 
            widget_to_remove = self.layout.takeAt(self.layout.count() - 3).widget()
            widget_to_remove.setParent(None)
            self.update_height()

    def update_height(self):
        # Calculate and set window height
        widget_height = self.layout.itemAt(0).widget().height()
        total_height = (self.layout.count() - 2) * widget_height
        total_height += self.add_button.height() + self.remove_button.height()
        total_height += (self.layout.spacing() * (self.layout.count() - 1)) + self.layout.contentsMargins().top() + self.layout.contentsMargins().bottom()
        self.setFixedHeight(total_height)
        
    def get_data(self):
        input_value = self.ui.lineEdit.text()

        selected_symbol = self.ui.comboBox.currentText()
        currency_conversion_data = self.currency_symbols[selected_symbol]['conversion']

        selected_weight_unit = self.ui.comboBox_2.currentText()
        weight_conversion_data = self.weight_units[selected_weight_unit]['conversion']

        return input_value, currency_conversion_data, weight_conversion_data
    
    def update_conversion_data(self):
        get_currency_conversion(self.currency_symbols)
        timer = QTimer()
        timer.timeout.connect(self.update_conversion_data)
        timer.start(600000)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    apply_stylesheet(app, theme='dark_pink.xml')
    current_style = app.styleSheet()
    app.setStyleSheet(current_style + "QToolTip {background-color: #1f2124; border: 1px solid white; font-size: 14px; }")
    window.show()
    app.exec()