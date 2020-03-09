# -*- coding:utf-8 -*-
from pymysql import cursors,connect
from datetime import datetime

def getConnection():
    connection=connect(host="host",
                        user='user',
                        password='password',
                        db='db_name',
                        cursorclass=cursors.DictCursor)
    return connection

def teachers():
    connection=getConnection()
    sql="SELECT teacher.name,teacher.title,webpage.url FROM teacher,webpage WHERE teacher.active = 1 AND teacher.webpage_id = webpage.id AND teacher.page_visibility = 1 ORDER BY teacher.page_order"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        connection.close()
        return result
    except Exception as e:
        connection.close()
        return -2

def subjects():
    connection=getConnection()
    sql="SELECT s.name,w.url FROM module_subject as s,webpage as w WHERE s.webpage_id=w.id"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        connection.close()
        return result
    except Exception as e:
        connection.close()
        return -2

def order_subjects():
    connection=getConnection()
    sql="SELECT name FROM module_order_subject"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        connection.close()
        return result
    except Exception as e:
        connection.close()
        return -2

def is_registered(uid):
    connection=getConnection()
    sql=f"SELECT * FROM bot_users_1 WHERE tg_chat_id={uid}"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        connection.close()
        if len(result)>0:
            return True
        else:
            return False
    except Exception as e:
        connection.close()

def write_to_db(where,value,uid):
    connection=getConnection()
    sql=f"UPDATE bot_users_1 SET {where}={value} WHERE tg_chat_id={uid}"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
    except Exception as e:
        connection.close()

def is_dublicate(number):
    connection=getConnection()
    sql=f"SELECT * FROM bot_users_1 WHERE phone='{number}'"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        if len(result)>0:
            connection.close()
            return True
        else:
            connection.close()
            return False
    except Exception as e:
        connection.close()

def is_number_exist(number,uid):
    connection=getConnection()
    sql=f"SELECT * FROM user WHERE phone='{number}'"
    sql2=f"INSERT IGNORE INTO bot_users_1 (phone,tg_chat_id,state,sub) VALUES ('{number}',{uid},0,1)"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        if len(result)>0:
            cursor.execute(sql2)
            connection.commit()
            connection.close()
            return True
        else:
            connection.close()
            return False
    except Exception as e:
        connection.close()

def get_sub(uid):
    connection=getConnection()
    sql=f"SELECT sub FROM bot_users_1 WHERE tg_chat_id={uid}"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        sub=cursor.fetchall()[0]
        connection.close()
        return sub
    except Exception as e:
        connection.close()

def get_gaps(uid):
    connection=getConnection()
    sql1=f'''SELECT ev.event_date, g.name,u.name
            FROM
              bot_users_1 as b, `group` as g, event_member as em, user as u, group_pupil as gp, event as ev
            WHERE
              b.tg_chat_id={uid}
              AND u.phone = b.phone
              AND gp.user_id = u.id
              AND em.group_pupil_id = gp.id
              AND g.id = gp.group_id
              AND em.event_id = ev.id
              AND em.status = 2
              AND ev.status = 1
              AND ev.event_date > NOW() - INTERVAL 90 DAY ORDER BY u.name,ev.event_date'''
    try:
        cursor=connection.cursor()
        cursor.execute(sql1)
        result=cursor.fetchall()
        connection.close()
        return result
    except Exception as e:
        connection.close()

def get_marks(uid):
    connection=getConnection()
    sql1=f'''SELECT ev.event_date, g.name,u.name,em.mark
            FROM
              bot_users_1 as b, `group` as g, event_member as em, user as u, group_pupil as gp, event as ev
            WHERE
              b.tg_chat_id={uid}
              AND u.phone = b.phone
              AND gp.user_id = u.id
              AND em.group_pupil_id = gp.id
              AND g.id = gp.group_id
              AND em.event_id = ev.id
              AND em.status = 1
              AND ev.status = 1
              AND em.mark IS NOT NULL
              AND ev.event_date > NOW() - INTERVAL 90 DAY ORDER BY u.name,ev.event_date'''
    try:
        cursor=connection.cursor()
        cursor.execute(sql1)
        result=cursor.fetchall()
        connection.close()
        return result
    except Exception as e:
        print(e)
        connection.close()

def get_balans(uid):
    connection=getConnection()
    sql=f"SELECT u.money,u.name FROM bot_users_1 as b,user as u WHERE b.tg_chat_id={uid} AND u.phone=b.phone ORDER BY u.name"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        money=cursor.fetchall()
        connection.close()
        return money
    except Exception:
        connection.close()

def get_courses():
    connection=getConnection()
    sql=f"SELECT legal_name FROM `group` WHERE active=1"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        connection.close()
        return result
    except Exception as e:
        connection.close()

def get_debt(uid):
    connection=getConnection()
    sql=f"SELECT d.amount,d.created_at,g.name,u.name FROM `group` as g,debt as d,bot_users_1 as b,user as u WHERE b.tg_chat_id={uid} AND u.phone=b.phone AND d.user_id=u.id AND g.id=d.group_id AND d.created_at > NOW() - INTERVAL 90 DAY ORDER BY u.name"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        connection.close()
        return result
    except Exception:
        connection.close()

def get_payment(uid):
    connection=getConnection()
    sql=f"SELECT p.amount,p.created_at,g.name,u.name FROM `group` as g,payment as p,bot_users_1 as b,user as u WHERE b.tg_chat_id={uid} AND u.phone=b.phone AND p.user_id=u.id AND g.id=p.group_id AND p.amount < 0 AND p.created_at > NOW() - INTERVAL 30 DAY ORDER BY u.name,p.created_at"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        connection.close()
        return result
    except Exception:
        connection.close()

def add_module_order(subjects_list,uid,name):
    connection=getConnection()
    subs=",".join(subjects_list)
    sql=f"SELECT phone FROM bot_users WHERE tg_chat_id={uid}"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        phone=cursor.fetchall()[0]['phone']
        sql2=f"INSERT INTO module_order (source,subject,name,phone,created_at) VALUES ('Телеграм бот','{subs}','{name}','{phone}',NOW())"
        cursor.execute(sql2)
        connection.commit()
        connection.close()
    except Exception:
        connection.close()

def add_module_order_unregistered(subjects_list,phone,name):
    connection=getConnection()
    subs=",".join(subjects_list)
    try:
        cursor=connection.cursor()
        sql2=f"INSERT INTO module_order (source,subject,name,phone,created_at) VALUES ('Телеграм бот','{subs}','{name}','{phone}',NOW())"
        cursor.execute(sql2)
        connection.commit()
        connection.close()
    except Exception as e:
        print("@@@",e)
        connection.close()

def get_uid(phone):
    connection=getConnection()
    sql=f"SELECT tg_chat_id FROM bot_users_1 WHERE phone='{phone}'"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()[0]
        connection.close()
        return result
    except Exception:
        connection.close()

def get_group_name(group_id):
    connection=getConnection()
    sql=f"SELECT legal_name FROM `group` WHERE id={group_id}"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        result=cursor.fetchall()[0]
        connection.close()
        return result
    except Exception:
        connection.close()

def delete_bot_user(uid):
    connection=getConnection()
    sql=f"DELETE FROM `bot_users_1` WHERE tg_chat_id={uid}"
    try:
        cursor=connection.cursor()
        cursor.execute(sql)
        #result=cursor.fetchall()[0]
        connection.commit()
        connection.close()
        #return result
    except Exception as e:
        print("!!!",e)
        connection.close()

#add_module_order(["test1","test2"],145109083,'test')
#print(teachers())
#print(get_marks(145109083))
