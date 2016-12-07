# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from adminpage.views import *


__author__ = "xyzS"


urlpatterns = [
    url(r'^admin/?$', AdminPageView.as_view()),
]
