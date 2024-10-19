from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.models import Course
from materials.services import get_list_email_user


@shared_task
def send_mail_update_course(pk_course):
    """
    Отправляет сообщение подписчикам курса.
    """

    course = Course.objects.get(id=pk_course)
    send_mail(
        subject=f"Обновление",
        message=f"Курс {course.title_course} обновлен",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=get_list_email_user(course),
        fail_silently=False,
    )
