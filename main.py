import tkinter as tk
from tkinter import ttk


class ApplicationWindow:
    def __init__(self, master):
        self.master = master
        self.cell_size = 100
        self.row_no = 5
        self.col_no = 5
        self.m = {}
        self.db = {r: {c: 0 for c in range(1, self.col_no + 1)} for r in range(1, self.row_no + 1)}
        self.db[3][3] = 1
        # print(self.db)

        self.draw_widgets()
        self.draw_squares()
        # self.m['canvas'].after(3000, lambda: self.m['canvas'].itemconfigure('dead', fill='white', state=tk.DISABLED))
        # for i in range(1, 26):
        #     print(self.m['canvas'].gettags(i))

    def draw_widgets(self):
        self.master.option_add('*tearOff', False)
        main_menu = tk.Menu(self.master)
        self.master['menu'] = main_menu
        file_menu = tk.Menu(main_menu)
        main_menu.add_cascade(label='File', menu=file_menu, underline=0)

        control_panel = ttk.Frame(self.master, width=100, height=500, borderwidth=2, relief='solid')
        control_panel.grid(column=0, row=0, sticky='n')
        self.m['canvas'] = tk.Canvas(self.master, width=self.cell_size * self.col_no,
                                     height=self.cell_size * self.row_no, background='green', highlightthickness=1)
        self.m['canvas'].grid(column=1, row=0, sticky='n')

    def draw_squares(self):
        for r in self.db:
            for c in self.db[r]:
                if self.db[r][c] == 1:
                    fill = 'white'
                    status = 'live'
                else:
                    fill = 'grey20'
                    status = 'dead'
                x0 = (c - 1) * self.cell_size
                y0 = (r - 1) * self.cell_size
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                self.m['canvas'].create_rectangle(x0, y0, x1, y1, fill=fill, outline='grey40',
                                                  activefill='red', width=1, tag=(f'{r},{c}', status))
                # # e not used but always created as event, so a new kw parameter n is created which is local to lambda
                self.m['canvas'].tag_bind(f'{r},{c}', '<Button-1>', lambda e, n=(r, c): self.modify_cell(n))

    def modify_cell(self, n):
        r, c = n
        if self.db[r][c] == 1:
            self.db[r][c] = 0
            new_fill = 'grey20'
            new_status = 'dead'
        else:
            self.db[r][c] = 1
            new_fill = 'white'
            new_status = 'live'
        self.m['canvas'].itemconfigure(f'{r},{c}', fill=new_fill, tag=(f'{r},{c}', new_status))
        # print(r, c)
        # print(self.db)


if __name__ == '__main__':
    root = tk.Tk()
    ApplicationWindow(root)
    root.mainloop()
