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
        # self.m['canvas'].after(3000, lambda: self.m['canvas'].delete('all'))
        # for i in range(1, 26):
        #     print(self.m['canvas'].gettags(i))
        self.master.bind('<<Increment>>', lambda e: print('incr'))
        self.master.bind('<<Decrement>>', lambda e: print('decr'))
        self.master.bind('<<MyOwnEvent>>', lambda e: print('cell_d'))

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
        cell_frame.grid(column=0, row=5, sticky='e')

        self.m['cell_d'] = tk.IntVar(value=1)
        self.m['cell_u'] = tk.IntVar(value=9)
        cell_d = ttk.Spinbox(cell_frame, from_=0.0, to=9.0, width=2, textvariable=self.m['cell_d'], command=lambda: self.master.event_generate("<<MyOwnEvent>>"))
        cell_d.grid(column=0, row=0, pady=0, padx=1)
        cell_u = ttk.Spinbox(cell_frame, from_=0.0, to=9.0, width=2, textvariable=self.m['cell_u'])
        cell_u.grid(column=1, row=0, pady=0, padx=1)

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
