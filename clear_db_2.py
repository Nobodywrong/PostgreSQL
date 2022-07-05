#!/usr/bin/python
"""
Clear OLD DATABASE
"""
import psycopg2
import datetime
import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

clear_delta = 14  # days for delete
month_mls = (86400*clear_delta)*1000
mess = "None" #return if there is no object class

def get_session(
    *,
    host: str,
    user: str,
    pwd: str,
    port: int,
    name: str
):
    engine = create_engine(
        'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user, pwd, host, port, name),
        connect_args={
            "application_name": 'cleaner'
        }
    )
    session = sessionmaker(bind=engine)
    # TODO: scoped_session?
    return session()

def clear_func(
    *,
    host: str,
    user: str,
    pwd: str,
    port: int,
    name: str
):
    conn = get_session(
        host=host,
        user=user,
        name=name,
        pwd=pwd,
        port=port
    )

    rows = conn.execute('select id_camera, min(object_time), max(object_time) from detector.objects group by id_camera').all()

    if len(rows) > 0:
        sql_string = "delete from detector.objects where "
        for row in rows:
            print(row)
            last_element = row[2]
            first_element = row[1]
            print(f"ID_CAMERA: {row[0]}; FIRST BBOX: {datetime.datetime.fromtimestamp(first_element/1000)}; LAST BBOX: {datetime.datetime.fromtimestamp(last_element/1000)}")
            if (last_element-first_element) > month_mls:
                if sql_string.endswith(")"):
                    sql_string += " or "
                sql_string += f"(id_camera = {row[0]} and object_time <= {last_element-month_mls})"

    print(sql_string)

    if not sql_string.endswith("where "):
        sql_string += ";"
        conn.execute(sql_string)

    conn.commit()

    print("Deletion successful")

    rows = conn.execute('select id_camera, min(begin_time), max(begin_time) from detector.tracker group by id_camera').all()

    if len(rows) > 0:
        sql_string = "delete from detector.tracker where "
        for row in rows:
            last_element = row[2]
            first_element = row[1]
            print(f"ID_CAMERA: {row[0]}; FIRST BBOX: {datetime.datetime.fromtimestamp(first_element/1000)}; LAST BBOX: {datetime.datetime.fromtimestamp(last_element/1000)}")
            if (last_element-first_element) > month_mls:
                if sql_string.endswith(")"):
                    sql_string += " or "
                sql_string += f"(id_camera = {row[0]} and begin_time <= {last_element-month_mls})"

    print(sql_string)

    if not sql_string.endswith("where "):
        sql_string += ";"
        conn.execute(sql_string)

    conn.commit()

    print("Deletion successful")

    rows = conn.execute('select to_timestamp((select min(object_time) from auto.car_objects)/1000), to_timestamp((select max(object_time) from auto.car_objects)/1000);').all()

    if len(rows) > 0:
        sql_string = "delete from auto.car_objects where "
        for row in rows:
            print(row)
            last_element = row[2]
            first_element = row[1]
            print(f"ID_CAMERA: {row[0]}; FIRST BBOX: {datetime.datetime.fromtimestamp(first_element / 1000)}; LAST BBOX: {datetime.datetime.fromtimestamp(last_element / 1000)}")
            if (last_element - first_element) > month_mls:
                if sql_string.endswith(")"):
                    sql_string += " or "
                sql_string += f"(id_camera = {row[0]} and object_time <= {last_element - month_mls})"

    print(sql_string)

    if not sql_string.endswith("where "):
        sql_string += ";"
        conn.execute(sql_string)


    conn.commit()

    print("Deletion successful")

    conn.close()

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()

    my_parser.add_argument('--host',
                           help='Specify the host address')
    my_parser.add_argument('--user',
                           help='Specify the database user')
    my_parser.add_argument('--pwd',
                           help='Specify the database password')
    my_parser.add_argument('--port',
                           help='Specify the database port')
    my_parser.add_argument('--database',
                           help='Specify the database name')
    args = my_parser.parse_args()

    clear_func(host=args.host, user=args.user, pwd=args.pwd, port=args.port, name=args.database)