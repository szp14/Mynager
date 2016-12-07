from codex.baseerror import *
from codex.baseview import APIView
from wechat.models import MyUser, Meeting, Attachment
import urllib
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
        meetings = Meeting.objects.filter(status__gt=0)
        return [
            {
                "meeting_type": meet0.meeting_type,
                "name": meet0.name,
                "organizer": meet0.organizer.name,
                "pic_url": meet0.pic_url,
                "start_time": meet0.start_time,
                "place": meet0.place,
            } for meet0 in meetings
        ]


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
    @login_required
    def get(self):
        logout(self.request)

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