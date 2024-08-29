from face_recognition import face_main
from add_face import add_with_data
from add_camera import AddFaceByCam
import tkinter as tk
from tkinter import messagebox,PhotoImage,filedialog
from pathlib import Path
from PIL import ImageTk, Image
import cv2
from creditsTopLevel import CreditsTopLevel
import threading


names = set()


class StartPage(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master=master, width=500, height=820)

        self.isruning = False


        canvas_width = 500
        canvas_height = 820

        background_path='data/image/bg.jpg'
        background_path = Path(background_path).as_posix()
        image_item = cv2.imread(background_path)
        resized_image = cv2.resize(image_item, (canvas_width, canvas_height))
        image_item_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_item_rgb)
        photo = ImageTk.PhotoImage(image=image_pil)
        # Create a canvas covering the entire frame
        canvas = tk.Canvas(self, width=canvas_width, height=canvas_height)
        canvas.pack(fill="both")
        
        # Place the image on the canvas
        canvas.create_image(canvas_width/2, canvas_height/2, image=photo, anchor=tk.CENTER)
        # Make sure to keep a reference to the image object to prevent it from being garbage collected
        canvas.image = photo





        button_width = 200
        button_height = 50
        row_spacing = 15
        x=canvas_width/2
        y=canvas_height/2

        render = PhotoImage(file='data/image/homepagepic.png')
        img = tk.Label(self, image=render,bg="#1b122d")
        img.image = render
        img.place(x=x, y=180,anchor=tk.CENTER)

        self.credits_button = tk.Button(self, text="Credits", bg="#1b122d", fg='gold', font="ariel 15 bold")
        

        self.button1 = tk.Button(self, text="Add face\nwith camera", fg="white",font="ariel 15 bold", bg="#1b122d")
        self.button2 = tk.Button(self, text="Train\nwith data", fg="white", bg="#1b122d",font="ariel 15 bold")
        self.button3 = tk.Button(self, text="Start\nFace recognition", fg="white", bg="#1b122d",font="ariel 16 bold")
        # self.button4 = tk.Button(self, text="Quit", fg="#ffffff", bg="#1b122d", font="ariel 15 bold",command=self.on_closing)
        self.button1.place(x=x, y=y+1*(button_height + row_spacing), width=button_width, height=button_height,anchor=tk.CENTER)
        self.button2.place(x=x, y=y+2*(button_height + row_spacing), width=button_width-50, height=button_height,anchor=tk.CENTER)
        self.button3.place(x=x, y=y, width=button_width+50, height=button_height,anchor=tk.CENTER)
        self.credits_button.place(x=x, y=y+160+3*(button_height + row_spacing), width=button_width-100, height=button_height,anchor=tk.CENTER)
        # self.button4.place(x=x, y=4*(button_height + row_spacing), width=button_width, height=button_height,anchor=tk.CENTER)


        self.button1.bind("<ButtonRelease>", self.add_by_camera_button_released)
        self.button2.bind("<ButtonRelease>", self.add_by_data_button_released)
        self.button3.bind("<ButtonRelease>", self.face_recongition_released)
        self.credits_button.bind("<ButtonRelease>", self.credits_button_released)

        # # self.after(100, self.set_button_state)
        # self.check = threading.Thread(target=self.set_button_state)
        # self.check.start()
        self.set_button_state()

    def credits_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.credits_button:
            self.credits_frame = CreditsTopLevel()
            self.credits_frame.grab_set()

    def add_by_camera_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.button1:
            if not self.isruning:
                self.add_by_cam_frame = AddFaceByCam()
                self.add_by_cam_frame.grab_set()   

    def add_by_data_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.button2:
            if not self.isruning:
                folder_selected = filedialog.askdirectory()
                train=add_with_data(folder_selected)
                if train:
                    messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
                else:
                    messagebox.showerror("Error", "No data to train")
    def face_recongition_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.button3:
            if not self.isruning:
                # print("c2")
                self.isruning = not self.isruning
                self.run_ = threading.Thread(target=self.run)
                self.run_.start()
                
                # self.set_button_state(self.isruning)

    def set_button_state(self):
        if self.isruning:
            self.button1.config(state="disabled")
            self.button2.config(state="disabled")
            self.button3.config(state="disabled")
        else:
            self.button1.config(state="normal")
            self.button2.config(state="normal")
            self.button3.config(state="normal")

        self.after(1000, self.set_button_state)

    def run(self):
        self.isruning=face_main()
        

    # def on_closing(self):
    #     if messagebox.askokcancel("Quit", "Are you sure?"):
    #         self.destroy()






# if __name__ == "__main__":
#     app = StartPage()
#     app.iconphoto(True, tk.PhotoImage(file=relative_to_assets('icon.ico')))
#     app.mainloop()

