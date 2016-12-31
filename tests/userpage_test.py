from django.test import LiveServerTestCase
from django.test import testcases
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from django.core import management
from django.contrib.auth.models import User
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import time
from datetime import datetime
from wechat.models import Meeting
from wechat.models import MyUser
from wechat.models import Relation
from wechat.models import Notice


class Test_login(LiveServerTestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        super(Test_login, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(Test_login, cls).tearDownClass()

    def test(self):
        user = User.objects.create_superuser('admin', '', '123456')
        user.save()
        self.browser.get('%s%s' % (self.live_server_url, '/user/login'))
        self.browser.set_window_size(1024, 768)
        name_box = WebDriverWait(self.browser, 3).until(
            expected_conditions.presence_of_element_located((By.ID, 'username'))
        )
        name_box.send_keys("admin")
        self.browser.find_element_by_id('pass').send_keys("1234567")
        self.browser.find_elements_by_class_name('btn-default')[1].click()
        time.sleep(1)
        a = self.browser.find_elements_by_xpath("//div[@id='header']/div")
        self.assertTrue(len(a) == 2)
        self.browser.find_element_by_id('pass').clear()
        self.browser.find_element_by_id('pass').send_keys("123456")
        self.browser.find_elements_by_class_name('btn-default')[1].click()
        time.sleep(1)
        a = self.browser.find_elements_by_xpath("//div[@id='header']/div")
        self.assertTrue(len(a) != 2)

class Test_meetings(LiveServerTestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        super(Test_meetings, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()
        user = MyUser.create_new_user({'account_name': '1admin', 'account_pass': '123456', 'user_type': 2})
        meet = Meeting.create_new_meeting({'meeting_type': 'boring',
                                    'name': 'DoHomework',
                                    'max_people_num': 4,
                                    'phone_num': '15546540758',
                                    'description': 'work for living',
                                    'start_time': datetime.strptime("2017-12-25 10:0:0", "%Y-%m-%d %H:%M:%S"),
                                    'end_time': datetime.strptime("2017-12-25 12:0:0", "%Y-%m-%d %H:%M:%S"),
                                    'place': 'dormitory',
                                    'status': 1,
                                    'pic_url': 'http',
                                    'organizer': user})
        xsx = MyUser.create_new_user({'account_name': 'xsx', 'account_pass': '123456', 'user_type': 1})
        relation = Relation(
            user=xsx,
            meeting=meet,
            status=3
        )
        relation.save()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(Test_meetings, cls).tearDownClass()

    def test(self):
        self.browser.get('%s%s' % (self.live_server_url, '/user/login'))
        self.browser.set_window_size(1024, 768)
        name_box = WebDriverWait(self.browser, 3).until(
            expected_conditions.presence_of_element_located((By.ID, 'username'))
        )
        name_box.send_keys("1admin")
        self.browser.find_element_by_id('pass').send_keys("123456")
        self.browser.find_elements_by_class_name('btn')[1].click()
        time.sleep(0.2)
        self.browser.get('%s%s' % (self.live_server_url, '/publisher/meetings'))
        WebDriverWait(self.browser, 3).until(
            expected_conditions.presence_of_element_located((By.ID, 'meet_list'))
        )
        meetinglist = self.browser.find_elements_by_class_name('item_name')
        time.sleep(0.1)
        self.assertTrue(len(meetinglist) == 1 and meetinglist[0].text == 'DoHomework')
        time.sleep(0.2)
        self.browser.get_screenshot_as_file('fdghdhdgfh')
        self.browser.find_elements_by_class_name('btn')[2].click()
        mwindows = self.browser.window_handles
        self.browser.switch_to_window(mwindows[1])
        time.sleep(0.1)
        self.browser.find_elements_by_class_name('base_input')[0].clear()
        self.browser.find_elements_by_class_name('base_input')[0].send_keys('Do')
        time.sleep(0.1)
        self.browser.find_elements_by_class_name('base_input')[1].clear()
        self.browser.find_elements_by_class_name('base_input')[1].send_keys('lalala')
        time.sleep(0.1)
        self.browser.find_elements_by_class_name('base_input')[2].clear()
        self.browser.find_elements_by_class_name('base_input')[2].send_keys('ooo')
        time.sleep(0.1)
        self.browser.find_elements_by_class_name('base_input')[3].clear()
        self.browser.find_elements_by_class_name('base_input')[3].send_keys('222')
        time.sleep(0.1)
        self.browser.find_elements_by_class_name('base_input')[4].clear()
        self.browser.find_elements_by_class_name('base_input')[4].send_keys('567')
        time.sleep(0.1)
        self.browser.find_elements_by_class_name('base_input')[5].clear()
        self.browser.find_elements_by_class_name('base_input')[5].send_keys('2222-12-2')
        time.sleep(0.1)
        self.browser.find_elements_by_class_name('base_input')[6].clear()
        self.browser.find_elements_by_class_name('base_input')[6].send_keys('2222-12-22')
        time.sleep(0.1)
        self.browser.find_elements_by_class_name('base_textarea')[0].clear()
        self.browser.find_elements_by_class_name('base_textarea')[0].send_keys('233')
        time.sleep(0.1)
        self.browser.find_elements_by_class_name('single_btn')[0].click()
        self.browser.get('%s%s' % (self.live_server_url, '/publisher/meetings'))
        WebDriverWait(self.browser, 3).until(
            expected_conditions.presence_of_element_located((By.ID, 'meet_list'))
        )
        meetinglist1 = self.browser.find_elements_by_class_name('item_name')
        meetinglist3 = self.browser.find_elements_by_class_name('item_intro')
        self.assertTrue(len(meetinglist1) == 1 and meetinglist1[0].text == 'Do' and meetinglist3[0].text == '233')
        self.browser.find_elements_by_class_name('btn')[0].click()
        mwindows1 = self.browser.window_handles
        self.browser.switch_to_window(mwindows1[2])
        userlist1 = self.browser.find_elements_by_class_name('item_name')
        self.assertTrue(userlist1[0].text == '用户xsx')
        self.browser.get('%s%s' % (self.live_server_url, '/publisher/meetings'))
        WebDriverWait(self.browser, 3).until(
            expected_conditions.presence_of_element_located((By.ID, 'meet_list'))
        )
        self.browser.find_elements_by_class_name('btn')[1].click()
        self.browser.refresh()
        meetinglist2 = self.browser.find_elements_by_class_name('item_name')
        self.assertTrue(len(meetinglist2) == 0)

class Test_Register(LiveServerTestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        super(Test_Register, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(Test_Register, cls).tearDownClass()

    def test(self):
        self.browser.get('%s%s' % (self.live_server_url, '/user/register'))
        name_box = WebDriverWait(self.browser, 3).until(
            expected_conditions.presence_of_element_located((By.ID, 'account_name'))
        )
        name_box.send_keys("admin")
        self.browser.find_element_by_id('pass').send_keys("123456")
        self.browser.find_element_by_id('repass').send_keys("1234567")
        self.browser.find_elements_by_class_name('btn-default')[2].click()
        a = self.browser.find_elements_by_xpath("//div[@id='header']/div")
        self.assertTrue(len(a) == 2)
        time.sleep(0.5)
        self.browser.find_element_by_id('repass').clear()
        self.browser.find_element_by_id('repass').send_keys("123456")
        self.browser.find_elements_by_class_name('btn-default')[2].click()
        time.sleep(1)
        a = self.browser.find_elements_by_xpath("//div[@id='header']/div")
        self.assertTrue(len(a) != 2)