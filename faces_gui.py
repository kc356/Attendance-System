import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys
import PySimpleGUI as sg
import smtplib, ssl
from email.mime.text import MIMEText


def coming_class_info(cursor, student_name, course_info):
    sg.theme('TanBlue')
    courseID = course_info[0]
    course_title = course_info[1]
    lecture_room_address = course_info[2]
    start_time = course_info[3]
    start_time = course_info[4]
    weekday = course_info[5]
    teacher_name = course_info[6]
    link = course_info[7]
    department = course_info[8]
    layout = [
        [sg.Text(course_info[0] + " " + course_info[1], font='Any 20')],
        [sg.Text(course_info[2], font='Any 15')],
        [sg.Text(course_info[3] + " - " + course_info[4] + " " + course_info[5], font='Any 15')],
        [sg.Text("Lecturer: " + course_info[6], font='Any 15')],
        [sg.Text("Zoom Link: " + course_info[7], font='Any 15')],
        [sg.Text("From: " + course_info[8] + " Department", font='Any 15')],
        [sg.Button('Send the info as a email to me', key='send email')],
        [sg.Cancel()]
        ]
    window = sg.Window("Second Window", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        elif event == 'send email':
            sql = "SELECT email FROM student WHERE name = '%s'"%(student_name)
            cursor.execute(sql)
            extract_data = cursor.fetchall()
            student_email = extract_data[0][0]
            # print(student_email)
            send_email = Email()
            send_email.construct('testing content', student_email,'testing subject')
            send_email.send()

    window.close()

# def coming_course():
#     layout = [
#         [sg.Text("Coming course", key="new")],
#         [sg.Text("info of the coming course")],
#         [sg.Cancel()]
#         ]
#     window = sg.Window("Second Window", layout, modal=True)
#     choice = None
#     while True:
#         event, values = window.read()
#         if event == "Cancel" or event == sg.WIN_CLOSED:
#             break
#     window.close()

class Email:
    sender = 'FaceRecognitionDatabase3278@gmail.com'
    def construct(self, new_content, receiver_email, new_subj):
        self.msg = MIMEText(new_content, 'html')
        self.msg['From'] = self.sender
        self.msg['To'] = receiver_email
        self.msg['Subject'] = new_subj
    def send(self):
        s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
        s.login(user = self.sender, password = 'comp3278')
        s.sendmail(self.sender, self.msg['To'], self.msg.as_string())
        s.quit()

# 1 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="00624ckn", database="facerecognition")
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()


#2 Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# create text to speech
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)


# 3 Define pysimplegui setting
sg.theme('TanBlue')
layout =  [
    [sg.Text('Press OK to log in', size=(18,1), font=('Any',18),text_color='#1c86ee' ,justification='left')],
    [sg.OK(), sg.Cancel()]
      ]
win = sg.Window('Attendance System',
        default_element_size=(21,1),
        text_justification='right',
        auto_size_text=False).Layout(layout)
event, values = win.Read()
if event is None or event =='Cancel':
    exit()

# if event == "open":
#     open_window()

args = values
gui_confidence = 30
win_started = False

# 4 Open the camera and start face recognition
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        print(x, w, y, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        # predict the id and confidence for faces
        id_, conf = recognizer.predict(roi_gray)

        # If the face is recognized
        if conf >= gui_confidence:
            # print(id_)
            # print(labels[id_])
            font = cv2.QT_FONT_NORMAL
            id = 0
            id += 1
            name = labels[id_]
            current_name = name
            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            # Find the student information in the database.
            select = "SELECT student_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Student WHERE name='%s'" % (name)
            name = cursor.execute(select)
            result = cursor.fetchall()
            # print(result)
            data = "error"

            for x in result:
                data = x

            # If the student's information is not found in the database
            if data == "error":
                # the student's data is not in the database
                print("The student", current_name, "is NOT FOUND in the database.")

            # If the student's information is found in the database
            else:
                """
                Implement useful functions here.
                Check the course and classroom for the student.
                    If the student has class room within one hour, the corresponding course materials
                        will be presented in the GUI.
                    if the student does not have class at the moment, the GUI presents a personal class
                        timetable for the student.

                """
                update =  "UPDATE Student SET login_date=%s WHERE name=%s"
                val = (date, current_name)
                cursor.execute(update, val)
                update = "UPDATE Student SET login_time=%s WHERE name=%s"
                val = (current_time, current_name)
                cursor.execute(update, val)
                myconn.commit()

                hello = ("Hello ", current_name, "You did attendance today")
                print(hello)
                # engine.say(hello)


                sql = "SELECT student_id FROM student WHERE name = '%s'"%(current_name)
                cursor.execute(sql)
                extract_data = cursor.fetchall()
                student_id = extract_data[0][0]

                sql = "SELECT course_id FROM takes WHERE student_id = '%s'"%(student_id)
                cursor.execute(sql)
                extract_data = cursor.fetchall()
                student_courses = extract_data[0]

                for course in student_courses:
                    sql = "SELECT * FROM course WHERE courseID = '%s'"%(course)
                    cursor.execute(sql)
                    extract_data = cursor.fetchall()
                    course_info = extract_data[0]
                    course_start_time = course_info[3]
                    FMT = '%H:%M:%S'
                    tdelta = datetime.strptime(course_start_time, FMT) - datetime.strptime(current_time, FMT)
                    break

                #test will the function be shown only within 1 hr
                course_start_time = "19:00:00"
                FMT = '%H:%M:%S'
                tdelta = datetime.strptime(course_start_time, FMT) - datetime.strptime(current_time, FMT)


                hour = tdelta.seconds//3600
                if hour <= 1:
                    coming_class_info(cursor, current_name, course_info)
                win.Close()

        # If the face is unrecognized
        else:
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            hello = ("Your face is not recognized")
            print(hello)
            engine.say(hello)
            # engine.runAndWait()




    # GUI
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    if not win_started:
        win_started = True
        sg.theme('TanBlue')
        layout = [
            [sg.Text('Attendance System Interface', size=(30,1))],
            [sg.Image(data=imgbytes, key='_IMAGE_')],
            [sg.Exit()]
        ]
        win = sg.Window('Attendance System',
                default_element_size=(14, 1),
                text_justification='right',
                auto_size_text=False).Layout(layout).Finalize()
        image_elem = win.FindElement('_IMAGE_')
    else:
        image_elem.Update(data=imgbytes)

    event, values = win.Read(timeout=20)
    if event is None or event == 'Exit':
        break
    gui_confidence = 30


win.Close()
cap.release()
