# -*- coding: utf-8 -*-
from dooray import Login
from dooray.project import DoorayProject

Login(user_id="<USER_ID>", password="<USER_PASS>", driver_path="<chromedriver path>")

if __name__ == "__main__":
    project = DoorayProject()
    titles = project.get_project_title_list()
    print(titles)
