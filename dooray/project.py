# -*- coding: utf-8 -*-
from dooray import Login


class DoorayProject:
    def __init__(self):
        self._login: Login = Login.current()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        l: Login = Login.current()
        l.close()

    def get_title_list(self):
        """
        접근 가능한 프로젝트 제목을 리턴한다.

        :return: 프로젝트 제목 (type: List)
        """
        d = self._login.webdriver()
        d.get("{}/project/project-lists".format(self._login.url()))
        result = []
        for row in d.find_elements_by_css_selector("div.projectLine") or []:
            title = row.find_element_by_css_selector("a.projectLine__title").text
            result.append(title.strip())
        return result

