import smtplib


def pushEmail():
    """

    :return:
    """
    server = smtplib.SMTP_SSL('', port=1)
    server.ehlo()
    pass
