import tkinter as tk
from tkinter import ttk


class ApplicationWindow:
    def __init__(self, master):
        self.master = master
        self.cell_size = tk.IntVar(value=100)
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
        # self.master.option_add('*tearOff', False)
        # main_menu = tk.Menu(self.master)
        # self.master['menu'] = main_menu
        # file_menu = tk.Menu(main_menu)
        # main_menu.add_cascade(label='File', menu=file_menu, underline=0)

        control_panel = ttk.Frame(self.master, width=100, height=500, borderwidth=2, relief='solid')
        control_panel.grid(column=0, row=0, sticky='n, s')
        controls_label = ttk.Label(control_panel, text='Controls:')
        controls_label.grid(column=0, row=0, pady=5, padx=5)
        play_button = ttk.Button(control_panel, text='Play')
        pause_button = ttk.Button(control_panel, text='Pause')
        play_button.grid(column=0, row=1, pady=2, padx=5)
        pause_button.grid(column=0, row=2, pady=2, padx=5)
        prm_label = ttk.Label(control_panel, text='Grid parameters:')
        prm_label.grid(column=0, row=3, pady=5, padx=5)

        cell_label = ttk.Label(control_panel, text='Cell size')
        cell_label.grid(column=0, row=4, pady=0, padx=5)
        cell_frame = ttk.Frame(control_panel)
        cell_frame.grid(column=0, row=5, sticky='e', padx=5)

        cell_h_u = tk.Button(cell_frame, text='▲', width=1, height=1, command=lambda: self.modify_cell_size(100))
        cell_h_u.grid(column=0, row=0)
        cell_d_u = tk.Button(cell_frame, text='▲', width=1, height=1, command=lambda: self.modify_cell_size(10))
        cell_d_u.grid(column=1, row=0)
        cell_u_u = tk.Button(cell_frame, text='▲', width=1, height=1, command=lambda: self.modify_cell_size(1))
        cell_u_u.grid(column=2, row=0)

        cell_size_label = ttk.Label(cell_frame, textvariable=self.cell_size, font='helvetica 24')
        cell_size_label.grid(column=0, row=1, columnspan=3, sticky='e')

        cell_h_d = tk.Button(cell_frame, text='▼', width=1, height=1, command=lambda: self.modify_cell_size(-100))
        cell_h_d.grid(column=0, row=2)
        cell_d_d = tk.Button(cell_frame, text='▼', width=1, height=1, command=lambda: self.modify_cell_size(-10))
        cell_d_d.grid(column=1, row=2)
        cell_u_d = tk.Button(cell_frame, text='▼', width=1, height=1, command=lambda: self.modify_cell_size(-1))
        cell_u_d.grid(column=2, row=2)

    def draw_squares(self):
        self.m['canvas'] = tk.Canvas(self.master, width=self.cell_size.get() * self.col_no,
                                     height=self.cell_size.get() * self.row_no, background='green',
                                     highlightthickness=1)
        self.m['canvas'].grid(column=1, row=0, sticky='n')
        for r in self.db:
            for c in self.db[r]:
                if self.db[r][c] == 1:
                    fill = 'white'
                    status = 'live'
                else:
                    fill = 'grey20'
                    status = 'dead'
                x0 = (c - 1) * self.cell_size.get()
                y0 = (r - 1) * self.cell_size.get()
                x1 = c * self.cell_size.get()
                y1 = r * self.cell_size.get()
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

    def modify_cell_size(self, increment):
        if self.cell_size.get() + increment > 0:
            self.cell_size.set(self.cell_size.get() + increment)
        self.m['canvas'].destroy()
        self.draw_squares()


if __name__ == '__main__':
    root = tk.Tk()
    ApplicationWindow(root)
    root.mainloop()
