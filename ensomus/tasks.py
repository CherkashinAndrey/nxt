from __future__ import absolute_import

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_emails(recipients, email_subject, email_body, sender):
    for email_addr in recipients:
        send_mail(
            email_subject,
            email_body,
            sender,
            [email_addr],
            html_message=email_body
        )
