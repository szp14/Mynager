# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import *

__author__ = "xyzS"

urlpatterns = [
    url(r'^login/?$', LogInView.as_view()),
    url(r'^logout/?$', LogOutView.as_view()),
    url(r'^meeting/detail/?$', MeetingDetailView.as_view()),
    url(r'^meeting/list/?$', MeetingListView.as_view()),
    url(r'^meeting/create/?$', MeetingCreateView.as_view()),
    url(r'^meeting/participate/?$', ParticipantManageView.as_view()),
    url(r'^publish/list/?$', GetPublishView.as_view()),
    url(r'^participant/?$', ParticipantManageView.as_view()),
    url(r'^user/detail/?$', UserMessageView.as_view()),
    url(r'^user/bind/?$', UserBindView.as_view()),
    url(r'^user/verify/?$', UserVerifyView.as_view()),
    url(r'^relation/change/?$', ChangeRelationView.as_view()),
    url(r'^relation/get/?$', GetRelationView.as_view()),
    url(r'^notice/create/?$', CreateNoticeView.as_view()),
    url(r'^notice/message/?$', NoticeMessageView.as_view()),
    url(r'^attachment/create/?$', CreateAttachView.as_view()),
    url(r'^register/?$', RegisterView.as_view()),
]
