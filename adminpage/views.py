from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from operator import indexOf
from django.utils import timezone
from Mynager.settings import MEDIA_ROOT, SITE_DOMAIN
# Create your views here.