import requests
import json

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
        api_url = f'http://{self.host}/wapi/zpgeek/miniapp/search/joblist.json?pageSize=15&query={keyword}&city=101280600&source=1&sortType=0&subwayLineId=&subwayStationId=&districtCode=&businessCode=&longitude=&latitude=&position=&expectId=&expectPosition=&page=1&appId=10002'
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
        for _ in zpdata_joblist:
            job_securityid = _.get('securityId')
            job_id = _.get('encryptJobId')
            job_lid = _.get('lid')
            self.get_jobs_detail_by_securityid_jobid(job_securityid, job_id, job_lid)
            break

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
    boss.search_job_by_keyword('python')  # search_job('python')  # get_joblist()  # get_jobs_detail_by_securityid_jobid
