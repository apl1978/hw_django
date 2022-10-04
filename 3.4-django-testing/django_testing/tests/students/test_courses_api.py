import pytest
from rest_framework.test import APIClient
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


@pytest.mark.django_db
def test_get_one_course(client, course_factory):
    count = Course.objects.count()
    courses = course_factory(_quantity=1)
    course = courses[0]
    response = client.get(f'/api/v1/courses/{course.id}/')

    assert response.status_code == 200
    assert Course.objects.count() == count + 1
    data = response.json()
    assert data['name'] == course.name


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    course = courses[0]
    response = client.get('/api/v1/courses/', data={'course_id': course.id})

    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == course.id


@pytest.mark.django_db
def test_filter_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    Course.objects.create(name='first course test search name')
    Course.objects.create(name='second course test search name')
    name = 'first course test search name'
    response = client.get('/api/v1/courses/', data={'name': name})

    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'test name'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_patch_course(client, course_factory):
    courses = course_factory(_quantity=1)
    course = courses[0]
    test_name = 'test name'
    response = client.patch(f'/api/v1/courses/{course.id}/', data={'name': test_name})

    assert (response.status_code == 204) or (response.status_code == 200)
    data = response.json()
    assert data['name'] == test_name


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=1)
    course = courses[0]
    count = Course.objects.count()
    response = client.delete(f'/api/v1/courses/{course.id}/')

    assert (response.status_code == 204) or (response.status_code == 200)
    assert Course.objects.count() == count - 1
