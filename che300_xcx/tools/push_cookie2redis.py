from redis import Redis
from tqdm import tqdm

redis_cli = Redis(host="192.168.1.248", port=6379, db=3)
with open('../che300_cookies.txt', 'r') as f:
    lines = f.readlines()
    for line in tqdm(lines):
        if line != '\n':
            redis_cli.sadd("che300_xcx_cookie", line)
