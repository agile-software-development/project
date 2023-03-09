from django.test import TestCase
from task.models import User, Task


# Create your tests here.

class UserTest(TestCase):
    def test_register(self):
        # create new account
        self.client.post("/user/signup/", data={"phone_number": "09227562938",
                                                "username": "user1",
                                                "firstname": "user1_firstname",
                                                "lastname": "user1_lastname",
                                                "password1": "a;ljf034",
                                                "password2": "a;ljf034"
                                                })
        self.assertEqual(User.objects.count(), 1)


class TaskTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("user1", password="a;ljf034")

    def test_create_task(self):
        self.client.login(username="user1", password="a;ljf034")
        response = self.client.post("/user/create-task/", data={"name": "task1",
                                                                "creator": "1",
                                                                "state": "2",
                                                                "description": "description1",
                                                                "members": "1"
                                                                })
        print(response)
        self.assertEqual(Task.objects.count(), 1)
