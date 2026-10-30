import csv
import sqlite3
from tkinter import *
from tkinter import messagebox, filedialog

fields = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age",
          "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]

conn = sqlite3.connect('titanic.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS passengers (
    PassengerId INTEGER PRIMARY KEY,
    Survived INTEGER,
    Pclass INTEGER,
    Name TEXT,
    Sex TEXT,
    Age REAL,
    SibSp INTEGER,
    Parch INTEGER,
    Ticket TEXT,
    Fare REAL,
    Cabin TEXT,
    Embarked TEXT)""")
conn.commit()

def showrows(rows):
    text_db.delete('1.0', END)
    text_db.insert(END, str(fields) + "\n")
    for row in rows:
        text_db.insert(END, str(row) + "\n")

def showresult(text):
    text_result.delete('1.0', END)
    text_result.insert(END, text)

def clearfields():
    for i in entries:
        i.delete(0, END)

def opencsv():
    path = filedialog.askopenfilename()
    if path == '':
        return
    f = open(path, encoding="utf-8")
    reader = csv.reader(f)
    next(reader)
    rows = []
    for row in reader:
        if len(row) != 12:
            messagebox.showerror("Ошибка", "Нужен titanic.csv")
            f.close()
            return
        newrow = []
        for i in row:
            if i == '':
                newrow.append(None)
            else:
                newrow.append(i)
        rows.append(newrow)
    f.close()

    cur.executemany("INSERT OR REPLACE INTO passengers VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", rows)
    conn.commit()
    showdb()
    showresult("Импортировано записей: " + str(len(rows)))

def showdb():
    cur.execute("SELECT * FROM passengers")
    rows = cur.fetchall()
    showrows(rows)
    showresult("Записей в бд: " + str(len(rows)))

def calc():
    step = 10

    cur.execute("SELECT COUNT(*) FROM passengers WHERE Sex = 'female'")
    allwomen = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE Sex = 'female' AND Age IS NOT NULL")
    n = cur.fetchone()[0]
    if n == 0:
        messagebox.showwarning("Нет данных", "Нет женщин с известным возрастом")
        return
    if n % 2 == 1:
        cur.execute("SELECT Age FROM passengers WHERE Sex = 'female' AND Age IS NOT NULL "
                    "ORDER BY Age LIMIT 1 OFFSET ?", (n // 2,))
    else:

        cur.execute("SELECT AVG(Age) FROM (SELECT Age FROM passengers "
                    "WHERE Sex = 'female' AND Age IS NOT NULL "
                    "ORDER BY Age LIMIT 2 OFFSET ?)", (n // 2 - 1,))
    med = cur.fetchone()[0]

    left = med - step
    right = med + step

    cur.execute("SELECT COUNT(*), SUM(Survived) FROM passengers "
                "WHERE Sex = 'female' AND Age BETWEEN ? AND ?", (left, right))
    count, alive = cur.fetchone()
    if alive is None:
        alive = 0

    showresult("Всего женщин: " + str(allwomen) + "\n"
                + "Женщин с известным возрастом: " + str(n) + "\n"
                + "Медиана возраста: " + str(med) + "\n"
                + "Интервал: от " + str(left) + " до " + str(right) + "\n"
                + "Женщин в интервале: " + str(count) + "\n"
                + "Из них выжило: " + str(alive) + "\n"
                + "Из них погибло: " + str(count - alive))
    cur.execute("SELECT * FROM passengers WHERE Sex = 'female' AND Age BETWEEN ? AND ?", (left, right))
    showrows(cur.fetchall())

def addrecord():
    values = []
    for e in entries:
        s = e.get().strip()
        if s == "":
            values.append(None)
        else:
            values.append(s)
    if values[0] is None:
        messagebox.showwarning("Ошибка", "Заполните PassengerId")
        return
    try:
        cur.execute("INSERT INTO passengers VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", values)
        conn.commit()
    except sqlite3.Error:
        messagebox.showerror("Ошибка", "Такой PassengerId уже есть или данные неверные")
        return
    showdb()
    showresult("Запись добавлена")

def gorecord():
    id = entries[0].get().strip()
    cur.execute("SELECT * FROM passengers WHERE PassengerId = ?", (id,))
    row = cur.fetchone()
    if row is None:
        messagebox.showwarning("Не найдено", "Такой записи нет")
        return
    for i in range(12):
        entries[i].delete(0, END)
        if row[i] is not None:
            entries[i].insert(0, str(row[i]))
    showrows([row])
    showresult("Показана запись " + id)

def editrecord():
    values = []
    for e in entries:
        s = e.get().strip()
        if s == "":
            values.append(None)
        else:
            values.append(s)
    if values[0] is None:
        messagebox.showwarning("Ошибка", "Заполните PassengerId")
        return
    cur.execute("UPDATE passengers SET Survived = ?, Pclass = ?, Name = ?, Sex = ?, Age = ?, "
                "SibSp = ?, Parch = ?, Ticket = ?, Fare = ?, Cabin = ?, Embarked = ? "
                "WHERE PassengerId = ?", values[1:] + [values[0]])
    conn.commit()
    if cur.rowcount == 0:
        messagebox.showwarning("Не найдено", "Такой записи нет")
        return
    showdb()
    showresult("Запись изменена")

def deleterecord():
    id = entries[0].get().strip()
    if id == "":
        messagebox.showwarning("Ошибка", "Заполните PassengerId")
        return
    if not messagebox.askyesno("Удаление", "Удалить запись " + id + "?"):
        return
    cur.execute("DELETE FROM passengers WHERE PassengerId = ?", (id,))
    conn.commit()
    if cur.rowcount == 0:
        messagebox.showwarning("Не найдено", "Такой записи нет")
        return
    showdb()
    showresult("Запись удалена")

def search():
    # адаптивный поиск: способ сравнения зависит от типа поля
    where = []
    params = []
    for i in range(12):
        name = fields[i]
        s = entries[i].get().strip()
        if s == "":
            continue

        if name == "Name" or name == "Ticket" or name == "Cabin":
            # длинный текст: ищем часть слова, регистр не важен
            where.append(name + " LIKE ?")
            params.append("%" + s + "%")

        elif name == "Sex" or name == "Embarked":
            # короткий текст: точное совпадение, регистр не важен
            where.append(name + " = ? COLLATE NOCASE")
            params.append(s)

        elif name == "PassengerId" and s.isdigit():
            # номер: ищем все номера, которые НАЧИНАЮТСЯ с введённых цифр (1 -> 1, 10-19, 100-199)
            where.append("CAST(PassengerId AS TEXT) LIKE ?")
            params.append(s + "%")

        else:
            # число: можно написать 30, >30, >=30, <30, <=30 или диапазон 20-40
            op = "="
            text = s
            for o in [">=", "<=", ">", "<", "="]:
                if s.startswith(o):
                    op = o
                    text = s[len(o):].strip()
                    break
            try:
                if op == "=" and "-" in text[1:]:
                    a, b = text.split("-")
                    a = float(a)
                    b = float(b)
                    if a > b:
                        a, b = b, a
                    where.append(name + " BETWEEN ? AND ?")
                    params.append(a)
                    params.append(b)
                else:
                    where.append(name + " " + op + " ?")
                    params.append(float(text))
            except ValueError:
                showresult("Неверное значение в поле " + name + ": " + s)
                return

    sql = "SELECT * FROM passengers"
    if len(where) > 0:
        sql = sql + " WHERE " + " AND ".join(where)
    cur.execute(sql, params)
    rows = cur.fetchall()
    showrows(rows)
    showresult("Найдено записей: " + str(len(rows)))

def keysearch(event):
    # вызывается при вводе в любое поле, если стоит галочка
    if live.get() == 1:
        search()

def cleardb():
    if not messagebox.askyesno("Очистка", "Удалить все?"):
        return
    cur.execute("DELETE FROM passengers")
    conn.commit()
    showrows([])
    showresult("бд очищена")

window = Tk()
window.title("Лаб 12 - Титаник")
window.geometry("1100x700")

frame_buttons = Frame(window)
frame_buttons.pack(pady=5)
Button(frame_buttons, text="Импорт CSV", width=20, command=opencsv).grid(row=0, column=0, padx=3, pady=3)
Button(frame_buttons, text="Просмотр БД", width=20, command=showdb).grid(row=0, column=1, padx=3, pady=3)
Button(frame_buttons, text="Вычислить", width=20, command=calc).grid(row=0, column=2, padx=3, pady=3)
Button(frame_buttons, text="Ввести запись", width=20, command=addrecord).grid(row=0, column=3, padx=3, pady=3)
Button(frame_buttons, text="Перейти к записи", width=20, command=gorecord).grid(row=0, column=4, padx=3, pady=3)
Button(frame_buttons, text="Редактировать запись", width=20, command=editrecord).grid(row=1, column=0, padx=3, pady=3)
Button(frame_buttons, text="Удалить запись", width=20, command=deleterecord).grid(row=1, column=1, padx=3, pady=3)
Button(frame_buttons, text="Поиск по полям", width=20, command=search).grid(row=1, column=2, padx=3, pady=3)
Button(frame_buttons, text="Очистить бд", width=20, command=cleardb).grid(row=1, column=3, padx=3, pady=3)
Button(frame_buttons, text="Очистить поля", width=20, command=clearfields).grid(row=1, column=4, padx=3, pady=3)

# галочка: искать сразу при вводе
live = IntVar(value=1)
Checkbutton(frame_buttons, text="Искать при вводе", variable=live).grid(row=2, column=0, columnspan=2)

text_db = Text(window, height=20, width=140)
text_db.pack(pady=5)

frame_fields = Frame(window)
frame_fields.pack(pady=5)
entries = []
for i in range(12):
    Label(frame_fields, text=fields[i]).grid(row=(i // 6) * 2, column=i % 6)
    e = Entry(frame_fields, width=22)
    e.grid(row=(i // 6) * 2 + 1, column=i % 6, padx=3)
    e.bind("<KeyRelease>", keysearch)
    entries.append(e)

text_result = Text(window, height=9, width=140)
text_result.pack(pady=5)

window.mainloop()
