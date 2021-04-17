import mysql.connector
from datetime import datetime, date

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

sql = "UPDATE student SET email = 'u3557110@connect.hku.hk' WHERE student_id = '1'"
cursor.execute(sql)



myconn.commit()
