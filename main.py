import tkinter as tk
from tkinter import ttk


class ApplicationWindow:
    def __init__(self, master):
        self.master = master
        self.v = {'cell_size': tk.IntVar(value=100), 'row_no': tk.IntVar(value=5), 'col_no': tk.IntVar(value=5)}
        self.m = {}     # this has to be a separate dict from self.v otherwise error
        self.db = {
            r: {c: 0 for c in range(1, self.v['col_no'].get() + 1)} for r in range(1, self.v['row_no'].get() + 1)}
        self.db[3][3] = 1
        # print(self.db)

        self.draw_widgets()
        self.draw_grid()
        # self.m['canvas'].after(3000, lambda: self.m['canvas'].itemconfigure('dead', fill='white', state=tk.DISABLED))
        # for i in range(1, 26):
        #     print(self.m['canvas'].gettags(i))
        # print(self.m)

    def draw_widgets(self):
        def generate_control(parent, name, btn_no, variable):
            gen = [('_u_', 1), ('_d_', 10), ('_h_', 100), ('_k_', 1000)]
            gen_used = gen[btn_no-1::-1]
            col = 0
            for btn, icr in gen_used:
                self.m[name + btn + 'u'] = tk.Button(
                    parent, text='▲', width=1, height=1, command=lambda n=name, i=icr: self.modify_grid(n, i))
                self.m[name + btn + 'd'] = tk.Button(
                    parent, text='▼', width=1, height=1, command=lambda n=name, i=icr: self.modify_grid(n, -i))
                self.m[name + btn + 'u'].grid(column=col, row=0)
                self.m[name + btn + 'd'].grid(column=col, row=2)
                col += 1
                self.m[name + '_label'] = ttk.Label(parent, textvariable=variable, font='helvetica 24')
                self.m[name + '_label'].grid(column=0, row=1, columnspan=btn_no, sticky='e')

        control_panel = ttk.Frame(self.master, relief='solid', padding=6)
        control_panel.grid(column=0, row=0, sticky='n, s')

        controls_label = ttk.Label(control_panel, text='Controls:')
        play_button = ttk.Button(control_panel, text='Play')
        pause_button = ttk.Button(control_panel, text='Pause')
        parameters_label = ttk.Label(control_panel, text='Grid parameters:')
        cell_label = ttk.Label(control_panel, text='Cell size:')
        cell_controls = ttk.Frame(control_panel)
        row_label = ttk.Label(control_panel, text='Number of rows:')
        row_controls = ttk.Frame(control_panel)
        col_label = ttk.Label(control_panel, text='Number of columns:')
        col_controls = ttk.Frame(control_panel)
        controls_label.grid(column=0, row=0, pady=5)
        play_button.grid(column=0, row=1, pady=2)
        pause_button.grid(column=0, row=2, pady=2)
        parameters_label.grid(column=0, row=3, pady=5)
        cell_label.grid(column=0, row=4)
        cell_controls.grid(column=0, row=5, sticky='e')
        row_label.grid(column=0, row=6)
        row_controls.grid(column=0, row=7, sticky='e')
        col_label.grid(column=0, row=8)
        col_controls.grid(column=0, row=9, sticky='e')

        generate_control(cell_controls, 'cell_size', 3, self.v['cell_size'])
        generate_control(row_controls, 'row_no', 4, self.v['row_no'])
        generate_control(col_controls, 'col_no', 4, self.v['col_no'])

    def draw_grid(self):
        self.m['canvas'] = tk.Canvas(self.master, width=self.v['cell_size'].get() * self.v['col_no'].get(),
                                     height=self.v['cell_size'].get() * self.v['row_no'].get(), background='green',
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
                x0 = (c - 1) * self.v['cell_size'].get()
                y0 = (r - 1) * self.v['cell_size'].get()
                x1 = c * self.v['cell_size'].get()
                y1 = r * self.v['cell_size'].get()
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

    def modify_grid(self, parameter, increment):
        if parameter == 'cell_size' and 0 < self.v['cell_size'].get() + increment < 301:
            self.v['cell_size'].set(self.v['cell_size'].get() + increment)
        elif parameter == 'row_no' and 0 < self.v['row_no'].get() + increment < 1002:
            length = len(self.db)
            if increment > 0:
                for d in range(increment):
                    self.db[length + d + 1] = {c: 0 for c in range(1, self.v['col_no'].get() + 1)}
            else:
                absolute = abs(increment)
                for d in range(absolute):
                    self.db.pop(length - d, None)
            self.v['row_no'].set(self.v['row_no'].get() + increment)
        elif parameter == 'col_no' and 0 < self.v['col_no'].get() + increment < 1002:
            length = len(self.db[1])
            if increment > 0:
                for r in self.db:
                    for d in range(increment):
                        self.db[r][length + d + 1] = 0
            else:
                absolute = abs(increment)
                for r in self.db:
                    for d in range(absolute):
                        self.db[r].pop(length - d, None)
            self.v['col_no'].set(self.v['col_no'].get() + increment)
        self.m['canvas'].destroy()
        self.draw_grid()


if __name__ == '__main__':
    root = tk.Tk()
    ApplicationWindow(root)
    root.mainloop()
