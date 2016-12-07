from django.db import models
from time import timezone
from codex.baseerror import LogicError


class Organizer(models.Model):
    organizer_type = models.IntegerField()
    account_name = models.CharField(unique=True, max_length=128)
    account_password = models.CharField(max_length=128)
    description = models.TextField()
    email_address = models.CharField(max_length=128)
    phone_num = models.IntegerField()
    pic_url = models.CharField(max_length=128)
    homepage_url = models.CharField(max_length=128)
    name = models.CharField(max_length=128, db_index=True)
    registered_time = models.DateTimeField()

    @classmethod
    def create_new_organizer(self, dic):
        organizer = Organizer(account_name= dic['account_name'],
                        account_password = dic['account_password'],
                        )
        organizer.registered_time = timezone.now()
        organizer.save()


    def change_information(self, dic):
        own_keys = [
            'account_password',
            'description',
            'email_address',
            'phone_num',
            'pic_url',
            'homepage_url'
        ]
        for key in list(set(dic.keys()) & set(own_keys)):
            self[key] = dic[key]
        self.save()

    HOLDER_COMPANY = 1
    HOLDER_PERSON = 2
    HOLDER_GROUP = 3
    HOLDER_GOVERNMENT = 4
    HOLDER_OTHERS = 0

class Meeting(models.Model):
    meeting_type = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    organizer = models.ForeignKey(Organizer)
    max_people_num = models.IntegerField()
    phone_num = models.IntegerField()
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=256)
    status = models.IntegerField()
    pic_url = models.CharField(max_length=256)
    homepage_url = models.CharField(max_length=256)
    #users_joined = models.ManyToManyField(User)
    #users_registered = models.ManyToManyField(User)

    @classmethod
    def create_new_meeting(self, dic):
        meeting = Meeting()
        own_keys = [
            'meeting_type',
            'name',
            'organizer',
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
            meeting[key] = dic[key]
        meeting.save()

    def change_information(self, dic):
        own_keys = [
            'meeting_type',
            'name',
            'max_people_num',
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
            self[key] = dic[key]
        self.save()

    STATUS_SAVING = -2
    STATUS_PENDING = -1
    STATUS_READY = 0
    STATUS_HOLD = 1
    STATUS_OVER = 2

class Attachment(models.Model):
    filename = models.CharField(max_length=128)
    meeting = models.ForeignKey(Meeting)

class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    user_type = models.IntegerField(default = 2)
    account_name = models.CharField(unique=True, max_length=128)
    account_password = models.CharField(max_length=128, default = '')
    description = models.CharField(max_length=256, default = '')
    email_address = models.CharField(max_length=128, default = '')
    phone_num = models.IntegerField(default = 0)
    pic_url = models.CharField(max_length=128, default = '')
    user_name = models.CharField(max_length=64, default = '')
    user_IDnum = models.IntegerField(unique=True)
    registered_time = models.DateTimeField(null = True)

    @classmethod
    def create_new_user(self, dic):
        user = User(account_name = dic['account_name'],
                    account_password = dic['account_password'],
                    )
        user.registered_time = timezone.now()
        user.save()

    def change_information(self, dic):
        own_keys = [
            'user_type',
            'account_password',
            'email_address',
            'phone_num',
            'description',
            'pic_url'
        ]
        for key in list(set(dic.keys()) & set(own_keys)):
            self[key] = dic[key]
        self.save()

    USER_ADMIN = 1
    USER_PARTICIPANTS = 2
    USER_OTHERS = 0

class Relation(models.Model):
    user = models.ForeignKey(User)
    meeting = models.ForeignKey(Meeting)
    status = models.IntegerField()

    STATUS_JOINED = 0
    STATUS_SIGNUP = 1
    STATUS_INVITED = 2