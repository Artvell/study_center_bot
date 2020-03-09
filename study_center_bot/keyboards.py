# -*- coding:utf-8 -*-
from telebot.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
import text,database

def main_1():
    button_1=KeyboardButton(text.info)
    button_2=KeyboardButton(text.registry)
    button_3=KeyboardButton(text.connect)
    button_4=KeyboardButton(text.request)
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(button_1)
    kb.row(button_2)
    kb.row(button_3)
    kb.row(button_4)
    return kb

def main_2():
    button_1=KeyboardButton(text.info)
    button_2=KeyboardButton(text.cabinet)
    button_3=KeyboardButton(text.connect)
    button_4=KeyboardButton(text.request)
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(button_1)
    kb.row(button_2)
    kb.row(button_3)
    kb.row(button_4)
    return kb

def info_kb():
    button_1=KeyboardButton(text.teachers)
    button_2=KeyboardButton(text.subjects)
    button_3=KeyboardButton(text.prices)
    button_4=KeyboardButton(text.to_main)
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(button_1)
    kb.row(button_2)
    kb.row(button_3)
    kb.row(button_4)
    return kb

def back():
    button_1=KeyboardButton(text.back_1)
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(button_1)
    return kb

def contact():
    button_1=KeyboardButton(text.send_number,request_contact=True)
    button_2=KeyboardButton(text.to_main)
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(button_1)
    kb.row(button_2)
    return kb

def registered_menu(ind):
    button_1=KeyboardButton(text.gaps_text)
    button_2=KeyboardButton(text.balans)
    button_5=KeyboardButton(text.debt)
    button_6=KeyboardButton(text.payment)
    if ind==1:
        button_3=KeyboardButton(text.sub_1)
    else:
        button_3=KeyboardButton(text.sub_0)
    button_4=KeyboardButton(text.to_main)
    button_7=KeyboardButton(text.reset_phone)
    button_8=KeyboardButton(text.marks_text)
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(button_1,button_2)
    kb.row(button_5,button_6)
    kb.row(button_8,button_7)
    kb.row(button_3)
    kb.row(button_4)
    return kb

def courses():
    kourses=database.order_subjects()
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0,len(kourses)-1,2):
        button=KeyboardButton(kourses[i]['name'])
        button_2=KeyboardButton(kourses[i+1]['name'])
        kb.row(button,button_2)
    kb.add(KeyboardButton(text.basket))
    kb.add(KeyboardButton(text.to_main))
    return kb

def basket(subjects_list):
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    if len(subjects_list)!=0:
        for sub in subjects_list:
            button=KeyboardButton(f"❌ {sub}")
            kb.row(button)
        kb.row(KeyboardButton(text.send))
    button_1=KeyboardButton(text.subjects_list)
    button_2=KeyboardButton(text.to_main)
    kb.row(button_1,button_2)
    return kb

def go_main():
    button_1=KeyboardButton(text.to_main)
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(button_1)
    return kb

#courses()