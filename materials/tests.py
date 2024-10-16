from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """
    Тестирование CRUD уроков.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(email='test888@gmail.com')
        self.moderator = User.objects.create(email='test777@gmail.com')
        self.owner = User.objects.create(email='9232485@gmail.com')
        self.group = Group.objects.create(name='moderator')
        self.moderator.groups.add(self.group)
        self.course = Course.objects.create(title_course='Тестовый курс', owner=self.owner)
        self.lesson = Lesson.objects.create(title_lesson='Тестовый урок', course=self.course, owner=self.owner)

        self.new_lesson = Lesson.objects.create(title_lesson='Тестовый урок', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.owner)

    def test_lesson_create(self):
        """
        Тестирование: создания урока, пользователь не авторизован, ссылка на видео валидна.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:lesson-create")
        data = {
            "title_lesson": "Тестовый урок",
            "link_video": "http://youtube.com/"
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_create_authenticate(self):
        """
        Тестирование: создания урока, пользователь авторизован, ссылка на видео валидна.
        """

        url = reverse("materials:lesson-create")
        data = {
            "title_lesson": "Тестовый урок",
            "link_video": "http://youtube.com/"
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_lesson_create_moderator(self):
        """
        Тестирование: создание урока, пользователь модератор, ссылка на видео валидна.
        """

        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lesson-create")
        data = {
            "title_lesson": "Тестовый урок",
            "link_video": "http://youtube.com/"
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_validate_link_video(self):
        """
        Тестирование: создание урока, пользователь авторизован, ссылка на видео не валидна.
        """

        url = reverse("materials:lesson-create")
        data = {
            "title_lesson": "Тестовый урок",
            "link_video": "http://slkjhfuv.com/"
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_lesson_list(self):

        """
        Тестирование: вывод списка уроков, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse('materials:lesson-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_list_authenticate(self):
        """
        Тестирование: вывод списка уроков, пользователь авторизован.
        """

        url = reverse('materials:lesson-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_list_moderator(self):
        """
        Тестирование: вывод списка уроков, пользователь модератор.
        """

        self.client.force_authenticate(user=self.moderator)
        url = reverse('materials:lesson-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_retrieve(self):
        """
        Тестирование: вывод одного урока, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_retrieve_authenticate(self):
        """
        Тестирование: вывод одного урока, пользователь авторизован.
        """

        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_retrieve_moderator(self):
        """
        Тестирование: вывод одного урока, пользователь модератор.
        """

        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update(self):
        """
        Тестирование: редактирование урока, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            'title_lesson': 'Измененный тестовый урок',
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_update_authenticate(self):
        """
        Тестирование: редактирование урока, пользователь авторизован.
        """

        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            'title_lesson': 'Измененный тестовый урок',
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            data.get('title_lesson'),
            'Измененный тестовый урок'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update_moderator(self):
        """
        Тестирование: редактирование урока, пользователь модератор.
        """

        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            'title_lesson': 'Измененный тестовый урок',
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_delete(self):
        """
        Тестирование: удаление урока, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_delete_authenticate(self):
        """
        Тестирование: удаление урока, пользователь авторизован.
        """

        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_lesson_delete_moderator(self):
        """
        Тестирование: удаление урока, пользователь модератор.
        """

        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )


class SubscriptionTestCase(APITestCase):
    """
    Тестирование подписок на обновления курса.
    """

    def setUp(self):
        self.user = User.objects.create(email='9232485@gmail.com')
        self.course_subscription = Course.objects.create(title_course='Тестовый курс', owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course_subscription, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        """
        Тестирование: создание подписки, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:subscription")
        data = {
            "course": self.course_subscription.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_create_subscription_authenticate(self):
        """
        Тестирование: создание подписки, пользователь авторизован.
        """

        url = reverse("materials:subscription")
        data = {
            "course": self.course_subscription.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_subscription(self):
        """
        Тестирование: удаление подписки, пользователь авторизован.
        """

        url = reverse("materials:subscription")
        data = {
            "course": self.course_subscription.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_subscription_authenticate(self):
        """
        Тестирование: удаление подписки, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:subscription")
        data = {
            "course": self.course_subscription.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
