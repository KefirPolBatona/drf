from rest_framework.serializers import ValidationError


def validate_link_video(value=None):
    """
    Проверяет ссылку на наличие в ней youtube.com.
    """

    if value and 'youtube.com' not in value:
        raise ValidationError("Ссылка на недопустимый ресурс")
