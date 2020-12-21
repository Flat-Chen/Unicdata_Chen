# %%

import pyautogui as pag
import matplotlib.pyplot as plt
import os
import time
import pyautogui as pag

i = 0
xs, ys = [], []
while i < 400:
    x, y = pag.position()  # 获取当前鼠标的位置
    xs.append(x)
    ys.append(y)
    time.sleep(0.005)
    print(x, y, time)
    i = i + 1

plt.xlabel('x')
plt.ylabel('y')
plt.title('the mouse log')
# plt.plot(xs,ys) #轨迹图
plt.scatter(xs, ys)  # 散点图
# plt.hist(xs) #直方图
plt.show()
