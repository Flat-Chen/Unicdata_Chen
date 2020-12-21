import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')

driver = Chrome(options=chrome_options)

with open('stealth.min.js') as f:
    js = f.read()

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": js
})
driver.get('https://www.che300.com/forbidden/partner_index?pd=87a38998227cbbc23dcad51cd7f76ab2&r_u=%2Fpartner%2Fresult.php%3Fprov%3D22%26city%3D22%26brand%3D30%26series%3D386%26model%3D21359%26registerDate%3D2014-1%26mileAge%3D13.17%26intention%3D0%26partnerId%3Ddouyin%26unit%3D1%26sn%3D93a15125acc736ab66bb791a1e37ae1a%26sld%3Dcd%2F')
time.sleep(500)
# driver.save_screenshot('walkaround.png')

# 你可以保存源代码为 html 再双击打开，查看完整结果
# source = driver.page_source
# with open('result.html', 'w') as f:
#     f.write(source)
