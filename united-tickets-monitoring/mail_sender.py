import os
import smtplib
import ssl

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSender:

    def __init__(self):
        load_dotenv()
        self.sender_email = os.getenv('MAIL_FROM')
        self.sender_email_password = os.getenv('MAIL_FROM_PW')

    def send_instant_notification(self, receiver_email: str, submission: dict):
        message = MIMEMultipart("alternative")
        message["Subject"] = "New Man Utd Ticket Alert"
        message["From"] = self.sender_email
        message["To"] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.sender_email_password)

            text = f"""\
            This is a new Man United ticket ad submission.
            
            Title: {submission['title']}
            Content: {submission['content']}
            Platform: {submission['platform']}
            Channel: {submission['channel']}
            Author: {submission['author']}
            URL: {submission['url']}
            Submission Date: {submission['submission_date']}
            """
            html = f"""\
            <html>
              <body>
                <p>This is a new Man United ticket ad submission.<br>
                   <br>
                   Title: {submission['title']}<br>
                   Content: {submission['content']}<br>
                   Platform: {submission['platform']}<br>
                   Channel: {submission['channel']}<br>
                   Author: {submission['author']}<br>
                   URL: <a href="{submission['url']}">{submission['url']}</a><br>
                   Submission Date: {submission['submission_date']}<br>
                </p>
              </body>
            </html>
            """
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
