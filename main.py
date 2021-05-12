import tkinter as tk


class ApplicationWindow:
    def __init__(self, master):
        self.master = master


if __name__ == '__main__':
    root = tk.Tk()
    ApplicationWindow(root)
    root.mainloop()
