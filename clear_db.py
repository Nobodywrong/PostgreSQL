import psycopg2

conn = psycopg2.connect(
    dbname='db_name',
    user='db_user',
    password='db_passwd',
    host='db_host')

print("Database opened successfully")

cursor = conn.cursor()

cursor.execute('select to_timestamp((select min(begin_time) from detector.tracker)/1000), to_timestamp((select max(begin_time) from detector.tracker)/1000);')
records = cursor.fetchall()
for row in records:
    print("detector.tracker early=", row[0])
    print("detector.tracker late =", row[1])

cursor.execute('select to_timestamp((select min(object_time) from detector.objects)/1000), to_timestamp((select max(object_time) from detector.objects)/1000);')
records = cursor.fetchall()
for row in records:
    print("detector.objects early=", row[0])
    print("detector.objects late =", row[1])

cursor.execute('select to_timestamp((select min(object_time) from auto.car_objects)/1000), to_timestamp((select max(object_time) from auto.car_objects)/1000);')
records = cursor.fetchall()
for row in records:
    print("auto.car_objects early=", row[0])
    print("auto.car_objects late =", row[1])

print("Operation done successfully")

print(type(cursor.execute))

mark_1 = str(input("Replacing the time for detector.tracker. Example - 2022-06-01\n"))
mark_2 = str(input('Replacing the time for detector.objects. Example - 2022-06-01\n'))
mark_3 = str(input("Replacing the time for auto.car_objects. Example - 2022-06-01\n"))

sql=(f"delete from detector.tracker where begin_time < (extract(epoch from '{str(mark_1)}'::timestamp) * 1000);" )
cursor.execute(sql)

sql2=(f"delete from detector.objects where object_time < (extract(epoch from '{str(mark_2)}'::timestamp) * 1000);" )
cursor.execute(sql2)

sql3=(f"delete from detector.objects where object_time < (extract(epoch from '{str(mark_3)}'::timestamp) * 1000);" )
cursor.execute(sql3)

conn.commit()

print("Deletion successful")

cursor.close()
conn.close()




