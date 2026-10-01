import tkinter as tk
from tkinter import filedialog

allowedtypes = ['Жилое', 'Коммерческое', 'Промышленное', 'Сельхоз']
colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']

class contract:
    contracts = [] 
    def __init__(self, number, objecttype, manager, area, term):
        self.number, self.objecttype, self.manager, self.area, self.term = number, objecttype, manager, area, term # атр экземпляра
    def segment(self, field): # вспомог м1
        res = {}
        for i in contract.contracts:
            key = getattr(i, field)
            res[key] = res.get(key, 0) + 1
        return res
    
    def pie(self, data, canvas): # вспомог м2
        canvas.delete('all')
        total, start, x, y = sum(data.values()) or 1, 0, 0, 10
        for key, value in data.items():
            angle = 360 * value / total
            if len(data) == 1:
                canvas.create_oval(20, 20, 300, 300, fill=colors[x % len(colors)])
            else:
                canvas.create_arc(20, 20, 300, 300, start=start, extent=angle, fill=colors[x % len(colors)])
            canvas.create_text(400, y, text=f'{key}: {value} ({round(100*value/total,1)}%)', anchor = 'w')
            start, x, y = start + angle, x + 1, y + 20
    
    def segmenttype(self): # м1
        return self.segment('objecttype')
    def segmentmanager(self): # м3
        return self.segment('manager')
    def typepie(self, canvas): # м2
        self.pie(self.segmenttype(), canvas)
    def managerpie(self, canvas): # м4 
        self.pie(self.segmentmanager(), canvas)

def load():
    path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])
    if not path: return
    contract.contracts.clear()
    for line in open(path, encoding='utf-8'):
        p = line.split()
        if len(p) != 5 or p[1] not in allowedtypes:
            continue
        try:
            p[3], p[4] = float(p[3]), int(p[4])
        except ValueError:
            continue
        if p[3] > 0 and 0 < p[4] <= 49:
            contract.contracts.append(contract(*p))
    status.config(text='Загружено договоров: ' + str(len(contract.contracts)))

c = contract('', '', '', 0, 0) # объект
win = tk.Tk()
win.geometry('650x350')
tk.Button(win, text='Загрузить TXT', command=load).pack()
tk.Button(win, text='Диаграмма по видам', command=lambda: c.typepie(canvas)).pack()
tk.Button(win, text='Диаграмма по менеджерам', command=lambda: c.managerpie(canvas)).pack()
status = tk.Label(win, text='Файл не загружен')
status.pack()
canvas = tk.Canvas(win, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)
win.mainloop()
