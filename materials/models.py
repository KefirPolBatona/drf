from django.db import models


NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """
    Модель курса.
    """

    title_course = models.CharField(max_length=250, verbose_name="название курса")
    description_course = models.TextField(verbose_name="описание курса", **NULLABLE)
    image_course = models.ImageField(upload_to="image_course/", verbose_name="превью", **NULLABLE)

    def __str__(self):
        return self.title_course

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-id']


class Lesson(models.Model):
    """
    Модель урока.
    """

    title_lesson = models.CharField(max_length=250, verbose_name="название урока")
    description_lesson = models.TextField(verbose_name="описание урока", **NULLABLE)
    image_lesson = models.ImageField(upload_to="image_lesson/", verbose_name="превью", **NULLABLE)
    link_video = models.URLField(max_length=350, verbose_name="ссылка на видео", **NULLABLE)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        **NULLABLE,
    )

    def __str__(self):
        return self.title_lesson

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['-id']

