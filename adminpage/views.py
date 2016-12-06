from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from operator import indexOf
from django.utils import timezone
from Mynager.settings import MEDIA_ROOT, SITE_DOMAIN
from wechat.models import Holder, Meeting, User
# Create your views here.

class RegisterView(APIView):
    def regisHolder(self):
        self.check_input('account_name',
                         'account_password',
                         )
        Holder.create_new_holder(self.input)

    def regisUser(self):
        self.check_input('account_name',
                         'account_password',
                         )
        User.create_new_user(self.input)

class LogInView(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            return {}
        else:
            raise InputError('You have not logged in')

    def post(self):
        self.check_input('username', 'password')
        user = authenticate(username = self.input['username'],
                            password = self.input['password'])
        if user is not None:
            login(self.request, user)
            return
        else:
            raise InputError('Fail to log in')

class LogOutView(APIView):
    def post(self):
        logout(self.request)

