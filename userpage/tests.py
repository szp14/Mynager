from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from mock import Mock, patch
from wechat.models import User
from codex.baseerror import InputError
import json
import userpage.urls

class URLTest(TestCase):
    def test_u_bind(self):
        response = self.client.get('/u/bind/')
        self.assertContains(response, 'inputUsername')

class GetTest(TestCase):
    def test_get_with_openid(self):
        found = resolve('/user/bind/', urlconf=userpage.urls)
        request = Mock(wraps = HttpRequest(), method = 'GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"openid": "2"}')
        request.user = Mock()
        with patch.object(User, 'get_by_openid',
                           return_value= Mock(student_id = 1)) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['code'], 0)

    # def test_get_without_openid(self):
    #     found = resolve('/user/bind/', urlconf=userpage.urls)
    #     with self.assertRaisesMessage(InputError, 'Field "openid" required'):
    #         request = Mock(wraps = HttpRequest(), method = 'GET')
    #         request.body = Mock()
    #         request.body.decode = Mock(return_value='{}')
    #         request.user = Mock()
    #         found.func(request)

