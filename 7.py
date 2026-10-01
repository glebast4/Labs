import tkinter as tk
from tkinter import messagebox, scrolledtext

import itertools, timeit
#1
def alg_schedule(n):
    pairs = []
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            pairs.append((i,j))
    def permutations(pairs, size):
        if size == 1:
            yield tuple(pairs)
            return
        for i in range(size):
            yield from permutations(pairs, size - 1)
            if size % 2 == 1:
                pairs[0], pairs[size - 1] = pairs[size - 1], pairs[0]
            else:
                pairs[i], pairs[size - 1] = pairs[size - 1], pairs[i]
    return permutations(pairs, len(pairs))

def py_schedule(n):
    return itertools.permutations(list(itertools.combinations(range(1, n+1), 2)))

def bench(n, repeats=10_000):
    alg = timeit.timeit(lambda: alg_schedule(n), number=repeats)
    py = timeit.timeit(lambda: py_schedule(n), number=repeats)
    print("\nЗамеры и сравнение")
    print(f" Алгоритмический: {alg} сек.")
    print(f" Itertools: {py} сек.")
    fast = "Itertools" if py < alg else "Алгоритмический"
    print(f" Быстрее: {fast}")

#2
def constraint(schedule): #(1, 2) играют в первой половине
    half = len(schedule) // 2
    for i in range(half):
        if schedule[i] == (1, 2):
            return True
    return False

def max_gap(schedule, n):
    worst = 0
    for i in range(1, n+1):
        rounds = [j for j, pair in enumerate(schedule) if i in pair]
        if len(rounds) > 1:
            gaps = [rounds[x+1] - rounds[x] for x in range(len(rounds) -1)]
            worst = max(worst, max(gaps))
    return worst

def opt_schedule(n):
    best = None
    best_score = float('inf')
    for schedule in alg_schedule(n):
        if not constraint(schedule):
            continue
        score = max_gap(schedule, n)
        if score < best_score:
            best_score = score
            best = schedule
    return best, best_score

def main():
    n = 3
    print("1 часть")
    print('\n'.join(str(i) for i in alg_schedule(n)))
    bench(n)

root = tk.Tk()
root.title("Расписания шахматных турниров")

def get_n():
    try:
        n = int(entry_n.get())
        if n < 2:
            raise ValueError
        return n
    except ValueError:
        messagebox.showerror("Ошибка", "N>2")
        return None
    
def run():
    n = get_n()
    if n is None:
        return
    best, score = opt_schedule(n)
    output.config(state="normal")
    output.delete("1.0", "end")
    if best:
        output.insert("end", "Ограничение: (1, 2) играют в первой половине\n")
        output.insert("end", f"Max перерыв между партиями одного игрока: {score}\n\n")
        for i, (a, b) in enumerate(best, 1):
            output.insert("end", f"{i}) {a} x {b}\n")
    else:
        output.insert("end", "Расписаний удовлетворяющих ограничению нет")
    output.config(state="disabled")

tk.Label(root, text="Колво шахматистов:").pack(padx=10, pady=(10,0))
entry_n = tk.Entry(root, width=5)
entry_n.insert(0, "3")
entry_n.pack(pady=4)

tk.Button(root, text="Найти расписания", command=run).pack(padx=10, pady=4)
output = scrolledtext.ScrolledText(root, width=50, height=15, font=("Courier New", 10), state="disabled")
output.pack(padx=10, pady=(0,10))

root.update_idletasks()
w = root.winfo_width()
h = root.winfo_height()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

if __name__ == "__main__":
    #main()
    root.mainloop()
