import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Template

from .config import config, logger


class Email:
    def __init__(self, account, name):
        self.smtp = None
        self.account = account
        self.name = name

    def connect(self):
        self.smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.smtp.ehlo()
        self.smtp.login(self.account, config['email'][self.account])

    def sendmail(self, to, subject, template, cc=None, bcc=None, attachment=None, attachments=None, **text):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = '{} <{}>'.format(self.name, self.account)
        msg['To'] = to
        destinations = [email.strip() for email in to.split(',')]
        if cc is not None:
            msg['Cc'] = cc
            destinations += [email.strip() for email in cc.split(',')]
        if bcc is not None:
            msg['Bcc'] = bcc
            destinations += [email.strip() for email in bcc.split(',')]

        with open('templates/{}.html'.format(template)) as template_file:
            template = Template(template_file.read())
        content = template.render(**text)

        msg.attach(MIMEText(content, 'html'))
        if attachment is not None:
            part = MIMEApplication(
                attachment[0].read(),
                Name=attachment[1]
            )
            part['Content-Disposition'] = 'attachment; filename="{}"'.format(attachment[1])
            msg.attach(part)
        if attachments is not None:
            for attachment in attachments:
                part = MIMEApplication(
                    attachment[0].read(),
                    Name=attachment[1])
                part['Content-Disposition'] = 'attachment; filename="{}"'.format(attachment[1])
                msg.attach(part)
        logger.debug('[Emails] Sending email to {}'.format(destinations))
        if len(to) > 0:
            self.smtp.sendmail(self.account, destinations, msg.as_string())

    def close(self):
        self.smtp.quit()


no_reply = Email('my_email@email.com', 'my app')
