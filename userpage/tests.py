from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from wechat.models import MyUser
from wechat.models import Meeting
from wechat.models import Relation
from codex.baseerror import InputError
from django.contrib.auth.models import User as SuperUser
import json
import userpage.urls
import userpage.views
import userpage.models
import unittest
from unittest import mock
from unittest.mock import patch
from datetime import datetime

class TestMeetingList(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name':'admin', 'account_pass':'123456', 'user_type':3})
        Meeting.create_new_meeting({'meeting_type':'boring',
            'name':'DoHomework',
            'max_people_num':4,
            'phone_num':'15546540758',
            'description':'work for living',
            'start_time':datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
            'end_time':datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
            'place':'dormitory',
            'status':0,
            'pic_url':'http',
            'organizer':user})

    def test_get(self):
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=1&status=0')
        self.assertTrue(response.json()['data']['status'] and len(response.json()['data']['list']) == 1)
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=2&status=0')
        self.assertTrue(not response.json()['data']['status'])
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=1&status=-1')
        self.assertTrue(response.json()['data']['status'] and len(response.json()['data']['list']) == 0)

class TestMeetingDetail(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name':'admin', 'account_pass':'123456', 'user_type':3})
        Meeting.create_new_meeting({'meeting_type':'boring',
            'name':'DoHomework',
            'max_people_num':4,
            'phone_num':'15546540758',
            'description':'work for living',
            'start_time':datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
            'end_time':datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
            'place':'dormitory',
            'status':0,
            'pic_url':'http',
            'organizer':user})

    def test_get(self):
        self.client.login(username='admin', password='123456')
        a = Meeting.objects.all()[0]
        response = self.client.get('/api/u/meeting/detail?meeting_id=6')
        self.assertTrue(response.json()['code'] == 0 and response.json()['data']['name'] == 'DoHomework')
        try:
            response = self.client.get('/api/u/meeting/detail?meeting_id=2')
        except:
            self.assertTrue(response.json()['msg'] == '未找到id为2的会议')

class TestMeetingCreate(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name':'admin', 'account_pass':'123456', 'user_type':2})
        Meeting.create_new_meeting({'meeting_type':'boring',
            'name':'DoHomework',
            'max_people_num':4,
            'phone_num':'15546540758',
            'description':'work for living',
            'start_time':datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
            'end_time':datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
            'place':'dormitory',
            'status':0,
            'pic_url':'http',
            'organizer':user})

    def test_get(self):
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/meeting/create?meeting_id=5')
        self.assertTrue(response.json()['code'] == 0)

class TestRegister(TestCase):
    def test_post(self):
        response = self.client.post('/api/u/register',{'account_name':'admin', 'account_pass':'123456', 'user_type':2})
        self.assertTrue(response.json()['code'] == 0)

class TestLogin(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})

    def test_get(self):
        response = self.client.get('/api/u/login')
        self.assertTrue(response.json()['data']['type'] == 0)
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/login')
        self.assertTrue(response.json()['data']['type'] == 2 and response.json()['data']['name'] == '用户admin')

    def test_post(self):
        response = self.client.post('/api/u/login',{'username': 'admin', 'password': '123456'})
        self.assertTrue(response.json()['code'] == 0 and response.json()['data'] == 1)

class TestLogout(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})

    def test_get(self):
        response = self.client.get('/api/u/logout')
        self.assertTrue(response.json()['code'] == -1)
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/logout')
        self.assertTrue(response.json()['code'] == 0)

class TestUserBind(TestCase):
    def setUp(self):
        fixtures = ['users.json']
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})

    def test(self):
        response = self.client.get('/api/u/user/bind?open_id=1')
        self.assertTrue(response.json()['msg'] == '未找到符合要求的对应微信用户!')
        response = self.client.post('/api/u/user/bind',{'openid':1, 'account': 'admin', 'password': '123456'})
        self.assertTrue(response.json()['code'] == -1)
        #response = self.client.get('/api/u/user/bind?open_id=1')
        #self.assertTrue(response.json()['code'] == 0)

class TestUserMessage(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})

    def test(self):
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/user/detail')
        self.assertTrue(response.json()['code'] == 0)
        response = self.client.post('/api/u/user/detail',{'description':'lalala'})
        self.assertTrue(response.json()['code'] == 0)
        response = self.client.get('/api/u/user/detail')
        self.assertTrue(response.json()['code'] == 0 and response.json()['data']['description'] == 'lalala')

class TestGetRelation(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})
        meet = Meeting(meeting_type='boring',
                       name='DoHomework',
                       max_people_num=4,
                       phone_num='15546540758',
                       description='work for living',
                       start_time=datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                       end_time=datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                       place='dormitory',
                       status=0,
                       pic_url='http',
                       organizer=user)
        meet.save()
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 1})
        relation = Relation(user=user2, meeting=meet, status=3)
        relation.save()

    def test_get(self):
        self.client.login(username='admin2', password='123456')
        response = self.client.get('/api/u/relation/get')
        self.assertTrue(response.json()['code'] == 0 and len(response.json()['data']['rel3']) == 1)

class TestChangeRelation(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})
        meet = Meeting(meeting_type='boring',
                        name='DoHomework',
                        max_people_num=4,
                        phone_num='15546540758',
                        description='work for living',
                        start_time=datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                        end_time=datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                        place='dormitory',
                        status=0,
                        pic_url='http',
                        organizer=user)
        meet.save()
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 1})
        relation = Relation(user=user2,meeting=meet,status=3)
        relation.save()

    def test_get(self):
        self.client.login(username='admin2', password='123456')
        response = self.client.get('/api/u/relation/change?relation=2&meet_id=1')
        self.assertTrue(response.json()['code'] == 0)

    def test_post(self):
        self.client.login(username='admin', password='123456')
        a = Relation.objects.all()[0]
        b = Meeting.objects.all()[0]
        c = MyUser.objects.all()[0]
        d = MyUser.objects.all()[1]
        #self.client.post('/api/u/relation/change?relation=2&meet_id=2&user_id=4')

class TestGetPublish(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})
        meet = Meeting(meeting_type='boring',
                        name='DoHomework',
                        max_people_num=4,
                        phone_num='15546540758',
                        description='work for living',
                        start_time=datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                        end_time=datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                        place='dormitory',
                        status=0,
                        pic_url='http',
                        organizer=user)
        meet.save()
    def test_get(self):
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/publish/list')
        self.assertTrue(response.json()['code'] == 0 and len(response.json()['data']) == 1)

class TestParticipateManage(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})
        meet = Meeting(meeting_type='boring',
                       name='DoHomework',
                       max_people_num=4,
                       phone_num='15546540758',
                       description='work for living',
                       start_time=datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                       end_time=datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                       place='dormitory',
                       status=0,
                       pic_url='http',
                       organizer=user)
        meet.save()
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 1})
        relation = Relation(user=user2, meeting=meet, status=3)
        relation.save()

    def test_get(self):
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/participant?meet_id=8')
        self.assertTrue(response.json()['code'] == 0 and len(response.json()['data']) == 1)







