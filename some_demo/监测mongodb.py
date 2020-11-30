import time

import pymongo

while 1:
    try:
        connection = pymongo.MongoClient('192.168.2.149', 27017)
        db = connection["crawlab"]
        collection = db["users"]
        result = collection.find()
        result_list = list(result)
        connection.close()
        print('mongo服务正常')
        time.sleep(10)
    except:
        print('mongo服务掉了')
        break
