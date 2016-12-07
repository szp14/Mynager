# -*- coding: utf-8 -*-
#
import logging

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from wechat.views import CustomWeChatView
from wechat.models import Meeting


__author__ = "xyzS"


class Command(BaseCommand):
    help = 'Query WeChat menu'

    logger = logging.getLogger('getmenu')

    def handle(self, *args, **options):
        current_menu = CustomWeChatView.lib.get_wechat_menu()
        self.logger.info('Got menu: %s', current_menu)

        existed_buttons = list()
        for btn in current_menu:
            if btn['name'] == '我的会议':
                existed_buttons += btn.get('sub_button', list())

        self.logger.info('Got %d activities', len(existed_buttons))
        self.logger.info('=' * 32)
        for idx, met in enumerate(existed_buttons):
            self.logger.info('%d. %s (%s)', idx, met.get('name', ''), met.get('key', ''))


Command.logger.setLevel(logging.DEBUG)
