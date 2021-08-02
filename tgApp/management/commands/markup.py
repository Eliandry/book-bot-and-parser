from django.core.management.base import BaseCommand
import telebot
from tgApp.models import *
from telebot import types
import re


def example(list, size):
    btn_list = list

    markup = types.InlineKeyboardMarkup(size)
    for i in range(0, len(btn_list), size):
        part = btn_list[i:i + size]
        if len(part) == 3:
            markup.add(part[0], part[1], part[2])
        elif len(part) == 2:
            markup.add(part[0], part[1])
        else:
            markup.add(part[0])
    return markup


def markup_genre():
    btn_list = []
    for i in Genre.objects.all():
        btn_list.append(types.InlineKeyboardButton(i.name, callback_data='genre' + str(i.id)))
    markup = types.InlineKeyboardMarkup()
    for i in btn_list:
        markup.add(i)
    return markup
def markup_prof_genre(message):
    prof = Profile.objects.get(name=message.from_user.username)
    btn_list = []
    for i in prof.genre.all():
        btn_list.append(types.InlineKeyboardButton(i.name, callback_data='prof_genre' + str(i.id)))
    markup = types.InlineKeyboardMarkup()
    for i in btn_list:
        markup.add(i)
    return markup