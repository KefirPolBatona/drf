from rest_framework import serializers


from materials.models import Course, Lesson, Subscription
from materials.validators import validate_link_video


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    is_subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title_course', 'description_course', 'image_course',
                  'count_lesson', 'lessons', 'owner', 'is_subscription')

    def get_count_lesson(self, instance):
        """
        Возвращает количество уроков курса.
        """

        return instance.lesson.all().count()

    def get_lessons(self, instance):
        """
        Возвращает все уроки курса.
        """

        return [lesson.title_lesson for lesson in instance.lesson.all()]

    def get_is_subscription(self, course):
        """
        Возвращает True, если пользователь подписан на курс.
        """

        return Subscription.objects.filter(user=self.context['request'].user, course=course).exists()


class LessonSerializer(serializers.ModelSerializer):

    link_video = serializers.CharField(validators=[validate_link_video], default=None)

    class Meta:
        model = Lesson
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"
