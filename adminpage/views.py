from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.decorators import login_required
from operator import indexOf
from django.utils import timezone
from Mynager.settings import MEDIA_ROOT, SITE_DOMAIN
from wechat.models import Meeting, MyUser, Attachment
# Create your views here.

class UserListView(APIView):
    @login_required
    def get(self):
        if self.user.myuser.user_type < 3:
            raise InputError("您没有权限访问该内容！")
        users = MyUser.objects.all()
        data = [{
            "name": user.name,
            "id": user.id,
            "description": user.description,
            "true_name": user.name_true,
            "user_type": user.user_type,
            "idcard_num": user.user_IDnum,
            "status": user.user_status,
            "image1": user.user_image,
            "image2": user.idcard_image
            }for user in users
        ]
        return data

class UserDetailView(APIView):
    @login_required
    def get(self):
        if self.user.myuser.user_type < 3:
            raise InputError("您没有权限访问该内容！")
        self.check_input("user_id")
        user = MyUser.objects.all().filter(id=int(self.input["user_id"]))
        if len(user) < 1:
            raise InputError("该用户不存在！")
        user = user[0]
        if user.user_type == 3:
            raise InputError("您无法访问该用户的数据")
        data = {
            "name": user.name,
            "id": user.id,
            "description": user.description,
            "true_name": user.name_true,
            "idcard_num": user.user_IDnum,
            "status": user.user_status,
            "image1": user.user_image,
            "image2": user.idcard_image,
            'user_type': user.user_type,
            'phone_num': user.phone_num,
            'pic_url': user.pic_url,
            'email': user.user.email,
            "account": user.user.username,
            'user_status': user.user_status,
            'open_id': user.open_id,
        }
        return data

    @login_required
    def post(self):
        if self.user.myuser.user_type < 3:
            raise InputError("您没有权限访问该内容！")
        self.check_input("user_id")
        user = MyUser.objects.all().filter(id=int(self.input["user_id"]))
        if len(user) < 1:
            raise InputError("该用户不存在！")
        user = user[0]
        if user.user_type == 3:
            raise InputError("您无法访问该用户的数据")
        user.user.delete()
        user.delete()