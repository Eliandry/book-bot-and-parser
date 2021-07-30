from django.core.management.base import BaseCommand
import telebot
from tgApp.models import *
from telebot import types
import re
from .markup import markup_genre


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        bot = telebot.TeleBot('1340385330:AAGpsOtKDp_CKGxedsTHorpDIHE2SojQAC4')

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

            bot.send_message(message.chat.id, 'Выберите ваши любимые жанры (max 25). Когда закончите введите /next',
                             reply_markup=markup_genre())

        @bot.callback_query_handler(lambda c: c.data and c.data.startswith('genre'))
        def callback(callback_query: types.CallbackQuery):
            user = Profile.objects.get(external_id=callback_query.from_user.id)
            s = callback_query.data
            nums = re.findall(r'\d+', s)
            nums = [int(i) for i in nums]

            genre = Genre.objects.get(id=nums[0])
            if user.genre.count() > 25:
                bot.answer_callback_query(callback_query.id)
                bot.send_message(callback_query.from_user.id,
                                 'Вы выбрали достаточно жанров. Введите /next')
                return
            user.genre.add(genre)

        @bot.message_handler(commands=['profile'])
        def profile(message):
            prof=Profile.objects.get(name=message.from_user.username)
            f=[]
            for i in prof.genre.all():
               f.append(i.name)
            str_a = ' '.join(f)
            bot.send_message(message.chat.id, f'Имя: {message.from_user.username}, '
                                              f'Любимые жанры: {str_a}')

        bot.polling()
