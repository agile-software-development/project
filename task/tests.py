from django.test import TestCase
from task.models import User


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