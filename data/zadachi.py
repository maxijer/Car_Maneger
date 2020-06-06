import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("Select * from mashin WHERE id=1",
                             ).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE films SET\n"
            for key in self.modified.keys():
                que += "{}='{}'\n".format(key, self.modified.get(key))
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())