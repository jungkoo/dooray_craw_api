# -*- coding: utf-8 -*-
from dooray import Login


class DoorayProject:
    def __init__(self):
        self._login: Login = Login.current()

    def get_project_title_list(self):
        d = self._login.webdriver()
        d.get("{}/project/project-lists".format(self._login.url()))
        result = []
        for row in d.find_elements_by_css_selector("div.projectLine") or []:
            title = row.find_element_by_css_selector("a.projectLine__title").text
            result.append(title.strip())
        return result

    def close(self):
        if self._driver:
            self._driver.close()

