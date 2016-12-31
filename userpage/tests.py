from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from wechat.models import MyUser
from wechat.models import Meeting
from wechat.models import Relation
from wechat.models import Notice
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

#获取会议列表
class TestMeetingList(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name':'admin', 'account_pass':'123456', 'user_type':3})
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 2})
        Meeting.create_new_meeting({'meeting_type':'haha',
            'name':'DoHomework',
            'max_people_num':4,
            'phone_num':'15546540758',
            'description':'work for living',
            'start_time':datetime.strptime("2017-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
            'end_time':datetime.strptime("2017-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
            'place':'dormitory',
            'status':0,
            'pic_url':'http',
            'organizer':user2})
        Meeting.create_new_meeting({'meeting_type': 'haha',
            'name': 'DoHomework2',
            'max_people_num': 4,
            'phone_num': '15546540758',
            'description': 'work for living',
            'start_time': datetime.strptime("2017-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
            'end_time': datetime.strptime("2017-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
            'place': 'dormitory',
            'status': 1,
            'pic_url': 'http',
            'organizer': user2})
        Meeting.create_new_meeting({'meeting_type': 'haha',
            'name': 'DoHomework3',
            'max_people_num': 4,
            'phone_num': '15546540758',
            'description': 'work for living',
            'start_time': datetime.strptime("2017-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
            'end_time': datetime.strptime("2017-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
            'place': 'dormitory',
            'status': 2,
            'pic_url': 'http',
            'organizer': user2})

    def test_get(self):
        self.client.login(username='admin', password='123456')
        #正常输入
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=1&status=-1')
        Judge = response.json()['data']['status'] and len(response.json()['data']['list']) == 2 \
                and response.json()['data']['list'][0]['name'] == 'DoHomework2' \
                and response.json()['data']['list'][1]['name'] == 'DoHomework3'
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=1&status=0')
        Judge = Judge and response.json()['data']['status'] and len(response.json()['data']['list']) == 1 \
                and response.json()['data']['list'][0]['name'] == 'DoHomework'
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=1&status=1')
        Judge = Judge and response.json()['data']['status'] and len(response.json()['data']['list']) == 1 \
                and response.json()['data']['list'][0]['name'] == 'DoHomework2'
        response = self.client.get('/api/u/meeting/list?meeting_num=1&page_index=1&status=-1')
        Judge = Judge and response.json()['data']['status'] and len(response.json()['data']['list']) == 1 \
                and response.json()['data']['list'][0]['name'] == 'DoHomework2'
        response = self.client.get('/api/u/meeting/list?meeting_num=1&page_index=2&status=-1')
        Judge = Judge and response.json()['data']['status'] and len(response.json()['data']['list']) == 1 \
                and response.json()['data']['list'][0]['name'] == 'DoHomework3'
        #错误输入
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=2&status=-1')
        Judge = Judge and not response.json()['data']['status'] and len(response.json()['data']['list']) == 0
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=2&status=0')
        Judge = Judge and not response.json()['data']['status'] and len(response.json()['data']['list']) == 0
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=2&status=1')
        Judge = Judge and not response.json()['data']['status'] and len(response.json()['data']['list']) == 0
        Meeting.objects.all().delete()
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=2&status=-1')
        Judge = Judge and not response.json()['data']['status'] and len(response.json()['data']['list']) == 0
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=2&status=0')
        Judge = Judge and not response.json()['data']['status'] and len(response.json()['data']['list']) == 0
        response = self.client.get('/api/u/meeting/list?meeting_num=10&page_index=2&status=1')
        Judge = Judge and not response.json()['data']['status'] and len(response.json()['data']['list']) == 0
        self.assertTrue(Judge)

#获取会议详情
class TestMeetingDetail(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 3})
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 2})
        user3 = MyUser.create_new_user({'account_name': 'admin3', 'account_pass': '123456', 'user_type': 1})
        Meeting.create_new_meeting({'meeting_type': 'haha',
                'name': 'DoHomework',
                'max_people_num': 4,
                'phone_num': '15546540758',
                'description': 'work for living',
                'start_time': datetime.strptime("2017-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                'end_time': datetime.strptime("2017-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                'place': 'dormitory',
                'status': 0,
                'pic_url': 'http',
                'organizer': user})
        Meeting.create_new_meeting({'meeting_type': 'haha',
                'name': 'DoHomework2',
                'max_people_num': 4,
                'phone_num': '15546540758',
                'description': 'work for living',
                'start_time': datetime.strptime("2017-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                'end_time': datetime.strptime("2017-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                'place': 'dormitory',
                'status': 1,
                'pic_url': 'http',
                'organizer': user3})
        Meeting.create_new_meeting({'meeting_type': 'haha',
                'name': 'DoHomework3',
                'max_people_num': 4,
                'phone_num': '15546540758',
                'description': 'work for living',
                'start_time': datetime.strptime("2017-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                'end_time': datetime.strptime("2017-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                'place': 'dormitory',
                'status': 2,
                'pic_url': 'http',
                'organizer': user2})

    def test_get(self):
        #正确输入
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/meeting/detail?meeting_id=1')
        Judge = response.json()['code'] == 0 and response.json()['data']['name'] == 'DoHomework'
        response = self.client.get('/api/u/meeting/detail?meeting_id=2')
        Judge = Judge and response.json()['code'] == 0 and response.json()['data']['name'] == 'DoHomework2'
        response = self.client.get('/api/u/meeting/detail?meeting_id=3')
        Judge = Judge and response.json()['code'] == 0 and response.json()['data']['name'] == 'DoHomework3'
        self.client.logout()
        self.client.login(username='admin2', password='123456')
        response = self.client.get('/api/u/meeting/detail?meeting_id=1')
        Judge = Judge and response.json()['code'] == 0 and response.json()['data']['name'] == 'DoHomework'
        response = self.client.get('/api/u/meeting/detail?meeting_id=2')
        Judge = Judge and response.json()['code'] == 0 and response.json()['data']['name'] == 'DoHomework2'
        response = self.client.get('/api/u/meeting/detail?meeting_id=3')
        Judge = Judge and response.json()['code'] == 0 and response.json()['data']['name'] == 'DoHomework3'
        self.client.logout()
        self.client.login(username='admin3', password='123456')
        response = self.client.get('/api/u/meeting/detail?meeting_id=1')
        Judge = Judge and response.json()['code'] == 2
        response = self.client.get('/api/u/meeting/detail?meeting_id=2')
        Judge = Judge and response.json()['code'] == 0 and response.json()['data']['name'] == 'DoHomework2'
        response = self.client.get('/api/u/meeting/detail?meeting_id=3')
        Judge = Judge and response.json()['code'] == 0 and response.json()['data']['name'] == 'DoHomework3'
        #错误输入
        try:
            response = self.client.get('/api/u/meeting/detail?meeting_id=4')
        except:
            Judge = Judge and response.json()['msg'] == '未找到id为4的会议'
            self.assertTrue(Judge)

class TestMeetingCreate(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 3})
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 2})
        user3 = MyUser.create_new_user({'account_name': 'admin3', 'account_pass': '123456', 'user_type': 1})
        user4 = MyUser.create_new_user({'account_name': 'admin4', 'account_pass': '123456', 'user_type': 2})
        Meeting.create_new_meeting({'meeting_type': 'haha',
                                    'name': 'DoHomework',
                                    'max_people_num': 4,
                                    'phone_num': '15546540758',
                                    'description': 'work for living',
                                    'start_time': datetime.strptime("2017-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                                    'end_time': datetime.strptime("2017-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                                    'place': 'dormitory',
                                    'status': 0,
                                    'pic_url': 'http',
                                    'organizer': user2})
        Meeting.create_new_meeting({'meeting_type': 'haha',
                                    'name': 'DoHomework2',
                                    'max_people_num': 4,
                                    'phone_num': '15546540758',
                                    'description': 'work for living',
                                    'start_time': datetime.strptime("2017-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                                    'end_time': datetime.strptime("2017-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                                    'place': 'dormitory',
                                    'status': 1,
                                    'pic_url': 'http',
                                    'organizer': user2})
        Meeting.create_new_meeting({'meeting_type': 'haha',
                                    'name': 'DoHomework3',
                                    'max_people_num': 4,
                                    'phone_num': '15546540758',
                                    'description': 'work for living',
                                    'start_time': datetime.strptime("2017-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                                    'end_time': datetime.strptime("2017-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                                    'place': 'dormitory',
                                    'status': 2,
                                    'pic_url': 'http',
                                    'organizer': user2})

    def test_get(self):
        #正确输入
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/meeting/create?meeting_id=1')
        Judge = response.json()['code'] == 0
        self.client.logout()
        self.client.login(username='admin2', password='123456')
        response = self.client.get('/api/u/meeting/create?meeting_id=2')
        Judge = Judge and response.json()['code'] == 0
        self.client.logout()
        self.client.login(username='admin3', password='123456')
        # 错误输入
        try:
            response = self.client.get('/api/u/meeting/create?meeting_id=3')
        except:
            Judge = Judge and response.json()['msg'] == '您没有权限删除该会议！'
            self.client.logout()
            self.assertTrue(Judge)

    def test_post(self):
        self.client.login(username='admin4', password='123456')
        response = self.client.post('/api/u/meeting',{
            'meeting_type':'haha',
            'name':'haha',
            'max_people_num':4,
            'phone_num':'15546540758',
            'description':'haha',
            'start_time':"2017-12-25-0",
            'end_time':"2017-12-25-12",
            'place':'haha',
            'uploadpic':'../static/img/bg.png'
        })

class TestRegister(TestCase):
    def test_post(self):
        response = self.client.post('/api/u/register',{'account_name':'admin', 'account_pass':'123456', 'user_type':2})
        Judge = response.json()['code'] == 0
        response = self.client.post('/api/u/register',{'account_name':'admin2', 'account_pass': '123456', 'user_type': 2})
        Judge = Judge and response.json()['code'] == 0
        response = self.client.post('/api/u/register',{'account_name':'admin3', 'account_pass': '123456', 'user_type': 2})
        Judge = Judge and response.json()['code'] == 0
        response = self.client.post('/api/u/register',{'account_name':'admin', 'account_pass':'123456', 'user_type':1})
        Judge = Judge and response.json()['code'] == -1
        self.assertTrue(Judge)

class TestLogin(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})

    def test_get(self):
        response = self.client.get('/api/u/login')
        Judge = response.json()['data']['type'] == 0
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/login')
        Judge = Judge and response.json()['data']['type'] == 2 and response.json()['data']['name'] == '用户admin'
        self.assertTrue(Judge)

    def test_post(self):
        response = self.client.post('/api/u/login',{'username': 'admin', 'password': '123456'})
        Judge = response.json()['code'] == 0 and response.json()['data'] == 1
        self.client.logout()
        response = self.client.post('/api/u/login',{'username': 'admin', 'password': '1234567'})
        Judge = Judge and response.json()['code'] == 0 and response.json()['data'] == 2
        self.assertTrue(Judge)

class TestLogout(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})

    def test_get(self):
        response = self.client.get('/api/u/logout')
        Judge = response.json()['code'] == -1
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/logout')
        Judge = Judge and response.json()['code'] == 0
        self.assertTrue(Judge)

class TestUserBind(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})
        user2 = MyUser.create_new_user({'account_name': '1', 'account_pass': '123456', 'user_type': 2})

    def test(self):
        response = self.client.get('/api/u/user/bind?open_id=1')
        Judge = response.json()['msg'] == '未找到符合要求的对应微信用户!'
        response = self.client.post('/api/u/user/bind',{'openid':1, 'account': 'admin', 'password': '123456'})
        a = response.json()
        Judge = Judge and response.json()['code'] == 0
        self.assertTrue(Judge)

class TestUserMessage(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})

    def test(self):
        self.client.login(username='admin', password='123456')
        response = self.client.get('/api/u/user/detail')
        Judge = response.json()['code'] == 0
        response = self.client.post('/api/u/user/detail',{'description':'lalala',
                                                          'old_pass':'123456',
                                                          'new_pass':'1234567'
                                                          })
        Judge = Judge and response.json()['code'] == 0
        self.client.logout()
        self.client.login(username='admin', password='1234567')
        response = self.client.get('/api/u/user/detail')
        Judge = Judge and response.json()['code'] == 0
        self.assertTrue(Judge)


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
        meet2 = Meeting(meeting_type='boring',
                       name='DoHomework2',
                       max_people_num=4,
                       phone_num='15546540758',
                       description='work for living',
                       start_time=datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                       end_time=datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                       place='dormitory',
                       status=0,
                       pic_url='http',
                       organizer=user)
        meet2.save()
        meet3 = Meeting(meeting_type='boring',
                       name='DoHomework3',
                       max_people_num=4,
                       phone_num='15546540758',
                       description='work for living',
                       start_time=datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                       end_time=datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                       place='dormitory',
                       status=0,
                       pic_url='http',
                       organizer=user)
        meet3.save()
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 1})
        relation = Relation(user=user2, meeting=meet, status=3)
        relation.save()
        relation2 = Relation(user=user2, meeting=meet2, status=2)
        relation2.save()
        relation3 = Relation(user=user2, meeting=meet3, status=1)
        relation3.save()

    def test_get(self):
        self.client.login(username='admin2', password='123456')
        response = self.client.get('/api/u/relation/get')
        Judge = response.json()['code'] == 0 and len(response.json()['data']['rel3']) == 1 \
                and len(response.json()['data']['rel2']) == 1 and len(response.json()['data']['rel1']) == 1 \
                and response.json()['data']['rel1'][0]['meet_name'] == 'DoHomework3' \
                and response.json()['data']['rel2'][0]['meet_name'] == 'DoHomework2' \
                and response.json()['data']['rel3'][0]['meet_name'] == 'DoHomework'
        self.assertTrue(Judge)

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
        meet2 = Meeting(meeting_type='boring',
                        name='DoHomework2',
                        max_people_num=4,
                        phone_num='15546540758',
                        description='work for living',
                        start_time=datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                        end_time=datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                        place='dormitory',
                        status=0,
                        pic_url='http',
                        organizer=user)
        meet2.save()
        meet3 = Meeting(meeting_type='boring',
                        name='DoHomework3',
                        max_people_num=4,
                        phone_num='15546540758',
                        description='work for living',
                        start_time=datetime.strptime("2016-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                        end_time=datetime.strptime("2016-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                        place='dormitory',
                        status=0,
                        pic_url='http',
                        organizer=user)
        meet3.save()
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 1})
        relation = Relation(user=user2, meeting=meet, status=3)
        relation.save()
        relation2 = Relation(user=user2, meeting=meet2, status=2)
        relation2.save()
        relation3 = Relation(user=user2, meeting=meet3, status=1)
        relation3.save()

    def test_get(self):
        self.client.login(username='admin2', password='123456')
        response = self.client.get('/api/u/relation/change?relation=2&meet_id=1')
        Judge = response.json()['code'] == 0
        response = self.client.get('/api/u/relation/get')
        Judge = Judge and response.json()['code'] == 0 and len(response.json()['data']['rel3']) == 0 \
                and len(response.json()['data']['rel2']) == 2 and len(response.json()['data']['rel1']) == 1
        try:
            response = self.client.get('/api/u/relation/change?relation=2&meet_id=4')
        except:
            Judge = Judge and response.json()['code'] == -1 and self.assertIn('does not exist',response.json()['msg'])
            self.assertTrue(Judge)

    def test_post(self):
        self.client.login(username='admin', password='123456')
        response = self.client.post('/api/u/relation/change',{'relation':2,
                                                    'meet_id':2,
                                                    'user_id':2})
        Judge = response.json()['code'] == 0
        self.client.logout()
        self.client.login(username='admin2', password='123456')
        response = self.client.get('/api/u/relation/get')
        Judge = Judge and response.json()['code'] == 0 and len(response.json()['data']['rel3']) == 0 \
                and len(response.json()['data']['rel2']) == 2 and len(response.json()['data']['rel1']) == 1
        self.client.logout()
        self.client.login(username='admin', password='123456')
        try:
            response = self.client.get('/api/u/relation/change',{'relation':2,
                                                    'meet_id':4,
                                                    'user_id':2})
        except:
            Judge = Judge and response.json()['code'] == -1 and self.assertIn('does not exist', response.json()['msg'])
            self.assertTrue(Judge)

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
        Judge = response.json()['code'] == 0 and len(response.json()['data']) == 1 \
                and response.json()['data'][0]['name'] == 'DoHomework'
        Meeting.objects.all().delete()
        response = self.client.get('/api/u/publish/list')
        Judge = Judge and response.json()['code'] == 0 and len(response.json()['data']) == 0
        self.assertTrue(Judge)

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
        response = self.client.get('/api/u/participant?meet_id=1')
        Judge = response.json()['code'] == 0 and len(response.json()['data']) == 1 \
                and response.json()['data'][0]['user_name'] == '用户admin2'
        try:
            response = self.client.get('/api/u/participant?meet_id=2')
        except:
            Judge = Judge and response.json()['code'] == -1
            self.assertTrue(Judge)

    def test_post(self):
        self.client.login(username='admin', password='123456')
        response = self.client.post('/api/u/participant',{
            'key_word':'admin',
            'meet_id':1
        })
        Judge = response.json()['code'] == 0 and len(response.json()['data']) == 2 \
                and response.json()['data'][0]['name'] == '用户admin' \
                and response.json()['data'][0]['name'] == '用户admin2'
        try:
            response = self.client.post('/api/u/participant',{
                'key_word':'admin',
                'meet_id':2
            })
        except:
            Judge = Judge and response.json()['code'] == -1
            self.assertTrue(Judge)

class TestCreateNotice(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 1})

    def test_post(self):
        self.client.login(username='admin', password='123456')
        response = self.client.post('/api/u/notice/create/', {
            'to_ids':[2],
            'content':'testestest'
        })
        Judge = response.json()['code'] == 0
        notices = Notice.objects.all()
        Judge = Judge and len(notices) == 1 and notices[0].content == 'testestest'
        self.client.logout()
        self.client.login(username='admin2', password='123456')
        try:
            response = self.client.post('/api/u/notice/create/', {
                'to_ids': [2],
                'content': 'testestest'
            })
        except:
            Judge = Judge and response.json()['code'] == -1
            self.assertTrue(Judge)

    def test_get(self):
        self.client.login(username='admin', password='123456')
        response = self.client.post('/api/u/notice/create/', {
            'to_ids': [2],
            'content': 'testestest'
        })
        response = self.client.get('/api/u/notice/create/?notice_id=1')
        Judge = response.json()['code'] == 0
        notices = Notice.objects.all()
        Judge = Judge and len(notices) == 0
        self.assertTrue(Judge)

class TestNoticeMessage(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 2})
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 1})
        Notice.CreateNotice(user2,'testest')

    def test_get(self):
        self.client.login(username='admin2', password='123456')
        response = self.client.get('/api/u/notice/message/')
        Judge = response.json()['code'] == 0 and len(response.json()['data']) == 1 \
            and response.json()['data'][0]['content'] == 'testest'
        Notice.objects.all().delete()
        response = self.client.get('/api/u/notice/message/')
        Judge = Judge and response.json()['code'] == 0 and len(response.json()['data']) == 0
        self.assertTrue(Judge)












