# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'price_currency_weight_row.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
QLineEdit, QSizePolicy, QWidget, QToolTip)
from PySide6 import QtCore

class ToolTipComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def showPopup(self):
        super().showPopup()

    def hidePopup(self):
        QToolTip.hideText()
        super().hidePopup()

    def event(self, e):
        if (e.type() == QtCore.QEvent.ToolTip):
            QToolTip.showText(e.globalPos(), self.itemData(self.currentIndex(), QtCore.Qt.ToolTipRole), self)
            return True
        return super().event(e)

class Ui_price_currency_weight_row(object):
    def setupUi(self, price_currency_weight_row):
        if not price_currency_weight_row.objectName():
            price_currency_weight_row.setObjectName(u"price_currency_weight_row")
        price_currency_weight_row.resize(380, 26)
        self.widget = QWidget(price_currency_weight_row)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 379, 25))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout.addWidget(self.label_2)

        self.comboBox = ToolTipComboBox(self.widget)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.horizontalLayout.addWidget(self.label_3)

        self.comboBox_2 = ToolTipComboBox(self.widget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout.addWidget(self.comboBox_2)


        self.retranslateUi(price_currency_weight_row)

        QMetaObject.connectSlotsByName(price_currency_weight_row)
    # setupUi

    def retranslateUi(self, price_currency_weight_row):
        price_currency_weight_row.setWindowTitle(QCoreApplication.translate("price_currency_weight_row", u"Form", None))
        self.label.setText(QCoreApplication.translate("price_currency_weight_row", u"Price:", None))
        self.label_2.setText(QCoreApplication.translate("price_currency_weight_row", u"Currency:", None))
        self.label_3.setText(QCoreApplication.translate("price_currency_weight_row", u"Weight:", None))
    # retranslateUi

    def get_height(self):
        return self.widget.size().height()
    
    def get_width(self):
        return self.widget.size().width()