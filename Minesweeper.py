from tkinter import *
from tkinter import ttk
import random


def mouse_in(i, j):
    buttons[i][j].focus()
    buttons[i][j].bind('<ButtonRelease-1>', lambda x: click(i, j))
    buttons[i][j].bind('<space>', lambda x: space(i, j))
    buttons[i][j].bind('<ButtonRelease-3>', lambda x: space(i, j))


def mouse_out(i, j):
    mainframe.focus()
    buttons[i][j].unbind('<ButtonRelease-1>')
    buttons[i][j].unbind('<space>')
    buttons[i][j].unbind('<ButtonRelease-3>')


def click(i, j):
    global mines
    if not mines:
        mines = plant_mines(30, 16, i, j)
        update_timer()

    if buttons[i][j].instate(['disabled']) or buttons[i][j]['text'] == 'F':
        pass
    elif no_of_mines(i, j) == 0:
        open_square(i, j)
    else:
        if [i, j] in mines:
            game_over()
        else:
            buttons[i][j]['text'] = str(no_of_mines(i, j))
            global cells
            cells += 1
            if cells == 381:
                game_won()
        buttons[i][j].state(['disabled'])


def space(i, j):
    if buttons[i][j].instate(['disabled']):
        if str(buttons[i][j]['text']) == str(no_of_flags(i, j)):
            open_square(i, j)
    else:
        global mines_remaining
        if buttons[i][j]['text'] == 'F':
            buttons[i][j]['text'] = ''
            mines_remaining += 1
            remaining['text'] = str(mines_remaining)
            flags.remove([i, j])
        else:
            buttons[i][j]['text'] = 'F'
            mines_remaining -= 1
            remaining['text'] = str(mines_remaining)
            flags.append([i, j])


def plant_mines(a, b, i, j):
    my_list = []
    k = 0
    while k < 99:
        x = random.randrange(0, a)
        y = random.randrange(0, b)
        if [x, y] in my_list:
            continue
        if abs(x-i) <= 1 and abs(y-j) <= 1:
            continue
        else:
            my_list.append([x, y])
            k += 1
    return my_list


def no_of_mines(i, j):
    count = 0
    for iter1 in range(3):
        for iter2 in range(3):
            if [i+iter1-1, j+iter2-1] in mines:
                count += 1
    return count


def no_of_flags(i, j):
    count1 = 0
    for iter5 in range(3):
        for iter6 in range(3):
            if 0 > i+iter5-1 or i+iter5-1 > 29 or 0 > j+iter6-1 or j+iter6-1 > 15:
                continue
            elif buttons[i+iter5-1][j+iter6-1]['text'] == 'F':
                count1 += 1
    return count1


def open_square(i, j):
    for iter3 in range(3):
        for iter4 in range(3):
            if 0 > i+iter3-1 or i+iter3-1 > 29 or 0 > j+iter4-1 or j+iter4-1 > 15:
                continue
            elif buttons[i+iter3-1][j+iter4-1]['text'] != 'F' and buttons[i+iter3-1][j+iter4-1]['text'] != 'X':
                if [i+iter3-1, j+iter4-1] not in mines and no_of_mines(i+iter3-1, j+iter4-1) != 0:
                    buttons[i+iter3-1][j+iter4-1]['text'] = no_of_mines(i+iter3-1, j+iter4-1)
                    if buttons[i+iter3-1][j+iter4-1].instate(['!disabled']):
                        global cells
                        cells += 1
                        if cells == 381:
                            game_won()
                elif [i+iter3-1, j+iter4-1] in mines:
                    game_over()
                buttons[i+iter3-1][j+iter4-1].state(['disabled'])

            if no_of_mines(i+iter3-1, j+iter4-1) == 0:
                if [i+iter3-1, j+iter4-1] not in zeroes:
                    cells += 1
                    if cells == 381:
                        game_won()
                    zeroes.append([i+iter3-1, j+iter4-1])
                    open_square(i+iter3-1, j+iter4-1)


def update_timer():
    global time1, callback
    time1 += 1
    timer['text'] = str(int(time1))
    callback = root.after(1000, update_timer)


def game_won():
    root.after_cancel(callback)
    for iter9 in range(30):
        for iter10 in range(16):
            buttons[iter9][iter10].unbind('<Enter>')
            buttons[iter9][iter10].unbind('<Leave>')
    for mine in mines:
        if buttons[mine[0]][mine[1]]['text'] != 'F':
            buttons[mine[0]][mine[1]]['text'] = 'F'
    message_box['text'] = 'You win!'


def game_over():
    root.after_cancel(callback)
    for iter11 in range(30):
        for iter12 in range(16):
            buttons[iter11][iter12].unbind('<Enter>')
            buttons[iter11][iter12].unbind('<Leave>')
    for mine in mines:
        if buttons[mine[0]][mine[1]]['text'] != 'F':
            buttons[mine[0]][mine[1]]['text'] = 'M'
            buttons[mine[0]][mine[1]].state(['disabled'])
    for flag in flags:
        if flag not in mines:
            buttons[flag[0]][flag[1]]['text'] = 'X'
    message_box['text'] = 'You lose!'


def new_game(*args):
    global buttons, flags, mines, cells, zeroes, mines_remaining, time1, message

    root.after_cancel(callback)
    flags = []
    mines = []
    cells = 0
    zeroes = []
    mines_remaining = 99
    time1 = -1
    message = 'New game'

    remaining['text'] = str(mines_remaining)
    message_box['text'] = message
    timer['text'] = '0'

    for iter13 in range(30):
        for iter14 in range(16):
            buttons[iter13][iter14]['text'] = ''
            buttons[iter13][iter14].state(['!disabled'])
            buttons[iter13][iter14].bind('<Enter>', lambda event, iter13=iter13, iter14=iter14: mouse_in(iter13, iter14))
            buttons[iter13][iter14].bind('<Leave>', lambda event, iter13=iter13, iter14=iter14: mouse_out(iter13, iter14))


buttons = []
flags = []
mines = []
cells = 0
zeroes = []
mines_remaining = 99
time1 = -1
message = 'New game'

root = Tk()
root.minsize(660, 425)
root.title("Minesweeper")

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

remaining = ttk.Label(mainframe, text=str(mines_remaining))
remaining.grid(column=0, row=0, columnspan=2)

message_box = ttk.Button(mainframe, text=message, command=new_game)
message_box.grid(column=12, row=0, columnspan=6)

timer = ttk.Label(mainframe, text='0')
timer.grid(column=28, row=0, columnspan=2)

for iter7 in range(30):
    buttons.append([])
    for iter8 in range(16):
        buttons[iter7].append(ttk.Button(mainframe, width=2))
        buttons[iter7][iter8].grid(column=iter7, row=iter8+1)
        buttons[iter7][iter8].bind('<Enter>', lambda event, iter7=iter7, iter8=iter8: mouse_in(iter7, iter8))
        buttons[iter7][iter8].bind('<Leave>', lambda event, iter7=iter7, iter8=iter8: mouse_out(iter7, iter8))

root.bind('<F2>', new_game)

root.mainloop()
