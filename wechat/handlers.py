# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from Mynager.settings import SITE_DOMAIN
from django.utils import timezone
from django.db import transaction
from wechat.models import User
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

class UnbindOrUnsubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('解绑') or self.is_event('unsubscribe')

    def handle(self):
        user = self.user
        self.user = User(open_id = user.open_id)
        user.open_id = ""
        user.save()
        return self.reply_text(self.get_message('unbind_account'))


class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))

class GetMeetingHandler(WeChatHandler):

    def check(self):
        return self.is_text('我的会议') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))