from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema

from src.api.mail_config import conf

from src.api.services.models import EmailSchema


async def send_email_async(email: EmailSchema):

    message = MessageSchema(
        subject=email.get('subject'),
        recipients=[email.get("email_to")],
        template_body=email.get("body"),
        subtype='html'
    )

    fm = FastMail(conf)

    await fm.send_message(message, template_name='email.html')


def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='html'
    )

    fm = FastMail(conf)

    background_tasks.add_task(
        fm.send_message, message, template_name='email.html')
