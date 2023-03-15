import requests
from django.test import TestCase
from task.models import User, Task, Board


# Create your tests here.

class UserTest(TestCase):
    def test_register(self):
        ## fails
        # passwords aren't equal
        self.client.post("/register/", data={"phone_number": "09227562938",
                                             "username": "user1",
                                             "firstname": "user1_firstname",
                                             "lastname": "user1_lastname",
                                             "password1": "1111",
                                             "password2": "2222"
                                             })

        self.assertEqual(User.objects.count(), 0)
        # password is only number
        self.client.post("/register/", data={"phone_number": "09227562938",
                                             "username": "user1",
                                             "firstname": "user1_firstname",
                                             "lastname": "user1_lastname",
                                             "password1": "111",
                                             "password2": "111"
                                             })
        self.assertEqual(User.objects.count(), 0)
        # password similar to username
        self.client.post("/register/", data={"phone_number": "09227562938",
                                             "username": "user1",
                                             "firstname": "user1_firstname",
                                             "lastname": "user1_lastname",
                                             "password1": "user1",
                                             "password2": "user1"
                                             })
        self.assertEqual(User.objects.count(), 0)

        # create new account successfully
        self.client.post("/register/", data={"phone_number": "09227562938",
                                             "username": "user1",
                                             "firstname": "user1_firstname",
                                             "lastname": "user1_lastname",
                                             "password1": "a;ljf034",
                                             "password2": "a;ljf034"
                                             })
        self.assertEqual(User.objects.count(), 1)
        # used username
        self.client.post("/register/", data={"phone_number": "09227562938",
                                             "username": "user1",
                                             "first_name": "user1_firstname",
                                             "last_name": "user1_lastname",
                                             "password1": "a;ljlkjf034",
                                             "password2": "a;ljlkjf034"
                                             })
        # no user should create - still one only
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username="user1").phone_number, "09227562938")


    def test_login(self):
        # setup   creating account
        User.objects.create_user("user1", password="a;ljf034")
        # wrong username
        response = self.client.login(username="user11", password="a;ljf034")
        self.assertEqual(response, False)

        # wrong password
        response = self.client.login(username="user1", password="a1;ljf034")
        self.assertEqual(response, False)

        # login successfully
        response = self.client.login(username="user1", password="a;ljf034")
        self.assertEqual(response, True)

    def test_edit_save(self):
        # setup   creating account
        User.objects.create_user("user1", password="a;ljf034")
        # edit successfully
        self.client.login(username="user1", password="a;ljf034")
        response = self.client.post("/profile/", data={"phone_number": "09227562939",
                                                       "first_name": "saleh",
                                                       "last_name": "shoji",
                                                       "theme": "light"
                                                       })
        self.assertEqual(str(response).__contains__("302"), True)
        self.assertEqual(User.objects.get(username="user1").phone_number, "09227562939")
        self.assertEqual(User.objects.get(username="user1").first_name, "saleh")
        self.assertEqual(User.objects.get(username="user1").last_name, "shoji")
        self.assertEqual(User.objects.get(username="user1").theme, "light")


class TaskTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("user1", password="a;ljf034")

    def test_create_task(self):
        # empty task list in start

        # create task successfully
        self.client.login(username="user1", password="a;ljf034")
        response = self.client.post("/create-task/", data={"name": "task1",
                                                           "creator": "1",
                                                           "state": "2",
                                                           "description": "description1",
                                                           "members": "1",
                                                           "priority": "3"
                                                           })
        print(response)
        self.assertEqual(Task.objects.count(), 1)


class BoardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("user1", password="a;ljf034")

    def test_create_board(self):
        # create task successfully
        res = self.client.login(username="user1", password="a;ljf034")
        response = self.client.post("/create-board/", data={"workspace": "",
                                                            "name": "board1",
                                                            "members": "1",
                                                            "creator": "1"})
        print(response)
        self.assertEqual(Board.objects.count(), 1)

# class BoardTest(TestCase):
