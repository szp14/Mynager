from codex.baseerror import *
from codex.baseview import APIView
from django.utils import timezone
from wechat.models import MyUser, Meeting, Attachment, Relation, Notice
from wechat.views import CustomWeChatView
from django.contrib.auth.models import User
import urllib
import datetime
import math
from urllib import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from Mynager.settings import MEDIA_ROOT, SITE_DOMAIN
from wechat.wrapper import WeChatLib
from Mynager.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET

def createNotice(user_openid, con):
    jsonPacket = {
        'touser': user_openid,
        'template_id': 'kbtmtmz1uqzQO-2DhGbasz9OjSjGYujg-R2U_rGbITg',
        'topcolor': '#FF0000',
        #'url': SITE_DOMAIN + '/meeting/detail?id=' + str(metId),
        'data': {
            'con': {
                'value': con,
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

class MeetingListView(APIView):
    def get(self):
        self.check_input("meeting_num", "page_index", "status")
        stat = int(self.input["status"])
        if stat == -1:
            meetings = Meeting.objects.filter(status__gt=0)
        elif stat == 0:
            if self.user.myuser.user_type < 3:
                raise InputError("您没有权限访问这些会议！")
            meetings = Meeting.objects.filter(status=0)
        else:
            if self.user.myuser.user_type < 3:
                raise InputError("您没有权限访问这些会议！")
            meetings = Meeting.objects.filter(status__in=[-2, -1, 1])
        data = {
            "status": False,
            "total_page": 1,
            "list": []
        }
        num0 = int(self.input["meeting_num"])
        num1 = int(self.input["page_index"])
        len0 = len(meetings)
        if len0 >= num0 * (num1 - 1):
            if len0 <= num0 * num1:
                end0 = len0
            else:
                end0 = num0 * num1
            start0 = num0 * (num1 - 1)
            data["status"] = True
            if len0 != 0:
                data["total_page"] = math.ceil(len0 / num0)
            else:
                data["total_page"] = 1
            if self.request.user.is_authenticated():
                data["list"] = [{
                    "id": meet0.id,
                    "meeting_type": meet0.meeting_type,
                    "relation": meet0.get_relationship(self.user.myuser),
                    "name": meet0.name,
                    "status": 3 if meet0.end_time < timezone.now() else meet0.status,
                    "organizer": meet0.organizer.name,
                    "organ_id": meet0.organizer.id,
                    "pic_url": meet0.pic_url,
                    "description": meet0.description,
                    "place": meet0.place,
                   } for meet0 in meetings[start0:end0]
                ]
            else:
                data["list"] = [{
                    "id": meet0.id,
                    "meeting_type": meet0.meeting_type,
                    "relation": -1,
                    "name": meet0.name,
                    "status": 3 if meet0.end_time < timezone.now() else meet0.status,
                    "organizer": meet0.organizer.name,
                    "organ_id": meet0.organizer.id,
                    "pic_url": meet0.pic_url,
                    "description": meet0.description,
                    "place": meet0.place,
                    } for meet0 in meetings[start0:end0]
                ]
        #print (data)
        return data

    def post(self):
        self.check_input("meeting_num", "page_index", "key_word")
        meetings = Meeting.objects.filter(status__gt=Meeting.STATUS_PENDING)
        num0 = int(self.input["meeting_num"])
        num1 = int(self.input["page_index"])
        key = self.input["key_word"]
        data = {
            "status": False,
            "total_page": 0,
            "list": []
        }
        meets = [meet0 for meet0 in meetings if meet0.name.find(key) > -1 or meet0.description.find(key) > -1]
        len0 = len(meets)
        if len0 >= num0 * (num1 - 1):
            if len0 <= num0 * num1:
                end0 = len0
            else:
                end0 = num0 * num1
            start0 = num0 * (num1 - 1)
            data["status"] = True
            data["total_page"] = math.ceil(len0 / num0)
            data["list"] = [{
                "id": meet0.id,
                "relation": meet0.get_relationship(self.user.myuser),
                "meeting_type": meet0.meeting_type,
                "name": meet0.name,
                "description": meet0.description,
                "organizer": meet0.organizer.name,
                "pic_url": meet0.pic_url,
                "place": meet0.place,
                } for meet0 in meets[start0:end0]
            ]
        #print(data)
        return data

class MeetingDetailView(APIView):
    def get(self):
        self.check_input("meeting_id")
        meeting1 = Meeting.objects.all().filter(id=int(self.input["meeting_id"]))
        if len(meeting1) < 1:
            raise LogicError("未找到id为" + self.input["meeting_id"] + "的会议！")
        meeting0 = meeting1[0]
        if self.request.user.is_authenticated():
            user_type = self.user.myuser.user_type
        else:
            user_type = 0
        if meeting0.status <= 0 and user_type < 2:
            raise LogicError("该会议不处于发布状态，您无法查看该会议的信息！")
        attachs = Attachment.objects.all().filter(meeting=meeting0)
        return {
            "meeting_type": meeting0.meeting_type,
            "name": meeting0.name,
            "organizer": meeting0.organizer.name,
            "max_people_num": meeting0.max_people_num,
            "phone_num": meeting0.phone_num,
            "description": meeting0.description,
            "start_time": datetime.datetime.strftime(meeting0.start_time, '%Y-%m-%d'),
            "end_time": datetime.datetime.strftime(meeting0.end_time, '%Y-%m-%d'),
            "place": meeting0.place,
            "status": meeting0.status,
            "pic_url": meeting0.pic_url,
            "attachs": [{
                "file_name": attach.filename,
                "file_url": attach.file_url,
                "file_size": attach.size,
                "id": attach.id
            }for attach in attachs]
        }

    @login_required
    def post(self):
        if self.user.myuser.user_type < 2:
            raise InputError("您没有权限修改会议状态！")
        self.check_input("meeting_id")
        if 'status' in self.input and self.user.myuser.user_type < 3:
            raise InputError("您没有权限修改会议状态！")

        data = self.input
        meeting0 = Meeting.objects.get(id = data["meeting_id"])
        if meeting0.end_time < timezone.now():
            raise LogicError("会议已经结束，您无法修改会议状态！")
        if "start_time" in data and "end_time" in data:
            data['start_time'] = datetime.datetime.strptime(data['start_time'] + "-8", "%Y-%m-%d-%H")
            data['end_time'] = datetime.datetime.strptime(data['end_time'] + "-8", "%Y-%m-%d-%H")
            if data['start_time'] < timezone.now().astimezone(timezone.utc).replace(tzinfo=None) and datetime.datetime.strftime(meeting0.start_time, '%Y-%m-%d') != datetime.datetime.strftime(data['start_time'], '%Y-%m-%d'):
                raise LogicError("会议开始时间早于当前时间！")
            if data['start_time'] > data['end_time']:
                raise LogicError("会议开始时间晚于会议结束时间！")
        if "uploadpic" in data:
            time_name = str(timezone.now().timestamp()) + ".png"
            img_path = MEDIA_ROOT + '/' + time_name
            open(img_path, "wb").write(data['uploadpic'][0].read())
            data['pic_url'] = SITE_DOMAIN + '/upload/' + time_name
        meeting0.change_information(self.input)

class MeetingCreateView(APIView):
    @login_required
    def post(self):
        if self.request.user.myuser.user_type != 2:
            raise InputError("您没有权限创建会议！")
        self.check_input('meeting_type', 'name', 'max_people_num', 'phone_num', 'description', 'start_time', 'end_time', 'place', 'uploadpic')
        data = {
            'status': 0
        }
        for key in self.input:
            data[key] = self.input[key]
        data['uploadpic'] = self.request.FILES['uploadpic']
        data['organizer'] = self.request.user.myuser
        data['start_time'] = datetime.datetime.strptime(data['start_time'] + "-8", "%Y-%m-%d-%H")
        data['max_people_num'] = int(data['max_people_num'])
        data['end_time'] = datetime.datetime.strptime(data['end_time'] + "-8", "%Y-%m-%d-%H")
        if data['start_time'] < timezone.now().astimezone(timezone.utc).replace(tzinfo=None):
            raise LogicError("会议开始时间早于当前时间！")
        if data['start_time'] > data['end_time']:
            raise LogicError("会议开始时间晚于会议结束时间！")
        time_name = str(timezone.now().timestamp()) + ".png"
        img_path = MEDIA_ROOT + '/' + time_name
        open(img_path, "wb").write(data['uploadpic'].read())
        data['pic_url'] = SITE_DOMAIN + '/upload/' + time_name
        meeting0 = Meeting.create_new_meeting(data)
        if not "uploadfile" in data:
            return
        Attachment.CreateAttachment(data["uploadfile"][0], meeting0)

    @login_required
    def get(self):
        self.check_input("meeting_id")
        if self.request.user.myuser.user_type < 2:
            raise InputError("您没有权限删除该会议！")
        meeting0 = Meeting.objects.get(id = int(self.input["meeting_id"]))
        if self.user.myuser.user_type == 2 and meeting0.organizer != self.user.myuser:
            raise LogicError("该会议不是由您创建，您无法删除该会议！")
        meeting0.delete()

class RegisterView(APIView):
    def post(self):
        self.check_input('user_type', 'account_name', 'account_pass')
        MyUser.create_new_user(self.input)

class LogInView(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            usr = self.request.user.myuser
            return {
                'type': usr.user_type,
                'name': usr.name,
            }
        else:
            return {
                "type": 0
            }

    def post(self):
        self.check_input('username', 'password')
        user = authenticate(username = self.input['username'], password = self.input['password'])
        if user is not None:
            login(self.request, user)
            return 1
        else:
            return 2

class LogOutView(APIView):
    @login_required
    def get(self):
        logout(self.request)

class UserBindView(APIView):
    def get(self):
        self.check_input("open_id")
        user = MyUser.objects.filter(open_id=self.input["open_id"])
        if len(user) < 1:
            raise LogicError("未找到符合要求的对应微信用户!")
        if user[0].user_type == 0:
            return False
        else:
            return True

    def post(self):
        self.check_input("openid", "account", "password")
        user = authenticate(username=self.input['account'], password=self.input['password'])
        if user is not None:
            if user.myuser.open_id:
                raise LogicError('该Mynager账号已绑定了微信号，请解绑后重试！')
            old_user = User.objects.get(username=self.input["openid"])
            old_user.delete()
            user.myuser.open_id = self.input["openid"]
            user.myuser.save()
            login(self.request, user)
        else:
            raise ValidateError("账号或者密码不正确，请重新输入！")

class UserMessageView(APIView):
    @login_required
    def get(self):
        if self.request.user.is_authenticated():
            usr = self.request.user.myuser
            return {
                'type': usr.user_type,
                'user_status': usr.user_status,
                'id': usr.id,
                'account': usr.user.username,
                'name': usr.name,
                'phone_num': usr.phone_num,
                'description': usr.description,
                'pic_url': usr.pic_url,
                'open_id': usr.open_id,
                'email': usr.user.email,
                'user_image': usr.user_image,
                'idcard_image': usr.idcard_image,
                'user_IDnum': usr.user_IDnum,
                'true_name': usr.name_true
            }

    @login_required
    def post(self):
        if self.request.user.is_authenticated():
            usr = self.request.user.myuser
            data = self.input
            if "old_pass" in data and "new_pass" in data:
                user = authenticate(username=self.user.username, password=data["old_pass"])
                if user:
                    user.set_password(data["new_pass"])
                    user.save()
                    return
                else:
                    raise InputError("您输入的旧密码不正确！")
            if "img" in data:
                time_name = str(timezone.now().timestamp()) + ".png"
                img_path = MEDIA_ROOT + '/' + time_name
                open(img_path, "wb").write(data['img'][0].read())
                data['pic_url'] = SITE_DOMAIN + '/upload/' + time_name
            usr.change_information(data)

class UserVerifyView(APIView):
    @login_required
    def post(self):
        self.check_input("true_name", "user_idnum", "user_image", "idcard_image")
        self.user.myuser.name_true = self.input["true_name"]
        self.user.myuser.user_IDnum = self.input["user_idnum"]
        time_name = str(timezone.now().timestamp()) + ".png"
        img_path = MEDIA_ROOT + '/' + time_name
        open(img_path, "wb").write(self.input['user_image'][0].read())
        self.user.myuser.user_image = SITE_DOMAIN + '/upload/' + time_name
        time_name1 = str(timezone.now().timestamp()) + ".png"
        img_path1 = MEDIA_ROOT + '/' + time_name1
        open(img_path1, "wb").write(self.input['idcard_image'][0].read())
        self.user.myuser.idcard_image = SITE_DOMAIN + '/upload/' + time_name1
        self.user.myuser.user_status = 1
        self.user.myuser.save()

    @login_required
    def get(self):
        if "user_id" in self.input:
            if self.user.myuser.user_type < 3:
                raise LogicError("您没有权限进行此项操作！")
            user1 = MyUser.objects.get(id=int(self.input["user_id"]))
            if(int(self.input["status"]) == 2):
                data = {
                    "user_status": 2
                }
            else:
                data = {
                    "name_true": '',
                    "user_IDnum": '',
                    "user_image": '',
                    "idcard_image": '',
                    "user_status": 0
                }
        else:
            data = {
                "name_true": '',
                "user_IDnum": '',
                "user_image": '',
                "idcard_image": '',
                "user_status": 0
            }
            user1 = self.user.myuser
        user1.change_information(data)

class ChangeRelationView(APIView):
    @login_required
    def get(self):
        self.check_input("relation", "meet_id")
        rel_num = int(self.input["relation"])
        meet = Meeting.objects.get(id=int(self.input["meet_id"]))
        Relation.ChangeRelation(self.user.myuser, meet, rel_num)
        return

    @login_required
    def post(self):
        self.check_input("relation", "meet_id", "user_id")
        meet = Meeting.objects.get(id=int(self.input["meet_id"]))
        if self.user.myuser.user_type != 2 or meet.organizer != self.user.myuser:
            raise LogicError("您没有权限访问这些数据")
        rel_num = int(self.input["relation"])
        user1 = MyUser.objects.get(id=self.input["user_id"])
        Relation.ChangeRelation(user1, meet, rel_num)

class GetRelationView(APIView):
    @login_required
    def get(self):
        relat0 = Relation.objects.all().filter(user=self.user.myuser)
        data = {
            "rel1": [{
                "meet_name": rel.meeting.name,
                "meet_id": rel.meeting.id
            } for rel in relat0 if rel.status == 1
            ],
            "rel2": [{
                "meet_name": rel.meeting.name,
                "meet_id": rel.meeting.id
            } for rel in relat0 if rel.status == 2
            ],
            "rel3": [{
                 "meet_name": rel.meeting.name,
                 "meet_id": rel.meeting.id
            } for rel in relat0 if rel.status == 3
            ]
        }
        return data

class GetPublishView(APIView):
    @login_required
    def get(self):
        if self.user.myuser.user_type != 2:
            raise LogicError("您没有权限访问这些数据！")
        meet_list = Meeting.objects.all().filter(organizer= self.user.myuser)
        data = [{
            "id": meet.id,
            "name": meet.name,
            "description": meet.description,
            "status": meet.status
        } for meet in meet_list]
        return data

class ParticipantManageView(APIView):
    @login_required
    def get(self):
        if self.user.myuser.user_type != 2:
            raise LogicError("您没有权限访问这些数据！")
        self.check_input("meet_id")
        meet = Meeting.objects.get(id=int(self.input["meet_id"]))
        if meet.organizer != self.user.myuser:
            raise LogicError("您不是活动的创建者，无权获取这些数据！")
        relats = Relation.objects.all().filter(meeting=meet)
        data = [{
            "user_name": relat.user.name,
            "status": relat.status,
            "user_id": relat.user.id
        }for relat in relats]
        return data

    @login_required
    def post(self):
        self.check_input("meet_id", "key_word")
        key = self.input["key_word"]
        meet = self.input["meet_id"]
        if self.user.myuser.user_type != 2:
            raise LogicError("您没有权限访问这些数据！")
        users = MyUser.objects.all()
        data = [{
            "name": user.name,
            "description": user.description,
            "id": user.id,
            "relation": Relation.GetRelation(user.id, meet)
        }for user in users if user.name.find(key) > -1 or user.description.find(key) > -1]
        return data



class CreateNoticeView(APIView):
    @login_required
    def post(self):
        self.check_input("to_ids", "content")
        to_ids = self.input["to_ids"]
        for to_id in to_ids:
            user = MyUser.objects.get(id=int(to_id))
            con = self.input["content"]
            Notice.CreateNotice(user, con)
            if(user.open_id != ""):
                createNotice(user.open_id, con)

    @login_required
    def get(self):
        self.check_input("notice_id")
        Notice.DelNotice(int(self.input["notice_id"]))

class NoticeMessageView(APIView):
    @login_required
    def get(self):
        notices = Notice.objects.all().filter(touser=self.user.myuser)
        data = [{
            "time": datetime.datetime.strftime(notice.time,'%Y-%m-%d %H:%M:%S'),
            "content": notice.content,
            "id": notice.id
        }for notice in notices]
        return data

class CreateAttachView(APIView):
    @login_required
    def post(self):
        self.check_input("uploadfile", "meet_id")
        meet = Meeting.objects.get(id=int(self.input["meet_id"]))
        Attachment.CreateAttachment(self.input["uploadfile"][0], meet)

    @login_required
    def get(self):
        self.check_input("attach_id")
        attach = Attachment.objects.get(id=int(self.input["attach_id"]))
        attach.delete()