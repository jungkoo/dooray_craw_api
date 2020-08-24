# -*- coding: utf-8 -*-
from selenium import webdriver
import threading
import logging

# 로그인 정보는 thread local 형태로 저장해서 여러번 입력 하지 않아도 정보를 활용 할 수 있도록 하자
_thread_local = threading.local()


class Login:
    def __init__(self, user_id, password, driver_path, domain="naverunion"):
        self._user_id = user_id
        self._password = password
        self._domain = domain
        self._driver_path = driver_path
        self._open_web_driver = []
        self._headless = True
        _thread_local.login = self

    def headless(self, headless=True):
        self._headless = headless
        return self

    def webdriver(self):
        option = webdriver.ChromeOptions()
        option.headless = self._headless
        option.add_argument('--lang=ko-KR')
        option.add_argument('--user-agent="Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/37.0.2049.0 Safari/537.36"')
        option.add_argument("window-size=1024x768")
        url = "https://{}.dooray.com".format(self._domain)
        d = webdriver.Chrome(self._driver_path, chrome_options=option)
        d.implicitly_wait(3)
        d.get(url)
        d.find_element_by_css_selector("input[type='text'][autocomplete='new-password']").send_keys(self._user_id)
        d.find_element_by_css_selector("input[type='password'][autocomplete='new-password']").send_keys(self._password)
        d.find_element_by_css_selector("button[type=\"submit\"]").click()
        self._open_web_driver.append(d)
        return d

    def url(self, post_url=""):
        return "https://{}.dooray.com{}".format(self._domain, post_url)

    def close(self):
        for ow in self._open_web_driver:
            if ow:
                ow.close()

    @staticmethod
    def current():
        try:
            val = _thread_local.login
        except AttributeError:
            logging.debug("current login info not found")
        else:
            return val
