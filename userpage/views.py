from codex.baseerror import *
from codex.baseview import APIView
from wechat.models import MyUser, Meeting, Attachment
from wechat.views import CustomWeChatView
from django.contrib.auth.models import User
import urllib
import math
from urllib import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

class HomePageView(APIView):
    @login_required
    def registerMeeting(self):
        self.check_input('id', 'meeting_id')
        user = MyUser.objects.get(id=self.input['id'])
        meeting = Meeting.objects.get(id=self.input['meeting_id'])
        meeting.users_registered.add(user)
        user.meetings_registered.add(meeting)

class MeetingListView(APIView):
    def get(self):
        self.check_input("meeting_num", "page_index")
        meetings = Meeting.objects.filter(status__gt=-1)
        data = {
            "status": False,
            "total_page": 0,
            "list": []
        }
        num0 = int(self.input["meeting_num"])
        num1 = int(self.input["page_index"])
        len0 = len(meetings)
        if len0 >= num0 * (num1 - 1):
            if len0 <= num0 * num1:
                end0 = len0
            else:
                end0 = num0 * num1
            start0 = num0 * (num1 - 1)
            data["status"] = True
            data["total_page"] = math.ceil(len0 / num0)
            data["list"] = [{
                "id": meet0.id,
                "meeting_type": meet0.meeting_type,
                "name": meet0.name,
                "organizer": meet0.organizer.name,
                "pic_url": meet0.pic_url,
                "start_time": meet0.start_time,
                "description": meet0.description,
                "place": meet0.place,
            } for meet0 in meetings[start0:end0]
        ]
        #print (data)
        return data

    def post(self):
        self.check_input("meeting_num", "page_index", "key_word")
        meetings = Meeting.objects.filter(status__gt=-1)
        num0 = int(self.input["meeting_num"])
        num1 = int(self.input["page_index"])
        key = self.input["key_word"]
        data = {
            "status": False,
            "total_page": 0,
            "list": []
        }
        meets = [meet0 for meet0 in meetings if meet0.name.find(key) > -1 or meet0.description.find(key) > -1]
        len0 = len(meets)
        if len0 >= num0 * (num1 - 1):
            if len0 <= num0 * num1:
                end0 = len0
            else:
                end0 = num0 * num1
            start0 = num0 * (num1 - 1)
            data["status"] = True
            data["total_page"] = math.ceil(len0 / num0)
            data["list"] = [{
                "id": meet0.id,
                "meeting_type": meet0.meeting_type,
                "name": meet0.name,
                "description": meet0.description,
                "organizer": meet0.organizer.name,
                "pic_url": meet0.pic_url,
                "start_time": meet0.start_time,
                "place": meet0.place,
                } for meet0 in meets[start0:end0]
            ]
        #print(data)
        return data



class MeetingDetailView(APIView):
    @login_required
    def get(self):
        self.check_input("meeting_id")
        meeting0 = Meeting.objects.get(id = self.input["meeting_id"])
        if meeting0.status < 0:
            raise LogicError("该会议还未处于发布状态，您无法查看该会议的信息！")
        return {
            "meeting_type": meeting0.meeting_type,
            "name": meeting0.name,
            "organizer": meeting0.organizer.name,
            "max_people_num": meeting0.max_people_num,
            "phone_num": meeting0.phone_num,
            "description": meeting0.description,
            "start_time": meeting0.start_time,
            "end_time": meeting0.end_time,
            "place": meeting0.place,
            "status": meeting0.status,
            "pic_url": meeting0.pic_url,
            "homepage_url": meeting0.homepage_url,
        }

    @login_required
    def post(self):
        if request.user.account_name:
            self.check_input("meeting_id")
            meeting0 = Meeting.objects.get(id = self.input["meeting_id"])
            meeting0.change_information(self.input)

class MeetingCreateView(APIView):
    @login_required
    def post(self):
        if request.user.myuser.user_type > 0:
            raise InputError("您没有权限创建会议！")
        self.input["organizer"] = self.user.myuser
        Meeting.create_new_meeting(self.input)

    @login_required
    def get(self):
        self.check_input("meeting_id")
        if request.user.myuser.user_type < 2:
            raise InputError("您没有权限删除该会议！")
        meeting0 = Meeting.objects.get(id = self.input["meeting_id"])
        meeting0.delete()

class RegisterView(APIView):
    def post(self):
        self.check_input('user_type', 'account_name', 'account_pass')
        MyUser.create_new_user(self.input)


class LogInView(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            return self.request.user.myuser.user_type
        else:
            return 0

    def post(self):
        self.check_input('username', 'password')
        user = authenticate(username = self.input['username'], password = self.input['password'])
        if user is not None:
            login(self.request, user)
            return 1
        else:
            return 2

class LogOutView(APIView):
    @login_required
    def get(self):
        logout(self.request)

class UserBindView(APIView):
    def get(self):
        self.check_input("open_id")
        user = MyUser.objects.filter(open_id=self.input["open_id"])
        if len(user) < 1:
            raise LogicError("未找到符合要求的对应微信用户!")
        if user[0].user_type == 0:
            return False
        else:
            return True

    def post(self):
        self.check_input("openid", "account", "password")
        user = authenticate(username=self.input['account'], password=self.input['password'])
        if user is not None:
            if user.myuser.open_id:
                raise LogicError('该Mynager账号已绑定了微信号，请解绑后重试！')
            old_user = User.objects.get(username=self.input["openid"])
            old_user.delete()
            user.myuser.open_id = self.input["openid"]
            user.myuser.save()
            login(self.request, user)
        else:
            raise ValidateError("账号或者密码不正确，请重新输入！")

class UserCenterView(APIView):
    @login_required
    def modInfo(self):
        self.check_input('id')
        MyUser.objects.get(id = self.input['id']).change_information(self.input)

    @login_required
    def lookupJoined(self):
        self.check_input('id')
        user = MyUser.objects.get(id = self.input['id'])
        return list(user.meetings_joined)

    @login_required
    def lookupInvited(self):
        self.check_input('id')
        user = MyUser.objects.get(id = self.input['id'])
        return list(user.meetings_invited)

    @login_required
    def lookupRegistered(self):
        self.check_input('id')
        user = MyUser.objects.get(id = self.input['id'])
        return list(user.meetings_registered)


class OrganizerCenterView(APIView):
    @login_required
    def modInfo(self):
        self.check_input('id')
        MyUser.objects.get(id = self.input['id']).change_information(self.input)

class ParticipantManageView(APIView):
    @login_required
    def lookupParticipant(self):
        self.check_input('id')
        meeting = Meeting.objects.get(id = self.input['id'])
        return list(meeting.users_joined)

    @login_required
    def removeParticipant(self):
        self.check_input('id', 'userid')
        meeting = Meeting.objects.get(id=self.input['id'])
        user = MyUser.objects.get(id=self.input['userid'])
        meeting.users_joined.remove(user)
        if meeting in user.meetings_invited:
            user.meetings_invited.remove(meeting)
        elif meeting in user.meetings_joined:
            user.meetings_joined.remove(meeting)
        elif meeting in user.meetings_registered:
            user.meetings_registered.remove(meeting)
        user.save()
        meeting.save()

    @login_required
    def sendNotice(self):
        pass

    @login_required
    def sendInvitation(self):
        self.check_input('id', 'userid')
        meeting = Meeting.objects.get(id=self.input['id'])
        user = MyUser.objects.get(id=self.input['userid'])
        meeting.users_joined.add(user)
        user.meetings_invited.add(meeting)
        meeting.save()
        user.save()
        #sendWechatInfo

    @login_required
    def lookupRegister(self):
        self.check_input('id')
        meeting = Meeting.objects.get(id=self.input['id'])
        return list(meeting.users_registered)

    @login_required
    def acptRegister(self):
        self.check_input('id', 'userid')
        meeting = Meeting.objects.get(id=self.input['id'])
        user = MyUser.objects.get(id=self.input['userid'])
        meeting.users_joined.add(user)
        user.meetings_joined.add(meeting)
        meeting.save()
        user.save()
        # sendWechatInfo

    @login_required
    def rjctRegister(self):
        self.check_input('id', 'userid')
        meeting = Meeting.objects.get(id=self.input['id'])
        user = MyUser.objects.get(id=self.input['userid'])
        meeting.users_registered.remove(user)
        user.meetings_registered.remove(meeting)
        meeting.save()
        user.save()
        # sendWechatInfo

class CreateMeetingView(APIView):
    @login_required
    def tempSave(self):
        self.input['status'] = Meeting.STATUS_SAVING
        Meeting.create_new_meeting(self.input)

    @login_required
    def publish(self):
        self.input['status'] = Meeting.STATUS_PENDING
        Meeting.create_new_meeting(self.input)