from tkinter import *
from jeuPak import *


root = Tk()
root.title("MarwenJeuLife")
frame = Frame(root, width=800, height=800)
frame.pack()
canvas = Canvas(frame, width=500, height=500)
canvas.pack()


def table():
    x = 10
    y = 10
    global g 
    global rec 
    rec = []
    g = []
    for i in range(70):
        g.append([])
        rec.append([])
        for j in range(70):
            rect = canvas.create_rectangle(x, y, x+10, y+10, fill="white")
            rec[i].append(rect)
            g[i].append(Cell(x, y, i, j))
            x += 10
        x = 10
        y += 10


def clik_xy(x, y):

    return (int(x- x%10), int(y - y%10))


def whi_to_blk(event):

    #print (event.x, event.y)
    x, y = clik_xy(event.x, event.y)
    try:
        iy =int( x / 10 ) - 1
        ix = int(y / 10) - 1
        if ix == -1 or iy == -1:
            raise IndexError
        if g[ix][iy].isAlive:
            canvas.itemconfig(rec[ix][iy], fill="white")
        else:
            canvas.itemconfig(rec[ix][iy], fill="black")
        g[ix][iy].switchStatus()
        #print (g[ix][iy].pos_matrix, g[ix][iy].pos_screen)
    except IndexError:
        return


def paint_grid():
    for i in g:
        for j in i:
            if j.nextStatus != j.isAlive:
                x, y = j.pos_matrix
                #print (x, y)
                if j.nextStatus:
                    canvas.itemconfig(rec[x][y], fill="black")
                    #print ("changed", j.pos_matrix, "from dead to alive")
                else:
                    canvas.itemconfig(rec[x][y], fill="white")
                    #print ("changed", j.pos_matrix, "from alive to dead")
                j.switchStatus()
                #print ("Current status of", j.pos_matrix, j.isAlive)


def changeInStatus(cell):
    ''' If the cell's status changes in the next gen, return True else False '''
    num_alive = 0
    x, y = cell.pos_matrix
    for i in (x-1, x, x+1):
        for j in (y-1, y, y+1):
            if i == x and j == y:
                continue
            if i == -1 or j == -1:
                continue
            try:
                if g[i][j].isAlive:
                    num_alive += 1
            except IndexError:
                pass
    if cell.isAlive:
        return not( num_alive == 2 or num_alive == 3 )
    else:
        return num_alive == 3


def gogame():
    for i in g:
        for j in i:
            if changeInStatus(j):
                j.nextStatus = not j.isAlive
                #print ("change in", j.pos_matrix, "from", j.isAlive, "to", j.nextStatus)
            else:
                j.nextStatus = j.isAlive
    paint_grid()
    global begin_id
    begin_id = root.after(200, gogame)


def arretgame():
    root.after_cancel(begin_id)

table()
start = Button(root, text="Goooo Marwen :p ", command=gogame)
start.pack(side = LEFT)
stop = Button(root, text="Arret Marwen !!!!!", command = arretgame)
stop.pack(side = RIGHT)
canvas.bind("<Button-1>", whi_to_blk)
root.mainloop()
