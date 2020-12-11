from random import shuffle
import pymongo
import datetime
from dateutil import rrule
from redis import Redis
from tqdm import tqdm

connection = pymongo.MongoClient('192.168.1.94', 27017)
db = connection["che300"]
collection = db["che300_car"]
result = collection.find()
result_list = list(result)
print(len(result_list))

nowyear = datetime.datetime.now().year
nowmonth = datetime.datetime.now().month
now_date = str(nowyear) + "-" + str(nowmonth)
start_date = datetime.datetime.strptime(now_date, '%Y-%m')

redis_url = 'redis://192.168.2.149:6379/8'
r = Redis.from_url(redis_url, decode_responses=True)
start_urls = []
for cars in tqdm(result_list):
    brand_id = cars['brand_id']
    family_id = cars['family_id']
    vehicle_id = cars['vehicle_id']
    min_reg_year = int(cars['min_reg_year'])
    max_reg_year = int(cars['max_reg_year'])

    # 遍历每款车型的最大最小上牌年
    for regyear in range(min_reg_year, max_reg_year + 1):
        reg_month_list = [1, 12] if regyear == min_reg_year else \
            ((([1, 12] if nowmonth == 12 else [1, nowmonth + 1]) if regyear == nowyear
              else [1, 12]) if regyear == max_reg_year else [12])
        for regmonth in reg_month_list:
            regDate = str(regyear) + '-' + str(regmonth)
            end_date = datetime.datetime.strptime(regDate, '%Y-%m')
            car_age = rrule.rrule(rrule.MONTHLY, dtstart=end_date, until=start_date).count()
            mile = "0.1" if car_age == 0 else str(round((2 / 12 * car_age), 2))
            mile = mile.replace('.0', '')
            # # 最小上牌年的上牌月 取1月和12月
            # if regyear == min_reg_year:
            #     month = [1, 12]
            # else:
            #     # 最大上牌年
            #     if regyear == max_reg_year:
            #         # 如果最大上牌年是今年
            #         if regyear == nowyear:
            #             # 如果当前月是12月 取上牌月为 1月和12月
            #             if nowmonth == 12:
            #                 month = [1, 12]
            #             # 如果当前月不是12月 则取上牌月为 1月和当前月+1
            #             else:
            #                 month = [1, nowmonth + 1]
            #         # 如果最大上牌年不是今年 取上牌月为 1月和12月
            #         else:
            #             month = [1, 12]
            #     # 非最大和最小上牌年 取上牌月为12月
            #     else:
            #         month = [12]

            url = f'https://m.che300.com/estimate/result/3/3/{brand_id}/{family_id}/{vehicle_id}/{regDate}/{mile}/1/null/{min_reg_year}/{max_reg_year}'
            # r.rpush('che300_gz:start_urls', url)
            start_urls.append(url)
shuffle(start_urls)
r.rpush('che300_gz:start_urls', *list(set(start_urls)))
