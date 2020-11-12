# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

user = "admin"
passwd = "admin"

def openweb():
    url_login = "http://192.168.1.1/userLogin.asp"
    # url_home = "http://192.168.1.1/home.asp"
    url_run = "http://192.168.1.1/maintain_running.asp"

    # driver = webdriver.PhantomJS(r"D:\software\anaconda\Scripts\phantomjs.exe")
    # driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    driver = webdriver.Firefox()    # 这里好像只有火狐才可以，另外两个浏览器失败了

    driver.get(url_login)
    # print "start login"
    driver.find_element_by_xpath('//div[@align="left"]/input[@name="account"]').send_keys(user)         # 输入用户名
    driver.find_element_by_xpath('//div[@align="left"]/input[@name="password"]').send_keys(passwd)      # 输入密码
    # driver.save_screenshot("a.png")   # 截个图看一下

    ###############    正常情况应该不需要使用验证码  ###################
    # try:
    #     vldcode = driver.find_element_by_xpath('//div[@align="left"]/input[@name="vldcode"]')
    #     print "$$$$$$$$$$$$$$$$$$$$$$$$"
    #     # yanzheng = ""
    #     yanzhengma = input()
    #     vldcode.send_keys(yanzhengma)
    # except:
    #     print u"验证码输入异常"
    ###############    如果需要输入验证码，就使用这里的代码  ###################

    # print driver.current_url
    # time.sleep(10)

    # ac = driver.find_element_by_xpath('//span/input[@class="button"]')
    # ActionChains(driver).move_to_element(ac).click(ac).perform()          # 单击，没用？
    # driver.find_element_by_xpath('//div[@class="da_width"]//span[3]').find_element_by_xpath('input').click()
    # try:
    #     driver.find_element_by_xpath('//div[@align="left"]/img[@id="vldimp"]')
    #     print u"登陆异常，稍后重新登陆..."
    #     driver.quit()
    #     time.sleep(100)
    #     openweb()
    # except:
    #     pass

    driver.find_element_by_xpath('//div[@align="left"]/input[@name="password"]').send_keys(Keys.RETURN)     # 单击没用就用回车登陆
    # print u"登陆成功！"

    # while userflag:
    #     try:
    #         txt = driver.find_element_by_xpath('//div[@class="da_width"]/div[@id="dl_margin"]//span[@id="messages"]').text
    #         if txt==u'当前已有5个用户登录，请稍后再试！':
    #             print u"用户超限，两分钟后重新打开"
    #             driver.quit()
    #             time.sleep(120)
    #             openweb()
    #     except:
    #         userflag = 0

    time.sleep(0.5)
    driver.get(url_run)             # 运行详情页

    userflag = 1        # 判断是否用户超限，每次只能有五个用户登录，五分钟后自动退出
    while userflag:
            resurl = driver.current_url
            if resurl==url_login:                       # url依旧是登录的页面，说明用户超限了
                print(u"用户超限，两分钟后重新打开")
                driver.quit()
                time.sleep(120)
                openweb()
            else:
                print(u"登陆成功！")
                userflag = 0

    # print driver.current_url

    # driver.save_screenshot("c.png")
    # print "c end"
    flag = 1
    while flag:
        oldip = driver.find_element_by_xpath('//div[@id="wan_info"]/table//tr[4]//td[3]').text          # 记录ip，确保拨号之后ip改变了

        driver.find_element_by_xpath('//div[@id="wan_info"]/table//tr[2]//tr//td[3]/input').click()     # 释放按钮
        print(u"正在释放...")
        time.sleep(5)
        driver.find_element_by_xpath('//div[@id="wan_info"]/table//tr[2]//tr//td[3]/input').click()     # 5秒后点击连接按钮，不能太快
        print(u"重新连接...")

        time.sleep(5)
        driver.get(url_run)     # 停留5秒然后刷新页面
        newip = driver.find_element_by_xpath('//div[@id="wan_info"]/table//tr[4]//td[3]').text          # 获得新的ip

        if oldip == newip:                      # 检查新的ip和之前的ip是否一样，如果一样说明经过释放和重连之后ip没有改变，那么就再次拨号
            print(u"ip更换失败，再次释放")
            # flag = 1
        else:
            flag = 0

    # driver.find_element_by_xpath('//div[@class="da_width"]//span[3]').find_element_by_xpath('input').click()

    # ActionChains(driver).move_to_element(ac).double_click(ac).perform()
    # ActionChains(driver).move_to_element(ac).click_and_hold(ac).perform()

    # driver.close()
    # driver.get(url_home)

    # driver.save_screenshot("b.png")
    # print "b end"
    # driver.switch_to.frame("menu_admin")
    # driver.switch_to.frame("menu_admin")
    # print driver.find_element_by_xpath('//li')

    # print driver.find_element_by_xpath('//frameset//frame[@name="menu_admin"]')
    # print driver.switch_to.frame("banner").text
    # driver.find_element_by_xpath(u'//li[2]').click()

    # driver.save_screenshot("d.png")
    # print "d end"
    driver.quit()       # 要确保浏览器可以正常退出
    # time.sleep(10)

def click():
    openweb()

def main():
    print("start")
    click()
    print("----------")

if __name__=="__main__":
    main()

