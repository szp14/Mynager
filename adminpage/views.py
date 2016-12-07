from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth.decorators import login_required
from operator import indexOf
from django.utils import timezone
from Mynager.settings import MEDIA_ROOT, SITE_DOMAIN
from wechat.models import Meeting, MyUser, Attachment
# Create your views here.

class AdminPageView(APIView):
    @login_required
    def lookupMeetingApply(self):
        return list(Meeting.objects.filter(status = Meeting.STATUS_PENDING))

    @login_required
    def acptApply(self):
        self.check_input('meetingid')
        meeting = Meeting.objects.get(id=self.input['meetingid'])
        meeting.status = meeting.STATUS_READY
        meeting.save()
        # sendWechatInfo

    @login_required
    def rjctApply(self):
        self.check_input('meetingid')
        meeting = Meeting.objects.get(id=self.input['meetingid'])
        meeting.status = meeting.STATUS_SAVING
        meeting.save()
        # sendWechatInfo