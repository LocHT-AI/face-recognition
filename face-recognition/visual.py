from tkinter import Frame, Canvas
import tkinter as tk
from PIL import ImageTk, Image
import os
import time
from datetime import datetime
import cv2
import csv

class ShowImage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, width=1080, height=820)

        self.canvas_width = 1080
        self.canvas_height = 820
        self.filename="user.csv"
        

        self.canvas = Canvas(self, width=self.canvas_width, height=self.canvas_height,bg="#1b122d")
        self.canvas.pack()

        self.current_image_index = 0

        self.show()



    def show(self):
        self.display_next_image()
        self.after(1000, self.show) 


    def read_csv_file(self):
        if not os.path.exists(self.filename):
            return None
        data = []
        with open(self.filename, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                data.append(row)
        return data
    def parse_date(self,date_str):
        formats = ['%m/%d/%y', '%Y-%m-%d', '%d-%m-%Y','%y-%m-%d','%m/%d/%Y']  # Add more formats as needed
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError("Invalid date format")
    def display_next_image(self):
        # self.canvas.delete(self.label)
        x=10
        y=350
        row_space = 55
        ts = time.time()
        self.date = str(datetime.fromtimestamp(ts).strftime("%d-%m-%Y"))
        path = f"Attendance/image/{self.date}"
        if not os.path.exists(path):
            os.makedirs(path)
        self.image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if self.current_image_index < len(self.image_paths):
            self.canvas.delete('all')
            image_path = self.image_paths[self.current_image_index]
            id_card = os.path.split(image_path)[-1].split("_")[2]
            # print(id_card)
            path_2 = f"data/user"
            path_image = [os.path.join(path_2, f) for f in os.listdir(path_2) if f.endswith((f'{id_card}.jpg', f'{id_card}.jpeg', f'{id_card}.png'))]
            # print(path_image[0])
            # image = Image.open(path_image[0])
            # photo = ImageTk.PhotoImage(image)
            # Ngày bắt đầu


            if path_image:
                image_item = cv2.imread(path_image[0])
                resized_image = cv2.resize(image_item, (300, 300))
                image_item_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
                image_pil = Image.fromarray(image_item_rgb)
                img = ImageTk.PhotoImage(image_pil)


                # Clear any existing image on the canvas
                self.canvas.delete('image')
                self.canvas.create_image(540, 150, image=img, tags='image',anchor=tk.CENTER)
                self.canvas.image = img
                # self.label = tk.Label(self.canvas, image=img, bg="#1b122d")
                # self.label.image = img
                # self.label.place(x=200+self.current_image_index*10, y=200)


                data = self.read_csv_file()
                if data is not None:
                    # print(data)
                    for i in range(len(data)):  # Corrected the loop syntax
                        if id_card in data[i]:
      
                            # print(data[i])
                            # if len(data[i])<3:
                            #     self.name_=Label(self.canvas, text=f"NAME : {data[i][0]}", fg="white", font='Helvetica 15 bold').place(x=x + 10 , y = button_height)
                            #     self.phone_=Label(self.canvas, text=f"PHONE NUMBER : {data[i][1]}", fg="white", font='Helvetica 15 bold').place(x=x + 10 , y =2* (button_height+row_space))
                            #     self.regis_data_=Label(self.canvas, text=f"Date :               ", fg="white", font='Helvetica 15 bold').place(x=x + 10 , y =3* (button_height+row_space))
                            #     self.end_data_=Label(self.canvas, text=f"End Date :              ", fg="white", font='Helvetica 15 bold').place(x=x + 10 , y =4* (button_height+row_space))
                            # else:
                            #     self.name_=Label(self.canvas, text=f"NAME : {data[i][0]}", fg="white", font='Helvetica 15 bold').place(x=x + 10 , y = button_height)
                            #     self.phone_=Label(self.canvas, text=f"PHONE NUMBER : {data[i][1]}", fg="white", font='Helvetica 15 bold').place(x=x + 10 , y =2* (button_height+row_space))
                            #     self.regis_data_=Label(self.canvas, text=f"Date : {data[i][2]}", fg="white", font='Helvetica 15 bold').place(x=x + 10 , y =3* (button_height+row_space))
                            #     self.end_data_=Label(self.canvas, text=f"End Date : {data[i][3]}", fg="white", font='Helvetica 15 bold').place(x=x + 10 , y =4* (button_height+row_space))
                            
                            if len(data[i])<3 or data[i][2] is None or len(data[i][2])==0:
            
                                self.canvas.create_text(x, y+row_space, text=f"HỌ VÀ TÊN : {data[i][0]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+2*row_space, text=f"SỐ ĐIỆN THOẠI : {data[i][1]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+3*row_space, text=f"NGÀY ĐĂNG KÝ : CHƯA ĐĂNG KÝ", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+4*row_space, text=f"NGÀY KẾT THÚC GÓI : CHƯA ĐĂNG KÝ ", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+5*row_space, text=f"SỐ NGÀY CÒN LẠI : CHƯA ĐĂNG KÝ ", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+6*row_space, text=f"GÓI TẬP : CHƯA ĐĂNG KÝ", fill="white", font='Helvetica 35 bold', anchor='w')
                            
                            else:

                                start_date = self.parse_date(data[i][2])
                                # Ngày kết thúc
                                end_date = self.parse_date(data[i][3])
                                # Tính số ngày còn lại
                                remaining_days = (end_date - start_date).days
                                # print(remaining_days)
                                self.canvas.create_text(x, y+row_space, text=f"HỌ VÀ TÊN : {data[i][0]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+2*row_space, text=f"SỐ ĐIỆN THOẠI : {data[i][1]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+3*row_space, text=f"NGÀY ĐĂNG KÝ : {data[i][2]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+4*row_space, text=f"NGÀY KẾT THÚC GÓI : {data[i][3]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+5*row_space, text=f"SỐ NGÀY CÒN LẠI : {remaining_days} NGÀY", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+6*row_space, text=f"GÓI TẬP : {data[i][4]}", fill="white", font='Helvetica 35 bold', anchor='w')
                
                self.current_image_index += 1
            else:
                image_item = cv2.imread("data/user/not_yet.jpg")
                resized_image = cv2.resize(image_item, (300, 300))
                image_item_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
                image_pil = Image.fromarray(image_item_rgb)
                img = ImageTk.PhotoImage(image_pil)
                self.canvas.delete('image')
                self.canvas.create_image(540, 150, image=img, tags='image',anchor=tk.CENTER)
                self.canvas.image = img
                # self.label = tk.Label(self.canvas, image=img, bg="#1b122d")
                # self.label.image = img
                # self.label.place(x=200+self.current_image_index*10, y=200)
                data = self.read_csv_file()
                if data is not None:
                    # print(data)
                    for i in range(len(data)):  # Corrected the loop syntax
                        if id_card in data[i]:
                            # print(data[i])
                            if len(data[i])<3 or data[i][2] is None or len(data[i][2])==0:
            
                                self.canvas.create_text(x, y+row_space, text=f"HỌ VÀ TÊN : {data[i][0]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+2*row_space, text=f"SỐ ĐIỆN THOẠI : {data[i][1]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+3*row_space, text=f"NGÀY ĐĂNG KÝ : CHƯA ĐĂNG KÝ", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+4*row_space, text=f"NGÀY KẾT THÚC GÓI : CHƯA ĐĂNG KÝ ", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+5*row_space, text=f"SỐ NGÀY CÒN LẠI : CHƯA ĐĂNG KÝ ", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+6*row_space, text=f"GÓI TẬP : CHƯA ĐĂNG KÝ", fill="white", font='Helvetica 35 bold', anchor='w')
                            
                            else:
                                start_date = self.parse_date(data[i][2])

                                # Ngày kết thúc
                                end_date = self.parse_date(data[i][3])
                                # Tính số ngày còn lại
                                remaining_days = (end_date - start_date).days
                                # print(remaining_days)

                                self.canvas.create_text(x, y+row_space, text=f"HỌ VÀ TÊN : {data[i][0]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+2*row_space, text=f"SỐ ĐIỆN THOẠI : {data[i][1]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+3*row_space, text=f"NGÀY ĐĂNG KÝ : {data[i][2]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+4*row_space, text=f"NGÀY KẾT THÚC GÓI : {data[i][3]}", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+5*row_space, text=f"SỐ NGÀY CÒN LẠI : {remaining_days} NGÀY", fill="white", font='Helvetica 35 bold', anchor='w')
                                self.canvas.create_text(x, y+6*row_space, text=f"GÓI TẬP : {data[i][4]}", fill="white", font='Helvetica 35 bold', anchor='w')
                self.current_image_index += 1

