from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
from wechat.models import Meeting
from Mynager.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        UnbindOrUnsubscribeHandler,
        BindAccountHandler,
        GetMeetingHandler,
    ]
    error_message_handler = ErrorHandler
    default_handler = DefaultHandler

    event_keys = {
        'get_meeting': 'SERVICE_GET_MEETING',
        'account_bind': 'SERVICE_BIND',
        'help': 'SERVICE_HELP',
        'meeting_empty': 'MEETING_EMPTY',
        'meeting_header': 'MEETING_HEADER'
    }

    menu = {
        'button': [
            {
                "name": "服务",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "绑定",
                        "key": event_keys['account_bind'],
                    },
                    {
                        "type": "click",
                        "name": "帮助",
                        "key": event_keys['help'],
                    }
                ]
            },
            {
                "name": "我的会议",
                "sub_button": []
            }
        ]
    }

    @classmethod
    def get_meeting_btn(cls):
        return cls.menu['button'][-1]

    @classmethod
    def update_meeting_button(cls, meetings):
        book_btn = cls.get_meeting_btn()
        if len(meetings) == 0:
            book_btn['type'] = 'click'
            book_btn['key'] = cls.event_keys['meeting_empty']
        else:
            book_btn.pop('type', None)
            book_btn.pop('key', None)
        book_btn['sub_button'] = list()
        for met in meetings:
            book_btn['sub_button'].append({
                'type': 'click',
                'name': met['name'],
                'key': cls.event_keys['meeting_header'] + str(met['id']),
            })

    @classmethod
    def getMetIdsInMenu(cls):
        current_menu = cls.lib.get_wechat_menu()
        existed_buttons = list()
        for btn in current_menu:
            if btn['name'] == '我的会议':
                existed_buttons += btn.get('sub_button', list())
        meeting_ids = list()
        for btn in existed_buttons:
            if 'key' in btn:
                meeting_id = btn['key']
                if meeting_id.startswith(cls.event_keys['meeting_header']):
                    meeting_id = meeting_id[len(cls.event_keys['meeting_header']):]
                if meeting_id and meeting_id.isdigit():
                    meeting_ids.append(int(meeting_id))
        return meeting_ids

    @classmethod
    def update_menu(cls, meetings=None):
        """
        :param activities: list of Activity
        :return: None
        """
        if meetings is not None:
            if len(meetings) > 5:
                cls.logger.warn('Custom menu with %d activities, keep only 5', len(meetings))
            cls.update_meeting_button([{'id': met.id, 'name': met.name} for met in meetings[:5]])
        else:
            meeting_ids = cls.getMetIdsInMenu()
            return cls.update_menu(Meeting.objects.filter(
                id__in = meeting_ids, status = Meeting.STATUS_HOLD, end_time__gt=timezone.now()
            ).order_by('end_time')[: 5])
        cls.lib.set_wechat_menu(cls.menu)
