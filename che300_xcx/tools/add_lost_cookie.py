import json
import time
from tqdm import tqdm
from redis import Redis

redis_url = 'redis://192.168.2.149:6379/8'
r = Redis.from_url(redis_url, decode_responses=True)


def list_iter(name):
    """
    自定义redis列表增量迭代
    :param name: redis中的name，即：迭代name对应的列表
    :return: yield 返回 列表元素
    """
    list_count = r.llen(name)
    for index in range(list_count):
        yield r.lindex(name, index)


def get_rest():
    cookie_rest = []
    for item in list_iter('che300_gz:cookies'):  # 遍历这个列表
        item = item.replace("'", '"')
        cook = json.loads(item)['cookie'].replace("\n", '"')
        cookie_rest.append(cook)
    return cookie_rest


def all_cookie():
    cookie_list = []
    for item in list_iter('che300_gz:cookies_copy'):  # 遍历这个列表
        item = item.replace("'", '"')
        json_data = json.loads(item)
        cookie = json_data['cookie'].replace("\n", '"')
        cookie_list.append(cookie)
    return cookie_list


def get_lost():
    cookie_rest = get_rest()
    cookie_list = all_cookie()
    lost_cookies = list(set(cookie_list).difference(set(cookie_rest)))
    return lost_cookies


if __name__ == '__main__':
    lost_cookies = get_lost()
    for cookie in tqdm(lost_cookies):
        #     last_use_time= time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        last_use_time = '2020-12-01 10:11:10'
        cookie_dict = {"cookie": cookie, "last_use_time": last_use_time}
        # print(cookie_dict)
        r.rpush('che300_gz:cookies', str(cookie_dict).replace("'", '"').replace("\n", '"'))
