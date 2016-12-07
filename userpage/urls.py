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
    url(r'^homepage/?$', HomePageView.as_view()),
    url(r'^participant/?$', ParticipantManageView.as_view()),
    url(r'^user/center/?$', UserCenterView.as_view()),
    url(r'^publisher/?$', OrganizerCenterView.as_view()),
    url(r'^register/?$', RegisterView.as_view()),
]
