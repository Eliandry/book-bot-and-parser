from time import sleep
import random
from django.core.management.base import BaseCommand
import telebot
from tgApp.models import *
from telebot import types
import re
from .markup import markup_genre,markup_prof_genre
import schedule
from threading import Thread
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
            bot.send_message(message.chat.id, f'Имя: {message.from_user.username} \nЛюбимые жанры: {str_a}'
                                              f'\nЧтобы изменить введите /ch')

        @bot.message_handler(commands=['ch'])
        def change(message):
            bot.send_message(message.chat.id,'Выберите жанры которые нужно удалить',reply_markup=markup_prof_genre(message))

        @bot.callback_query_handler(lambda c: c.data and c.data.startswith('prof_genre'))
        def callback(callback_query: types.CallbackQuery):
            user = Profile.objects.get(external_id=callback_query.from_user.id)
            s = callback_query.data
            nums = re.findall(r'\d+', s)
            nums = [int(i) for i in nums]
            genre=user.genre.get(id=nums[0])
            user.genre.remove(genre)

        @bot.message_handler(commands=['book'])
        def book(message):
            prof=Profile.objects.get(name=message.from_user.username)
            books=Book.objects.all()
            book_list=[]
            for i in range(5):
                obj=random.choice(prof.genre.all())
                x=books.filter(genre=obj)
                b=random.choice(x)
                book_list.append(b)
            book_set=set(book_list)
            for i in book_set:
                genre_list=[]
                for k in i.genre.all():
                    genre_list.append(k.name)
                    genre = ' '.join(genre_list)

                markup = types.InlineKeyboardMarkup()
                lib=types.InlineKeyboardButton('Читать', callback_data='lib' + str(i.id))
                markup.add(lib)
                dont = types.InlineKeyboardButton('Не нравится', callback_data='delete' + str(i.id))
                markup.add(dont)

                bot.send_message(message.chat.id, f'Название: {i.name}\n'
                                                  f'\n'
                                                  f'Автор: {i.author}\n'
                                                  f'\n'
                                                  f'Жанры: {genre}\n'
                                                  f'\n'
                                                  f'Описание: {i.description}\n'
                                                  f'\n'
                                                  f'Читать: {i.url}\n',reply_markup=markup)

        @bot.callback_query_handler(lambda c: c.data and c.data.startswith('lib'))
        def callback(callback_query: types.CallbackQuery):
            user = Profile.objects.get(external_id=callback_query.from_user.id)
            s = callback_query.data
            nums = re.findall(r'\d+', s)
            nums = [int(i) for i in nums]
            bk=Book.objects.get(id=nums[0])
            user.library.add(bk)

        @bot.callback_query_handler(lambda c: c.data and c.data.startswith('delete'))
        def callback(callback_query: types.CallbackQuery):
            user = Profile.objects.get(external_id=callback_query.from_user.id)
            s = callback_query.data
            nums = re.findall(r'\d+', s)
            nums = [int(i) for i in nums]
            bk = Book.objects.get(id=nums[0])
            user.badbook.add(bk)
        def schedule_checker():
            while True:
                schedule.run_pending()
                sleep(1)

        def function_to_run(message):
            return bot.send_message(message.chat.id, "This is a message to send.")
        if __name__ == "__main__":
            schedule.every().saturday.at("12:00").do(function_to_run())
            Thread(target=schedule_checker).start()
        bot.polling()
