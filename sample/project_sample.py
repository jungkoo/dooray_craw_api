# -*- coding: utf-8 -*-
from dooray import Login
from dooray.project import DoorayProject

Login(user_id="<USER_ID>", password="<USER_PASS>", driver_path="<chromedriver path>")

if __name__ == "__main__":
    with DoorayProject() as projects:
        project = projects.get_project_list()
        for p in project:
            print("# 프로젝트 : {}".format(p.title))
            issues = projects.get_issue_list(project_id=p.id)
            for issue in issues:
                print(issue)


