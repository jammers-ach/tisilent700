import os

import smtplib
import time
import imaplib
import email

import logging

from terminalapp import TerminalApp

logger = logging.getLogger(__name__)


FROM_EMAIL  = os.getenv("TERMINAL_EMAIL_USER")
FROM_PWD    = os.getenv("TERMINAL_EMAIL_PWD")

SMTP_SERVER = os.getenv("TERMINAL_EMAIL_SERVER", "imap.gmail.com")
SMTP_PORT   = os.getenv("TERMINAL_EMAIL_PORT",993)

SLEEP_TIME = os.getenv("SLEEP_TIME", 60)

def readmail(mark_seen=True):
    if FROM_EMAIL is None or FROM_PWD is None:
        raise Exception("There is no email or password")

    logger.info("Checking %s", FROM_EMAIL)
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    mail.select('inbox')
    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])


    mails = []
    for i in range(latest_email_id,first_email_id, -1):
        typ, data = mail.fetch('{}'.format(i), '(RFC822)' )
        if mark_seen:
            mail.store('{}'.format(i),'+FLAGS','\Seen')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                mails.append(msg)

    logger.info("Got %d new mail", len(mails))
    return mails


def format_email(email):
    '''
    Takes an email and formats it as it should be for the terminal
    '''

    template="""From: {sender}
To: {to}
Date: {date}
Subject: {subject}


{body}"""

    if email.is_multipart():
        body = email.get_payload()[0].get_payload()
    else:
        body = email.get_payload()

    template = template.format(sender=email['from'],
        to=email['to'],
        date=email['date'],
        subject=email['Subject'],
        body=body)

    return template


class EmailApp(TerminalApp):

    def start(self):

        if FROM_PWD is None or FROM_EMAIL is None:
            self.send("There are no email credentials, exiting")
            return

        mails = readmail()
        while True:
            for mail in mails:
                logger.info("Received an email from %s", mail['from'])
                self.send(format_email(mail))
                self.ser.send_line()
            self.sleep(SLEEP_TIME)
