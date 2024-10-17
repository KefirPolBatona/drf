from rest_framework import viewsets, generics, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.permissons import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPagination

    def get_permissions(self):
        """
        Определяет права доступа к эндпоинтам.
        """

        if self.action == 'create':
            self.permission_classes = (~IsModerator,)
        elif self.action in ['destroy']:
            self.permission_classes = (~IsModerator | IsOwner,)
        elif self.action in ['list']:
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = (IsModerator | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Привязывает пользователя к создаваемому им курсу.
        """

        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """
        Привязывает пользователя к создаваемому им уроку.
        """

        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MaterialsPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]


class SubscriptionAPIView(views.APIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        """
        Создает / удаляет  подписку.
        """

        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка создана'

        return Response({"message": message})
