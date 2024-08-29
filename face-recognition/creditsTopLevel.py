from tkinter import Toplevel, Button, Label, CENTER
import webbrowser


def callback(url):
    webbrowser.open_new(url)


class CreditsTopLevel(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master, bg='#1b122d', width=500, height=450)
        self.resizable(False, False)
       
       
        self.general_page = Label(master=self, text=
                                                    "\nCreating by Py\n"
                                                    " Zalo: 0375143973\n",
                                bg="gold", fg="black", font="ariel 15 bold")
        self.instagram_page = Label(master=self, text="My Instagram Page", bg="blue", fg="white",
                                    font="ariel 15 bold", cursor="hand2")
        self.facebook_page = Label(master=self, text="My Facebook Page", bg="blue", fg="white",
                                font="ariel 15 bold", cursor="hand2")
        self.github_page = Label(master=self, text="My Github Page", bg="blue", fg="white",
                                font="ariel 15 bold", cursor="hand2")
        self.linkedin_page = Label(master=self, text="My Linkedin Page", bg="blue", fg="white",
                                font="ariel 15 bold", cursor="hand2")


        self.exit_button = Button(self, text="Exit Credits Page", bg="blue", fg='white', width=15, font="ariel 13 bold")


        self.linkedin_page.bind("<Button-1>", lambda e: callback("https://www.linkedin.com/in/hu%E1%BB%B3nh-t%E1%BA%A5n-l%E1%BB%99c-8b7475251/"))
        self.github_page.bind("<Button-1>", lambda e: callback("https://github.com/pysing"))
        self.instagram_page.bind("<Button-1>", lambda e: callback("https://www.instagram.com/pidy01201/"))
        self.facebook_page.bind("<Button-1>", lambda e: callback("https://www.facebook.com/hdhd.nha.5/"))
        self.exit_button.bind("<ButtonRelease>", self.exit_button_released)

        button_width = 300
        button_height = 50
        row_spacing = 10
        x_bu = 500/2

        self.general_page.place(x=x_bu, y=50, width=button_width, height=70,anchor=CENTER)
        self.github_page.place(x=x_bu, y=2*(button_height + row_spacing), width=button_width, height=button_height,anchor=CENTER)
        self.instagram_page.place(x=x_bu, y=3*(button_height + row_spacing), width=button_width, height=button_height,anchor=CENTER)
        self.facebook_page.place(x=x_bu, y=4*(button_height + row_spacing), width=button_width, height=button_height,anchor=CENTER)
        self.linkedin_page.place(x=x_bu, y=5*(button_height + row_spacing), width=button_width, height=button_height,anchor=CENTER)
        self.exit_button.place(x=x_bu, y=20+6*(button_height + row_spacing), width=button_width, height=button_height,anchor=CENTER)

        self.mainloop(3)

    def exit_button_released(self, event):
        self.destroy()

# app = CreditsTopLevel()
# app.mainloop()