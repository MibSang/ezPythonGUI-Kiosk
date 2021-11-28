import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5 import uic

form_class = uic.loadUiType('myqt_1.ui')[0]
form_secondwindow = uic.loadUiType("myqt_2.ui")[0]
pay_success = False

ITEM_INFO = [
    {"name": "밀떡", "price": 2500},
    {"name": "쌀떡", "price": 3000},
    {"name": "찹쌀순대", "price": 3000},
    {"name": "오징어순대", "price": 4000},
    {"name": "김말이", "price": 700},
    {"name": "오징어튀김", "price": 1000},
    {"name": "새우튀김", "price": 700}

]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.totalPrice.setText("0")
        self.btn_milddeok.clicked.connect(lambda: self.item_clicked(0))
        self.btn_ssalddeok.clicked.connect(lambda: self.item_clicked(1))
        self.btn_chapsundae.clicked.connect(lambda: self.item_clicked(2))
        self.btn_squidsundae.clicked.connect(lambda: self.item_clicked(3))
        self.btn_gimmari.clicked.connect(lambda: self.item_clicked(4))
        self.btn_squidtuigim.clicked.connect(lambda: self.item_clicked(5))
        self.btn_shrimptuigim.clicked.connect(lambda: self.item_clicked(6))
        self.btn_reset.clicked.connect(self.item_clearall)
        self.item_selected = []
        self.btn_pay.clicked.connect(self.item_pay)

    def item_show(self):
        count_item = []
        for _ in range(len(ITEM_INFO)):
            count_item.append(0)

        for i in self.item_selected:
            count_item[i] += 1

        model = QStandardItemModel()
        for x in range(len(ITEM_INFO)):
            if count_item[x] == 0:
                continue
            temp = QStandardItem("{}를 {}개 주문하였습니다.".format(ITEM_INFO[x]["name"], count_item[x]))
            model.appendRow(temp)
        self.foodList.setModel(model)

    def item_clicked(self, item):
        self.item_selected.append(item)
        self.item_show()
        total = int(self.totalPrice.text())
        self.totalPrice.setText(str(total + ITEM_INFO[self.item_selected[-1]]['price']))

    def item_clearall(self):
        self.item_selected = []
        self.totalPrice.setText("0")
        self.item_show()

    def item_pay(self):
        global pay_success
        self.hide()
        second = Secondwindow(int(self.totalPrice.text()))
        pay_success = False
        second.exec()
        if pay_success:
            self.item_clearall()
        self.show()


class Secondwindow(QDialog, QWidget, form_secondwindow):
    def __init__(self, price):
        super(Secondwindow, self).__init__()
        self.setupUi(self)
        self.label_price.setText(f"{str(price)}원")
        self.btn_card.clicked.connect(self.card)
        self.btn_cash.clicked.connect(self.cash)
        self.show()

    def card(self):
        global pay_success
        ret = QMessageBox.question(self, '결제 확인', '결제를 진행하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ret == QMessageBox.Yes:
            pay_success = True
            self.close()

    def cash(self):
        self.card()
        # 현재 현금결제 기능은 카드결제와 동일한 일을 수행함!



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
