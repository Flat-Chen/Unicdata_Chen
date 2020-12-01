import pymongo
import datetime
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

redis_url = 'redis://192.168.2.149:6379/8'
r = Redis.from_url(redis_url, decode_responses=True)
for cars in tqdm(result_list):
    brand_id = cars['brand_id']
    family_id = cars['family_id']
    vehicle_id = cars['vehicle_id']
    min_reg_year = int(cars['min_reg_year'])
    max_reg_year = int(cars['max_reg_year'])
    for regyear in range(min_reg_year, max_reg_year + 1):
        if regyear == nowyear:
            regmonth = nowmonth - 1
            regdate = str(regyear) + '-' + str(regmonth)
            mile = 0.1
        else:
            regmonth = nowmonth
            regdate = str(regyear) + '-' + str(regmonth)
            mile = (nowyear - regyear) * 2
        url = f'https://m.che300.com/estimate/result/3/3/{brand_id}/{family_id}/{vehicle_id}/{regdate}/{mile}/1/null/{min_reg_year}/{max_reg_year}'
        r.rpush('che300_gz:start_urls', url)
