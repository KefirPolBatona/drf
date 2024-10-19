from datetime import datetime, timedelta

import pytz
from celery import shared_task

from config import settings
from users.models import User


@shared_task
def execute_user_is_block():
    """
    Блокирует пользователя при не активности более месяца.
    """

    timezone = pytz.timezone(settings.TIME_ZONE)
    required_datetime = datetime.now(timezone) - timedelta(days=30)
    for user in User.objects.filter(last_login__lt=required_datetime, is_block=False):
        user.is_block = True
        user.save()
