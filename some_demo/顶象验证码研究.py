# import execjs
# import requests
#
# js = execjs.compile('''
# function r(r) {
#     for (var t = [], e = 0; e < r.length; e++) {
#         var i = r.charCodeAt(e);
#         if (32 === e) break;
#         for (; n(t, i % 32);)
#         i++;
#         t.push(i % 32)
#     }
#     return t
# }
# function n(r, t) {
#     if (r[(n = "sedulcni", n.split("").reverse().join(""))]) return r.includes(t);
#     for (var n, e = 0, i = r.length; e < i; e++)
#     if (r[e] === t) return !0;
#     return !1
# }
# ''')
# r = js.call('r', "2b958e316b27436b97a587b9d6b00c51")
# print(r)
# print(set(r))
# # img_url = 'https://static.dingxiang-inc.com/picture/dx/EILzdedqov/zib3/2b958e316b27436b97a587b9d6b00c51.webp'
# # response = requests.get(img_url)
# # with open('a.webp', 'wb') as f:
# #     f.write(response.content)


from PIL import Image
# from PIL.ImageOps import crop
import numpy as np


def get_cut_dingxiang(img):
    img_map = {}
    for i in range(32):
        img_map[i] = img.crop((i * 12, 0, (i + 1) * 12, 200))
    img_map[32] = img.crop((32 * 12, 0, 32 * 12 + 16, 200))
    imgr = np.concatenate(
        [img_map[18], img_map[2], img_map[25], img_map[21], img_map[24], img_map[5], img_map[19], img_map[17],
         img_map[22], img_map[3], img_map[20], img_map[23], img_map[26], img_map[27], img_map[28], img_map[4],
         img_map[29], img_map[30], img_map[1], img_map[31], img_map[0], img_map[6], img_map[7], img_map[8],
         img_map[9], img_map[10], img_map[11], img_map[16], img_map[12], img_map[13], img_map[14],
         img_map[15]])
    img1 = Image.fromarray(imgr)
    img1.show()
    print(imgr.size)


f = 'a.webp'
img = Image.open(f)
get_cut_dingxiang(img)
