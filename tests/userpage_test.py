from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os, time
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


def fillInTable(browser, tabId, key):
    browser.find_element_by_id(tabId).clear()
    time.sleep(0.1)
    browser.find_element_by_id(tabId).send_keys(key)
    time.sleep(0.1)