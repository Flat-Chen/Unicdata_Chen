# RandomProxy


Capture a large number of proxy IP from the Internet, and then through the agent cascade to achieve random forwarding traffic. Compatible with most support HTTP / HTTPS proxy procedures, such as Sqlmap, Burpsuite, FireFox, you can also run on Linux, Windows, MacOS.

Install 
```
git clone https://github.com/UUUUnotfound/Randomproxy.git
cd Randomproxy/
#install random_proxy dependency
pip install request tornado pycurl
#install IPProxyPool dependency

#### Ubuntu,debian
# Install sqlite and python-lxml:
apt-get install sqlite3 python-lxml
# Install requests,chardet,web.py,gevent psutil:
pip install requests chardet web.py sqlalchemy gevent psutil

#### Windows
# Download[sqlite](http://www.sqlite.org/download.html),and add it to Path
# Install requests,chardet,web.py,gevent:
pip install requests chardet web.py sqlalchemy gevent
# Install lxml:
pip install lxml
# Or [lxml windows](https://pypi.python.org/pypi/lxml/)
```
Usage
```
Usage: python random_proxy.py [-H 127.0.0.1] [-p 8888] [-c 0] [-a http://127.0.0.1:8000] [-t 0] [-p 2]

Options:
  -h, --help            show this help message and exit
  -H HOST_IP, --host=HOST_IP
                        [RandomProxy] The RandomProxy listen host_ip; default
                        127.0.0.1
  -p HOST_PORT, --port=HOST_PORT
                        [RandomProxy] The RandomProxy listen host_port;
                        default 8888
  -c CHANGE, --change=CHANGE
                        [RandomProxy] Default (0); (0): every request has a
                        new IP; (60): Change IP every 60 seconds  ;  (less
                        than 0): curl http://127.0.0.1:8888/next to change IP
  -a ADDRESS, --address=ADDRESS
                        [IPProxyPool] The IPProxyPool api url;default
                        http://127.0.0.1:8000
  -t TYPE, --type=TYPE  [IPProxyPool] Default (0): high anonymous, (1):
                        anonymous, (2) transparent
  -P PROTOCOL, --protocol=PROTOCOL
                        [IPProxyPool] HTTP/HTTPS proxy you want ? (0): http,
                        (1) https, (2) http/https(default)
```

Reference
```
qiyeboy/IPProxyPool: IPProxyPool代理池项目，提供代理ip
https://github.com/qiyeboy/IPProxyPool
rfyiamcool/toproxy: 😈 high performance simple tornado http proxy.
https://github.com/rfyiamcool/toproxy
```
PS
```
if something wrong on windows,
because that pycurl not support python2 64bit on windows.
you can install python2 32bit to solve it.
```
