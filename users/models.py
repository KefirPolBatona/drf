from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Модель пользователя.
    """

    username = None
    email = models.EmailField(verbose_name='электронный адрес', unique=True)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(
        upload_to="avatar/", verbose_name="аватарка", **NULLABLE
    )

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    is_block = models.BooleanField(
        verbose_name='заблокирован',
        **NULLABLE,
        default=False
    )
    last_login = models.DateTimeField(verbose_name="Дата последнего входа", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ("сan_block_user", "Сan block user"),
        ]
        ordering = ['-id']


class Payment(models.Model):
    """
    Модель платежа.
    """

    PAYMENT_METHODS = (
        ("bank transfer", "банковский перевод"),
        ("cash", "наличные"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payment",
        **NULLABLE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        related_name="payment",
        **NULLABLE,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Урок",
        related_name="payment",
        **NULLABLE,
    )
    payment_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="сумма оплаты", **NULLABLE)
    date_payment = models.DateTimeField(auto_now_add=True, verbose_name="дата и время оплаты", **NULLABLE)
    payment_method = models.CharField(choices=PAYMENT_METHODS, verbose_name="способ оплаты", **NULLABLE)
    session_id = models.CharField(max_length=255, verbose_name="ID сессии", **NULLABLE)
    link = models.URLField(max_length=400, verbose_name="ссылка на оплату", **NULLABLE)

    def __str__(self):
        return f"Оплата {self.payment_amount} за '{self.course if self.course else self.lesson}' ({self.user})"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-id']
