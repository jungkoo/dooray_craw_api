# -*- coding: utf-8 -*-
from dooray import Login
from dooray.project import DoorayProject

Login(user_id="<USER_ID>", password="<USER_PASS>", driver_path="<chromedriver path>")

if __name__ == "__main__":
    with DoorayProject() as project:

        titles = project.get_title_list()
        print(titles)

