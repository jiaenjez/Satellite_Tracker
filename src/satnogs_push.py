import smtplib


def pushEmail():
    server = smtplib.SMTP_SSL('', port=1)
    server.ehlo()
