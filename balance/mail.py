from django.core.mail import send_mail, EmailMultiAlternatives
from django.core import mail
from urllib3.util import connection
import re
import os
import time
subject = 'That’s your subject'

from_email = 'event@rsti.ru'
to = 'admin1@rsti.ru'


def send():
    email1 = mail.EmailMessage(
        'Оплата мегафон {0}'.format(time.strftime('%d-%m-%y')),
        'Таблица под скрепкой',
        'event@rsti.ru',
        [
            'admin1@rsti.ru',
            'maralin@rsti.ru',
            'PEO@rsti.ru',
            'peo5@rsti.ru',
            'bank@rsti.ru',
        ]
    )
    email1.attach_file('./payment.csv')
    email1.send()
    os.remove('./payment.csv') 
