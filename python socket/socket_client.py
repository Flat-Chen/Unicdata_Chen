import requests
from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.chrome.options import Options

# from socket import *
#
# HOST = '127.0.0.1'  # or 'localhost'
# PORT = 21567
# BUFSIZ = 1024
# ADDR = (HOST, PORT)
#
# tcpCliSock = socket(AF_INET, SOCK_STREAM)
# tcpCliSock.connect(ADDR)
# while True:
#     data1 = input('>')
#     # data = str(data)
#     if not data1:
#         break
#     tcpCliSock.send(data1.encode())
#     data1 = tcpCliSock.recv(BUFSIZ)
#     if not data1:
#         break
#     print(data1.decode('utf-8'))
# tcpCliSock.close()
def start_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # ip = getProxy()
    # ip = '81.68.214.148:16128'
    chrome_options.add_argument('--proxy-server=192.168.1.92:8100')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                                ' (KHTML, like Gecko)Chrome/86.0.4240.198 Safari/537.36')

    driver = Chrome(options=chrome_options)
    driver.get('http://www.baidu.com')
    return driver


driver = start_driver()
# url = 'http://www.baidu.com'
# response = requests.get(url=url, proxies={'http': '192.168.1.92:8100'})
# print(response.text)
