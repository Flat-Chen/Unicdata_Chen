__author__ = 'cagey'

import pymysql
import pandas as pd
import numpy as np
from datetime import datetime
import time
from sqlalchemy import create_engine

settings = {
    "MYSQL_USER": "dataUser94",
    "MYSQL_PWD": "94dataUser@2020",
    "MYSQL_SERVER": "192.168.1.94",
    "MYSQL_PORT": "3306",
    "MYSQL_DB": "huachen",
    "MYSQL_TABLE": "content_senti",
}


def readMysql(tablename):
    dbconn = pymysql.connect(
        host="192.168.1.94",
        database='shangqi',
        user="dataUser94",
        password="94dataUser@2020",
        port=3306,
        charset='utf8')
    # 查询
    sqlcmd = "select * from " + tablename
    df = pd.read_sql(sqlcmd, dbconn)
    return df


conn = create_engine(
    f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')
pd.set_option('display.max_columns', None)


def replace_brand(x):
    x = x.replace("集团", "乘用车")
    if "上汽通用" in x:
        x = "上汽通用"
    return x


table_list = ["a12345auto", "a315tousu", "qctsw", "tousu315che"]
for table in table_list:
    df_tmp = readMysql(table)
    df_current_month = df_tmp[df_tmp["tousu_date"].str.contains(f"{datetime.now().year}-{datetime.now().month}")]
    df_not_yq = df_current_month[df_current_month["brand"].dropna().str.contains("一汽") == False]
    df_not_yq["brand"] = df_not_yq["brand"].apply(lambda x: replace_brand(x))
    df = df_not_yq.loc[:, ["csName", "brand", "series", "dataSource", "detail_url", "introduct", "tousu_date"]]
    df.rename(columns={'csName': '厂商', 'brand': '品牌', 'series': '车系', 'dataSource': "网站", "detail_url": "链接",
                       "introduct": "投诉内容", "tousu_date": "投诉时间"}, inplace=True)
    df.to_csv(f"/Users/cagey/Downloads/{table}.csv")
