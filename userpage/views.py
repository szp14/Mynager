from codex.baseerror import *
from codex.baseview import APIView
from wechat.models import User, Organizer, Meeting, Attachment, Relation
import urllib
from urllib import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

class HomePageView(APIView):
    @login_required
    def registerMeeting(self):
        self.check_input('id', 'meetingid')
        user = User.objects.get(id=self.input['id'])
        meeting = Meeting.objects.get(id=self.input['meetingid'])
        relation = Relation(user = user, meeting = meeting, status = Relation.STATUS_SIGNUP)
        relation.save()

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
        return [r.meeting for r in Relation.objects.filter(user = user, status = Relation.STATUS_JOINED)]

    @login_required
    def lookupInvited(self):
        self.check_input('id')
        user = User.objects.get(id = self.input['id'])
        return [r.meeting for r in Relation.objects.filter(user = user, status = Relation.STATUS_INVITED)]

    @login_required
    def lookupSignUp(self):
        self.check_input('id')
        user = User.objects.get(id = self.input['id'])
        return [r.meeting for r in Relation.objects.filter(user=user, status=Relation.STATUS_SIGNUP)]

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
        return [r.user for r in Relation.objects.filter(meeting=meeting, status=Relation.STATUS_JOINED)]

    @login_required
    def removeParticipant(self):
        self.check_input('id', 'userid')
        meeting = Meeting.objects.get(id=self.input['id'])
        user = User.objects.get(id=self.input['userid'])
        Relation.objects.get(user = user, meeting = meeting).delete()

    @login_required
    def sendNotice(self):
        pass

    @login_required
    def sendInvitation(self):
        self.check_input('id', 'userid')
        meeting = Meeting.objects.get(id=self.input['id'])
        user = User.objects.get(id=self.input['userid'])
        relation = Relation(user = user, meeting = meeting, status = Relation.STATUS_INVITED)
        relation.save()
        #sendWechatInfo

    @login_required
    def lookupSignUp(self):
        self.check_input('id')
        meeting = Meeting.objects.get(id=self.input['id'])
        return [r.user for r in Relation.objects.filter(meeting=meeting, status=Relation.STATUS_SIGNUP)]

    @login_required
    def acptSignUp(self):
        self.check_input('id', 'userid')
        meeting = Meeting.objects.get(id=self.input['id'])
        user = User.objects.get(id=self.input['userid'])
        relation = Relation(user=user, meeting=meeting, status=Relation.STATUS_JOINED)
        relation.save()
        # sendWechatInfo

    @login_required
    def rjctSignUp(self):
        self.check_input('id', 'userid')
        meeting = Meeting.objects.get(id=self.input['id'])
        user = User.objects.get(id=self.input['userid'])
        Relation.objects.get(user=user, meeting=meeting).delete()
        # sendWechatInfo

class CreateMeetingView(APIView):
    @login_requiredw
    def tempSave(self):
        self.input['status'] = Meeting.STATUS_SAVING
        Meeting.create_new_meeting(self.input)

    @login_required
    def publish(self):
        self.input['status'] = Meeting.STATUS_PENDING
        Meeting.create_new_meeting(self.input)