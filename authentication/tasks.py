from .utils import Util
from celery import shared_task


@shared_task
def send_password_reset_email_task(data):
    return Util.send_password_reset_email(data)