from api import BossApi
from xlsx import write_data_into_excel


def main():
    boss = BossApi()
    ret_school = boss.search_job_by_keyword('机器学习')
    # write_data_into_excel('kyb_all_schools.xlsx', ret_school)


if __name__ == '__main__':
    main()