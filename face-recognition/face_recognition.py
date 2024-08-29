from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime

from win32com.client import Dispatch

def speak(text):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(text)

def initialize_face_recognition():
    # Load names and faces data
    with open('data/model/names.pkl', 'rb') as names_file:
        LABELS = pickle.load(names_file)

    name_list, ids, infor = [], [], {}
    for idx, label_dict in enumerate(LABELS):
        for key, value in label_dict.items():
            name_list.append(value)
            ids.append(key)
            infor[key] = value
            # logger.debug(ids)
    with open('data/model/faces_data.pkl', 'rb') as faces_file:
        FACES = pickle.load(faces_file)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(FACES, ids)

    return knn, infor

def capture_video():
    return cv2.VideoCapture(0)

def recognize_faces(frame, facedetect, knn, infor, img_background):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    attendance=[]
    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        conf = knn.predict_proba(resized_img)
        conf = np.max(conf)

        if conf == 1:
            output = knn.predict(resized_img)
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            # cv2.putText(frame, f"{infor[str(output[0])]} {str(output[0])}", (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.putText(frame, f"{infor[str(output[0])]}", (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

            attendance = [str(output[0]),infor[str(output[0])], str(timestamp),str(date)]
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
            cv2.putText(frame, "unknown", (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

    img_background[25:25 + 480, 55:55 + 640] = frame
    resized_image = cv2.resize(img_background, (400, 400))
    cv2.imshow("Frame", resized_image)
    # # Display the frame with Matplotlib
    # plt.imshow(cv2.cvtColor(img_background, cv2.COLOR_BGR2RGB))
    # plt.show()
    return attendance,frame

def face_main():
    knn, infor = initialize_face_recognition()
    video = capture_video()
    facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    img_background = cv2.imread("data/image/background.png")

    COL_NAMES = ['NO.','NAME','PHONE NUMBER','DATE','TIME']
    ts = time.time()
    date = str(datetime.fromtimestamp(ts).strftime("%d-%m-%Y"))
    path=f"Attendance/image/{date}/saveint.txt"
    if not os.path.exists(path):
        save_int=0
    else:
        # If the file exists, open it in read mode and read the first line
        with open(path, 'r') as file:
            # Read one line
            line = file.readline().strip()  # Strip any leading/trailing whitespace

            # Check if the line is not empty
            if line:
                # If not empty, convert it to an integer
                save_int = int(line)
            else:
                # If empty, set save_int to 0
                save_int = 0
    while True:
        ret, frame = video.read()
        if not ret :
            print("khong chay duoc cam")
            time.sleep(5)
            continue

        attendance,frame = recognize_faces(frame, facedetect, knn, infor, img_background)
        
        k = cv2.waitKey(1)
        if (k == ord('o') or k == ord('O'))  and attendance:
            speak(f"Attendance Taken")
            # time.sleep(2)
            # plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # plt.show()
            
            image_out=f"Attendance/image/{attendance[3]}"
            if not os.path.exists(image_out):
                os.makedirs(image_out)
            img_path = os.path.join(image_out, f"{save_int}_{attendance[1]}_{attendance[0]}_checked.jpg")
            file_path = os.path.join(image_out, "saveint.txt")
            cv2.imwrite(img_path, frame)
            user=[save_int,attendance[1],attendance[0],attendance[3],attendance[2]]
            save_int+=1
            with open(file_path, "w") as file:
                file.write(str(save_int))
            exist = os.path.isfile(f"Attendance/Attendance_{attendance[3]}.csv")
            
            with open(f"Attendance/Attendance_{attendance[3]}.csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                if not exist:
                    writer.writerow(COL_NAMES)
                writer.writerow(user)

        if k == ord('q') or k == ord('Q'):
            break


    video.release()
    cv2.destroyAllWindows()
    
    return False

if __name__ == "__main__":
    face_main()
