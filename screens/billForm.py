from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class billForm(QDialog):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        loadUi('Interface/Bill.ui',self)
        self.payment_button.clicked.connect(self.send_bill)

    def send_bill(self):
        pass
