import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('disable-infobars')
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--proxy-server=socks5://192.168.11.157:1080')
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')

driver = Chrome(options=chrome_options)

with open('stealth.min.js') as f:
    js = f.read()

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})
driver.get('https://2021.ip138.com/')
time.sleep(500)
