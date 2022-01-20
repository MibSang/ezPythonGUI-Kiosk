import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5 import uic

form_class = uic.loadUiType('myqt_1.ui')[0]
form_secondwindow = uic.loadUiType("myqt_2.ui")[0]
pay_success = False

# 아이템 정보를 담는 딕셔너리의 리스트
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
        # 선택된 아이템을 저장하는 변수(리스트)
        self.item_selected = []

        # 버튼 클릭 이벤트 연결
        self.btn_milddeok.clicked.connect(lambda: self.item_clicked(0))
        self.btn_ssalddeok.clicked.connect(lambda: self.item_clicked(1))
        self.btn_chapsundae.clicked.connect(lambda: self.item_clicked(2))
        self.btn_squidsundae.clicked.connect(lambda: self.item_clicked(3))
        self.btn_gimmari.clicked.connect(lambda: self.item_clicked(4))
        self.btn_squidtuigim.clicked.connect(lambda: self.item_clicked(5))
        self.btn_shrimptuigim.clicked.connect(lambda: self.item_clicked(6))
        self.btn_reset.clicked.connect(self.item_clearall)
        self.btn_pay.clicked.connect(self.item_pay)

    """
    * item_show(self)
    * QStandardItemModel 에 표시할 내용 처리 및 표시
    """
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

    """
    * item_clicked(self, item)
    * 판매 물품 클릭 이벤트 처리 메소드
    """
    def item_clicked(self, item):
        self.item_selected.append(item)
        self.item_show()
        total = int(self.totalPrice.text())
        self.totalPrice.setText(str(total + ITEM_INFO[self.item_selected[-1]]['price']))

    """
    * item_clearall(self)
    * 모든 선택된 물품 초기화
    """
    def item_clearall(self):
        self.item_selected = []
        self.totalPrice.setText("0")
        self.item_show()

    """
    * item_pay(self)
    * 선택된 물품 구매, SecondWindow 클래스 사용
    """
    def item_pay(self):
        global pay_success
        self.hide()
        second = SecondWindow(int(self.totalPrice.text()))
        pay_success = False
        second.exec()
        if pay_success:
            self.item_clearall()
        self.show()


class SecondWindow(QDialog, QWidget, form_secondwindow):
    def __init__(self, price):
        super(SecondWindow, self).__init__()
        self.setupUi(self)
        self.label_price.setText(f"{str(price)}원")
        self.btn_card.clicked.connect(self.card)
        self.btn_cash.clicked.connect(self.cash)
        self.show()

    """
    * card(self)
    * 카드결제 진행
    """
    def card(self):
        global pay_success
        ret = QMessageBox.question(self, '결제 확인', '카드결제를 진행하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ret == QMessageBox.Yes:
            pay_success = True
            self.close()

    """
    * cash(self)
    * 현금결제 진행
    """
    def cash(self):
        global pay_success
        ret = QMessageBox.question(self, '결제 확인', '현금결제를 진행하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ret == QMessageBox.Yes:
            pay_success = True
            self.close()
        # 현재 현금결제 기능은 카드결제와 동일한 작업을 수행함!



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
