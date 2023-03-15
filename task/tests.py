import requests
from django.test import TestCase
from task.models import User, Task, Board, Workspace


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
                                             "first_name": "user1_firstname",
                                             "last_name": "user1_lastname",
                                             "password1": "a;ljf034",
                                             "password2": "a;ljf034",
                                             })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username="user1").phone_number, "09227562938")
        self.assertEqual(User.objects.get(username="user1").first_name, "user1_firstname")
        self.assertEqual(User.objects.get(username="user1").last_name, "user1_lastname")
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
        board1 = Board.objects.get(name="board1")
        self.assertEqual(Board.objects.count(), 1)
        self.assertEqual(board1.members.get(username="user1"), User.objects.get(username="user1"))
        self.assertEqual(board1.workspace, None)
        self.assertEqual(board1.creator, User.objects.get(username="user1"))


class TaskTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("user1", password="a;ljf034")

    def test_create_task(self):
        # setup board
        self.client.login(username="user1", password="a;ljf034")
        self.client.post("/create-board/", data={"workspace": "",
                                                 "name": "board1",
                                                 "members": "1",
                                                 "creator": "1"})
        response = self.client.post("/create-task/", data={"name": "task1", "state": "1",
                                                           "description": "description1",
                                                           "members": "1",
                                                           "board": "1",
                                                           "priority": "1"
                                                           })
        print(response)
        task = Task.objects.get(name="task1")
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.creator, User.objects.get(username="user1"))
        self.assertEqual(task.state, 1)
        self.assertEqual(task.description, "description1")
        self.assertEqual(list(task.members.all()), [User.objects.get(username="user1")])
        self.assertEqual(task.board, Board.objects.get(name="board1"))
        self.assertEqual(task.priority, 1)





class FullScenarioTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user("user1", password="a;ljf034", phone_number="09381009988")
        user2 = User.objects.create_user("user2", password="asdfl;j34ro34jf", phone_number="09381009989")
        user3 = User.objects.create_user("user3", password="lf97ds9afkjls", phone_number="09381009990")
        user4 = User.objects.create_user("user4", password="ljfa;slf", phone_number="09381009987")
        workspace = Workspace.objects.create(name="work1", creator_id=1)
        workspace.members.set([user1, user2, user3, user4])
        board1 = Board.objects.create(workspace=workspace, name="board1")
        board1.members.set([user1, user2, user3, user4])
        task1 = Task.objects.create(name="task1", creator_id=1, state=1, description="description11", board=board1,
                                    priority=1)
        task1.members.set([user1, user2, user3, user4])

    def test_all_scenario(self):
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(Board.objects.count(), 1)
        self.assertEqual(Task.objects.count(), 1)
        self.client.login(username="user1", password="a;ljf034")
        self.client.post("/create-task/", data={"name": "task2", "state": 1,
                                                "description": "des1",
                                                "members": "1",
                                                "board": "1",
                                                "priority": 1
                                                })
        task = Task.objects.get(name="task2")
        self.assertEqual(task.creator.username, "user1")
        self.assertEqual(task.state, 1)
        self.assertEqual(task.description, "des1")
        self.assertEqual(task.members.get(username="user1").username, "user1")
        self.assertEqual(task.board.name, "board1")
        self.assertEqual(task.priority, 1)