import tkinter as tk
from tkinter import ttk
import time


class ApplicationWindow:
    def __init__(self, master):
        self.master = master
        self.v = {'cell_size': tk.IntVar(value=10), 'row_no': tk.IntVar(value=40), 'col_no': tk.IntVar(value=40)}
        self.m = {}     # this has to be a separate dict from self.v otherwise error
        self.db = {
            r: {c: 0 for c in range(1, self.v['col_no'].get() + 1)} for r in range(1, self.v['row_no'].get() + 1)}
        self.valid_coordinates = [str(r) + ',' + str(c) for r in self.db for c in self.db[r]]
        self.play_going = True
        self.currently_selected = tk.StringVar()

        # glider
        self.db[1][1] = 1
        self.db[2][2] = 1
        self.db[2][3] = 1
        self.db[3][1] = 1
        self.db[3][2] = 1

        self.draw_widgets()
        self.draw_grid()
        # self.m['canvas'].after(1000, lambda: self.m['canvas'].itemconfigure('dead', fill='white', state=tk.DISABLED))

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
        play_button = ttk.Button(control_panel, text='Play', command=self.play_loop)
        pause_button = ttk.Button(control_panel, text='Pause', command=self.pause_loop)
        next_button = ttk.Button(control_panel, text='Next', command=self.iterate)
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
        next_button.grid(column=0, row=3, pady=2)
        parameters_label.grid(column=0, row=4, pady=5)
        cell_label.grid(column=0, row=5)
        cell_controls.grid(column=0, row=6, sticky='e')
        row_label.grid(column=0, row=7)
        row_controls.grid(column=0, row=8, sticky='e')
        col_label.grid(column=0, row=9)
        col_controls.grid(column=0, row=10, sticky='e')

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
            self.valid_coordinates = [str(r) + ',' + str(c) for r in self.db for c in self.db[r]]
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
            self.valid_coordinates = [str(r) + ',' + str(c) for r in self.db for c in self.db[r]]
        self.m['canvas'].destroy()
        self.draw_grid()

    def iterate(self):
        def nb_count(r, c):
            neighbour_rel = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            neighbours = 0
            for rel in neighbour_rel:
                row_rel, col_rel = rel
                if str(r + row_rel) + ',' + str(c + col_rel) in self.valid_coordinates:
                    neighbours += self.db[r + row_rel][c + col_rel]
            return neighbours

        def cell_outcome(r, c):
            if self.db[r][c] == 1:
                if nb_db[r][c] == 2 or nb_db[r][c] == 3:
                    return 1
                else:
                    return 0
            else:
                if nb_db[r][c] == 3:
                    return 1
                else:
                    return 0

        nb_db = {r: {c: nb_count(r, c) for c in self.db[r]} for r in self.db}
        self.db = {r: {c: cell_outcome(r, c) for c in self.db[r]} for r in self.db}
        for r in self.db:
            for c in self.db[r]:
                if self.db[r][c] == 1:
                    new_fill = 'white'
                    new_status = 'live'
                else:
                    new_fill = 'grey20'
                    new_status = 'dead'
                self.m['canvas'].itemconfigure(f'{r},{c}', fill=new_fill, tag=(f'{r},{c}', new_status))

    def play_loop(self):
        self.play_going = True
        while self.play_going:
            self.iterate()
            self.master.after(10, lambda: self.currently_selected.set('demo'))
            self.m['canvas'].wait_variable(self.currently_selected)

    def pause_loop(self):
        self.play_going = False


if __name__ == '__main__':
    root = tk.Tk()
    ApplicationWindow(root)
    root.mainloop()
