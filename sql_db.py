from urllib.parse import _ResultMixinStr
import mysql.connector
from mysql.connector import Error
import pandas as pd
import config as c


def make_query(conn_type, query):
    try:
        connection = mysql.connector.connect(host=c.sql_host,
                                             user=c.sql_user,
                                             password=c.sql_pwd,
                                             database=c.sql_db)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()

            if conn_type == 'df':
                res = pd.read_sql(query, con=connection)

            elif conn_type == 'crs_read':
                cursor.execute(query)
                res = cursor.fetchall()

            elif conn_type == 'crs_write':
                print("crs_write")
                cursor.execute(query)
                connection.commit()
                res = cursor.fetchall()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")
    return res


def get_faculty_names():
    query = 'select name from faculty'
    res = make_query('df', query)
    print("refreshing faculty names")
    return res


def get_citations():
    query = 'select title, num_citations from publication limit 10'
    res = make_query('df', query)
    return res


def get_faculty_nfo(fac_name):
    query = f"select f.name, f.position, u.name, f.email, f.phone from faculty f, university u where f.university_id = u.id and f.name='{fac_name}'"
    res = make_query('crs_read', query)
    return res


def delete_faculty(fac_name):
    # deleting dependent faculty keywords relation

    query = f"delete from faculty_keyword where faculty_id = (select id from faculty where name='{fac_name}')"
    print(query)
    res = make_query('crs_write', query)
    print("select", res)

    # deleting dependent faculty_publication relation
    query = f"delete from faculty_publication where faculty_id = (select id from faculty where name='{fac_name}')"
    res = make_query('crs_write', query)
    print("fac_pubs deleted")

    # deleting faculty member from faculty
    query = f"delete from faculty where name='{fac_name}'"
    res = make_query('crs_write', query)
    print("faculty deleted")
