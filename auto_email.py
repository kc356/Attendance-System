import smtplib, ssl
from email.mime.text import MIMEText

# sender = 'FaceRecognitionDatabase3278@gmail.com'
#
# # receiver input below
# receivers = ['u3557110@connect.hku.hk']
#
# # content input below
# body_of_email = 'testing email'
#
# msg = MIMEText(body_of_email, 'html')
# msg['Subject'] = 'Testing'
# msg['From'] = sender
# msg['To'] = ','.join(receivers)
#
# s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
# s.login(user = sender, password = 'comp3278')
# s.sendmail(sender, receivers, msg.as_string())
# s.quit()

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

content = "test content"
subj = "test subject"
target_email = 'u3557110@connect.hku.hk'
send_email = Email()
send_email.construct(content, target_email, subj)
send_email.send()
