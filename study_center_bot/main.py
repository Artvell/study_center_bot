# -*- coding:utf-8 -*-
import telebot
from config import token
import database,keyboards,text
from datetime import datetime
bot = telebot.TeleBot(token)
is_registered={} #user_id:True/False
state={}
sub={}
is_active={}
stock={} #user_id:[]
subjects_list=[s['name'] for s in database.order_subjects()]

#telebot.apihelper.proxy={"tg":"socks?server=sr.spry.fail&port=1080&user=telegram&pass=telegram"}
'''@bot.message_handler(content_types=["text"])
def aa(message):
    print(message.text)'''

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id=message.from_user.id
    database.write_to_db('state',0,message.from_user.id)
    state[message.from_user.id]=0
    registered=is_registered.get(user_id,database.is_registered(user_id))
    if registered:
        is_registered[user_id]=True
        bot.send_message(user_id,text.hello_2,reply_markup=keyboards.main_2())
    else:
        is_registered[user_id]=False
        bot.send_message(user_id,text.hello_1,reply_markup=keyboards.main_1())

@bot.message_handler(func=lambda message: message.text == text.to_main)
def to_main(message):
    user_id=message.from_user.id
    registered=is_registered.get(user_id,database.is_registered(user_id))
    database.write_to_db('state',0,message.from_user.id)
    state[message.from_user.id]=0
    is_active[user_id]=False
    if registered:
        is_registered[user_id]=True
        bot.send_message(user_id,text.hello_2,reply_markup=keyboards.main_2())
    else:
        is_registered[user_id]=False
        bot.send_message(user_id,text.hello_1,reply_markup=keyboards.main_1())

@bot.message_handler(func=lambda message: message.text == text.back_1)
def back_1(message):
    bot.send_message(message.from_user.id,text.info_text,reply_markup=keyboards.info_kb())

@bot.message_handler(func=lambda message: message.text == text.info)
def info(message):
    bot.send_message(message.from_user.id,text.info_text,reply_markup=keyboards.info_kb())

@bot.message_handler(func=lambda message: message.text == text.teachers)
def teachers(message):
    m_text=text.teachers_list
    teachers=database.teachers()
    for teacher in teachers:
        m_text+=f"{teacher['title']} <a href='5plus.uz/{teacher['url']}'>{teacher['name']}</a>\n"
    bot.send_message(message.from_user.id,m_text,parse_mode="HTML",disable_web_page_preview=True,reply_markup=keyboards.back())

@bot.message_handler(func=lambda message: message.text == text.prices)
def prices(message):
    bot.send_message(message.from_user.id,text.price_text,parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == text.subjects)
def subjects(message):
    subjects=database.subjects()
    m_text=text.subjects_list
    for subject in subjects:
        m_text+=f"\n<a href='5plus.uz/{subject['url']}'>{subject['name']}</a>"
    bot.send_message(message.from_user.id,m_text,parse_mode="HTML",disable_web_page_preview=True,reply_markup=keyboards.back())

@bot.message_handler(func=lambda message: message.text == text.connect)
def connect(message):
    user_id=message.from_user.id
    bot.send_message(user_id,text.connect_message,parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == text.registry)
def registry(message):
    state[message.from_user.id]=1
    database.write_to_db('state',1,message.from_user.id)
    bot.send_message(message.from_user.id,text.number_request,reply_markup=keyboards.contact())


@bot.message_handler(func=lambda message: message.text == text.cabinet)
def cabinet(message):
    ind=int(sub.get(message.from_user.id,database.get_sub(message.from_user.id)['sub']))
    database.write_to_db('state',0,message.from_user.id)
    state[message.from_user.id]=0
    bot.send_message(message.from_user.id,text.success,reply_markup=keyboards.registered_menu(ind))

@bot.message_handler(func=lambda message: state.get(message.from_user.id,0)==1,content_types=['text'])
def get_contact_text(message):
    message_text=message.text
    if not database.is_dublicate(message_text):
        if database.is_number_exist(message_text,message.from_user.id):
            database.write_to_db('state',0,message.from_user.id)
            state[message.from_user.id]=0
            ind=int(sub.get(message.from_user.id,database.get_sub(message.from_user.id)['sub']))
            bot.send_message(message.from_user.id,text.success,reply_markup=keyboards.registered_menu(ind))
        else:
            bot.send_message(message.from_user.id,text.failed,reply_markup=keyboards.contact())
    else:
        bot.send_message(message.from_user.id,text.number_in_use)

@bot.message_handler(func=lambda message: state.get(message.from_user.id,0)==1,content_types=['contact'])
def get_contact_number(message):
    message_text=message.contact.phone_number
    if len(message_text)==12:
        message_text="+"+message_text
    if not database.is_dublicate(message_text):
        if database.is_number_exist(message_text,message.from_user.id):
            database.write_to_db('state',0,message.from_user.id)
            state[message.from_user.id]=0
            ind=int(sub.get(message.from_user.id,database.get_sub(message.from_user.id)['sub']))
            bot.send_message(message.from_user.id,text.success,reply_markup=keyboards.registered_menu(ind))
        else:
            bot.send_message(message.from_user.id,text.failed,reply_markup=keyboards.contact())
    else:
        bot.send_message(message.from_user.id,text.number_in_use)

@bot.message_handler(func=lambda message: state.get(message.from_user.id,0)==3,content_types=['text'])
def contact_text_for_number(message):
    user_id=message.from_user.id
    message_text=message.text
    if len(message_text)==12:
        message_text="+"+message_text
    database.write_to_db('state',0,message.from_user.id)
    state[message.from_user.id]=0
    database.add_module_order_unregistered(stock.get(user_id,[]),message_text,message.from_user.first_name)
    stock[user_id]=[]
    bot.send_message(user_id,text.send_text,reply_markup=keyboards.go_main())

@bot.message_handler(func=lambda message: state.get(message.from_user.id,0)==3,content_types=['contact'])
def contact_for_order(message):
    user_id=message.from_user.id
    message_text=message.contact.phone_number
    if len(message_text)==12:
        message_text="+"+message_text
    database.write_to_db('state',0,message.from_user.id)
    state[message.from_user.id]=0
    database.add_module_order_unregistered(stock.get(user_id,[]),message_text,message.from_user.first_name)
    stock[user_id]=[]
    bot.send_message(user_id,text.send_text,reply_markup=keyboards.go_main())

@bot.message_handler(func=lambda message: message.text==text.gaps_text)
def gaps(message):
    user_id=message.from_user.id
    gapps=database.get_gaps(user_id)
    if user_id not in is_registered or user_id not in sub:
        is_registered[user_id]=database.is_registered(user_id)
        database.write_to_db('state',0,message.from_user.id)
        state[message.from_user.id]=0
        sub[user_id]=database.get_sub(message.from_user.id)['sub']
    if len(gapps)<1:
        bot.send_message(user_id,text.no_gaps)
    else:
        message_text=text.gaps.format(len(gapps))
        name=""
        for gap in gapps:
            date=datetime.strftime(gap["event_date"],r"%d-%m-%Y")
            if gap['u.name']!=name:
                message_text+=f'{gap["u.name"]}\n{date}: {gap["name"]}\n'
                name=gap['u.name']
            else:
                message_text+=f'{date}: {gap["name"]}\n'
        bot.send_message(user_id,message_text)

@bot.message_handler(func=lambda message: message.text==text.balans)
def balans(message):
    user_id=message.from_user.id
    if user_id not in is_registered or user_id not in sub:
        is_registered[user_id]=database.is_registered(user_id)
        database.write_to_db('state',0,message.from_user.id)
        state[message.from_user.id]=0
        sub[user_id]=database.get_sub(message.from_user.id)['sub']
    balans=database.get_balans(user_id)
    if len(balans)>1:
        message_text=""
        name=""
        for bal in balans:
            if bal['name']!=name:
                message_text+=(bal['name']+"\n"+text.show_balans.format(bal['money']))
                name=bal['name']
            else:
                message_text+=text.show_balans.format(bal['money'])
        bot.send_message(user_id,message_text)
    else:
        bot.send_message(user_id,text.balans_kol.format(balans[0]['money']))

@bot.message_handler(func=lambda message: message.text==text.debt)
def debt(message):
    user_id=message.from_user.id
    debts=database.get_debt(user_id)
    if user_id not in is_registered or user_id not in sub:
        is_registered[user_id]=database.is_registered(user_id)
        database.write_to_db('state',0,message.from_user.id)
        state[message.from_user.id]=0
        sub[user_id]=database.get_sub(message.from_user.id)['sub']
    message_text=""
    if len(debts)==0:
        bot.send_message(user_id,text.no_debt,parse_mode="HTML")
    else:
        name=""
        for d in debts:
            date=datetime.strftime(d["created_at"],r"%d-%m-%Y")
            if d['u.name']!=name:
                message_text+=(d['u.name']+"\n"+text.debt_text.format(d["amount"],date,d['name']))
                name=d['u.name']
            else:
                message_text+=text.debt_text.format(d["amount"],date,d['name'])
        bot.send_message(user_id,message_text,parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text==text.payment)
def payment(message):
    user_id=message.from_user.id
    payments=database.get_payment(user_id)
    if user_id not in is_registered or user_id not in sub:
        is_registered[user_id]=database.is_registered(user_id)
        database.write_to_db('state',0,message.from_user.id)
        state[message.from_user.id]=0
        sub[user_id]=database.get_sub(message.from_user.id)['sub']
    if len(payments)!=0:
        message_text=text.payment_text
        name=""
        for pay in payments:
            date=datetime.strftime(pay["created_at"],r"%d-%m-%Y")
            if pay['u.name']!=name:
                message_text+=f"{pay['u.name']}\n{date}: {pay['name']} - {pay['amount']*(-1)}\n"
                name=pay['u.name']
            else:
                message_text+=f"{date}: {pay['name']} - {pay['amount']*(-1)}\n"
        bot.send_message(user_id,message_text)
    else:
        bot.send_message(user_id,text.no_payment)

@bot.message_handler(func=lambda message: message.text==text.marks_text)
def marks(message):
    user_id=message.from_user.id
    marks=database.get_marks(user_id)
    if user_id not in is_registered or user_id not in sub:
        is_registered[user_id]=database.is_registered(user_id)
        database.write_to_db('state',0,message.from_user.id)
        state[message.from_user.id]=0
        sub[user_id]=database.get_sub(message.from_user.id)['sub']
    if len(marks)!=0:
        message_text=text.marks
        name=""
        for mark in marks:
            date=datetime.strftime(mark["event_date"],r"%d-%m-%Y")
            if mark['u.name']!=name:
                message_text+=f'{mark["u.name"]}\n{date}: {mark["name"]} - <b>{mark["mark"]}</b>\n'
                name=mark['u.name']
            else:
                message_text+=f'{date}: {mark["name"]} - <b>{mark["mark"]}</b>\n'
        bot.send_message(user_id,message_text,parse_mode="HTML")
    else:
        bot.send_message(user_id,text.no_marks)

@bot.message_handler(func=lambda message: message.text==text.sub_0)
def sub_0(message):
    user_id=message.from_user.id
    if user_id not in is_registered or user_id not in sub:
        is_registered[user_id]=database.is_registered(user_id)
        database.write_to_db('state',0,message.from_user.id)
        state[message.from_user.id]=0
        sub[user_id]=database.get_sub(message.from_user.id)['sub']
    sub[user_id]=1
    database.write_to_db('sub',1,user_id)
    bot.send_message(user_id,text.sub_on,reply_markup=keyboards.registered_menu(1))

@bot.message_handler(func=lambda message: message.text==text.sub_1)
def sub_1(message):
    user_id=message.from_user.id
    if user_id not in is_registered or user_id not in sub:
        is_registered[user_id]=database.is_registered(user_id)
        database.write_to_db('state',0,message.from_user.id)
        state[message.from_user.id]=0
        sub[user_id]=database.get_sub(message.from_user.id)['sub']
    sub[user_id]=0
    database.write_to_db('sub',0,user_id)
    bot.send_message(user_id,text.sub_off,reply_markup=keyboards.registered_menu(0))



@bot.message_handler(func=lambda message:message.text==text.request or message.text==text.subjects_list)
def courses(message):
    user_id = message.from_user.id
    is_active[user_id]=True
    state[message.from_user.id]=0
    database.write_to_db('state',0,message.from_user.id)
    bot.send_message(user_id,text.request_text,reply_markup=keyboards.courses())

@bot.message_handler(func=lambda message: is_active.get(message.from_user.id,False)==True and message.text in [s['name'] for s in database.order_subjects()],content_types=['text'])
def to_stock(message):
    user_id=message.from_user.id
    if user_id in stock:
        stock[user_id].append(message.text)
    else:
        stock[user_id]=[message.text]
    bot.send_message(user_id,text.stock_success)

@bot.message_handler(func=lambda message:message.text==text.basket)
def basket(message):
    user_id=message.from_user.id
    bot.send_message(user_id,text.basket,reply_markup=keyboards.basket(stock.get(user_id,[])))

@bot.message_handler(func=lambda message:message.text==text.send)
def send(message):
    user_id=message.from_user.id
    registered=is_registered.get(user_id,database.is_registered(user_id))
    print(registered)
    if registered:
        database.add_module_order(stock.get(user_id,[]),user_id,message.from_user.first_name)
        stock[user_id]=[]
        bot.send_message(user_id,text.send_text,reply_markup=keyboards.go_main())
    else:
        database.write_to_db('state',3,message.from_user.id)
        state[message.from_user.id]=3
        bot.send_message(user_id,text.send_number,reply_markup=keyboards.contact())

@bot.message_handler(func=lambda message: message.text == text.reset_phone)
def reset_phone(message):
    print("#####")
    user_id=message.from_user.id
    database.delete_bot_user(user_id)
    bot.send_message(user_id,text.success_reset,reply_markup=keyboards.main_1())

@bot.message_handler(func=lambda message:type(message.text)!=None)
def delete_subject(message):
    try:
        if (message.text.startswith("❌")==True and message.text[2:] in [s['name'] for s in database.order_subjects()]):
            user_id=message.from_user.id
            subj=message.text[2:]
            stock.get(user_id,[subj]).remove(subj)
            bot.send_message(user_id,text.basket,reply_markup=keyboards.basket(stock.get(user_id,[])))
    except Exception:
        pass



bot.polling()
