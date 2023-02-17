from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        students_limit = settings.MAX_STUDENTS_PER_COURSE
        if self.context['view'].action in ['update', 'partial_update']:
            if 'students' in data:
                if self.instance.students.count() > students_limit or len(data['students']) > students_limit:
                    raise ValidationError('Не может быть больше 20 студентов на курсе!')
            else:
                return data
        return data