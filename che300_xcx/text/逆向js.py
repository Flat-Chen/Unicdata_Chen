import requests
import json
import execjs
import os
from PIL import Image
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class HuanYuan_Photo:
    def __init__(self):
        self.get_yzm_url = 'https://cap.dingxiang-inc.com/api/a?w=300&h=150&s=50&ak=e0a73ec57a9f469dcce9b3b5da97648b&c=5fec4785XaYM7X4g2WLXrK761Nx15VNm6M563Eq1&jsv=1.4.5.1&aid=dx-1609923598391-43833125-1&wp=1&de=0&uid=&lf=0&tpc=&t=EA640969210A5346AFB82BA563C16FE8DBFEFB5F053539636AC6ED8CAD43DB198E85EE4C5D761AF3409633F4592D0C541878F2D8AF3480C0CA76A57E5276A6CA3061250D2A39731868BEF47CB3C7694F'

    def get_photo(self):
        response = requests.get(self.get_yzm_url)
        json_data = json.loads(response.text)
        # p1：有缺口的背景图  p2：缺口图  p3；无缺口原图
        p1_url = 'https://static.dingxiang-inc.com/picture' + json_data['p1']
        p1_name = json_data['p1'].split('/')[-1].split('.')[0]
        response = requests.get(p1_url)
        p1_img = './dx_img/' + str(count) + '-' + json_data['p1'].split('/')[-1].split('.')[0] + '.jpg'
        with open(p1_img, 'wb') as f:
            f.write(response.content)
        f.close()

        p2_url = 'https://static.dingxiang-inc.com/picture' + json_data['p2']
        response = requests.get(p2_url)
        p2_img = './dx_img/' + str(count) + '-' + json_data['p2'].split('/')[-1].split('.')[0] + '.jpg'
        with open(p2_img, 'wb') as f:
            f.write(response.content)
        f.close()

        p3_url = 'https://static.dingxiang-inc.com/picture' + json_data['p3']
        p3_name = json_data['p3'].split('/')[-1].split('.')[0]
        response = requests.get(p3_url)
        p3_img = './dx_img/' + str(count) + '-' + json_data['p3'].split('/')[-1].split('.')[0] + '.jpg'
        with open(p3_img, 'wb') as f:
            f.write(response.content)
        f.close()
        return p1_name, p3_name

    def huanyuan(self, photo_name):
        js = execjs.compile('''
        function r(r) {
              for (var t = [
              ], e = 0; e < r.length; e++) {
                var i = r.charCodeAt(e);
                if (32 === e) break;
                for (; n(t, i % 32); ) i++;
                t.push(i % 32)
              }
              return t
            }
        function n(r, t) {
              if (r[(n = 'sedulcni', n.split('').reverse().join(''))]) return r.includes(t);
              for (var n, e = 0, i = r.length; e < i; e++) if (r[e] === t) return !0;
              return !1
            }
            ''')
        r = js.call('r', photo_name)
        return r

    def get_yuantu(self, photo_name):
        # 获取还原顺序
        huanyuan_list = self.huanyuan(photo_name)
        # 切割
        img = Image.open('./dx_img/' + str(count) + '-' + photo_name + '.jpg')
        for i in range(32):
            a = 12 * i  # 图片距离左边的大小
            b = 0  # 图片距离上边的大小
            c = 12 * (i + 1)  # 图片距离左边的大小 + 图片自身宽度
            d = 200  # 图片距离上边的大小 + 图片自身高度
            croping = img.crop((a, b, c, d))
            croping.save('./dx_img/ge' + str(i) + '.jpg')
        croping = img.crop((384, 0, 400, 200))
        croping.save('./dx_img/ge32.jpg')

        # 还原拼接
        target = Image.new('RGB', (400, 200))  # 拼接前需要写拼接完成后的图片大小 1200*600
        c = 0
        for i in huanyuan_list:
            pj_img = Image.open('./dx_img/ge' + str(i) + '.jpg')
            a = c  # 图片距离左边的大小
            b = 0  # 图片距离上边的大小
            c = a + 12  # 图片距离左边的大小 + 图片自身宽度
            d = 200  # 图片距离上边的大小 + 图片自身高度
            target.paste(pj_img, (a, b, c, d))
            os.remove('./dx_img/ge' + str(i) + '.jpg')
        last_img = Image.open('./dx_img/ge32.jpg')
        target.paste(last_img, (384, 0, 400, 200))
        os.remove('./dx_img/ge32.jpg')
        target.save(f'./dx_img/{count}-{photo_name}.jpg')


if __name__ == '__main__':
    count = 10
    huanyuan = HuanYuan_Photo()
    for i in range(10):
        p1_name, p3_name = huanyuan.get_photo()
        for j in [p1_name, p3_name]:
            huanyuan.get_yuantu(j)
        count += 1
