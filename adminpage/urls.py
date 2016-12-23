# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from adminpage.views import *


__author__ = "xyzS"


urlpatterns = [
    url(r'^user/list?$', UserListView.as_view()),
    url(r'^user/detail?$', UserDetailView.as_view())
]
