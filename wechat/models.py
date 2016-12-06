from django.db import models
from time import timezone
from codex.baseerror import LogicError

class Holder(models.Model):
    holder_type = models.IntegerField()
    account_name = models.IntegerField(unique=True)
    account_password = models.CharField(max_length=128)
    description = models.TextField()
    email_address = models.CharField(max_length=128)
    phone_num = models.IntegerField()
    pic_url = models.CharField()
    homepage_url = models.CharField()
    name = models.CharField(max_length=128, unique=True)
    registered_time = models.DateTimeField()

    @classmethod
    def create_new_holder(self, dic):
        holder = Holder(account_name= dic['account_name'],
                        account_password = dic['account_password'],
                        )
        holder.registered_time = timezone.now()
        holder.save()


    def change_information(self, dic):
        own_dic = {
            'account_password' : self.account_password,
            'description': self.description,
            'email_address' : self.email_address,
            'phone_num' : self.phone_num,
            'pic_url' : self.pic_url,
            'homepage_url' : self.homepage_url
        }
        for key in dic:
            if key in own_dic:
                own_dic[key] = dic[key]
        self.save()

    HOLDER_COMPANY = 1
    HOLDER_PERSON = 2
    HOLDER_GROUP = 3
    HOLDER_GOVERNMENT = 4
    HOLDER_OTHERS = 0

class Meeting(models.Model):
    meeting_type = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    holder = models.ForeignKey(Holder)
    max_people_num = models.IntegerField()
    phone_num = models.IntegerField()
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=256)
    status = models.IntegerField()
    pic_url = models.CharField(max_length=256)
    homepage_url = models.CharField(max_length=256)

    @classmethod
    def create_new_meeting(self, dic):
        meeting = Meeting(meeting_type = dic['meeting_type'],
                          name = dic['name'],
                          holder = dic['holder'],
                          description = dic['description']
                          )
        meeting.save()

    def change_information(self, dic):
        own_dic = {
            'meeting_type': self.meeting_type,
            'name': self.name,
            'people_num': self.people_num,
            'phone_num': self.phone_num,
            'description': self.description,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'place': self.place,
            'pic_url': self.pic_url,
            'homepage_url': self.homepage_url
        }
        for key in dic:
            if key in own_dic:
                if key == 'start_time' and timezone.now() > own_dic[key]:
                    raise LogicError("在活动开始后修改活动开始时间！")
                if key == 'end_time' and timezone.now() > own_dic[key]:
                    raise LogicError("在活动结束后修改活动开始时间！")
                if key == 'name' and own_dic[key] != -1:
                    raise LogicError("活动已经审核通过，无法修改活动名称！")
                own_dic[key] = dic[key]
        self.save()

    STATUS_PENDING = -1
    STATUS_READY = 0
    STATUS_HOLD = 1
    STATUS_OVER = 2

class User(models.Model):
    user_type = models.IntegerField()
    account_name = models.IntegerField(unique=True)
    account_password = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    email_address = models.CharField(max_length=128, unique=True)
    phone_num = models.IntegerField(unique=True)
    pic_url = models.CharField(max_length=125)
    user_name = models.CharField()
    user_IDnum = models.IntegerField(unique=True)
    meetings = models.ManyToManyField(Meeting)
    registered_time = models.DateTimeField()

    @classmethod
    def create_new_user(self, dic):
        user = User(account_name = dic['account_name'],
                    account_password = dic['account_password'],
                    )
        user.registered_time = timezone.now()
        user.save()

    def change_information(self, dic):
        own_dic = {
            'user_type' : self.user_type,
            'account_password' : self.account_password,
            'email_address' : self.email_address,
            'phone_num' : self.phone_num,
            'description' : self.description,
            'pic_url' : self.pic_url,
        }
        for key in dic:
            if key in own_dic:
                own_dic[key] = dic[key]
        self.save()

    USER_ADMIN = 1
    USER_PARTICIPANTS = 2
    USER_OTHERS = 0

