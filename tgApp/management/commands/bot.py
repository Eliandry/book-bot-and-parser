from django.core.management.base import BaseCommand
import telebot
from tgApp.models import *
from telebot import types
import re
from .markup import markup_genre, markup_sub


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        bot = telebot.TeleBot('1340385330:AAEuzVzMjiX3E1F92nhTw9IPizmR-z7srZQ')

        @bot.message_handler(commands=['start'])
        def start_message(message):
            p, _ = Profile.objects.get_or_create(
                external_id=message.chat.id,
                defaults={
                    'name': message.from_user.username,
                }
            )
            bot.send_message(message.chat.id, f'Поздравляю, {message.from_user.username}, вы зарегестрированы! '
                                              f'Для начала выберите ваши любимые жанры /choice')

        @bot.message_handler(commands=['choice'])
        def choise(message):

            bot.send_message(message.chat.id, 'Выберите ваши любимые жанры (max 5). Когда закончите введите /next',
                             reply_markup=markup_genre())

        @bot.callback_query_handler(lambda c: c.data and c.data.startswith('genre'))
        def callback(callback_query: types.CallbackQuery):
            user = Profile.objects.get(external_id=callback_query.from_user.id)
            s = callback_query.data
            nums = re.findall(r'\d+', s)
            nums = [int(i) for i in nums]

            genre = Genre.objects.get(id=nums[0])
            if user.genre.count() > 5:
                bot.answer_callback_query(callback_query.id)
                bot.send_message(callback_query.from_user.id,
                                 'Вы выбрали достаточно жанров. Введите /next')
                return
            user.genre.add(genre)

        @bot.message_handler(commands=['next'])
        def next(message):
            bot.send_message(message.chat.id,
                             'Отлично. Осталось выбрать ваши любимые поджанры для более точного определения ваших интересов (max 10)',
                             reply_markup=markup_sub(message.chat.id))

        @bot.callback_query_handler(lambda c: c.data and c.data.startswith('subgenre'))
        def callback(callback_query: types.CallbackQuery):
            user = Profile.objects.get(external_id=callback_query.from_user.id)
            s = callback_query.data
            nums = re.findall(r'\d+', s)
            nums = [int(i) for i in nums]
            subgenre = Subgenre.objects.get(id=nums[0])
            if user.subgenre.count() > 10:
                bot.answer_callback_query(callback_query.id)
                bot.send_message(callback_query.from_user.id,
                                 'Вы выбрали достаточно поджанров. Введите /next')
                return
            user.subgenre.add(subgenre)

        bot.polling()
