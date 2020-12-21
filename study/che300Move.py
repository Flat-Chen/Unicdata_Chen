import random
import time

from selenium.webdriver import ActionChains


def move(self, distance):
    btn = self.driver.find_element_by_id("dx_captcha_basic_slider_1")
    mouse_action = ActionChains(self.driver).click_and_hold(btn)
#         # 因此要将滑块移动至指定位置，最多需要执行move_steps步
#         move_steps = int(offset/4)
#         for i in range(0, move_steps):
#             # 路程前半部分速度较快
#             if i < int(move_steps/2):
#                 # sleep(random.randint(1, 10) / 500)#
#                 # 滑块每次向右移动四个像素，鼠标Y坐标在上下5个像素内随机摆动
#                 mouse_action.move_by_offset(4, random.randint(-5, 5)).perform()
#             else:
#                 # 在路程的后半段，越接近终点速度越慢
#                 # 每次移动之前sleep一段时间，时间为总距离与已移动距离方差的倒数
#                 seed = 90.0/(pow(move_steps, 2) - pow(i, 2))
# #                 time.sleep(seed)
#                 mouse_action.move_by_offset(4, random.randint(-5, 5)).perform()

#             mouse_action = ActionChains(self.driver).click_and_hold(btn)
#         # 到达终点时，左右摆动，假装做调整。
#         #sleep(0.1)
#         #mouse_action.move_by_offset(5, random.randint(-5, 5)).perform()
#         #sleep(0.2)
#         mouse_action.move_by_offset(-6, random.randint(2,5)).perform()
#         time.sleep(0.5)
#         # 松开鼠标
#         mouse_action.release().perform()
    while distance > 0:
        if distance > 10:
            # 如果距离大于10，就让他移动快一点
            span = random.randint(5, 8)
        else:
            # 快到缺口了，就移动慢一点
            span = random.randint(2, 3)
        mouse_action.move_by_offset(span, 0).perform()
        distance -= span
        time.sleep(random.randint(1))

    time.sleep(3)
    if '验证成功' in self.driver.page_source:
        print('验证成功')
        return 1
    else:
        print('再接再厉吧!')
        return 0
