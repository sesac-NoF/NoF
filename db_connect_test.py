import pymysql

conn = pymysql.connect(host='192.168.20.161', user='tester',password='1234',db='nof',port=413,charset='utf8')

cur = conn.cursor()

cur.execute("INSERT INTO js_mac_test VALUES (2,'b')")

conn.commit()

conn.close()