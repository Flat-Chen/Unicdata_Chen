import logging
import random
import re
import time

import execjs
import requests
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.http import Headers
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message
from twisted.internet.error import TimeoutError
from twisted.internet.error import TimeoutError

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',

    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',

    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',

    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',

    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',

    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',

    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',

    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',

    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',

    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']


def get_ug():
    ua = random.choice(user_agent_list)
    return ua


def get_Proxy():
    url = 'http://192.168.2.120:5000/'
    headers = {
        'Connection': 'close',
    }
    # while True:
    #     try:

    proxy = requests.get(url, headers=headers, auth=('admin', 'zd123456'), timeout=5).text[0:-6]

    return proxy


class ProxyMiddleware(object):
    def __init__(self):
        self.chian_new_cookie='__jsl_clearance=1585646667.223|0|FwUchT1pNKX7lg%2FVm33MHVzA2jw%3D'
        self.chian_new_headers='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11'


    def get_toutiao_cookie(self):
        code = r"""function aa() {
        var t = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".split("")
          , e = t.length
          , n = (new Date).getTime().toString(36)
          , i = [];
        i[8] = i[13] = i[18] = i[23] = "_",
        i[14] = "4";
        for (var a, r = 0; r < 36; r++)
            i[r] || (a = 0 | Math.random() * e,
            i[r] = t[19 == r ? 3 & a | 8 : a]);
        return n + "_" + i.join("")
    }"""
        js_code = execjs.compile(code)
        a = js_code.call('aa')
        return a
    def get_china_new_cookie(self,js,url):
        header ="""var window ={
    addEventListener:function(){}
}
setTimeout =function(a,b){}
var document ={}
document ={
    cookie:"",
    createElement:function(a){
      return {
          innerHTML:""
          ,firstChild:{
            href:"%s"
          }

    }
    },
    addEventListener:function(a,b,c){return b()},
    attachEvent:function(a,b){return b()}
}
"""%(url)
        end ="""function get_cookie(){
    return document.cookie
}"""
        code=header+js+end
        js_code =execjs.compile(code)
        self.chian_new_cookie= js_code.call('get_cookie').split(";")[0]

    def process_request(self, request, spider):
        if "https://weibo.cn/" in request.url and 'info' in request.url:
            request.cookies = "ALF=1581060496; SCF=Ag1oJ0wUTnrUmfEoncpMVMV0gnCZrlSgfyd8E85Ca5975ikhDUg8oCdXfL6X5VCJ_iI5Ejfj4BrtyNrb_xMBROA.; SUB=_2A25zEfTjDeRhGeBH41EQ8CjFzDqIHXVQ_ZyrrDV6PUJbktANLXLikW1NQb4OCx_AV0F2xJWGvecZlK14-eLh53Ys; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW-flm.UEgV.hlhNb4pjk025JpX5K-hUgL.Foq41hepehq4S0q2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMc1Kn0eK5c1KMc; SUHB=0IIFUvWUh6Svuh; SSOLoginState=1578468531; _T_WM=03834d962d7dfbc522bb79239d3403da"
        if spider.name != "huachen_dealer" and "https://weibo.cn/" not in request.url and spider.name != 'china_new_article':
            proxy = get_Proxy()
            logging.log(msg="use           " + proxy, level=logging.INFO)

            request.headers['User-Agent'] = get_ug()
            request.meta['proxy'] = "http://" + proxy
        if '/intf/topic/counter.ajax' in request.url:
            proxy = get_Proxy()
            logging.log(msg="use           " + proxy, level=logging.INFO)
            request.cookies = {"pcsuv": ""}
            request.headers['User-Agent'] = get_ug()
            request.meta['proxy'] = "http://" + proxy
        if 'www.toutiao.com' in request.url:
            # proxy = get_Proxy()
            # logging.log(msg="use           " + proxy, level=logging.INFO)
            request.cookies = {"s_v_web_id": self.get_toutiao_cookie()}
            request.headers['User-Agent'] = get_ug()
            # request.meta['proxy'] = "http://" + proxy
        if spider.name == 'china_new_article':
            proxy = get_Proxy()
            logging.log(msg="use           " + proxy, level=logging.INFO)
            request.cookies = {self.chian_new_cookie.split("=")[0]: self.chian_new_cookie.split("=")[1]}
            #  不需要头
            # request.headers['User-Agent'] = self.chian_new_headers
            request.meta['proxy'] = "http://" + proxy

    def process_response(self, request, spider, response):
        # print(response.status,"*"*50)
        print("*" * 50, response.status)
        # print("*" * 50, request.headers)
        # print(response.text)
        if response.status != 200:
            if spider.name !='china_new_article':
                proxy = get_Proxy()
                request.meta['proxy'] = "http://" + proxy
                logging.log(msg="{}    url Redirecting ".format(response.url), level=logging.INFO)
                return request
            else:
                url =request.url
                js =re.findall(r'<script>(.*)</script>',response.text)[0] .replace('\n', '')
                self.get_china_new_cookie(js,url)
                proxy = get_Proxy()
                logging.log(msg="use           " + proxy, level=logging.INFO)
                request.cookies = {self.chian_new_cookie.split("=")[0]: self.chian_new_cookie.split("=")[1]}
                #  不需要头
                request.headers['User-Agent'] = self.chian_new_headers
                request.meta['proxy'] = "http://" + proxy
                return request
        return response


class WEIXINMiddleware(object):
    def __init__(self):
        #   xwRXvOf9blITO6qwrjALlwFRG1jvNNQ0w1JoEqj4-jnrBC_mZHqYEkbg1mMnirL9CZgOAxap3WcMlY6xDUVZabIAhiTkPO7IikF5d7Z2BJKPoLBcQ0r7Rof2rV4IFW15dFnE7Y8b6t9azPP08Do2ZTQ_qy97PS0ONYgbG20Hjk;
        self.cookie_list = [{
            "SNUID": "F049B889F5F36D480A7CB09CF6C4C709",
            "ppinf": "5|1578619757|1579829357|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlOEElQUElRTUlOEElQUF8Y3J0OjEwOjE1Nzg2MTk3NTd8cmVmbmljazoxODolRTUlOEElQUElRTUlOEElQUF8dXNlcmlkOjQ0Om85dDJsdUlEaUFwWERZbFBCSUotTDBBUzFSUXNAd2VpeGluLnNvaHUuY29tfA",
            "pprdig": "fmVn8jhfv4yyheRqWqBwYYN8ZZxiBX8Cq6sHaVkPcer_-RaeAvOW78uBuVllPChAaqv_yULE1eaz_mKZ5CC4Lwc7CjhlLRHAcWrn9uq0UpN5BkowhVMHUc4Z6TbEvo0IKacIH2XAWKmiFUa8fpdWJMRIacG1tKYL8QSeCD5ohoo"

        },
            {
                "SUID": "7650A7B42E18960A000000005CF0E7CF",
                "ppinf": "5|1578645160|1579854760|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo5OiVFNSVCRCVBQ3xjcnQ6MTA6MTU3ODY0NTE2MHxyZWZuaWNrOjk6JUU1JUJEJUFDfHVzZXJpZDo0NDpvOXQybHVIS2N4YmVSVmtpeklIaTRrMTBQMXgwQHdlaXhpbi5zb2h1LmNvbXw",
                "pprdig": "xwRXvOf9blITO6qwrjALlwFRG1jvNNQ0w1JoEqj4-jnrBC_mZHqYEkbg1mMnirL9CZgOAxap3WcMlY6xDUVZabIAhiTkPO7IikF5d7Z2BJKPoLBcQ0r7Rof2rV4IFW15dFnE7Y8b6t9azPP08Do2ZTQ_qy97PS0ONYgbG20Hjk"
            },
            {
                "SUID": "FB1DC0B73865860A5DFB617F000DADB2",
                "ppinf": "5|1578626725|1579836325|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo0OkNhZ2V8Y3J0OjEwOjE1Nzg2MjY3MjV8cmVmbmljazo0OkNhZ2V8dXNlcmlkOjQ0Om85dDJsdUpfWlhlOGJfeEk4YkRFWExVSmM1QzRAd2VpeGluLnNvaHUuY29tfA",
                "pprdig": "WfFB1ZRzE2QPGtZUiA2lXbRMQrlunJs_F4H35gsB3dQd_gdrqfM2V2Kd_fZy0-hUJCyNeb-j2BNmsmil8s5wSK8dsil65aZuWb-BgkCGuNZKo7M0Z4S_GkrOO2LBvi-KuauB1OM0YhNgIACVxA3FQ__F4ily6JysVSVc76lylzI"

            }]

    def process_request(self, request, spider):
        #     ,"Cookie": ";"
        request.cookies = random.choice(self.cookie_list)

    def process_response(self, request, spider, response):
        if response.status != 200:
            return request
        return response


class User_AgentMiddleware(object):
    @staticmethod
    def get_ug():
        ua = random.choice(user_agent_list)
        return ua

    def process_request(self, request, spider):
        if spider.name == 'autohome_meb_fans':
            User_Agent = {'User-Agent': User_AgentMiddleware.get_ug(),
                          'Referer': 'https://www.autohome.com.cn/', }
            request.headers = Headers(User_Agent)
        elif spider.name == 'xcar_meb_fans':
            cookies = {
                'nguv': 'c_1579065847302750013617172186474040',
                '_Xdwuv': '5e1ea1f7b34ea',
                '_Xdwnewuv': '1',
                '_PVXuv': '5818a1f806387',
                'zg_did': '%7B%22did%22%3A%20%2216fa7a8b35d5b-04a170e89e2443-396a4605-144000-16fa7a8b35e4e6%22%7D',
                'place_prid_lin': '2',
                'place_crid_lin': '507',
                'place_prname': '%E4%B8%8A%E6%B5%B7%E5%B8%82',
                '_locationInfo_': '%7Burl%3A%22http%3A%2F%2Fsh.xcar.com.cn%2F%22%2Ccity_id%3A%22507%22%2Cprovince_id%3A%222%22%2C%20city_name%3A%22%25E4%25B8%258A%25E6%25B5%25B7%22%7D',
                '_newLocationInfo': '%7B%22url%22%3A%22http%3A%2F%2Fsh.xcar.com.cn%2F%22%2C%22city_id%22%3A%22507%22%2C%22province_id%22%3A%222%22%2C%20%22city_name%22%3A%22%25E4%25B8%258A%25E6%25B5%25B7%22%7D',
                'fw_slc': '1%3A1579065848%3B1%3A1579065856%3B1%3A1579065857%3B1%3A1579065891%3B1%3A1579065895',
                'Hm_lvt_53eb54d089f7b5dd4ae2927686b183e0': '1579065849,1579065891,1579144374',
                'zg_8f3d0255011c4bc5bae66beca6584825': '%7B%22sid%22%3A%201579144374521%2C%22updated%22%3A%201579144375004%2C%22info%22%3A%201579065848679%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E7%88%B1%E5%8D%A1%E6%B1%BD%E8%BD%A6%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22landHref%22%3A%20%22http%3A%2F%2Fwww.xcar.com.cn%2F%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201579144374521%7D',
                'place_crname': '%E4%B8%8A%E6%B5%B7%E8%BD%A6%E5%B8%82',
                'fw_pvc': '1%3A1579065848%3B1%3A1579065856%3B1%3A1579065891%3B1%3A1579144374%3B1%3A1579144377',
                '__jsluid_h': '11c98c0681f8a5708215b6419c4308ff',
                'iwt_uuid': '9e240aff-d1fe-4f13-b8de-693536617910',
                'gdxidpyhxdE': 'nrHZlq3dK2ce3jz%2BS2qBIAaMl%5CCcB4g8sisnchaoltdyyteGijszQ%5C97tNj9qnIyL2CAD7PiB%2Fg6R%2BNUKp7XOEIj%2B33hdwD%2FbGHJCZkj5HTtI%2BaN2vY4IOKjEe%2B%2Bp6SEc8cZf64w2JsBzb1Zv8M6zof2ZzdflfmI5qmcBMKq%5C%2BUHmlgn%3A1579145288441',
                '_9755xjdesxxd_': '32',
                'YD00788855712789%3AWM_NI': 'd2jeiUvkJy2%2BAtgew05Z5S%2BZyjyyCiF8jTkNnVRnrdGIJCVAs7WJLAsmGoppYGA2POjBlr1IwoVvzAPB7qemzsnYmqS%2Bj4z5y3tJxx2YIUH8BCe%2FTEie%2BfE7M%2FTzm9l4MW8%3D',
                'YD00788855712789%3AWM_NIKE': '9ca17ae2e6ffcda170e2e6eed4fb7ea8acaeb6b85987868ba6c14f938f8a85f221b4eeb9bbf9349ce9a285c42af0fea7c3b92aa8eea686ec5fb6b5869ab12183aca986f63cf786fbb4aa52bbb6b79ac26386e8a6b5ea46ae8a9e8ff170859786a4d54bb1e999abcf4bb1b38990f37c9b998fd3d345aa9ea493b443b5b19a97f94b949ef992e867baada2baf07b91f5a6d5f93fbbedbcabfb74f28787b6cb34829dabd0d74fabbbe587c83d8ff19c9bf033b0ec83b8bb37e2a3',
                'YD00788855712789%3AWM_TID': '33lMnXl%2BgIVEAUEAUEIp%2F52hYz4Xv3dE',
                'fw_exc': '1%3A1579065855%3B1%3A1579065920%3B1%3A1579065921%3B1%3A1579144378%3B1%3A1579144390',
                'cooperation_referer': 'http%253A%252F%252Finfo.xcar.com.cn%252F201911%252Fnews_2043849_1.html',
                'weibo_referer': 'http%253A%252F%252Finfo.xcar.com.cn%252F201911%252Fnews_2043849_1.html',
                'fw_clc': '1%3A1579144379%3B1%3A1579144758%3B1%3A1579144760%3B1%3A1579144763%3B1%3A1579144771',
                '_discuz_uid': '18228917',
                '_discuz_pw': 'ad273fb969f86f16141d7edaafee0fb8',
                '_xcar_name': 'xuser18328917',
                '_discuz_vip': '11',
                'bbs_cookietime': '31536000',
                'bbs_auth': 'Vk%2FrulB5%2BEdbMCVz78EXvQo4siWMuBvpPSfb78CNBXkJ3WP1tuwNpobRKkqkaFJNDjs',
                'bbs_sid': 'Ak5wSs',
                '__isshowad': 'no',
                'Hm_lpvt_53eb54d089f7b5dd4ae2927686b183e0': '1579146217',
            }
            User_Agent = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',

                'Referer': 'http://my.xcar.com.cn/'
                , "Upgrade-Insecure-Requests": "1"
            }
            request.headers = Headers(User_Agent)
            proxy = get_Proxy()
            request.cookies = cookies
            request.headers['User-Agent'] = get_ug()
            request.meta['proxy'] = "http://" + proxy

        else:
            User_Agent = {'User-Agent': User_AgentMiddleware.get_ug()}
            request.headers = Headers(User_Agent)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        if isinstance(exception, TimeoutError):
            return requests
