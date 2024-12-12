import pymysql

conn = pymysql.connect(host='localhost', port=3305, 
                       user='root', 
                       password='root', 
                       db='issue', 
                       charset='utf8')

cur = conn.cursor()

cur.execute("INSERT INTO keyword (`word`, `site`, `rank`, `time`) VALUES ('test', 'zum', 1, '2024-12-11 20:00:00')")

conn.commit()

conn.close()