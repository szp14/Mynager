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

class TestUserList(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 3})

    def test_get(self):
        self.client.login(username='admin', password='123456')
        response = self.client.post('/api/u/user/detail', {'name_true': 'lalala'})
        response = self.client.get('/api/u/user/detail')
        response = self.client.get('/a/user/list')
        Judge = len(response.json()['data']) == 1 \
                and response.json()['data'][0]['true_name'] == 'lalala'
        self.assertTrue(Judge)

class TestUserDetail(TestCase):
    def setUp(self):
        user = MyUser.create_new_user({'account_name': 'admin', 'account_pass': '123456', 'user_type': 3})
        user2 = MyUser.create_new_user({'account_name': 'admin2', 'account_pass': '123456', 'user_type': 2})
        user3 = MyUser.create_new_user({'account_name': 'admin3', 'account_pass': '123456', 'user_type': 1})

    def test_get(self):
        self.client.login(username='admin', password='123456')
        response = self.client.get('/a/user/detail?user_id=2')
        Judge = response.json()['code'] == 0 \
            and response.json()['data']['name'] == '用户admin2'
        response = self.client.get('/a/user/detail?user_id=3')
        Judge = Judge and response.json()['code'] == 0 \
                and response.json()['data']['name'] == '用户admin3'
        self.assertTrue(Judge)

    def test_post(self):
        self.client.login(username='admin', password='123456')
        response = self.client.post('/a/user/detail',{'user_id':5})
        Judge = response.json()['code'] == 0 \
                and MyUser.objects.all()[1].name == '用户admin3'
        self.assertTrue(Judge)


# Create your tests here.
