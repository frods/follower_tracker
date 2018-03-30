import time
import smtplib
from email.mime.text import MIMEText

import logging

LOGGER = logging.getLogger(__name__)


class StoreFile:
    def __init__(self, filename, email, email_account, email_password):
        self.filename = filename
        self.email = email
        self.email_account = email_account
        self.email_password = email_password

    def store_followers(self, platform, count, date, url):
        def clean_count(count):
            clean_count = count.replace(',', '')
            return clean_count

        with open(self.filename, "a") as writter:
            writter.write("%s\t%s\t%s\n" % (
                time.asctime(), clean_count(count), url))

    def finalize(self):
        if not self.email:
            return

        if not self.email_account and not self.email_password:
            LOGGER.error("Email account and password must be specified.")

        with open(self.filename, "r") as reader:
            msg = MIMEText(reader.read())

        sender = "follower@getter.com"
        msg['Subject'] = "Follower update"
        msg['From'] = sender
        msg['To'] = self.email

        s = smtplib.SMTP('smtp.gmail.com:587')
        s.starttls()
        s.login(self.email_account, self.email_password)
        s.sendmail(sender, [self.email], msg.as_string())
        s.quit()
