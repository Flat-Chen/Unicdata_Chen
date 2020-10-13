import os

from fontTools.ttLib import TTFont


def comp(l1, l2):  # 定义一个比较函数，比较两个列表的坐标信息是否相同
    if len(l1) != len(l2):
        return False
    else:
        mark = 1
        for i in range(len(l1)):
            if abs(l1[i][0] - l2[i][0]) < 40 and abs(l1[i][1] - l2[i][1]) < 40:
                pass
            else:
                mark = 0
                break
        return mark


def get_be_p1_list():
    # 手动确定一组编码和字符的对应关系
    # print(os.listdir())
    u_list = ['uniEDA9', 'uniEDFB', 'uniED47', 'uniED99', 'uniECE6', 'uniEC32', 'uniEC84', 'uniEDC5', 'uniED11',
              'uniED63',
              'uniECB0', 'uniED01', 'uniEC4E', 'uniED8F', 'uniEDE0', 'uniED2D', 'uniEC7A', 'uniECCB', 'uniEC18',
              'uniEC6A',
              'uniEDAA', 'uniECF7', 'uniED49', 'uniEC95', 'uniEDD6', 'uniEC34', 'uniED74', 'uniEDC6', 'uniED13',
              'uniEC5F',
              'uniECB1', 'uniEDF2', 'uniED3E', 'uniED90', 'uniECDD', 'uniED2F', 'uniEC7B', 'uniEDBC']

    # font1 = TTFont('text.ttf')
    # window
    font1 = TTFont('./luntan/text.ttf')
    # linux
    # font1 = TTFont('/home/home/mywork/font/luntan/text.ttf')

    be_p1 = []  # 保存38个字符的（x,y）信息
    for uni in u_list:
        p1 = []  # 保存一个字符的(x,y)信息
        p = font1['glyf'][uni].coordinates  # 获取对象的x,y信息，返回的是一个GlyphCoordinates对象，可以当作列表操作，每个元素是（x,y）元组
        # p=font1['glyf'][i].flags #获取0、1值，实际用不到
        for f in p:  # 把GlyphCoordinates对象改成一个列表
            p1.append(f)
        be_p1.append(p1)
    return be_p1

def get_map_yuqing(be_p1, word_list):
    # window
    font2 = TTFont('./luntan/text_yuqing.ttf')
    # linux
    # font2 = TTFont('/home/home/mywork/font/luntan/text_yuqing.ttf')

    uni_list2 = font2.getGlyphOrder()[1:]
    on_p1 = []
    for i in uni_list2:
        pp1 = []
        p = font2['glyf'][i].coordinates
        for f in p:
            pp1.append(f)
        on_p1.append(pp1)
    n2 = 0
    x_list = []
    for d in on_p1:
        n2 += 1
        n1 = 0
        for a in be_p1:
            n1 += 1
            if comp(a, d):
                # print(uni_list2[n2 - 1], word_list[n1 - 1])
                x_list.append({"key": uni_list2[n2 - 1], "value": word_list[n1 - 1]})
    # print(x_list)
    return x_list
# print(be_p1)
def get_map(be_p1, word_list):
    # font2 = TTFont('text1.ttf')
    # window
    # font2 = TTFont('./luntan/text1.ttf')
    # linux
    font2 = TTFont('/home/home/mywork/font/luntan/text2.ttf')

    uni_list2 = font2.getGlyphOrder()[1:]
    on_p1 = []
    for i in uni_list2:
        pp1 = []
        p = font2['glyf'][i].coordinates
        for f in p:
            pp1.append(f)
        on_p1.append(pp1)
    n2 = 0
    x_list = []
    for d in on_p1:
        n2 += 1
        n1 = 0
        for a in be_p1:
            n1 += 1
            if comp(a, d):
                # print(uni_list2[n2 - 1], word_list[n1 - 1])
                x_list.append({"key": uni_list2[n2 - 1], "value": word_list[n1 - 1]})
    # print(x_list)
    return x_list


def get_map1(be_p1, word_list):
    # font2 = TTFont('text1.ttf')
    # window
    font2 = TTFont('./luntan/text_dazhong1.ttf')
    # linux
    # font2 = TTFont('/home/home/mywork/font/luntan/text_dazhong1.ttf')

    uni_list2 = font2.getGlyphOrder()[1:]
    on_p1 = []
    for i in uni_list2:
        pp1 = []
        p = font2['glyf'][i].coordinates
        for f in p:
            pp1.append(f)
        on_p1.append(pp1)
    n2 = 0
    x_list = []
    for d in on_p1:
        n2 += 1
        n1 = 0
        for a in be_p1:
            n1 += 1
            if comp(a, d):
                # print(uni_list2[n2 - 1], word_list[n1 - 1])
                x_list.append({"key": uni_list2[n2 - 1], "value": word_list[n1 - 1]})
    # print(x_list)
    return x_list


def get_map2(be_p1, word_list):
    # font2 = TTFont('text1.ttf')
    # window
    # font2 = TTFont('./luntan/text_dazhong1.ttf')
    # linux
    font2 = TTFont('/home/home/mywork/font/luntan/text_dazhong2.ttf')

    uni_list2 = font2.getGlyphOrder()[1:]
    on_p1 = []
    for i in uni_list2:
        pp1 = []
        p = font2['glyf'][i].coordinates
        for f in p:
            pp1.append(f)
        on_p1.append(pp1)
    n2 = 0
    x_list = []
    for d in on_p1:
        n2 += 1
        n1 = 0
        for a in be_p1:
            n1 += 1
            if comp(a, d):
                # print(uni_list2[n2 - 1], word_list[n1 - 1])
                x_list.append({"key": uni_list2[n2 - 1], "value": word_list[n1 - 1]})
    # print(x_list)
    return x_list


def get_map3(be_p1, word_list):
    # font2 = TTFont('text1.ttf')
    # window
    # font2 = TTFont('./luntan/text_dazhong1.ttf')
    # linux
    font2 = TTFont('/home/home/mywork/font/luntan/text_dazhong3.ttf')

    uni_list2 = font2.getGlyphOrder()[1:]
    on_p1 = []
    for i in uni_list2:
        pp1 = []
        p = font2['glyf'][i].coordinates
        for f in p:
            pp1.append(f)
        on_p1.append(pp1)
    n2 = 0
    x_list = []
    for d in on_p1:
        n2 += 1
        n1 = 0
        for a in be_p1:
            n1 += 1
            if comp(a, d):
                # print(uni_list2[n2 - 1], word_list[n1 - 1])
                x_list.append({"key": uni_list2[n2 - 1], "value": word_list[n1 - 1]})
    # print(x_list)
    return x_list


# 分行打印出来，方便和FontCreator中进行比较确认
# print(x_list[:16])
# print(x_list[16:32])
# print(x_list[-6:])
if __name__ == "__main__":
    word_list = ['呢', '近', '八', '着', '更', '短', '三', '少', '是', '大', '好', '上', '十', '低', '不', '的', '六', '很', '坏', '长',
                 '右',
                 '高', '四', '五', '一', '二', '了', '下', '左', '得', '多', '远', '七', '九', '地', '小', '和', '矮']
    be_p1 = get_be_p1_list()
    a = get_map(be_p1, word_list)
    print(a)
