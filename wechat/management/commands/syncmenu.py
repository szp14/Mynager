# -*- coding: utf-8 -*-
#
import logging

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from wechat.views import CustomWeChatView
from wechat.models import Meeting


__author__ = "xyzS"


class Command(BaseCommand):
    help = 'Automatically synchronize WeChat menu'

    logger = logging.getLogger('syncmenu')

    def handle(self, *args, **options):
        CustomWeChatView.update_menu(Meeting.objects.filter(
            status=Meeting.STATUS_HOLD , end_time__gt=timezone.now()
        ).order_by('end_time'))
        met_btns = CustomWeChatView.get_meeting_btn().get('sub_button', list())
        self.logger.info('Updated %d meetings', len(met_btns))
        self.logger.info('=' * 32)
        for idx, act in enumerate(met_btns):
            self.logger.info('%d. %s (%s)', idx, act.get('name', ''), act.get('key', ''))


Command.logger.setLevel(logging.DEBUG)
