import mysql.connector
from datetime import datetime, date
import calendar

myconn = mysql.connector.connect(host="localhost", user="root", passwd="00624ckn", database="facerecognition")
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()


now_time = datetime.now().strftime('%H:%M:%S')
today_date = date.today().strftime('%Y-%m-%d')

# sql = "INSERT INTO student (student_id, name, login_time, login_date, enrollment_time, major, email) VALUES (%s, %s, %s,%s,%s,%s,%s)"
# val = ("123", "Kin", now_time, today_date, "2018-09-01", "CE", "u3557110@connect.hku.hk")
# cursor.execute(sql, val)

# sql = "UPDATE student SET email = 'u3557110@connect.hku.hk' WHERE student_id = '1'"
# cursor.execute(sql)
#
# sql = "INSERT INTO course (courseID, course_title, lecture_room_address, start_time, end_time, weekday, teacher_name, link, department) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s)"
# val = ("comp3278", "Intro to DB", "off-site", "17:00:00", "20:00:00", "Sunday", "Ping Luo", "https://hku.zoom.us/j/97686555806?pwd=NWxSNVRKTlNDU0NjYTgremxaQ3pldz09", "Computer Science")
# cursor.execute(sql, val)

sql = "INSERT INTO takes (student_id, course_id) VALUES (%s, %s)"
val = ("1", "comp3278")
cursor.execute(sql, val)

myconn.commit()
