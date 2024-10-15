from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.permissons import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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
