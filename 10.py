import tkinter as tk

field = [' ']*9
buttons = []
gameover = False

lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

def win(zn):
    for a, b,c in lines:
        if field[a] == field[b] == field[c] == zn:
            return True
    return False

def minimax(bot, depth):
    if win("O"):
        return 10 - depth
    if win("X"):
        return depth - 10
    if ' ' not in field:
        return 0

    if bot:
        best = -100
        for i in range(9):
            if field[i] == ' ':
                field[i] = 'O'
                best = max(best, minimax(False, depth + 1))
                field[i] = ' '
        return best
    else:
        worst = 100
        for i in range(9):
            if field[i] == ' ':
                field[i] = 'X'
                worst = min(worst, minimax(True, depth + 1))
                field[i] = ' '
        return worst

def botm():
    bestmove = -1
    bestscore = -100
    for i in range(9):
        if field[i] == ' ':
            field[i] = 'O'
            score = minimax(False, 0)
            field[i] = ' '
            if score > bestscore:
                bestscore = score
                bestmove = i
    field[bestmove] = 'O'
    buttons[bestmove].config(text='O')

def click(i):
    global gameover

    if gameover:
        return

    if field[i] != ' ':
        return
    field[i] = 'X'
    buttons[i].config(text='X')

    if win("X"):
        label.config(text="You win!")
        gameover = True
        return

    if ' ' not in field:
        label.config(text="Tie!")
        gameover = True
        return

    botm()

    if win("O"):
        label.config(text="You lose!")
        gameover = True
    elif ' ' not in field:
        label.config(text="Tie!")
        gameover = True

def newgame():
    global field, gameover
    field = [' ']*9
    gameover = False
    for button in buttons:
        button.config(text=' ')
    label.config(text='Your move')

window = tk.Tk()

for i in range(9):
    b = tk.Button(window, text=' ', width=4, height=2, command=lambda i=i: click(i))
    b.grid(row=i // 3, column=i % 3)
    buttons.append(b)

label = tk.Label(window, text='Your move')
label.grid(row=3, column=0, columnspan=3)
newbutton = tk.Button(window, text='New game', command=newgame)
newbutton.grid(row=4, column=0, columnspan=3)

window.mainloop()