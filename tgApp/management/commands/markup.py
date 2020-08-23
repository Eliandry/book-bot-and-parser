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
    size = 2
    for i in Genre.objects.all():
        btn_list.append(types.InlineKeyboardButton(i.name, callback_data='genre' + str(i.id)))
    markup = example(btn_list, size)
    return markup


def markup_sub(id):
    btn_list = []
    size = 2
    user = Profile.objects.get(external_id=id)
    genres = user.genre.all()
    for genre in genres:
        subgenres = genre.subgenre.all()
        for subgenre in subgenres:
            btn_list.append(types.InlineKeyboardButton(subgenre.name, callback_data='subgenre' + str(subgenre.id)))
    markup_sub = example(btn_list, size)
    return markup_sub
