import cv2
import pickle
import numpy as np
import os
import os
import csv


def capture_faces( output_folder,name,phone):
    infor={}
    name=get_last_word(name)
    # name = input("Enter Your Name: ")
    # id = input("ENTER ID: ")
    infor[phone] = name
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    video=cv2.VideoCapture(0)
    facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    i=0
    while True:
        ret,frame=video.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=facedetect.detectMultiScale(gray, 1.3 ,5)
        for (x,y,w,h) in faces:
            crop_img=frame[y:y+h, x:x+w, :]
            resized_img=cv2.resize(crop_img, (50,50))
            if i%10==0:
                img_path = os.path.join(output_folder, f"{name}_{phone}_{i}.jpg")
                cv2.imwrite(img_path, resized_img)
            
            i=i+1
            cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
        cv2.imshow("Frame",frame)
        k=cv2.waitKey(1)
        if k==ord('q') or i == 500 :
            break
    video.release()
    cv2.destroyAllWindows()
    # face_data(faces_data)

def get_img_ori(path,output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(path):
        return False
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    # print(image_paths)
    if len(image_paths)==0:
        return False
    facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    i=0
    users=[]
    phones=[]
    phones_read=read_second_csv_file("user.csv")
    for imagePath in image_paths:
        faceImage = cv2.imread(imagePath)
        gray=cv2.cvtColor(faceImage, cv2.COLOR_BGR2GRAY)
        faces=facedetect.detectMultiScale(gray, 1.3 ,5)
        # print("c2")
        for (x,y,w,h) in faces:
            # print("c2")
            crop_img=faceImage[y:y+h, x:x+w, :]
            resized_img=cv2.resize(crop_img, (50,50))
            name = os.path.split(imagePath)[-1].split("_")[0]
            phone = os.path.split(imagePath)[-1].split("_")[1]
            if phones_read is not None:
                if phone in phones_read:
                    continue

            if phone not in phones:
                phones.append(phone)
                user=[name,phone]
                users.append(user)
            i += 1
            for j in range(20):
                img_path = os.path.join(output_folder, f"{name}_{phone}_{i}_{j}.jpg")
                cv2.imwrite(img_path, resized_img)
            
            
    # print(users)
    for user in users:
        COL_NAMES = ['NAME','PHONE NUMBER','REGISTRATION DATE','END DATE','NOTE']
        exist = os.path.isfile("user.csv")
        with open("user.csv", "+a") as csvfile:
            writer = csv.writer(csvfile)
            if not exist:
                writer.writerow(COL_NAMES)
            writer.writerow(user)
    return True


def get_img_deteted(path):
    imagePath = [os.path.join(path, f) for f in os.listdir(path)]
    faces_data=[]

    for imagePaths in imagePath:
        faceImage = cv2.imread(imagePaths)
        infor={}
        faces_data.append(faceImage)
        name = os.path.split(imagePaths)[-1].split("_")[0]
        id_card = os.path.split(imagePaths)[-1].split("_")[1]
        infor[id_card] = name
        # print(infor)
        infor_data(infor)
    train=face_data(faces_data)
    return train


def face_data(faces_data):
    if not os.path.exists('data/model'):
        os.makedirs('data/model')
    # print(len(faces_data))
    if len(faces_data) == 0:
        return False
    faces_data=np.asarray(faces_data)
    faces_data=faces_data.reshape(len(faces_data), -1)
    if 'faces_data.pkl' not in os.listdir('data/model/'):
        with open('data/model/faces_data.pkl', 'wb') as f:
            pickle.dump(faces_data, f)
    else:
        with open('data/model/faces_data.pkl', 'rb') as f:
            faces=pickle.load(f)
        faces=np.append(faces, faces_data, axis=0)
        with open('data/model/faces_data.pkl', 'wb') as f:
            pickle.dump(faces, f)
    return True


def read_first_csv_file(filename):
    if not os.path.exists(filename):
        return None
    first_column = []
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row and row[0]: 
                first_column.append(row[0])
    return first_column[1:]

def read_second_csv_file(filename):
    if not os.path.exists(filename):
        return None
    second_column = []
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row and len(row) >= 2: 
                second_column.append(row[1])  # Change index to 1 for the second column
    return second_column[1:]  # Exclude the header row

def infor_data(infor):
    if not os.path.exists('data/model'):
        os.makedirs('data/model')
    if 'names.pkl' not in os.listdir('data/model/'):
        infor_list=[infor]
        with open('data/model/names.pkl', 'wb') as f:
            pickle.dump(infor_list, f)
    else:
        with open('data/model/names.pkl', 'rb') as f:
            infor_list=pickle.load(f)
        infor_list=infor_list+[infor]
        with open('data/model/names.pkl', 'wb') as f:
            pickle.dump(infor_list, f)

def get_last_word(sentence):
    # Chia câu thành các từ
    words = sentence.split()
    # Lấy từ cuối cùng trong danh sách các từ
    last_word = words[-1]
    return last_word


def remove_diacritics(text):
    diacritics_map = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
        'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
        'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
        'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
        'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
        'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
        'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
        'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
        'đ': 'd', 'Đ': 'D',
    }
    
    for char in diacritics_map:
        text = text.replace(char, diacritics_map[char])
    
    return text

output_folder='data/datasets'
def add_with_camera(name,phone,regis_date,end_date,note):
    train= False
    name=remove_diacritics(name)
    note=remove_diacritics(note)
    names=read_first_csv_file("user.csv")
    phones=read_second_csv_file("user.csv")
    if names is not None:
        if name in names and phone in phones:
            return train
    user=[name,phone,regis_date,end_date,note]
    COL_NAMES = ['NAME','PHONE NUMBER','REGISTRATION DATE','END DATE','NOTE']
    exist = os.path.isfile("user.csv")
    with open("user.csv", "+a") as csvfile:
        writer = csv.writer(csvfile)
        if not exist:
            writer.writerow(COL_NAMES)
        writer.writerow(user)
    capture_faces(output_folder,name,phone)
    train=get_img_deteted(output_folder)
    return train

def add_with_data(folder_input):
    data=get_img_ori(folder_input,output_folder)
    train=False
    if data:
        train=get_img_deteted(output_folder)
    return train


def add_face_main():
    output_folder='data/datasets'
    print("(1) for colect face with camera")
    print("(2) if you already have data")
    print("other to exit")
    k = input("ENTER WHAT YOU WANT : ")
    if k=="1":
        capture_faces(output_folder)
        get_img_deteted(output_folder)
    elif k=="2":
        get_img_ori('data/datasets_ori',output_folder)
        get_img_deteted(output_folder)


if __name__ == "__main__":
    add_face_main()