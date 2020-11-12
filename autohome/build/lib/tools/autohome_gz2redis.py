__author__ = 'cagey'

import pymongo
import redis

settings = {
    'MONGODB_USER': 'admin',
    # 'MONGODB_PORT': 1206,
    'MONGODB_PORT': 27017,
    'MONGODB_DB': 'baogang',
    'MONGODB_COLLECTION': 'ouyeel_new',
    'MONGODB_PWD': 'ABCabc123',
    # 'MONGODB_SERVER': '180.167.80.118',
    'MONGODB_SERVER': '192.168.1.92',

}

# uri = f'mongodb://{settings["MONGODB_USER"]}:{settings["MONGODB_PWD"]}@{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'
# connection = pymongo.MongoClient(uri)
url_list = ['http://www.baidu.com']
# pool = redis.ConnectionPool(host='192.168.1.241', port=6379)
pool = redis.ConnectionPool(host='192.168.1.241', port=6379, db=15)
con = redis.Redis(connection_pool=pool)
c = con.client()
c.lpush('autohome_gz:start_urls', *url_list)
# p = c.lpop('autohome_gz:start_urls')
# p = bytes.decode(p)
# print(p)
# con.close()




