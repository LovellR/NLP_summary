import pymysql

conn = pymysql.connect(host='localhost', port=3305, 
                       user='root', 
                       password='root', 
                       db='issue', 
                       charset='utf8')

cur = conn.cursor()

cur.execute("INSERT INTO summary (`idnews`, `summary`) VALUES (1, 'test ')")

conn.commit()

conn.close()