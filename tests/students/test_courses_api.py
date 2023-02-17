import random

from rest_framework.test import APIClient
import pytest
from model_bakery import baker

from students.models import Course, Student

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_name():
    return ["Python", "1C", "Java"]

@pytest.fixture
def random_int():
    return set([random.randint(0, 20) for i in range(10)])


@pytest.mark.django_db
def test_course_retrive(client, course_factory):
    course = course_factory(name='Python')
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Python'


@pytest.mark.django_db
def test_course_list(client, course_factory, course_name):
    course = course_factory(_quantity=10, name=random.choice(course_name))
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 10
    for i, d in enumerate(data):
        assert d['name'] in course_name
        assert d['name'] == data[i]['name']


@pytest.mark.django_db
def test_course_filter_id(client, course_factory):
    course = course_factory(id=40)
    response = client.get('/api/v1/courses/?id=40')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == 40



@pytest.mark.django_db
def test_course_filter_name(client, course_factory, course_name):
    course = course_factory(_quantity=10, name=random.choice(course_name))
    response = client.get('/api/v1/courses/?name=Python')
    data = response.json()
    assert response.status_code == 200
    for d in data:
        assert d['name'] == "Python"


@pytest.mark.django_db
def test_course_create(client):
    count = Course.objects.count()
    context = {'name': 'C#'}
    response = client.post('/api/v1/courses/', data=context)
    assert response.status_code == 201
    assert Course.objects.count() == count+1


@pytest.mark.django_db
def test_course_update(client, course_factory):
    course = course_factory(name="Linux")
    id = Course.objects.get(name='Linux').id
    response = client.patch(f'/api/v1/courses/{id}/', data={'name': 'SQL'})
    assert response.status_code == 200
    assert Course.objects.get(id=id).name == "SQL"


@pytest.mark.django_db
def test_course_delete(client, course_factory):
    course = course_factory(name="PostgreSQL")
    id = Course.objects.get(name='PostgreSQL').id
    request_get = client.get(f'/api/v1/courses/')
    data = request_get.json()
    assert data[0]['name'] == 'PostgreSQL'
    response = client.delete(f'/api/v1/courses/{id}/')
    assert response.status_code == 204
    assert Course.objects.filter(id=id).first() == None


@pytest.mark.parametrize(
['student_count', 's_code'],
    ((2, 200), (3, 400), (1, 200), (4, 400))
)
@pytest.mark.django_db
def test_student_validation(client, student_count, student_factory, course_factory, settings, s_code):
    settings.MAX_STUDENTS_PER_COURSE = 2
    stud = student_factory(_quantity=student_count)
    course = course_factory()
    response = client.patch(f'/api/v1/courses/{course.id}/', data={'students': [s.id for s in stud]})
    assert response.status_code == s_code




