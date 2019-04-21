import os

import smtplib
import time
import imaplib
import email

import logging

from ti700.app import TerminalApp

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
    response, data = mail.search(None, 'UNSEEN')

    if response != 'OK':
        logger.info("imap response wans't ok: %s", response)
        return
    mail_ids = data[0]

    if mail_ids == b'':
        logger.info("no new email")
        return []

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    ids = range(latest_email_id,first_email_id, -1) if first_email_id != latest_email_id else [first_email_id]

    mails = []
    for i in ids:
        typ, data = mail.fetch('{}'.format(i), '(RFC822)' )
        if mark_seen:
            logger.info("Marking %d as seen", i)
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
    appname = "email checker"

    def start(self):

        if FROM_PWD is None or FROM_EMAIL is None:
            self.send("There are no email credentials, exiting")
            return
        else:
            self.send("Email checker started")

        while True:
            mails = readmail()
            for mail in mails:
                logger.info("Received an email from %s", mail['from'])
                self.send(format_email(mail))
                self.sleep(1)
            self.sleep(SLEEP_TIME)
