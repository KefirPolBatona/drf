from rest_framework import serializers


from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('title_course', 'description_course', 'image_course', 'count_lesson', 'lessons')

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


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

