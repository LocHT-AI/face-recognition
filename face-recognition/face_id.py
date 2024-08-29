import threading
import tkinter as tk
from app_gui import StartPage
from visual import ShowImage

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.interface_thread = threading.Thread(target=self.create_interface)
        self.interface_functions_thread = threading.Thread(target=self.create_interface_functions)

        self.interface_thread.start()
        self.interface_functions_thread.start()

        self.resizable(True, True)
        self.configure(bg="#1b122d")

    def create_interface(self):
        self.interface = StartPage(master=self)
        self.interface.pack( side='left',anchor='e')

    def create_interface_functions(self):
        self.interface_functions = ShowImage(master=self)
        self.interface_functions.pack( side="left",anchor='w')

if __name__ == "__main__":
    app = Main()
    app.iconphoto(True, tk.PhotoImage(file='data/image/icon.ico'))
    app.mainloop()
