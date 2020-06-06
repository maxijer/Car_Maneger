import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QInputDialog, QListWidget, \
    QListWidgetItem, \
    QTableWidget, QTableWidgetItem, QFileDialog, QComboBox
from PyQt5.QtGui import QPalette, QImage, QBrush, QIcon
from PyQt5.QtCore import QSize
import sqlite3
import hashlib
import random
import csv

znach = ''
count_for_play = 0
true_otw = 0
flag = False
korzina = list()
titeks = list()
sravnenie = list()
role = ''
cena = 0


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/avtorization.ui', self)
        palette = QPalette()
        oImage = QImage("data/й.jpg")
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)
        self.registrate.clicked.connect(self.registrated)
        self.login.clicked.connect(self.whod)
        self.setWindowTitle('Авторизация')

    def registrated(self):  ## функция регистрации пользователей
        z = self.login1.text()
        w = self.password.text()
        has = hashlib.md5(w.encode('utf-8')).hexdigest()
        if len(z) == 0 or len(w) == 0:
            i, okBtnPressed = QInputDialog.getText(self, "Логин ил пароль", "Придумайте новый лоигн "
                                                                            "или пароль")
        else:
            con = sqlite3.connect('db/rabota.db')

            cur1 = con.cursor()
            pepole = cur1.execute("""SELECT  id FROM users
            WHERE login = ?""", (z,)).fetchall()
            if len(pepole) == 0:
                try:
                    # Создание курсора
                    cur = con.cursor()

                    # Выполнение запроса и добавляем логин и пароль
                    cur.execute("""INSERT INTO users("login", "password", "role") VALUES(?, ?, ?)
                                    """, (z, has, "user"))
                    con.commit()
                    con.close()
                    i, okBtnPressed = QInputDialog.getText(self, "Регистрация",
                                                           "Пользователь успешно зарегистрирован")
                except sqlite3.IntegrityError:
                    i, okBtnPressed = QInputDialog.getText(self, "Логин или павроль", "Смените"
                                                                                      "логин или "
                                                                                      "пароль")
            else:
                i, okBtnPressed = QInputDialog.getText(self, "Такой пользователь уже существует",
                                                       "придумайте другой логин")

    def whod(self):  ## функция для проверки и входа в систему
        z = self.login1.text()
        w = self.password.text()
        has = hashlib.md5(w.encode('utf-8')).hexdigest()
        con = sqlite3.connect('db/rabota.db')

        # Создание курсора
        cur = con.cursor()

        # Выполнение запроса и добавляем логин и пароль
        z = cur.execute("""SELECT login, password, role FROM users
        WHERE login = ? AND password = ?
                               """, (z, has)).fetchall()
        con.close()
        if len(z) == 0:
            i, okBtnPressed = QInputDialog.getText(self, "Ошибка",
                                                   "Пользователь не зарегистрирован")
        else:
            global role
            role = z[0][2]
            self.new = Glaw_form()
            self.new.show()
            self.hide()


class Glaw_form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/mashin.ui', self)
        self.korz.clicked.connect(self.korzin)
        self.play.clicked.connect(self.gamepad)
        self.volkswagen.clicked.connect(lambda: self.all_form("volkswagen"))
        self.Ferrari.clicked.connect(lambda: self.all_form("ferrari"))
        self.bently.clicked.connect(lambda: self.all_form("bently"))
        self.porshe.clicked.connect(lambda: self.all_form("porshe"))
        self.lamborghini.clicked.connect(lambda: self.all_form("lamborghini"))
        self.rols_royce.clicked.connect(lambda: self.all_form("rolls royce"))
        self.listWidget.itemDoubleClicked.connect(self.information)
        self.plus.clicked.connect(self.add_table)
        self.trade_in.clicked.connect(self.trade_in2)
        self.setWindowTitle('Помощник выбора автомобиля')
        palette = QPalette()
        oImage = QImage("data/з_фон.jpg")
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)
        self.srav.clicked.connect(self.sra)

    def all_form(self, marka):
        self.listWidget.clear()
        dla_cik = self.kol_car(marka)  ## количество марок для цикла
        mod_and_pict = self.izob(marka)  ## модель и изображение
        for i in range(dla_cik):
            w = All_mashin(self)
            w.photo.setIcon(QIcon(mod_and_pict[i][1]))
            w.photo.setIconSize(QSize(120, 120))
            w.model.setText(mod_and_pict[i][0])
            self.dobav_list(w)

    def gamepad(self):  ## входим в игру
        self.listWidget.clear()
        p = Play()
        self.dobav_list(p)

    def information(self):
        global znach
        item = self.listWidget.currentItem()
        self.widget = self.listWidget.itemWidget(item)
        znach = self.widget.model.text()
        self.s = Info()
        self.s.show()

    def kol_car(self, marka):  ## считает количество машин
        con = sqlite3.connect('db/rabota.db')

        cur = con.cursor()

        kol_mashin = cur.execute("""SELECT марка FROM mashin
                    WHERE марка = ? """, (marka,)).fetchall()
        return len(kol_mashin)

    def sra(self):
        global sravnenie
        # Получили результат запроса, который ввели в текстовое поле
        result = sravnenie
        if len(sravnenie) == 0:
            i, okPressed = QInputDialog.getText(self, "Ошибка",
                                                "Вы ничего не добавили в сравнение")
        else:
            self.listWidget.clear()
            self.z = Sam(self)
            self.z.tableWidget.setRowCount(len(result))
            self.z.tableWidget.setColumnCount(len(result[0][0]))
            # Заполнили размеры таблицы
            w = 0
            one = ["марка", "модель", "коробка передач", "Макс.скорость", "разгон 0 - 100",
                   "Общая масса", "расход", "картинка", "Длинна", "Ширина",
                   "Высота", "Дор. просвет", "цена",
                   "количество мест", "вид"]
            # Заполнили таблицу полученными элементами
            self.titles = [description for description in one]
            self.z.tableWidget.setHorizontalHeaderLabels(self.titles)
            for k in range(len(sravnenie)):
                for i, elem in enumerate(list(result[k])):
                    for j, val in enumerate(elem):
                        self.z.tableWidget.setItem(w, j, QTableWidgetItem(str(val)))
                w += 1
            self.dobav_list(self.z)

    def korzin(self):
        self.listWidget.clear()
        z = Clear(self)
        self.dobav_list(z)
        global korzina
        for i in range(len(korzina)):
            w = All_mashin(self)
            w.photo.setIcon(QIcon(korzina[i][0][8]))
            w.photo.setIconSize(QSize(120, 120))
            w.model.setText(korzina[i][0][2])
            self.dobav_list(w)

    def add_table(self):  ## Добавляем модели в таблицу

        fname = QFileDialog.getOpenFileName(self, 'Выбрать Таблицу',
                                            '', "Таблица(*.csv)")[0]
        try:
            with open(fname, encoding="utf8") as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                z = list(reader)
                for i in range(len(z)):
                    try:
                        con = sqlite3.connect('db/rabota.db')
                        cur = con.cursor()

                        # Выполнение запроса и добавляем логин и пароль
                        cur.execute("""INSERT INTO mashin("марка", "модель", "коробка передач", "Макс.скорость", "разгон 0 - 100",
                                "Общая масса", "расход", "картинка", "Длинна", "Ширина", 
                                "Высота", "Дор. просвет", "цена",
                                "количество мест", "вид") VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                                              """,
                                    (z[i][0], z[i][1], z[i][2], z[i][3], z[i][4], z[i][5], z[i][6],
                                     z[i][7], z[i][8], z[i][9], z[i][10], z[i][11], z[i][12],
                                     z[i][13],
                                     z[i][14]))
                        con.commit()
                        con.close()
                        i, okBtnPressed = QInputDialog.getText(self, "Таблица",
                                                               "Данные успешно добавленны")
                    except:
                        i, okBtnPressed = QInputDialog.getText(self, "Таблица",
                                                               "Таблица не соответсвует требованиям")
        except:
            i, okBtnPressed = QInputDialog.getText(self, "Таблица", "Вы не выбрали таблицу")

    def izob(self, marka):  ## добавляет изображение и пишет название машины
        con = sqlite3.connect('db/rabota.db')

        cur = con.cursor()

        mod_and_picture = cur.execute("""SELECT модель, картинка FROM mashin
                            WHERE марка = ? """, (marka,)).fetchall()

        return mod_and_picture

    def trade_in2(self):  ##  trade in
        self.listWidget.clear()
        self.z = Srav()
        self.dobav_list(self.z)

    def dobav_list(self, clas):  # добавляем виджеты на главный экран
        item = QListWidgetItem(self.listWidget)
        self.mywid = clas
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, self.mywid)
        item.setSizeHint(self.mywid.size())


class TEST(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/glav_form.ui', self)

    def all_form(self):
        self.dobav_list(All_mashin)


class All_mashin(QWidget):
    def __init__(self, Glav_form):
        super().__init__()
        self.Glav_form = Glav_form
        global role
        if role == 'admin':
            uic.loadUi('data/car.ui', self)
            self.korz.clicked.connect(self.add_korz)
            self.gal.clicked.connect(self.sravnenie)
            self.del_korz.clicked.connect(self.del_korzina)
            self.musor.clicked.connect(self.delit)
        else:
            uic.loadUi('data/car_3.ui', self)
            self.korz.clicked.connect(self.add_korz)
            self.gal.clicked.connect(self.sravnenie)
            self.del_korz.clicked.connect(self.del_korzina)

    def add_korz(self):
        global korzina
        model = self.model.text()

        con = sqlite3.connect('db/rabota.db')

        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и добавляем логин и пароль
        z = cur.execute("""SELECT * FROM mashin
                WHERE модель = ?
                                       """, (model,)).fetchall()
        con.close()
        if z in korzina or len(z) == 0:
            pass
        else:
            i, okBtnPressed = QInputDialog.getText(self, "Автомобиль",
                                                   "Автомобиль успешно добавлен в корзину")
            korzina.append(z)

    def del_korzina(self):
        global korzina
        model = self.model.text()
        con = sqlite3.connect('db/rabota.db')

        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и добавляем логин и пароль
        z = cur.execute("""SELECT * FROM mashin
                                   WHERE модель = ?
                                                          """, (model,)).fetchall()
        con.close()
        if z in korzina:
            self.Glav_form.listWidget.clear()
            self.Glav_form.korzin()
            del korzina[korzina.index(z)]
            i, okBtnPressed = QInputDialog.getText(self, "Корзина",
                                                   "Автомобиль удалён из корзины")
        else:
            pass

    def delit(self):
        model = self.model.text()
        con = sqlite3.connect('db/rabota.db')

        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и добавляем логин и пароль
        cur.execute("""DELETE  FROM mashin
                                           WHERE модель = ?
                                                                  """, (model,))
        con.commit()
        con.close()

    def sravnenie(self):
        global sravnenie
        global flag
        model = self.model.text()
        con = sqlite3.connect('db/rabota.db')

        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и добавляем логин и пароль
        z = cur.execute("""SELECT * FROM mashin
                           WHERE модель = ?
                                                  """, (model,)).fetchall()
        con.close()
        if z in sravnenie:
            self.gal.setIcon(QIcon('data/gal.png'))
            self.gal.setIconSize(QSize(20, 20))
            del sravnenie[sravnenie.index(z)]
        else:
            self.gal.setIcon(QIcon('data/green.jpg'))
            self.gal.setIconSize(QSize(35, 35))
            sravnenie.append(z)


class Info(QWidget):  ## информация о машине
    def __init__(self):
        super().__init__()
        uic.loadUi('data/info.ui', self)
        palette = QPalette()
        oImage = QImage("data/з_фон.jpg")
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)
        self.update_res()

    def update_res(self):
        con = sqlite3.connect('db/rabota.db')
        cur = con.cursor()

        # Получили результат запроса, который ввели в текстовое поле
        global znach
        kar = cur.execute("Select картинка FROM mashin WHERE модель=?", (znach,)).fetchall()
        self.pushButton.setIcon(QIcon(kar[0][0]))
        self.pushButton.setIconSize(QSize(120, 120))
        result = cur.execute("Select * FROM mashin WHERE модель=?", (znach,)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        # Заполнили таблицу полученными элементами
        self.titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}


class Play(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/play.ui', self)
        self.nachinka()
        self.contin.clicked.connect(self.check)

    def nachinka(self):
        con1 = sqlite3.connect('db/rabota.db')
        # Создание курсора
        cur = con1.cursor()

        # Выполнение запроса и добавляем логин и пароль
        model = cur.execute("""SELECT модель, марка, картинка FROM mashin
                                                      """).fetchall()
        con1.close()

        pict = random.choice(model)
        con1.close()
        self.photo.setIcon(QIcon(pict[2]))
        self.photo.setIconSize(QSize(900, 900))
        del model[model.index(pict)]
        self.knop = random.choice(['first', 'two', 'three', 'four'])
        if self.knop == 'first':
            self.first.setText(' '.join(pict[:2]))
            self.two.setText(' '.join(random.choice(model)[:2]))
            self.three.setText(' '.join(random.choice(model)[:2]))
            self.four.setText(' '.join(random.choice(model)[:2]))
        elif self.knop == 'two':
            self.first.setText(' '.join(random.choice(model)[:2]))
            self.two.setText(' '.join(pict[:2]))
            self.three.setText(' '.join(random.choice(model)[:2]))
            self.four.setText(' '.join(random.choice(model)[:2]))
        elif self.knop == 'three':
            self.three.setText(' '.join(pict[:2]))
            self.first.setText(' '.join(random.choice(model)[:2]))
            self.two.setText(' '.join(random.choice(model)[:2]))
            self.four.setText(' '.join(random.choice(model)[:2]))
        elif self.knop == 'four':
            self.four.setText(' '.join(pict[:2]))
            self.two.setText(' '.join(random.choice(model)[:2]))
            self.three.setText(' '.join(random.choice(model)[:2]))
        global count_for_play
        global true_otw
        count_for_play += 1
        if count_for_play == 11:
            self.res = Result_play()
            self.res.show()
            self.hide()

    def check(self):  ## проверка
        global true_otw
        if self.knop == 'first' and self.first.isChecked():
            true_otw += 1
        elif self.knop == 'two' and self.two.isChecked():
            true_otw += 1
        elif self.knop == 'three' and self.three.isChecked():
            true_otw += 1
        elif self.knop == 'four' and self.four.isChecked():
            true_otw += 1
        print(true_otw)
        self.nachinka()


class Result_play(QWidget):  ## вывод сообщений результатов
    def __init__(self):
        super().__init__()
        uic.loadUi('data/result.ui', self)
        global true_otw
        global count_for_play
        if true_otw < 4:
            self.medal.setIcon(QIcon('data/bronz.jpg'))
            self.medal.setIconSize(QSize(120, 120))
            self.label.setText('Твои знания не очень хороши , но если тренироваться всё получится')
        elif true_otw >= 4 and true_otw <= 7:
            self.medal.setIcon(QIcon('data/bronz1.jpg'))
            self.medal.setIconSize(QSize(120, 120))
            self.label.setText('Молодец , ты неплохо знаешь машины , но не до конца')
        elif true_otw >= 8:
            self.medal.setIcon(QIcon('data/gold.png'))
            self.medal.setIconSize(QSize(120, 120))
            self.label.setText('Ты великий мастер авто')

        true_otw = 0
        count_for_play = 0


class Clear(QWidget):
    def __init__(self, Glav_form):
        super().__init__()
        self.Glav_form = Glav_form
        uic.loadUi('data/чистка.ui', self)
        self.pushButton.clicked.connect(self.clin)

    def clin(self):
        global korzina
        self.Glav_form.listWidget.clear()
        korzina.clear()


class Srav(QWidget):  ## trade_in
    def __init__(self):
        super().__init__()
        uic.loadUi('data/prim.ui', self)
        self.pushButton.clicked.connect(self.sravnenie)

    def sravnenie(self):
        if self.lineEdit_2.text() == '' or self.lineEdit_4.text() == '' or not str(self.lineEdit_4.text(

        )).isdigit() or \
                self.lineEdit_5.text() \
                == '' or not str(self.lineEdit_5.text(

        )).isdigit() or self.lineEdit_6.text() == '' or not str(self.lineEdit_6.text(

        )).isdigit() or \
                self.lineEdit_7.text() == '' or not str(self.lineEdit_7.text(

        )).isdigit() or self.lineEdit_8.text() == '' or \
                not str(self.lineEdit_8.text(

                )).isdigit() or self.lineEdit_9.text() == '' or not str(self.lineEdit_9.text()) \
                or self.lineEdit_11.text() == '' \
                or not str(self.lineEdit_11.text(

        )).isdigit() or self.lineEdit_13.text() == '' or self.lineEdit_12.text() == '' or str(
            self.lineEdit_12.text()).isdigit() or \
                not str(self.lineEdit_13.text(

                )).isdigit() or \
                self.lineEdit_17.text() == '' or \
                self.lineEdit_17.text().isalpha() or self.lineEdit_6.text().isalpha():
            i, okBtnPressed = QInputDialog.getText(self, "Ошибка",
                                                   "Некоторые поля не заполнены или заполнены не правильно")
        else:
            if int(self.lineEdit_17.text()) < 10000:
                i, okBtnPressed = QInputDialog.getText(self, "Враньё",
                                                       "Стоимость не может быть меньше 100000")
            else:  ## Мы обработали все ошибки и начали выяснеть стоимость
                if 2019 - int(self.comboBox_4.currentText()) < 10:
                    global cena
                    if self.comboBox.currentText() == 'Citroen':
                        cen = int(self.lineEdit_17.text())  ## изначальная цена
                        goda = 2019 - int(self.comboBox_4.currentText())
                        cena_for_goda = 10000 * goda
                        probeg = 2000 * (int(self.lineEdit_6.text()) // 1000)
                        if self.comboBox_3.currentText() == "Да":
                            if self.comboBox_5.currentText() == 'идеальное':
                                cen = cen - cena_for_goda - probeg - 50000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'нормальное':
                                cen = cen - cena_for_goda - probeg - 50000 - 10000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'ужасное':
                                cen = cen - cena_for_goda - probeg - 50000 - 30000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                        else:
                            if self.comboBox_5.currentText() == 'идеальное':
                                cen = cen - cena_for_goda - probeg
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'нормальное':
                                cen = cen - cena_for_goda - probeg - 10000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'ужасное':
                                cen = cen - cena_for_goda - probeg - 30000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                    elif self.comboBox.currentText() == 'Opel':
                        cen = int(self.lineEdit_17.text())  ## изначальная цена
                        goda = 2019 - int(self.comboBox_4.currentText())
                        cena_for_goda = 15000 * goda
                        probeg = 4000 * (int(self.lineEdit_6.text()) // 1000)
                        if self.comboBox_3.currentText() == "Да":
                            if self.comboBox_5.currentText() == 'идеальное':
                                cen = cen - cena_for_goda - probeg - 50000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(cen)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'нормальное':
                                cen = cen - cena_for_goda - probeg - 50000 - 15000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'ужасное':
                                cen = cen - cena_for_goda - probeg - 50000 - 35000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                        else:
                            if self.comboBox_5.currentText() == 'идеальное':
                                cen = cen - cena_for_goda - probeg
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'нормальное':
                                cen = cen - cena_for_goda - probeg - 15000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'ужасное':
                                cen = cen - cena_for_goda - probeg - 35000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                    elif self.comboBox.currentText() == 'Volkswagen':
                        cen = int(self.lineEdit_17.text())  ## изначальная цена
                        goda = 2019 - int(self.comboBox_4.currentText())
                        cena_for_goda = 2000 * goda
                        probeg = 1000 * (int(self.lineEdit_6.text()) // 1000)
                        if self.comboBox_3.currentText() == "Да":
                            if self.comboBox_5.currentText() == 'идеальное':
                                cen = cen - cena_for_goda - probeg - 50000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'нормальное':
                                cen = cen - cena_for_goda - probeg - 50000 - 5000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'ужасное':
                                cen = cen - cena_for_goda - probeg - 50000 - 15000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                        else:
                            if self.comboBox_5.currentText() == 'идеальное':
                                cen = cen - cena_for_goda - probeg
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'нормальное':
                                cen = cen - cena_for_goda - probeg - 5000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()
                            elif self.comboBox_5.currentText() == 'ужасное':
                                cen = cen - cena_for_goda - probeg - 15000
                                q = str(abs(cen))
                                self.z = Pokaz_trdea(q)
                                self.z.show()



                else:
                    i, okBtnPressed = QInputDialog.getText(self, "Ошибка",
                                                           "Мы не принимаем машины возростом старше 10 лет")


class Sam(QWidget):
    def __init__(self, Glav_form):
        super().__init__()
        self.Glav_form = Glav_form
        uic.loadUi('data/sravnenie.ui', self)
        self.pushButton.clicked.connect(self.clear)

    def clear(self):
        global sravnenie
        self.Glav_form.listWidget.clear()
        sravnenie.clear()


class Pokaz_trdea(QWidget):
    def __init__(self, cen):
        super().__init__()
        uic.loadUi('data/trade_ob.ui', self)
        self.label_7.setText(cen)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
