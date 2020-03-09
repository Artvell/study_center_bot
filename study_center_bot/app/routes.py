# -*- coding:utf-8 -*-
import sys
sys.path.append('..')
from config import token
import requests
import database
from flask import Flask
app = Flask(__name__)
from flask import request
from text import add_money

url="https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=html&text={}"

@app.route('/')
@app.route('/bot_info/mark', methods=['POST'])
def mark():
    if request.method == 'POST':
        phone=request.form['phone']
        mark=request.form['mark']
        group_id=request.form["group_id"]
        subject=database.get_group_name(int(group_id))['legal_name']
        uid=int(database.get_uid(phone)['tg_chat_id'])
        text=f'Вы получили оценку <b>{mark}</b> по предмету "{subject}"'
        if database.get_sub(uid)['sub']==1:
            requests.get(url.format(token,uid,text))
        else:
            pass
    else:
        pass

@app.route('/bot_info/attendance', methods=['POST'])
def attendance():
    if request.method == "POST":
        phone=request.form['phone']
        group_id=request.form["group_id"]
        status=int(request.form["status"])
        subject=database.get_group_name(int(group_id))['legal_name']
        uid=int(database.get_uid(phone)['tg_chat_id'])
        if status==1:
            text=f'Вы посетили занятие по предмету "{subject}"'
        elif status==0:
            text=f'Вы пропустили занятие по предмету "{subject}"'
        if database.get_sub(uid)['sub']==1:
            requests.get(url.format(token,uid,text))
        else:
            pass
    else:
        pass

@app.route('/bot_info/low_balans', methods=['POST'])
def low_balans():
    if request.method == 'POST':
        phone=request.form['phone']
        group_id=request.form["group_id"]
        subject=database.get_group_name(int(group_id))['legal_name']
        uid=int(database.get_uid(phone)['tg_chat_id'])
        text=f'У вас не хватает денег на счету для следующего занятия по предмету <b>"{subject}"</b>\n{add_money}'
        if database.get_sub(uid)['sub']==1:
            requests.get(url.format(token,uid,text))
        else:
            pass
    else:
        pass

app.run(host='0.0.0.0', port=5000,debug=False)
