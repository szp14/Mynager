from django.db import models
from django.utils import timezone
from codex.baseerror import LogicError
import datetime
from django.contrib.auth.models import User
from Mynager.settings import MEDIA_ROOT, SITE_DOMAIN

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    open_id = models.CharField(max_length=64, db_index=True)
    user_type = models.SmallIntegerField(default=0)
    user_status = models.SmallIntegerField(default=0)
    description = models.CharField(max_length=256)
    phone_num = models.CharField(max_length=32)
    pic_url = models.CharField(max_length=128)
    user_image = models.CharField(max_length=128)
    idcard_image = models.CharField(max_length=128)
    name = models.CharField(max_length=64)
    name_true = models.CharField(max_length=64)
    user_IDnum = models.CharField(max_length=32)
    registered_time = models.DateTimeField(null = True)

    @classmethod
    def create_new_user(cls, dic):
        q = User.objects.create_user(dic["account_name"], '', dic['account_pass'])
        u = MyUser(user = q, user_type=dic["user_type"])
        u.name = "用户" + dic["account_name"]
        u.description = "这个人很懒，还没有编辑具体简介！"
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
            'name_true',
            'user_status',
            'user_IDnum',
            'open_id',
            'user_image',
            'idcard_image'
        ]
        for key in list(set(dic.keys()) & set(own_keys)):
            self.__dict__[key] = dic[key]
        if 'email' in dic:
            self.user.email=dic['email']
        self.user.save()
        self.save()

    STATUS_UNKNOWN = 0
    STATUS_PENGDING = 1
    STATUS_KNOWN = 2

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
        ]
        for key in list(set(dic.keys()) & set(own_keys)):
            meeting.__dict__[key] = dic[key]
        if 'organizer' in dic.keys():
            meeting.organizer = dic['organizer']
        meeting.save()
        return meeting

    def change_information(self, dic):
        own_keys = [
            'status',
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
            self.__dict__[key] = dic[key]
        self.save()

    def get_relationship(self, user0):
        relat = Relation.objects.all().filter(meeting=self, user=user0)
        if len(relat) == 0:
            return 0
        else:
            return relat[0].status

    STATUS_PENDING = 0
    STATUS_PASSED = 1
    STATUS_REFUSED = -2
    STATUS_PAUSE = -1

class Attachment(models.Model):
    filename = models.CharField(max_length=128)
    file_url = models.CharField(max_length=128)
    size = models.CharField(max_length=32)
    meeting = models.ForeignKey(Meeting)

    @classmethod
    def CreateAttachment(cls, file, meet):
        time_name1 = str(timezone.now().timestamp())[:10] + file.name
        file_path = MEDIA_ROOT + '/' + time_name1
        open(file_path, "wb").write(file.read())
        file_url = SITE_DOMAIN + '/upload/' + time_name1
        file_size = file.size / 1024
        if file_size < 1024:
            size = str(file_size)[:5] + "KB"
        else:
            file_size = file_size / 1024
            if file_size < 1024:
                size = str(file_size)[:5] + "MB"
            else:
                file_size = file_size / 1024
                size = str(file_size)[:5] + "GB"
        attach = Attachment(filename=file.name, file_url=file_url, meeting=meet, size=size)
        attach.save()

class Relation(models.Model):
    user = models.ForeignKey(MyUser)
    meeting = models.ForeignKey(Meeting)
    status = models.IntegerField(default = 0)

    @classmethod
    def ChangeRelation(cls, user, meet, status):
        relats = Relation.objects.all().filter(user=user, meeting=meet)
        if len(relats) < 1 and status > 0:
            rel = Relation(user=user, meeting=meet, status=status)
            rel.save()
            return
        elif len(relats) > 0:
            rel = relats[0]
            if status == 0:
                rel.delete()
            elif status > 0:
                rel.status = status
                rel.save()

    @classmethod
    def GetRelation(cls, user_id, meet_id):
        user = MyUser.objects.get(id=int(user_id))
        meet = Meeting.objects.get(id=int(meet_id))
        relats = Relation.objects.all().filter(user=user, meeting=meet)
        if len(relats) == 0:
            return 0
        else:
            return relats[0].status

    STATUS_JOINED = 3
    STATUS_SIGNUP = 1
    STATUS_INVITED = 2

class Notice(models.Model):
    time=models.DateTimeField(null=True)
    touser=models.ForeignKey(MyUser)
    fromname=models.CharField(max_length=64, null=True)
    content=models.CharField(max_length=256)

    @classmethod
    def CreateNotice(cls, user, con):
        note = Notice(touser=user, content=con, time=timezone.now() + timezone.timedelta(hours=8))
        note.save()

    @classmethod
    def DelNotice(cls, noteid):
        note1 = Notice.objects.all().filter(id=noteid)
        if(len(note1) > 0):
            note1[0].delete()
