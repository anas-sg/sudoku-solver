import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
import csv

window = tk.Tk()
window.title("Sudoku solver")
style = ttk.Style()
style.configure("Grey.TMenubutton", foreground="brown")
options = [i for i in range(10)]
puzzle = [[0] * 9 for i in range(9)]
grid = [[0] * 9 for i in range(9)]

for i in range(9):
    for j in range(9):
        var = tk.StringVar(window)
        var.set(options[0]) # default value of 0
        if (i // 3) % 2:
            if (j // 3) % 2:
                menu = ttk.OptionMenu(window, var, *options, style="Grey.TMenubutton")
            else:
                menu = ttk.OptionMenu(window, var, *options)
        else:
            if (j // 3) % 2:
                menu = ttk.OptionMenu(window, var, *options)
            else:
                menu = ttk.OptionMenu(window, var, *options, style="Grey.TMenubutton")    
        menu.grid(column=j, row=i)
        grid[i][j] = var, menu
        if i in {2, 5, 8}:
            seph = ttk.Separator(window, orient='horizontal')
            seph.grid(column=j, row=i, sticky="sew")
        if j in {2, 5}:
            sepv = ttk.Separator(window, orient='vertical')
            sepv.grid(column=j, row=i, sticky="ens")

def possible(y, x, n):
    for i in range(9):
        if puzzle[y][i] == n:
            return False
    for i in range(9):
        if puzzle[i][x] == n:
            return False
    x0, y0 = (x//3)*3, (y//3)*3
    for i in range(3):
        for j in range(3):
            if puzzle[y0+i][x0+j] == n:
                return False
    return True

def solve():
    for y in range(9):
        for x in range(9):
            if puzzle[y][x] == 0:
                for n in range(1, 10):
                    if possible(y,x,n):
                        puzzle[y][x] = n
                        solve()
                        puzzle[y][x] = 0
                return
    for i in range(9):
        for j in range(9):
            grid[i][j][0].set(puzzle[i][j])

def get_puzzle():
    for i in range(9):
        for j in range(9):
            puzzle[i][j] = int(grid[i][j][0].get())
    solve()

def clear_grid():
    for i in range(9):
        for j in range(9):
            grid[i][j][0].set(options[0])
            # grid[i][j][1].configure(state="enabled")

def open_csv():
    ftypes = [('CSV files', '*.csv'), ('All files', '*')]
    dialog = tkinter.filedialog.Open(filetypes = ftypes)
    fl = dialog.show()
    with open(fl, newline='') as f:
        txt = list(csv.reader(f))
    for i in range(9):
        for j in range(9):
            try:
                grid[i][j][0].set(int(txt[i][j]))
            except ValueError:
                grid[i][j][0].set(0)

def save():
    ftypes = [('CSV files', '*.csv'), ('All files', '*')]
    dialog = tkinter.filedialog.Open(filetypes = ftypes)
    fl = dialog.show()
    with open(fl, 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONE)
        for i in range(9):
            row = [j[0].get() for j in grid[i]]             
            writer.writerow(row)    

solve_btn = tk.Button(window, text="Solve", command=get_puzzle, bg="green")
solve_btn.grid(column=3, row=9)
reset = tk.Button(window, text="Reset", command=clear_grid, bg="red")
reset.grid(column=5, row=9)

menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Import from CSV", command=open_csv)
filemenu.add_command(label="Save to CSV", command=save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
window.config(menu=menubar)

window.mainloop()