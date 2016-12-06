from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from operator import indexOf
from django.utils import timezone
from Mynager.settings import MEDIA_ROOT, SITE_DOMAIN
from wechat.models import Organizer, Meeting, User, Attachment
# Create your views here.

class RegisterView(APIView):
    def regisOrganizer(self):
        self.check_input('account_name',
                         'account_password',
                         )
        Organizer.create_new_holder(self.input)

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

class UserCenterView(APIView):
    @login_required
    def modInfo(self):
        self.check_input('id')
        User.objects.get(id = self.input['id']).change_information(self.input)

    @login_required
    def lookupJoined(self):
        self.check_input('id')
        user = User.objects.get(id = self.input['id'])
        return list(user.meetings_joined)

    @login_required
    def lookupInvited(self):
        self.check_input('id')
        user = User.objects.get(id = self.input['id'])
        return list(user.meetings_invited)

    @login_required
    def lookupRegistered(self):
        self.check_input('id')
        user = User.objects.get(id = self.input['id'])
        return list(user.meetings_registered)

class OrganizerCenterView(APIView):
    @login_required
    def modInfo(self):
        self.check_input('id')
        Organizer.objects.get(id = self.input['id']).change_information(self.input)

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
        user = User.objects.get(id=self.input['userid'])
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
        user = User.objects.get(id=self.input['userid'])
        meeting.users_joined.add(user)
        user.meetings_invited.add(meeting)
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
        user = User.objects.get(id=self.input['userid'])
        meeting.users_joined.add(user)
        user.meetings_joined.add(meeting)
        # sendWechatInfo

    @login_required
    def rjctRegister(self):
        self.check_input('id', 'userid')
        meeting = Meeting.objects.get(id=self.input['id'])
        user = User.objects.get(id=self.input['userid'])
        meeting.users_registered.remove(user)
        user.meetings_registered.remove(meeting)
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

class HomePageView(APIView):
    @login_required
    def registerMeeting(self):
        self.check_input('id', 'meetingid')
        user = User.objects.get(id=self.input['id'])
        meeting = Meeting.objects.get(id=self.input['meetingid'])
        meeting.users_registered.add(user)
        user.meetings_registered.add(meeting)