from celery import task
from djcelery import models as celery_models
from wechat.models import User
from django.db import transaction
from django.utils import timezone
import datetime
import json
from wechat.wrapper import WeChatLib
from Mynager.settings import SITE_DOMAIN
from Mynager.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


def create_task(name, task, task_args, crontab_time):
    task, created = celery_models.PeriodicTask.objects.get_or_create(
        name=name,
        task=task)
    crontab = celery_models.CrontabSchedule.objects.filter(
        **crontab_time).first()
    if crontab is None:
        crontab = celery_models.CrontabSchedule.objects.create(
            **crontab_time)
    task.crontab = crontab
    task.enabled = True
    task.kwargs = json.dumps(task_args)
    # expiration = timezone.now() + datetime.timedelta(days = 1)
    # task.expires = expiration
    task.save()
    return True

def disable_task(name):
    try:
        task = celery_models.PeriodicTask.objects.get(name=name)
        task.enabled = False
        task.save()
        return True
    except celery_models.PeriodicTask.DoesNotExist:
        return True

def deleteTask(act):
    return celery_models.PeriodicTask.objects.filter(name__contains = 'NOTICE').delete()


@task()
def createNotice(actId, actName, actHour, actMinute):
    for user in User.objects.all():
        jsonPacket = {
            'touser': user.open_id,
            'template_id': 'gG9VdGmd1pj83VMGkBHnPZscG7OcyBJzXDOg3Engl-s',
            'topcolor': '#FF0000',
            'url': SITE_DOMAIN + '/u/activity/?id=' + str(actId),
            'data': {
                'actName': {
                    'value': actName,
                    'color': '#FF0000',
                },
                'actHour': {
                    'value': actHour,
                    'color': '#FF0000',
                },
                'actMinute': {
                    'value': actMinute,
                    'color': '#FF0000',
                },
            },
        }
        lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)
        token = lib.get_wechat_access_token()
        rsp = lib._http_post_dict(
            'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + token,
            jsonPacket
        )


# create_task('HELP', 'wechat.tasks.add', {'x': 1, 'y': 2},
#             {
#                 'month_of_year': timezone.now().month,
#                 'day_of_month': timezone.now().day,
#                 'hour': timezone.now().hour,
#                 'minute': timezone.now().minute + 1,
#             })

# create_task('NOTICE' + str(act.id), 'wechat.tasks.createNotice',
#             {
#                 'actId': act.id,
#                 'actName': act.name,
#                 'actHour': act.book_start.hour,
#                 'actMinute': act.book_start.minute,
#             },
#             {
#                 'month_of_year': 11,
#                 'day_of_month': 2,
#                 'hour': 18 - 8,
#                 'minute': timezone.now().minute + 1,
#             }