# -*- coding: utf-8 -*-
from dooray import Login
from dooray.project import DoorayProject
from datetime import datetime

Login(user_id="<USER_ID>", password="<USER_PASS>", driver_path="<chromedriver path>")

if __name__ == "__main__":
    with DoorayProject() as projects:
        project = projects.get_project_list()
        print("프로젝트\t이슈번호\t제목\t등록자\t담당자\t등록일\t마감일\t경과일\t상태\t진행상황")
        for p in project:
            # 등록 90일 + 등록/진행중
            issues = projects.get_issue_list(project_id=p.id,
                                             createdAt="prev-90d",)
            issues = [_x for _x in filter(lambda x: x.status != "완료", issues)]
            if len(issues) <= 0:
                continue

            for issue in issues:
                day_count = (datetime.now().date() - datetime.strptime(issue.reg_date[0:10], "%Y-%m-%d").date()).days
                comment = "지연"
                if day_count < 30:
                    comment = "양호"
                elif day_count < 90:
                    comment = "주의"

                data = dict(
                    project_title=p.title,
                    iss_seq=issue.seq,
                    iss_title=issue.title,
                    iss_user=issue.user,
                    iss_cc=issue.cc or "미지정",
                    iss_reg_date=issue.reg_date,
                    iss_close_date=issue.close_date or "미지정",
                    iss_date_count=day_count,
                    iss_status=issue.status,
                    iss_comment=comment
                )
                print("{project_title}\t{iss_seq}\t{iss_title}\t{iss_user}\t{iss_cc}\t{iss_reg_date}"
                      "\t{iss_close_date}\t{iss_date_count}\t{iss_status}\t{iss_comment}".format(**data))