from flask import Flask, request
from celery import Celery
from flask_mail import Mail, Message
import logging
from datetime import datetime

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.hostinger.com',
    MAIL_PORT=465,
    MAIL_USERNAME='hngtest@waltanforte.com',
    MAIL_PASSWORD='@HNGtest2024',
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
)

mail = Mail(app)

# Configure Celery
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['broker_url']
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

app.config.update(
    broker_url='amqp://localhost:5672',
    result_backend='rpc://'
)

celery = make_celery(app)

@celery.task
def send_async_email(recipients, subject, body):
    with app.app_context():
        msg = Message(subject, sender='hngtest@waltanforte.com', recipients=[recipients])
        msg.body = body
        mail.send(msg)

@app.route('/', methods=['GET'])
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        # Validate email format
        if '@' in sendmail:
            subject = 'Hello'
            body = 'This is a test email sent from the Flask app with Celery.'
            send_async_email.delay(sendmail, subject, body)
            return 'Email sent!'
        else:
            return 'Invalid email address format.'

    if talktome is not None:
        # Log current time to /var/log/messaging_system.log
        log_path = '/var/log/messaging_system.log'
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, 'a') as log_file:
            log_file.write(f'Message received at {current_time}\n')
        return 'Logged!'

    return 'No valid parameter provided.'

if __name__ == '__main__':
    app.run(debug=True)

