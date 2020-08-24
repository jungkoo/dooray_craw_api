# -*- coding: utf-8 -*-
from collections import namedtuple

from dooray import Login
import json

# [프로젝트] id, 프로젝트명
ProjectInfo = namedtuple('ProjectInfo', 'id title')
# [이슈] id, 순번, 제목, 등록자, 담당자, 등록일, 종료일
IssueInfo = namedtuple('IssueInfo', 'id seq title user cc reg_date close_date status')

_status_code = dict(working="진행중", closed="완료", registered="등록")


class DoorayProject:
    def __init__(self):
        self._login: Login = Login.current()
        self._current_driver = self._login.webdriver()  # login 한 브라우저창을 재활용한다.
        self._project_lists = self.__project_info_extract()
        self._issue_list_seed_url = self._login.url() + "/v2/wapi/projects/!{}/posts"

    def __enter__(self):
        return self

    def __project_info_extract(self):
        try:
            d = self._current_driver
            d.get("{}/v2/wapi/project-views/1".format(self._login.url()))
            text = d.find_element_by_tag_name("pre").get_attribute("innerHTML")
            el = json.loads(text)
            rsb = []
            if "result" not in el or "content" not in el["result"] or "projects" not in el["result"]["content"]:
                raise Exception("project load failed.")
            for row in el["result"]["content"]["projects"]:
                r = ProjectInfo(id=row["id"], title=row["code"])
                rsb.append(r)
        finally:
            if self._login:
                self._login.close
        return rsb

    def __exit__(self, exc_type, exc_val, exc_tb):
        l: Login = Login.current()
        l.close()

    def get_project_list(self):
        """

        [ProjectInfo(id='2185359473446434534', title='공지'), ....]
        :return:
        """
        return self._project_lists

    def get_issue_list(self, project_id, **params):
        """
        특정 프로젝트의 이슈 정보를 가져온다.

        :param project_id: 프로젝트 아이디  (get_project_list 에서 알수 있다)
        :param params: 필터링 조건을 넣을수 있다.
        :return: 이슈 정보
        """
        try:
            d = self._current_driver
            url = self._issue_list_seed_url.format(project_id)
            base_param = dict(order="postUpdatedAt", page=0, size=30)
            base_param.update(params)
            url += "?"
            for p in base_param:
                url += "{}={}&".format(p, base_param[p])

            d.get(url)
            text = d.find_element_by_tag_name("pre").get_attribute("innerHTML")
            el = json.loads(text)
            rsb = []
            if "result" not in el or "contents" not in el["result"]:
                raise Exception("project load failed.")
            for row in el["result"]["contents"]:
                user = row["users"]["from"]["member"]["name"]
                cc = []
                for cc_user in row["users"]["cc"]:
                    if cc_user["type"] == "group":
                        cc.append(cc_user["group"]["code"])
                    elif cc_user["type"] == "member":
                        cc.append(cc_user["member"]["name"])
                    else:
                        raise Exception("Unknown CC type.")

                r = IssueInfo(id=row["id"], seq=row["number"], title=row["subject"], user=user, cc=",".join(cc),
                              reg_date=row["createdAt"], close_date=row["dueDate"],
                              status=_status_code.get(row["workflowClass"]))
                rsb.append(r)
        finally:
            if self._login:
                self._login.close
        return rsb







