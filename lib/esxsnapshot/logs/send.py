import smtplib
from email.mime.text import MIMEText

__author__ = 'weldpua2008@gmail.com'


def by_mail(from_addr, to_addr, logfile):
    fp = open(logfile, 'rb')
    msg = MIMEText(fp.read())
    fp.close()
    msg['Subject'] = 'Snapshot tool log file %s' % logfile
    msg['From'] = from_addr
    msg['To'] = to_addr
    s = smtplib.SMTP('localhost')
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.quit()


def send_notification(from_addr, to_addr, action, status, message, vmname):
    msg = MIMEText(message)
    subject = '[%s] Snapshot on [%s] was [%s]' % (action, vmname, status)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    s = smtplib.SMTP('localhost')
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.quit()