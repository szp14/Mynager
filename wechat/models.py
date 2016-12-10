from django.db import models
from django.utils import timezone
from codex.baseerror import LogicError
from django.contrib.auth.models import User

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    open_id = models.CharField(max_length=64, db_index=True)
    user_type = models.SmallIntegerField(default=0)
    description = models.CharField(max_length=256)
    phone_num = models.CharField(max_length=32)
    pic_url = models.CharField(max_length=128)
    homepage_url = models.CharField(max_length=128)
    name = models.CharField(max_length=64)
    user_IDnum = models.CharField(max_length=32)
    registered_time = models.DateTimeField(null = True)

    @classmethod
    def create_new_user(cls, dic):
        q = User.objects.create_user(dic["account_name"], '', dic['account_pass'])
        u = MyUser(user = q, user_type=dic["user_type"])
        u.registered_time = timezone.now()
        u.save()
        return u

    def change_information(self, dic):
        own_keys = [
            'user_type',
            'phone_num',
            'description',
            'pic_url',
            'name',
            'user_IDnum',
            'homepage_url',
            'open_id'
        ]
        for key in list(set(dic.keys()) & set(own_keys)):
            self.__dict__[key] = dic[key]
        if 'account_pass' in dic:
            self.user.set_password(dic['account_pass'])
        if 'email' in dic:
            self.user.set_email(dic['email'])
        self.save()

    USER_PARTICIPANTS = 1
    USER_ORGANIZER = 2
    USER_ADMIN = 3

class Meeting(models.Model):
    meeting_type = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    organizer = models.ForeignKey(MyUser)
    max_people_num = models.IntegerField(default = 0)
    phone_num = models.CharField(max_length=32)
    description = models.TextField()
    start_time = models.DateTimeField(null = True)
    end_time = models.DateTimeField(null = True)
    place = models.CharField(max_length=256)
    status = models.IntegerField(default = -1)
    pic_url = models.CharField(max_length=256)
    homepage_url = models.CharField(max_length=256)

    @classmethod
    def create_new_meeting(cls, dic):
        meeting = Meeting()
        own_keys = [
            'meeting_type',
            'name',
            'max_people_num',
            'phone_num',
            'description',
            'start_time',
            'end_time',
            'place',
            'status',
            'pic_url',
            'homepage_url'
        ]
        for key in list(set(dic.keys()) & set(own_keys)):
            meeting.__dict__[key] = dic[key]
        if 'organizer' in dic.keys():
            meeting.organizer = dic['organizer']
        meeting.save()

    def change_information(self, dic):
        own_keys = [
            'meeting_type',
            'name',
            'max_people_num',
            'organizer',
            'phone_num',
            'description',
            'start_time',
            'end_time',
            'place',
            'pic_url',
            'homepage_url'
        ]
        for key in list(set(dic.keys()) & set(own_keys)):
            if key == 'start_time' and timezone.now() > self[key]:
                raise LogicError("在活动开始后修改活动开始时间！")
            if key == 'end_time' and timezone.now() > self[key]:
                raise LogicError("在活动结束后修改活动开始时间！")
            if key == 'name' and self['status'] > self.STATUS_PENDING:
                raise LogicError("活动已经审核通过，无法修改活动名称！")
            self.__dict__[key] = dic[key]
        self.save()

    STATUS_PENDING = -1
    STATUS_READY = 0
    STATUS_HOLD = 1
    STATUS_OVER = 2

class Attachment(models.Model):
    filename = models.CharField(max_length=128)
    meeting = models.ForeignKey(Meeting)

class Relation(models.Model):
    user = models.ForeignKey(MyUser)
    meeting = models.ForeignKey(Meeting)
    status = models.IntegerField(default = 0)

    STATUS_JOINED = 0
    STATUS_SIGNUP = 1
    STATUS_INVITED = 2