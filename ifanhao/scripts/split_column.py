# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-28
#

import MySQLdb as db_helper

db_host = '127.0.0.1'
db_user = 'root'
db_pass = '!@#456'
db_name = 'icomic'


s = 'av_tmp'
s_c_1 = 'id'
s_c_2 = 'actors'

t = 'av_2_actor'
t_c_1 = 'av_id'
t_c_2 = 'av_actor'

# s = 'av_tmp'
# s_c_1 = 'id'
# s_c_2 = 'tags'
#
# t = 'av_2_tag'
# t_c_1 = 'av_id'
# t_c_2 = 'av_tag'


def get_mysql_conn():
    return db_helper.connect(db_host, db_user, db_pass, db_name, charset='utf8')


def exe_sql(conn, sql="select 1", use_dict=False, close=False):
    cursor = conn.cursor(db_helper.cursors.DictCursor) if use_dict else conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.commit()
    if(close) :
        conn.close()
    return result


sources_sql = 'SELECT {},{} FROM {}'.format(s_c_1, s_c_2, s)
target_sql = 'insert into {} ({}, {}) values (%s, %s)'.format(t, t_c_1, t_c_2)

conn = get_mysql_conn()
sources = exe_sql(conn, sources_sql)

cursor = conn.cursor()
for source in sources:
    cursor.executemany(target_sql, [(source[0], splitted.strip())
                                    for splitted in source[1].split('|')
                                    if splitted.strip()])

cursor.close()
conn.commit()

conn.close()
