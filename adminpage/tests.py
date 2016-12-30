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
        response = self.client.get('/a/user/list')
        self.assertTrue(len(response.json()['data']) == 1)

# Create your tests here.
