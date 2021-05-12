import tkinter as tk
from tkinter import ttk


class ApplicationWindow:
    def __init__(self, master):
        self.master = master
        self.cell_size = 50
        self.row_no = 10
        self.col_no = 10
        self.db = {i: {j: 0 for j in range(1, self.col_no + 1)} for i in range(1, self.row_no + 1)}
        # print(self.db)

        self.master.option_add('*tearOff', False)
        main_menu = tk.Menu(self.master)
        self.master['menu'] = main_menu
        file_menu = tk.Menu(main_menu)
        main_menu.add_cascade(label='File', menu=file_menu, underline=0)

        control_panel = ttk.Frame(self.master, width=100, height=500, borderwidth=2, relief='solid')
        control_panel.grid(column=0, row=0, sticky='n')
        self.main_canvas = tk.Canvas(self.master, width=self.cell_size * self.col_no,
                                     height=self.cell_size * self.row_no, background='green', highlightthickness=1)
        self.main_canvas.grid(column=1, row=0, sticky='n')

        self.draw_squares()

    def draw_squares(self):
        for i in self.db:
            for j in self.db[i]:
                # print(i, j)
                x0 = (j - 1) * self.cell_size
                y0 = (i - 1) * self.cell_size
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                self.main_canvas.create_rectangle(x0, y0, x1, y1, fill='white', outline='black',
                                                  activefill='red', width=1, tag=(i, j))
                # # e not used but always created as event, so a new kw parameter n is created which is local to lambda
                # self.main_canvas.tag_bind((i, j), '<Button-1>', lambda e, n=(i, j): later_method(n))


if __name__ == '__main__':
    root = tk.Tk()
    ApplicationWindow(root)
    root.mainloop()
