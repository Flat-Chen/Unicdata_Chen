import os.path
from fontTools.ttLib import TTFont

myfont1 = os.path.join(os.path.dirname(__file__), 'koubei_font1.ttf')
myfont2 = os.path.join(os.path.dirname(__file__), 'koubei_font2.ttf')


# 比较函数，用于对比两个字形列表的坐标信息是否相同
# （根据对字体文件的采样调研，认为只要x,y在一定的误差范围内就认为是相同的）
def comp(base_glyf, target_glyf):
    if len(base_glyf) != len(target_glyf):
        return 0
    else:
        mark = 1
        for i in range(len(base_glyf)):
            if abs(base_glyf[i][0] - target_glyf[i][0]) < 40 and abs(base_glyf[i][1] - target_glyf[i][1]) < 40:
                pass
            else:
                mark = 0
                break
        return mark


# myfont1 = os.path.join('/home/home/luntan/luntan', 'koubei_font1.ttf')
# myfont2 = os.path.join('/home/home/luntan/luntan', 'koubei_font2.ttf')

def get_map(target_font_file):
    font1 = TTFont(myfont1)
    # 手动确定一组编码和字符的正确对应关系
    uni_list = [
        'uniED90', 'uniECDD', 'uniED2E', 'uniEC7B', 'uniECCD', 'uniEC19', 'uniED5A', 'uniEDAC', 'uniECF8',
        'uniEC45', 'uniEC97', 'uniEDD7', 'uniEC35', 'uniED76', 'uniECC2', 'uniED14', 'uniEC61', 'uniEDA1',
        'uniEDF3', 'uniED40', 'uniED92', 'uniECDE', 'uniEC2B', 'uniEC7D', 'uniEDBD', 'uniED0A', 'uniED5C',
        'uniECA8', 'uniECFA', 'uniEC47', 'uniED87', 'uniEDD9', 'uniED26', 'uniEC72', 'uniECC4', 'uniEE05',
        'uniEC63', 'uniEDA3', 'uniECF0', 'uniED42', 'uniEC8E', 'uniEDCF', 'uniEC2D', 'uniED6D', 'uniEDBF',
        'uniED0C', 'uniEC58', 'uniECAA', 'uniEDEB', 'uniED37', 'uniED89', 'uniECD6', 'uniED27', 'uniEC74',
        'uniEDB5', 'uniEE06', 'uniED53', 'uniECA0', 'uniECF1', 'uniEC3E', 'uniEC90', 'uniEDD0', 'uniED1D',
        'uniED6F', 'uniECBB', 'uniEDFC', 'uniEC5A', 'uniED9A', 'uniEDEC', 'uniED39', 'uniEC85', 'uniECD7',
        'uniEC24', 'uniED64', 'uniEDB6', 'uniED03', 'uniED55', 'uniECA1', 'uniEDE2', 'uniEC40', 'uniED80',
        'uniED1F', 'uniEC6B', 'uniECBD', 'uniEDFE', 'uniED4A', 'uniED9C', 'uniECE9', 'uniEC87', 'uniEDC8',
    ]
    words = '和远七路好只量九电短矮动排上雨地硬控自保机二门了八低的冷是副音无更级右皮比手盘长泥有坏很实内里过一孩加五四启十高灯问呢三空左身来少中公性近档坐着不多得大开味响油小软养外耗光下当六真'
    words_list = list(words)

    font2 = TTFont(target_font_file)
    base_glyf_coordinates = []  # 存储xx个字符的坐标信息
    for uni in uni_list:
        cdts = font1['glyf'][uni].coordinates
        base_glyf_coordinates.append(list(cdts))

    target_glyf_coordinates = []
    uni_list2 = font2.getGlyphOrder()[1:]
    for uni in uni_list2:
        cdts = font2['glyf'][uni].coordinates
        target_glyf_coordinates.append(list(cdts))

    font_map = {}
    for i, tgc in enumerate(target_glyf_coordinates):
        for j, bgc in enumerate(base_glyf_coordinates):
            if comp(tgc, bgc):
                font_map[uni_list2[i]] = words_list[j]
    return font_map


if __name__ == "__main__":
    print(get_map(myfont2))
