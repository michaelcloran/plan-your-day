from datetime import date
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, Tasks
from .views import *


# Create your tests here.
class TestViews(TestCase):
    """
    Test cases for Category and Task functions
    """
    def setUp(self):
        """ Setup Test """
        username = "tester"
        password = "ahzjsbajbs123"
        email = "tester@test.com"

        user_model = get_user_model()

        #  Create user
        self.user = user_model.objects.create_user(
            username = username,
            password = password,
            email = email,
            is_superuser = True
        )
        logged_in = self.client.login(username=username,
                                      password = password,
                                      email = email)
        self.assertTrue(logged_in)

        #  Create Category
        category = Category.objects.create(
            category_name = "project1",
            author = self.user
        )

        task = Tasks.objects.create(
            author = self.user,
            task_name = 'task1',
            task_description = 'test description',
            is_urgent = False,
            date = date.today(),
            start_time = "12",
            end_time = "13",
            category_id = category,
            finished_task = False
        )

    def test_category_list(self):
        """ Test manage Categories page """
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/categories.html")

    def test_add_category_page(self):
        """ Test adding a category page """
        response = self.client.get("/category/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/add_category.html')

    def test_add_task_page(self):
        """ Test adding a task page """
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/add_task.html')

    def test_tasks_list(self):
        """ Test manage Tasks page """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")

    def test_edit_task_page(self):
        """ Test edit task when owner """
        response = self.client.get(reverse("tasks_edit", args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_edit_task_page_unauthorized_user(self):
        """
        Test user cant edit another
        user tasks
        """
        user_model = get_user_model()
        self.client = Client()
        # Create second user for 403 errors
        username = 'test'
        password = 'Dirty56'
        email = 'test@test.com'
        user = user_model.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_superuser=False
        )
        logged_in = self.client.login(
            username=username,
            email=email,
            password=password
        )

        self.assertTrue(logged_in)

        category = Category.objects.create(
            category_name = "project1",
            author = self.user
        )

        print(self.user)

        task = Tasks.objects.create(
            author = self.user,
            task_name = 'task1',
            task_description = 'test description',
            is_urgent = False,
            date = date.today(),
            start_time = "12",
            end_time = "13",
            category_id = category,
            finished_task = False
        )

        data = {
            'author': 'tester',
            'task_name' : 'task1',
            'task_description' : 'test description testing',
            'is_urgent': False,
            'date': date.today(),
            'start_time' : "12",
            'end_time': "13",
            'category_id': category,
            'finished_task': False
        }

        response = self.client.post('/edit_task/1/', data)
        self.assertEqual(response.status_code, 404)

    def test_delete_task(self):
        """ Testing task delete with task id of 1 """
        response = self.client.delete(reverse(task_delete, args=[1]))
        self.assertEqual(response.status_code, 302)
