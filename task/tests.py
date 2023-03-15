from django.test import TestCase
from task.models import User, Task


# Create your tests here.

class UserTest(TestCase):
    def test_register(self):
        # passwords aren't equal
        self.client.post("/register/", data={"phone_number": "09227562938",
                                             "username": "user1",
                                             "firstname": "user1_firstname",
                                             "lastname": "user1_lastname",
                                             "password1": "1111",
                                             "password2": "2222"
                                             })

        self.assertEqual(User.objects.count(), 0)
        # create new account
        self.client.post("/register/", data={"phone_number": "09227562938",
                                             "username": "user1",
                                             "firstname": "user1_firstname",
                                             "lastname": "user1_lastname",
                                             "password1": "a;ljf034",
                                             "password2": "a;ljf034"
                                             })
        self.assertEqual(User.objects.count(), 1)
