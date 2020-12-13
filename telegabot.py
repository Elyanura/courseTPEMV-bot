import telebot
import time
import random
from telebot import types
from test import tests, Question

token = "1447946619:AAEhKT0eUUClh8kDFgfbszBzSYio6hDYMws"
bot = telebot.TeleBot(token)

allvars = {}


class Settings:
    def __init__(self):
        self.test_no = 0
        self.question_no = 0
        self.right = 0


def add_new_user(chat_id):
    global allvars
    if chat_id in allvars.keys():
        return
    a = Settings()
    allvars[chat_id] = a


def default_vars(chat_id):
    global allvars
    a = Settings()
    allvars[chat_id] = a


@bot.message_handler(commands=['start'])
def main(message):
    global allvars
    if message.chat.id in allvars.keys():
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Тестирование')
        keyboard.row('Учебные материалы')
        keyboard.row('Авторы')
        bot.send_message(message.chat.id, 'Здравствуйте еще раз!', reply_markup=keyboard)
        return
    add_new_user(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Тестирование')
    keyboard.row('Учебные материалы')
    keyboard.row('Авторы')
    bot.send_message(message.chat.id, 'Здравствуйте, выберите что-нибудь', reply_markup=keyboard)


@bot.message_handler(commands=['menu'])
@bot.message_handler(func=lambda message: message.text == 'Назад в меню')
def menu(message):
    default_vars(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Тестирование')
    keyboard.row('Учебные материалы')
    keyboard.row('Авторы')
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Авторы')
def authors(message):
    default_vars(message.chat.id)
    bot.send_message(message.chat.id, '*Авторы:*\nРЭТк-18-1\nАяпберген Жансая\nИбрагимова Элянура',
                     parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == 'Тестирование')
def test(message):
    default_vars(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Проверка знаний')
    keyboard.row('Назад в меню')
    bot.send_message(message.chat.id, 'Выберите тему', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Проверка знаний')
def test_ww2(message):
    global allvars
    add_new_user(message.chat.id)
    chat_id = message.chat.id
    if chat_id in allvars.keys():
        allvars[chat_id].test_no = 1
        allvars[chat_id].question_no = 1
        test_no = allvars[chat_id].test_no
        question_no = allvars[chat_id].question_no
        keyboard = types.ReplyKeyboardMarkup(True, False)
        question = tests[test_no][question_no]
        print(question.wrong)
        tmp = []
        for a in question.wrong:
            tmp.append(a)
        tmp.append(question.right)
        random.shuffle(tmp)
        for ans in tmp:
            keyboard.row(ans)
        keyboard.row('Назад в меню')
        bot.send_message(message.chat.id, tests[test_no][question_no].text, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Учебные материалы')
def articles(message):
    default_vars(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Силлабус ТПЭМВ')
    keyboard.row('СРС-1 мет указ')
    keyboard.row('СРС-2 мет указ')
    keyboard.row('РГР мет указ')
    keyboard.row('ТПЭВИА-ФУ лабы')
    keyboard.row('1 лекция')
    keyboard.row('2 лекция')
    keyboard.row('3 лекция')
    keyboard.row('4 лекция')
    keyboard.row('5 лекция')
    keyboard.row('6 лекция')
    keyboard.row('7 лекция')
    keyboard.row('8 лекция')
    keyboard.row('9 лекция')
    keyboard.row('10 лекция')
    keyboard.row('11,12 лекция')
    keyboard.row('Назад в меню')
    bot.send_message(message.chat.id, 'Выберите название учебного материала', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_articles(message):
    global allvars
    add_new_user(message.chat.id)
    chat_id = message.chat.id
    articles = {
        'Силлабус ТПЭМВ': 'Силлабус ТПЭМВ.doc',
        'СРС-1 мет указ': 'СРС-1 мет указ.docx',
        'СРС-2 мет указ': 'СРС-2 мет указ.docx',
        'РГР мет указ': 'РГР мет указ.docx',
        'ТПЭВИА-ФУ лабы': 'лабы.docx',
        '1 лекция': '1 лекция.pptx',
        '2 лекция': '2 лекция.pptx',
        '3 лекция': '3 лекция.pptx',
        '4 лекция': '4 лекция.pptx',
        '5 лекция': '5 лекция.pptx',
        '6 лекция': '6 лекция.pptx',
        '7 лекция': '7 лекция.pptx',
        '8 лекция': '8 лекция.pptx',
        '9 лекция': '9 лекция.doc',
        '10 лекция': '10 лекция.doc',
        '11,12 лекция': '11,12 лекция.doc'
    }
    if message.text in articles.keys():
        document = open(articles[message.text], 'rb')
        bot.send_document(message.chat.id, document)
    elif allvars[chat_id].test_no > 0:
        test_no = allvars[chat_id].test_no
        question_no = allvars[chat_id].question_no
        question = tests[test_no][question_no]
        if question.right == message.text:
            allvars[chat_id].right += 1
        allvars[chat_id].question_no += 1
        question_no += 1
        if question_no == 11:
            keyboard = types.ReplyKeyboardMarkup(True, False)
            keyboard.row('Тестирование')
            keyboard.row('Учебные материалы')
            bot.send_message(chat_id,
                             'Тестирование закончилось. Вы ответили на ' + str(allvars[chat_id].right) + '/10 вопросов',
                             reply_markup=keyboard)
            default_vars(chat_id)
            return
        keyboard = types.ReplyKeyboardMarkup(True, False)
        question = tests[test_no][question_no]
        tmp = []
        for a in question.wrong:
            tmp.append(a)
        tmp.append(question.right)
        random.shuffle(tmp)
        for ans in tmp:
            keyboard.row(ans)
        keyboard.row('Назад в меню')
        bot.send_message(message.chat.id, question.text, reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('Тестирование')
        keyboard.row('Учебные материалы')
        bot.send_message(message.chat.id, 'Выберите что-нибудь', reply_markup=keyboard)


bot.polling(none_stop=True)
