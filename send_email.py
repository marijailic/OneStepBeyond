import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from email_template import get_template
from dotenv import load_dotenv


def send_email(data):
    load_dotenv()
    message = Mail(
        from_email=os.environ.get('FROM_EMAIL'),
        to_emails=os.environ.get('TO_EMAIL'),
        subject='Potvrda o uspješno kupljenoj karti | One Step Beyond (OSB)',
        html_content=get_template(data)
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
