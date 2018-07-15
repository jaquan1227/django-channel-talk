from django.test import TestCase
from chat.models import Room, Message,User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testcase1",email="testcase1@jaquan.paik",nickname="testcase1")
       
    def test_users_create_test(self):
        user1 = User.objects.get(username="testcase1")
        self.assertEqual(user1.nickname, "testcase1")


class RoomTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testcase1",email="testcase1@jaquan.paik",nickname="testcase1")
        User.objects.create(username="testcase2",email="testcase2@jaquan.paik",nickname="testcase2")
        Room.objects.create(name="testroom1")

    def test_rooms_create_test(self):
        room1 = Room.objects.get(name='testroom1')
        user1 = User.objects.get(username="testcase1")
        user2 = User.objects.get(username="testcase2")
        self.assertEqual(room1.name, "testroom1")
        room1.user.add(user1)
        room1.user.add(user2)
        self.assertEqual(room1.user.first().nickname, "testcase2")


class MessageTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="testcase1",email="testcase1@jaquan.paik",nickname="testcase1")
        Room.objects.create(name="testroom1")
        
    def test_msgs_create_test(self):
        room1 = Room.objects.get(name='testroom1')
        user1 = User.objects.get(username="testcase1")
        msg1=Message.objects.create(text="test",user=user1,room=room1)
        self.assertEqual(msg1.user.username, "testcase1")

