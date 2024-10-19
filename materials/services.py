from materials.models import Subscription


def get_list_email_user(course):
    """
    Возвращает список email подписчиков курса.
    """

    list_email_user = []
    for subscription in Subscription.objects.all().filter(course=course):
        list_email_user.append(subscription.user.email)

    return list_email_user
