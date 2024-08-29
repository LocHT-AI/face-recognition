from tkinter import Toplevel, Button, Label, CENTER,messagebox,Entry,filedialog,Text,simpledialog,END
from add_face import add_with_camera
from PIL import Image
from tkcalendar import  DateEntry


class AddFaceByCam(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master, bg='#1b122d', width=400, height=700)
        self.resizable(False, False)

        button_width = 140
        button_height = 50
        row_spacing = 10
        self.file_path=None


            
        Label(self, text="NAME (*)", fg="#263942", font='Helvetica 12 bold').place(x=10, y=(button_height + row_spacing), width=button_width, height=button_height)
        self.user_name = Entry(self, background='white',foreground='white', borderwidth=3, fg="black", font='Helvetica 15 bold')

        validate_phone_number = self.register(self.validate)

        Label(self, text="PHONE\nNUMBER (*)", fg="#263942", font='Helvetica 12 bold').place(x=10, y=2*(button_height + row_spacing), width=button_width, height=button_height)
        self.user_phone_number = Entry(self, validate="key", validatecommand=(validate_phone_number, "%P"), background='white', borderwidth=3,  fg="black", font='Helvetica 15 bold')

        # Label(self, text="registration date", fg="#263942", font='Helvetica 12 bold').place(x=10, y=3*(button_height + row_spacing), width=button_width, height=button_height)
        # self.user_regis_date = Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')

        Label(self, text="REGISTRATION\nDATE (*)", fg="#263942", font='Helvetica 12 bold').place(x=10, y=3*(button_height + row_spacing), width=button_width, height=button_height)
        self.user_regis_date = DateEntry(self, background='darkblue',foreground='white', borderwidth=3, fg="#263942", font='Helvetica 15 bold')


        Label(self, text="END DATE (*)", fg="#263942", font='Helvetica 12 bold').place(x=10, y=4*(button_height + row_spacing), width=button_width, height=button_height)
        self.user_end_date = DateEntry(self, background='darkblue',foreground='white', borderwidth=3, fg="#263942", font='Helvetica 15 bold')

        Label(self, text="NOTE", fg="#263942", font='Helvetica 12 bold').place(x=10, y=6*(button_height + row_spacing), width=button_width, height=button_height)
        self.note = Text(self, background='white',foreground='white', borderwidth=3,  fg="black", font='Helvetica 15 bold')

        Label(self, text="ADD IMAGE", fg="#263942", font='Helvetica 12 bold').place(x=10, y=5*(button_height + row_spacing), width=button_width, height=button_height)
        
        self.buttontrain_1 = Button(self, text="Start\nTraining", fg="#ffffff", bg="#263942",width=15,font='Helvetica 12 bold',command=self.start_training)
        self.button_image = Button(self, text="Browser", fg="#ffffff", bg="#263942",width=15,font='Helvetica 12 bold',command=self.user_image)
        # self.buttonclear = Button(self, text="Clear", command=self.clear, fg="#ffffff", bg="#263942", width=15)
        # self.exit_button = Button(self, text="Exit", bg="#263942", fg='white', width=15)


    
        # self.buttontrain_1.grid(row=2, column=1, pady=10, ipadx=5, ipady=4)
        self.user_name.place(x=button_width+20, y=(button_height + row_spacing), width=button_width+90, height=button_height)
        self.user_phone_number.place(x=button_width+20, y=2*(button_height + row_spacing), width=button_width+90, height=button_height)
        self.user_regis_date.place(x=button_width+20, y=3*(button_height + row_spacing), width=button_width+90, height=button_height)
        self.user_end_date.place(x=button_width+20, y=4*(button_height + row_spacing), width=button_width+90, height=button_height)
        self.note.place(x=button_width+20, y=6*(button_height + row_spacing), width=button_width+90, height=button_height*2)

        self.buttontrain_1.place(x=button_width+20, y=8*(button_height + row_spacing), width=button_width, height=button_height*2+10)
        self.button_image.place(x=button_width+20, y=5*(button_height + row_spacing), width=button_width+90, height=button_height)
        # self.buttonclear.place(x=button_width+30, y=3*(button_height + row_spacing), width=button_width, height=button_height)
        # self.exit_button.place(x=0, y=3*(button_height + row_spacing), width=button_width, height=button_height)


        # self.exit_button.bind("<ButtonRelease>", self.exit_button_released)


        self.mainloop(3)

    # Validation function
    def validate(self, new_value):
        return new_value.isdigit() or new_value == ""

    def user_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])

    def start_training(self):
        if self.user_end_date.get_date()<self.user_regis_date.get_date():
            messagebox.showerror("Error", "End date must not be earlier than the registration date!")
            return          
        if self.user_name.get() == "None" or self.user_phone_number.get() == 'None'or self.user_regis_date.get_date() == 'None'or self.user_end_date.get_date() == 'None' :
            messagebox.showerror("Error", "Please enter all required information marked with *!")
            return
        elif len(self.user_name.get()) == 0 or len(self.user_phone_number.get()) == 0 :
            messagebox.showerror("Error", "Please enter all required information marked with *!")
            return

        # elif self.user_id.get() in csv_data:
        #     messagebox.showerror("Error", "ID user already exists!")
        #     return


        name = self.user_name.get()
        # print(name)
        phone= "'"+self.user_phone_number.get()
        regis_date = self.user_regis_date.get_date()
        end_date =self.user_end_date.get_date()
        note=self.note.get(1.0, END).strip()
    
        train=add_with_camera(name,phone,regis_date,end_date,note)
        if train:
            if self.file_path:
                user_path = f"data/user/{phone}.jpg"
                img = Image.open(self.file_path)
                img.save(user_path)
            messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
            self.destroy()
        else:
            messagebox.showerror("Error", "ID user already exists!")



    # def clear(self):
    #     self.user_name.delete(0, 'end')
    #     self.user_id.delete(0, 'end')  



    # def exit_button_released(self, event):
    #     self.destroy()
