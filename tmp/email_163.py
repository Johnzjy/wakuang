import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time

todaytime= datetime.date.today()

'''
    send email with massage
    need writ title and msg
    
'''
class Email_163():
    def __init__(self):
    self.sender = 'otkzhang@163.com'#sender adr
    self.SMTP = smtplib.SMTP('smtp.163.com',25)
    self.password='zjy011247'
    self.SMTP.login(self.sender, self.password )#password
    
def email_sendmsg(tiltle,msg,receivers):
    
    sender = 'otkzhang@163.com'
   # receivers = ['johnson.jy.zhang@philips.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    SMTP = smtplib.SMTP('smtp.163.com',25)


    SMTP.login(sender, 'zjy011247')
    SMTP.ehlo()

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header('tester<otkzhang@163.com>')
    #message['From'] = Header('tester<啥名字都不显示>')
    message['To'] =  u'<receivers>'

    

    subject = tiltle
    message['Subject'] = Header(subject, 'utf-8')

    try:
        SMTP.sendmail(sender, receivers, message.as_string())
        print ("消息发送成功")
        SMTP.quit()
        print("与SMTP服务器断开连接")
        return True
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")
        SMTP.quit()
        print("与SMTP服务器断开连接")
        return False
    '''
    send email with attacher

    '''

def email_sendfile(tiltle,file):

    sender = 'otkzhang@163.com'
    receivers = ['358739426@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    SMTP = smtplib.SMTP('smtp.163.com',25)


    SMTP.login(sender, 'zjy011247')
    SMTP.ehlo()

# 创建一个 附件
    message = MIMEMultipart()
    message['From'] = Header('otkzhang@163.com <otkzhang@163.com>')
    message['To'] =  u'<358739426@qq.com>'

    
    att1 = MIMEText(open(file, 'rb').read(), 'base64', 'gb2312')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="list.txt"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
    message.attach(att1)
    subject = tiltle
    message['Subject'] = Header(subject, 'utf-8')

    try:
        SMTP.sendmail(sender, receivers, message.as_string())
        print ("附件发送成功")
        SMTP.quit()
        print("与SMTP服务器断开连接")
        return True
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")
        SMTP.quit()
        print("与SMTP服务器断开连接")
        return False

'''
def email_receiver():
    host_email = 'otkzhang@163.com'
    host_paswrd= 'zjy011247'
    SMTP = smtplib.SMTP('smtp.163.com',25)
    try:
        SMTP.login(sender,host_paswrd)
    except:
        pass
'''       
        
if __name__=="__main__":

    for i in range(6):
        time.sleep(2)
        print(x[i])

        tiltle =    '测试邮件'
        #msg    = " 这是一封测试邮件,\n不要回复。\n"
        msg=x[i]
        #file   = 'd:\\list.txt'
        receivers = ['nat.yu@philips.com']
        print('start')
        email_sendmsg(tiltle,msg,receivers)
