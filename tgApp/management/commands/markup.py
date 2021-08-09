import telebot
from tgApp.models import *
from telebot import types


def example(list, size,call):
    buttons_in_row = size
    buttons_added = []
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row_width =3
    for timeslot in list:
        buttons_added.append(telebot.types.InlineKeyboardButton(timeslot.name, callback_data=call + str(timeslot.id)))
        if len(buttons_added) == buttons_in_row:
            keyboard.add(*buttons_added)
            buttons_added = []
    if buttons_added:
        print(*buttons_added)
    return keyboard
def markup_board():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonA = types.KeyboardButton('/profile')
    buttonB = types.KeyboardButton('/choice')
    buttonC = types.KeyboardButton('/book')

    markup.row(buttonA, buttonB)
    markup.row(buttonC)
    return markup
def markup_genre():
    i= Genre.objects.all()
    markup=example(i,3,'genre')
    return markup
def markup_prof_genre(message):
    prof = Profile.objects.get(name=message.from_user.username)
    alls= prof.genre.all()
    markup=example(alls,2,'prof_genre')
    return markup