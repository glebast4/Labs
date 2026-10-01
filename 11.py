import csv
from tkinter import *
from tkinter import messagebox, filedialog

data = []

def load():
    global data
    path = filedialog.askopenfilename()
    if path == ' ':
        return
    data = []
    f = open(path, encoding="utf-8")
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        data.append(row)
    f.close()

    text_data.delete('1.0', END)
    text_data.insert(END, ', '.join(header) + '\n\n')
    for row in data:
        text_data.insert(END, ', '.join(row) + '\n')
    text_result.delete('1.0', END)
    text_result.insert(END, 'Загружено стр: '+ str(len(data)))

def calc():
    if len(data) == 0:
        messagebox.showwarning('Ошибка', 'Загрузите файл')
        return
    # id - 0 sex - 4 age - 5
    women = []
    ages = []
    for row in data:
        if row[4] == 'female':
            women.append(row)
            if row[5] != '':
                ages.append(float(row[5]))

    ages.sort()
    n = len(ages)
    if n % 2 == 1:
        med = ages[n // 2]
    else:
        med = (ages[n // 2 - 1] + ages[n // 2]) / 2

    step = 10
    left = med - step
    right = med + step

    cnt, alive = 0, 0
    text_data.delete('1.0', END)
    for row in women:
        if row[5] != '':
            age = float(row[5])
            if age >= left and age <= right:
                cnt += 1
                text_data.insert(END, ', '.join(row) + '\n')
                if row[1] == '1':
                    alive += 1
    text_result.delete('1.0', END)
    text_result.insert(END, 'Всего женщин: ' + str(len(women)) + '\n')
    text_result.insert(END, 'Женщин с известным возрастом: ' + str(n) + '\n')
    text_result.insert(END, 'Медиана возраста: ' + str(med) + '\n')
    text_result.insert(END, 'Интервал: от ' + str(left) + ' до ' + str(right) + '\n')
    text_result.insert(END, 'Женщин в интервале: ' + str(cnt)+ '\n')
    text_result.insert(END, 'Из них выжило: ' + str(alive) + '\n')
    text_result.insert(END, 'Из них погибло: ' + str(cnt - alive) + '\n')

wnd = Tk()
wnd.title('Лаб 11 - Титаник')
wnd.geometry('900x600')

loadbutton = Button(wnd, text='Загрузить CSV', command=load)
loadbutton.pack(pady=5)

calcbutton = Button(wnd, text='Вычислить', command=calc)
calcbutton.pack(pady=5)

text_data = Text(wnd, height=20, width=110)
text_data.pack(pady=5)

text_result = Text(wnd, height=9, width=110)
text_result.pack(pady=5)

wnd.mainloop()




