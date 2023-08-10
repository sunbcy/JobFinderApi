import requests
import json
import time
from urllib.parse import quote
from xlsx import write_data_into_excel

api_host = 'www.zhipin.com'  # boss


class BossApi:
    def __init__(self, host=api_host):
        self.host = host

    def get_joblist(self):
        api_url = f'http://{self.host}/wapi/zpgeek/miniapp/homepage/recjoblist.json?cityCode=101280600&sortType=1&page=1&pageSize=15&districtCode=&salary=405&appId=10002'
        temp_ua = {"model": "iPhone SE (2nd generation)<iPhone12,8>", "platform": "ios"}
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'mpt': 'a9c8e32299ba928534224f1c423f856b',
            'ua': json.dumps(temp_ua),
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f37) NetType/WIFI Language/zh_CN'
        }  # mpt是授权的参数
        r = requests.get(api_url, headers=headers)
        r_json = json.loads(r.text)
        # print(r.text)
        code = r_json['code']
        message = r_json['message']
        zpData = r_json['zpData']
        zpdata_hasmore = zpData['hasMore']
        zpdata_joblist = zpData['jobList']
        for _ in zpdata_joblist:
            job_securityid = _.get('securityId')
            job_id = _.get('encryptJobId')
            job_lid = _.get('lid')
            self.get_jobs_detail_by_securityid_jobid(job_securityid, job_id, job_lid)
            break

    def search_job_by_keyword(self, keyword):
        """根据关键词搜索职位"""
        api_url = f'http://{self.host}/wapi/zpgeek/miniapp/search/joblist.json?pageSize=50&query={quote(keyword)}&city=101280600&source=1&sortType=0&subwayLineId=&subwayStationId=&districtCode=&businessCode=&longitude=&latitude=&position=&expectId=&expectPosition=&page=1&appId=10002'
        temp_ua = {"model": "iPhone SE (2nd generation)<iPhone12,8>", "platform": "ios"}
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'platform': 'zhipin/ios',
            'ver': '5.1500',
            'mpt': 'a9c8e32299ba928534224f1c423f856b',
            'ua': json.dumps(temp_ua),
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f37) NetType/WIFI Language/zh_CN'
        }  # mpt是授权的参数
        r = requests.get(api_url, headers=headers)
        r_json = json.loads(r.text)
        code = r_json['code']
        message = r_json['message']
        zpData = r_json['zpData']
        zpdata_hasmore = zpData['hasMore']
        zpdata_joblist = zpData['list']
        ret_jobinfos = []
        for _ in zpdata_joblist:
            job_info = {}
            job_securityid = _.get('securityId')
            job_id = _.get('encryptJobId')
            job_lid = _.get('lid')
            r_job_json = self.get_jobs_detail_by_securityid_jobid(job_securityid, job_id, job_lid)
            job_code = r_job_json.get('code')
            job_message = r_job_json.get('message')
            job_zpData = r_job_json.get('zpData')
            if job_zpData:
                job_zpData_bossBaseInfoVO = job_zpData.get('bossBaseInfoVO')
                recruiter_name = job_zpData_bossBaseInfoVO.get('name')
                recruiter_title = job_zpData_bossBaseInfoVO.get('title')
                recruiter_activetimedesc = job_zpData_bossBaseInfoVO.get('activeTimeDesc')
                recruiter_activetime = job_zpData_bossBaseInfoVO.get('activeTime')
                recruiter_bossonline = job_zpData_bossBaseInfoVO.get('bossOnline')
                recruiter_brandname = job_zpData_bossBaseInfoVO.get('brandName')
                recruiter_disablebossinfo = job_zpData_bossBaseInfoVO.get('disableBossInfo')

                job_info['recruiter_name'] = recruiter_name
                job_info['recruiter_title'] = recruiter_title
                job_info['recruiter_activetimedesc'] = recruiter_activetimedesc
                job_info['recruiter_activetime'] = recruiter_activetime
                job_info['recruiter_bossonline'] = recruiter_bossonline
                job_info['recruiter_brandname'] = recruiter_brandname
                job_info['recruiter_disablebossinfo'] = recruiter_disablebossinfo

                job_zpData_jobBaseinfovO = job_zpData.get('jobBaseInfoVO')
                jobid = job_zpData_jobBaseinfovO.get('jobId')
                jobValidStatus = job_zpData_jobBaseinfovO.get('jobValidStatus')
                job_deleted = job_zpData_jobBaseinfovO.get('deleted')
                job_position = job_zpData_jobBaseinfovO.get('position')
                job_positionName = job_zpData_jobBaseinfovO.get('positionName')
                job_positionCategory = job_zpData_jobBaseinfovO.get('positionCategory')
                job_location = job_zpData_jobBaseinfovO.get('location')
                job_locationName = job_zpData_jobBaseinfovO.get('locationName')
                job_areaDistrict = job_zpData_jobBaseinfovO.get('areaDistrict')
                job_businessDistrict = job_zpData_jobBaseinfovO.get('businessDistrict')
                job_locationDesc = job_zpData_jobBaseinfovO.get('locationDesc')
                job_experienceName = job_zpData_jobBaseinfovO.get('experienceName')
                job_degreeName = job_zpData_jobBaseinfovO.get('degreeName')
                job_lowSalary = job_zpData_jobBaseinfovO.get('lowSalary')
                job_highSalary = job_zpData_jobBaseinfovO.get('highSalary')
                job_jobDesc = job_zpData_jobBaseinfovO.get('jobDesc')
                job_requiredSkills = job_zpData_jobBaseinfovO.get('requiredSkills')
                job_address = job_zpData_jobBaseinfovO.get('address')
                job_longitude = job_zpData_jobBaseinfovO.get('longitude')
                job_latitude = job_zpData_jobBaseinfovO.get('latitude')
                job_staticMapUrl = job_zpData_jobBaseinfovO.get('staticMapUrl')
                job_pcStaticMapUrl = job_zpData_jobBaseinfovO.get('pcStaticMapUrl')
                job_salaryMonth = job_zpData_jobBaseinfovO.get('salaryMonth')
                job_performance = job_zpData_jobBaseinfovO.get('performance')
                job_salarySchemeDesc = job_zpData_jobBaseinfovO.get('salarySchemeDesc')
                job_jobType = job_zpData_jobBaseinfovO.get('jobType')
                job_jobSource = job_zpData_jobBaseinfovO.get('jobSource')
                job_daysPerWeekDesc = job_zpData_jobBaseinfovO.get('daysPerWeekDesc')
                job_leastMonthDesc = job_zpData_jobBaseinfovO.get('leastMonthDesc')
                job_salaryDesc = job_zpData_jobBaseinfovO.get('salaryDesc')
                job_salaryDescAppend = job_zpData_jobBaseinfovO.get('salaryDescAppend')
                job_salaryDetail = job_zpData_jobBaseinfovO.get('salaryDetail')
                job_afterNameIcon = job_zpData_jobBaseinfovO.get('afterNameIcon')
                job_afterNameIcons = job_zpData_jobBaseinfovO.get('afterNameIcons')
                job_proxyJob = job_zpData_jobBaseinfovO.get('proxyJob')
                job_proxyType = job_zpData_jobBaseinfovO.get('proxyType')
                job_anonymous = job_zpData_jobBaseinfovO.get('anonymous')
                job_salaryType = job_zpData_jobBaseinfovO.get('salaryType')
                job_newAddressTypeDesc = job_zpData_jobBaseinfovO.get('newAddressTypeDesc')
                job_recruitNumDesc = job_zpData_jobBaseinfovO.get('recruitNumDesc')
                job_jobSkills = job_zpData_jobBaseinfovO.get('jobSkills')
                job_jobTemplateModule = job_zpData_jobBaseinfovO.get('jobTemplateModule')
                job_blueCollarPosition = job_zpData_jobBaseinfovO.get('blueCollarPosition')
                job_graduateYearDesc = job_zpData_jobBaseinfovO.get('graduateYearDesc')
                job_recruitEndTimeDesc = job_zpData_jobBaseinfovO.get('recruitEndTimeDesc')

                job_info['jobid'] = jobid
                job_info['jobValidStatus'] = jobValidStatus
                job_info['job_deleted'] = job_deleted
                job_info['job_position'] = job_position
                job_info['job_positionName'] = job_positionName
                job_info['job_positionCategory'] = job_positionCategory
                job_info['job_location'] = job_location
                job_info['job_locationName'] = job_locationName
                job_info['job_areaDistrict'] = job_areaDistrict
                job_info['job_businessDistrict'] = job_businessDistrict
                job_info['job_locationDesc'] = job_locationDesc
                job_info['job_experienceName'] = job_experienceName
                job_info['job_degreeName'] = job_degreeName
                job_info['job_lowSalary'] = job_lowSalary
                job_info['job_highSalary'] = job_highSalary
                job_info['job_jobDesc'] = job_jobDesc
                job_info['job_requiredSkills'] = str(job_requiredSkills)
                job_info['job_address'] = job_address
                job_info['job_longitude'] = job_longitude
                job_info['job_latitude'] = job_latitude
                job_info['job_staticMapUrl'] = job_staticMapUrl
                job_info['job_pcStaticMapUrl'] = job_pcStaticMapUrl
                job_info['job_salaryMonth'] = job_salaryMonth
                job_info['job_performance'] = job_performance
                job_info['job_salarySchemeDesc'] = job_salarySchemeDesc
                job_info['job_jobType'] = job_jobType
                job_info['job_jobSource'] = job_jobSource
                job_info['job_daysPerWeekDesc'] = job_daysPerWeekDesc
                job_info['job_leastMonthDesc'] = job_leastMonthDesc
                job_info['job_salaryDesc'] = job_salaryDesc
                job_info['job_salaryDescAppend'] = job_salaryDescAppend
                job_info['job_salaryDetail'] = job_salaryDetail
                job_info['job_afterNameIcon'] = job_afterNameIcon
                job_info['job_afterNameIcons'] = str(job_afterNameIcons)
                job_info['job_proxyJob'] = job_proxyJob
                job_info['job_proxyType'] = job_proxyType
                job_info['job_anonymous'] = job_anonymous
                job_info['job_salaryType'] = job_salaryType
                job_info['job_newAddressTypeDesc'] = job_newAddressTypeDesc
                job_info['job_recruitNumDesc'] = job_recruitNumDesc
                job_info['job_jobSkills'] = job_jobSkills
                job_info['job_jobTemplateModule'] = job_jobTemplateModule
                job_info['job_blueCollarPosition'] = job_blueCollarPosition
                job_info['job_graduateYearDesc'] = job_graduateYearDesc
                job_info['job_recruitEndTimeDesc'] = job_recruitEndTimeDesc

                job_zpData_brandcominfovO = job_zpData.get('brandComInfoVO')
                comp_brandname = job_zpData_brandcominfovO.get('brandName')
                comp_proxyBrandName = job_zpData_brandcominfovO.get('proxyBrandName')
                comp_customerBrandName = job_zpData_brandcominfovO.get('customerBrandName')
                comp_logo = job_zpData_brandcominfovO.get('logo')
                comp_industryName = job_zpData_brandcominfovO.get('industryName')
                comp_stageName = job_zpData_brandcominfovO.get('stageName')
                comp_scaleName = job_zpData_brandcominfovO.get('scaleName')
                comp_brandIntroduce = job_zpData_brandcominfovO.get('brandIntroduce')
                comp_comName = job_zpData_brandcominfovO.get('comName')
                comp_legalPerson = job_zpData_brandcominfovO.get('legalPerson')
                comp_startDate = job_zpData_brandcominfovO.get('startDate')
                comp_regCapital = job_zpData_brandcominfovO.get('regCapital')
                comp_statusDesc = job_zpData_brandcominfovO.get('statusDesc')
                comp_regAddress = job_zpData_brandcominfovO.get('regAddress')
                comp_businessScope = job_zpData_brandcominfovO.get('businessScope')
                comp_srcFromDesc = job_zpData_brandcominfovO.get('srcFromDesc')
                comp_srcUrl = job_zpData_brandcominfovO.get('srcUrl')
                comp_brandWelfares = job_zpData_brandcominfovO.get('brandWelfares')
                comp_canJumpToBrandPage = job_zpData_brandcominfovO.get('canJumpToBrandPage')
                comp_introduce = job_zpData_brandcominfovO.get('introduce')

                job_info['comp_brandname'] = comp_brandname
                job_info['comp_proxyBrandName'] = comp_proxyBrandName
                job_info['comp_customerBrandName'] = comp_customerBrandName
                job_info['comp_logo'] = comp_logo
                job_info['comp_industryName'] = comp_industryName
                job_info['comp_stageName'] = comp_stageName
                job_info['comp_scaleName'] = comp_scaleName
                job_info['comp_brandIntroduce'] = comp_brandIntroduce
                job_info['comp_comName'] = comp_comName
                job_info['comp_legalPerson'] = comp_legalPerson
                job_info['comp_startDate'] = comp_startDate
                job_info['comp_regCapital'] = comp_regCapital
                job_info['comp_statusDesc'] = comp_statusDesc
                job_info['comp_regAddress'] = comp_regAddress
                job_info['comp_businessScope'] = comp_businessScope
                job_info['comp_srcFromDesc'] = comp_srcFromDesc
                job_info['comp_srcUrl'] = comp_srcUrl
                job_info['comp_brandWelfares'] = comp_brandWelfares
                job_info['comp_canJumpToBrandPage'] = comp_canJumpToBrandPage
                job_info['comp_introduce'] = comp_introduce

                ret_jobinfos.append(job_info)
            # break
        # print(ret_jobinfos)
        # quit()
        write_data_into_excel(xlspath=str('boss_' + keyword + '_jobinfos_' + time.strftime("%Y%m%d%H%M%S") + '.xlsx'), data_json_list=ret_jobinfos)

    def get_jobs_detail_by_securityid_jobid(self, securityid, jobid, lid):
        """实时获取详细职位信息(需要和上面的get_joblist()/search_job(keyword)函数配合使用)"""
        api_url = f'http://{self.host}/wapi/zpgeek/miniapp/job/detail.json?securityId={securityid}&jobId={jobid}&lid={lid}&source=10&scene=&appId=10002'
        temp_ua = {"model": "iPhone SE (2nd generation)<iPhone12,8>", "platform": "ios"}
        headers = {
            'ua': json.dumps(temp_ua),
            'platform': 'zhipin/ios',
            'ver': '5.1500',
            'mpt': 'a9c8e32299ba928534224f1c423f856b',
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f37) NetType/WIFI Language/zh_CN',
        }
        r = requests.get(api_url, headers=headers)
        r_json = json.loads(r.text)
        return r_json


if __name__ == '__main__':
    boss = BossApi()
    boss.search_job_by_keyword('嵌入式')  # search_job_by_keyword('python')  # get_joblist()  # get_jobs_detail_by_securityid_jobid
