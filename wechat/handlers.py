# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from Mynager.settings import SITE_DOMAIN
from django.utils import timezone
import datetime
from django.db import transaction
from wechat.models import User, Notice, MyUser
__author__ = "xyzS"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')

class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')

class AboutHandler(WeChatHandler):

    def check(self):
        return self.is_text("关于") or self.is_event_click(self.view.event_keys['about'])

    def handle(self):
        return self.reply_text(self.get_message('about_info'))

class HelpHandler(WeChatHandler):

    def check(self):
        return self.is_text("帮助") or self.is_event_click(self.view.event_keys['help'])

    def handle(self):
        return self.reply_text(self.get_message('help_description'))

class UnbindOrUnsubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('解绑') or (self.is_event_click(self.view.event_keys['account_bind']) and self.user.user_type)

    def handle(self):
        if self.user.user.username == self.user.open_id:
            return self.reply_text("您还没有绑定Mynager账号，请先绑定账号！")
        self.user.open_id = ""
        self.user.save()
        return self.reply_text(self.get_message('unbind_account'))

class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or (self.is_event_click(self.view.event_keys['account_bind']) and self.user.user_type == 0)

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))

class GetMeetingHandler(WeChatHandler):

    def check(self):
        return self.is_text('我的通知') or self.is_event_click(self.view.event_keys['notice'])

    def handle(self):
        if self.user.user.username == self.user.open_id:
            return self.reply_text("您还没有绑定Mynager账号，请先绑定账号！")
        notices = Notice.objects.all().filter(touser=self.user)
        if len(notices) == 0:
            return self.reply_text("暂时没有通知！")
        notes = [{
            'content': notice.content,
            'time': datetime.datetime.strftime(notice.time, '%Y-%m-%d %H:%M:%S'),
            'count': i + 1
        } for i, notice in enumerate(notices)]
        return self.reply_text(self.get_message('notice', notes))

