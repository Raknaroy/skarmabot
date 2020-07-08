#   ____  _  __
#  / ___|| |/ /__ _ _ __ _ __ ___   __ _
#  \___ \| ' // _` | '__| '_ ` _ \ / _` |
#   ___) | . \ (_| | |  | | | | | | (_| |
#  |____/|_|\_\__,_|_|  |_| |_| |_|\__,_|
#
# Yet another carma bot for telegram
# Copyright (C) 2020 Nikita Serba. All rights reserved
# https://github.com/sandsbit/skarmabot
#
# SKarma is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# SKarma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SKarma. If not, see <https://www.gnu.org/licenses/>.

import logging

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from skarma.config_parsers.email_info import EmailInfo


def send_email(to: str, subject: str, content: str):
    """Send email from email that is configured in email.conf"""

    blog = logging.getLogger('botlog')
    blog.info(f'Sending email "{subject}" to {to}')

    emi = EmailInfo()

    message = MIMEMultipart()
    message['From'] = emi.send_from
    message['To'] = to
    message['Subject'] = subject

    message.attach(MIMEText(content, 'plain'))

    blog.debug('Sending email: ended creating message')

    session = SMTP(emi.smtp_host, emi.smtp_port)
    session.starttls()
    session.login(emi.user, emi.password)

    blog.debug('Sending email: created SMTP session')

    body = message.as_string()
    session.sendmail(emi.send_from, to, body)

    blog.debug('Email successfully sent')
