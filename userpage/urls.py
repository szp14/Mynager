# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^login/?$', LogInView.as_view()),
    url(r'^logout/?$', LogOutView.as_view()),
    url(r'^meeting/?$', CreateMeetingView.as_view()),
    url(r'^homepage/?$', HomePageView.as_view()),
    url(r'^participant/?$', ParticipantManageView.as_view()),
    url(r'^personalcenter/?$', UserCenterView.as_view()),
    url(r'^publisher/?$', OrganizerCenterView.as_view()),
    url(r'^register/?$', RegisterView.as_view()),
]
