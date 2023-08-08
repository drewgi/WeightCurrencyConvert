from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QDoubleValidator
from qt_material import apply_stylesheet


from price_currency_weight_row import Ui_price_currency_weight_row
from currency_api import get_currencies, get_currency_conversion
from weight_units import get_weight_units

INITIAL_WIDGET_COUNT = 2
MINIMUM_LAYOUT_COUNT = 4
UPDATE_INTERVAL = 600000  # 10 minutes

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WeightCurrencyConvert")
        
        self.currency_symbols = get_currencies()
        self.valid_currency_dict = get_currency_conversion(self.currency_symbols)
        self.weight_units = get_weight_units()
        
        self.timer = self.update_timer()
        
        self.row_widgets = []
        self.active_widget = None

        self.setup_ui()

    def setup_ui(self):
        self.central_widget_setup()
        self.button_setup()
        self.initial_widget_setup()
        self.window_setup()

    def central_widget_setup(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def button_setup(self):
        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")
        self.add_button.clicked.connect(self.add_row_widget)
        self.remove_button.clicked.connect(self.remove_widget)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.remove_button)

    def initial_widget_setup(self):
        for _ in range(INITIAL_WIDGET_COUNT):
            self.add_row_widget()

    def window_setup(self):
        single_widget_width = self.layout.itemAt(0).widget().width()
        self.setFixedWidth(single_widget_width)
        QTimer.singleShot(0, self.update_height)

    def add_row_widget(self):
        widget = self.create_row_widget()
        self.row_widgets.append(widget)
        self.layout.insertWidget(self.layout.count() - 2, widget)
        self.update_height()       
    
    def create_row_widget(self):
        widget = QWidget()
        ui = Ui_price_currency_weight_row()
        ui.setupUi(widget)
        widget.ui = ui
        ui.lineEdit.setValidator(QDoubleValidator(0, 9999999.99, 2))
        ui.lineEdit.textChanged.connect(self.set_active_widget)
        ui.lineEdit.textChanged.connect(self.update_conversion)
        self.populate_comboboxes(ui)
        widget.setFixedSize(ui.get_width(), ui.get_height())
        return widget

    def remove_widget(self):
        if self.layout.count() > MINIMUM_LAYOUT_COUNT: 
            widget_to_remove = self.layout.takeAt(self.layout.count() - 3).widget()
            widget_to_remove.setParent(None)
            if widget_to_remove in self.row_widgets:#
                self.row_widgets.remove(widget_to_remove)
            self.update_height()

        
    def populate_comboboxes(self, ui):
        for currency_code, currency_data in self.currency_symbols.items():
            ui.comboBox.addItem(currency_code)
            ui.comboBox.setItemData(ui.comboBox.count() - 1, currency_data['description'], Qt.ToolTipRole)

        for weight_unit, weight_data in self.weight_units.items():
            ui.comboBox_2.addItem(weight_unit)
            ui.comboBox_2.setItemData(ui.comboBox_2.count() - 1, weight_data['description'], Qt.ToolTipRole)

    def update_height(self):
        widget_height = self.layout.itemAt(0).widget().height()
        total_height = (self.layout.count() - 2) * widget_height
        total_height += self.add_button.height() + self.remove_button.height()
        total_height += (self.layout.spacing() * (self.layout.count() - 1)) + self.layout.contentsMargins().top() + self.layout.contentsMargins().bottom()
        self.setFixedHeight(total_height)

    def set_active_widget(self):
         # Get the sender of the signal (the lineEdit that triggered the textChanged signal)
        active_line = self.sender()
        qhbox_layout = active_line.parent()
        self.active_widget = qhbox_layout.parent()

    def get_data(self):
        non_active_data = []

        for widget in self.row_widgets:
            if widget != self.active_widget:
                input_value = widget.ui.lineEdit.text()

                selected_symbol = widget.ui.comboBox.currentText()
                currency_conversion_data = self.currency_symbols[selected_symbol]['conversion']

                selected_weight_unit = widget.ui.comboBox_2.currentText()
                weight_conversion_data = self.weight_units[selected_weight_unit]['conversion']

                row_data = {
                    "input_value": input_value,
                    "currency_conversion": currency_conversion_data,
                    "weight_conversion": weight_conversion_data
                }

                non_active_data.append(row_data)

        return non_active_data
    
    def extract_data_from_widget(self, widget):
        price_text = widget.ui.lineEdit.text()
        if widget == self.active_widget and not price_text:
            price = None
        else:
            price = float(price_text) if price_text else 0.0
        currency = widget.ui.comboBox.currentText()
        weight_unit = widget.ui.comboBox_2.currentText()
        return price, currency, weight_unit
    
    def update_conversion(self):
        active_widget_price, active_widget_currency, active_widget_weight_unit = self.extract_data_from_widget(self.active_widget)
        
        if active_widget_price is None:
            return

        active_currency_conversion = self.valid_currency_dict[active_widget_currency]
        active_weight_conversion = self.weight_units[active_widget_weight_unit]['conversion']

        base_price = active_widget_price * active_currency_conversion / active_weight_conversion

        for widget in self.row_widgets:
            if widget != self.active_widget:
                desired_price, desired_currency, desired_weight_unit = self.extract_data_from_widget(widget)

                desired_currency_conversion = self.valid_currency_dict[desired_currency]
                desired_weight_conversion = self.weight_units[desired_weight_unit]['conversion']

                converted_price = base_price * desired_weight_conversion / desired_currency_conversion

                widget.ui.lineEdit.setText(str(round(converted_price, 2)))
    
    def update_timer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_conversion_data)
        timer.start(UPDATE_INTERVAL)
        return timer
    
    def update_conversion_data(self):
        get_currency_conversion(self.currency_symbols)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    apply_stylesheet(app, theme='dark_pink.xml')
    current_style = app.styleSheet()
    app.setStyleSheet(current_style + "QToolTip {background-color: #1f2124; border: 1px solid white; font-size: 14px; }")
    window.show()
    app.exec()