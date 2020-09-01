# -*- coding: utf-8 -*-
import os
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class DoorayEmail:
    def __init__(self, email, password, domain="smtp.dooray.com", port=465):
        """
        두레이 이메일을 발송한다
        :param dooray_email: 발송자 이메일 주소 (예: test@naverunion.dooray.com)
        :param password: 발송자 이메일 암호
        :param domain: 이메일 발송 도메인주소 (두레이 기본값 세팅됨)
        :param port: 이메일 발송 포트
        """
        self._from_mail = email
        self._mail = smtplib.SMTP_SSL(domain, port)
        self._mail.login(email, password)
        self._subject = "제목없음"
        self._contents = "내용없음"
        self._attach_file = None

    def subject(self, subject):
        self._subject = subject
        return self

    def contents(self, contents):
        self._contents = contents
        return self

    def attach_file(self, attach_file):
        self._attach_file = attach_file
        return self

    def send(self, to_mail):
        DoorayEmail.mail_check(to_mail)
        msg = MIMEMultipart("alternative")
        msg['Subject'] = Header(self._subject, 'utf-8')
        msg['From'] = self._from_mail
        msg['To'] = to_mail
        msg.attach(MIMEText(self._contents, 'html', 'utf-8'))

        # 파일추가
        if self._attach_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(self._attach_file, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(self._attach_file))
            msg.attach(part)

        self._mail.sendmail(self._from_mail, to_mail, msg.as_string())

    @classmethod
    def mail_check(cls, mail_address):
        if mail_address is None or len(mail_address) == 0:
            raise Exception("[EMAIL] email address is empty", mail_address)
        if mail_address.index("@") <= 0:
            raise Exception("[EMAIL] email address '@' not found.", mail_address)
        if mail_address.index(".") <= 0:
            raise Exception("[EMAIL] email address '.' not found.", mail_address)