# -*- coding: utf-8 -*-
from dooray import Login
from dooray.email import DoorayEmail
from dooray.project import DoorayProject
from datetime import datetime
import os
import csv

# CONFIGURATION
EMAIL = "아이디@도메인.dooray.com"
USER_ID = "아이"
PASSWORD = "암호"
TO_EMAIL = "이슈 리포트 받은 이메일"
DRIVER_PATH = "크롬드라이버 경로"

# SETUP
Login(user_id=USER_ID, password=PASSWORD, driver_path=DRIVER_PATH)
today = datetime.now().strftime("%Y-%m-%d")
email = DoorayEmail(email=EMAIL, password=PASSWORD)
email.subject("[이슈정리] {} : 과거 90일 이슈 리스트".format(today))
email.contents("첨부파일을 참고해주세요.\n이슈 : {} ~ 90일이전 미완료 이슈를 리스트업합니다".format(today))


def project_rows(prev_day=90, header=False):
    if header:
        yield ["프로젝트", "t이슈번호", "제목", "등록자", "담당자", "등록일", "마감일", "상태", "경과일", "진행상황"]
    with DoorayProject() as projects:
        project = projects.get_project_list()
        for p in project:
            # 등록 90일 + 등록/진행중
            all_issue = projects.get_issue_list(project_id=p.id, createdAt="prev-{}d".format(prev_day),)
            open_issue = [_x for _x in filter(lambda x: x.status != "완료", all_issue)]
            if len(open_issue) <= 0:
                continue

            for issue in open_issue:
                day_count = (datetime.now().date() - datetime.strptime(issue.reg_date[0:10], "%Y-%m-%d").date()).days
                comment = "지연"
                if day_count < 30:
                    comment = "양호"
                elif day_count < 90:
                    comment = "주의"

                project_title = p.title
                iss_seq = issue.seq
                iss_title = issue.title
                iss_user = issue.user
                iss_cc = issue.cc or "-"
                iss_reg_date = (issue.reg_date or "")[0:10]
                iss_close_date = (issue.close_date or "-")[0:10]
                iss_date_count = day_count
                iss_status = issue.status
                iss_comment = comment

                yield [project_title, iss_seq, iss_title, iss_user, iss_cc, iss_reg_date, iss_close_date,
                       iss_status, iss_date_count, iss_comment]


if __name__ == "__main__":
    # open issue - file create
    file = "open-issue-{}.csv".format(today)
    fp = open(file, "wt", encoding='euc_kr', newline='')
    writer = csv.writer(fp)
    for r in project_rows(header=True):
        writer.writerow(r)
    fp.close()

    # email send
    email.attach_file(fp.name)
    email.send(TO_EMAIL)
    os.remove(file)
    print("완료 ("+EMAIL+"->"+TO_EMAIL+"): " + today)
