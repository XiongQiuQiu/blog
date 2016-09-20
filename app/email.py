from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to, subject, template, **kwargs):
    app = current_app.get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PRFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(targer=send_async_email, args=[app, msg])
    the.start()
    return thr
