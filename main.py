import telebot
import time
from passwords_db import PasswordsDB

db = PasswordsDB()
bot = telebot.TeleBot('6232290157:AAGCtDeM_57GSY3R25pKu9xNjjbV8yWbhJU')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для хранения паролей. "
                                      "Вы можете использовать следующие комманды:\n"
                                      "/set - добавляет логин и пароль к сервису\n"
                                      "/get - получает логин и пароль по названию сервиса\n"
                                      "/del - удаляет данные для сервиса\n")


@bot.message_handler(commands=['set'])
def set_password(message):
    bot.send_message(message.chat.id, "Введите название сервиса:")
    bot.register_next_step_handler(message, set_password_name)


def set_password_name(message):
    if message.text is None or message.text.startswith("/"):
        bot.send_message(message.chat.id, text="Вы ввели некорректное значение")
        return
    if db.check_password_name(message.from_user.id, message.text):
        bot.send_message(message.chat.id, "Для данного сервиса уже сохранён пароль")
        return
    password_name = message.text
    bot.send_message(message.chat.id, "Введите логин:")
    bot.register_next_step_handler(message, set_login, password_name)


def set_login(message, password_name):
    if message.text is None or message.text.startswith("/"):
        bot.send_message(message.chat.id, text="Вы ввели некорректное значение")
        return
    login = message.text
    bot.send_message(message.chat.id, "Введите пароль:")
    bot.register_next_step_handler(message, save_password, password_name, login)


def save_password(message, password_name, login):
    password = message.text
    user_id = message.from_user.id
    if db.add_password(user_id, password_name, login, password):
        bot.send_message(message.chat.id, "Пароль успешно сохранен!")
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так...")


@bot.message_handler(commands=['get'])
def get_password(message):
    bot.send_message(message.chat.id, "Введите название сервиса:")
    bot.register_next_step_handler(message, get_password_name)


def get_password_name(message):
    if message.text is None or message.text.startswith("/"):
        bot.send_message(message.chat.id, text="Вы ввели некорректное значение")
        return
    if not db.check_password_name(message.from_user.id, message.text):
        bot.send_message(message.chat.id, "Для данного сервиса нет сохраннёных паролей")
        return
    password_name = message.text
    result = db.get_password(message.from_user.id, password_name)
    if result:
        message_text = f"Логин: {result[0]}\nПароль: {result[1]}"
        message_to_delete = bot.send_message(message.chat.id, message_text)
        time.sleep(600)
        bot.delete_message(chat_id=message.chat.id, message_id=message_to_delete.message_id)
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так...")


@bot.message_handler(commands=['del'])
def del_password(message):
    bot.send_message(message.chat.id, "Введите название сервиса:")
    bot.register_next_step_handler(message, del_password_name)


def del_password_name(message):
    if message.text is None or message.text.startswith("/"):
        bot.send_message(message.chat.id, text="Вы ввели некорректное значение")
        return
    if not db.check_password_name(message.from_user.id, message.text):
        bot.send_message(message.chat.id, "Для данного сервиса нет сохраннёных паролей")
        return
    password_name = message.text
    if db.delete_password(message.from_user.id, password_name):
        bot.send_message(message.chat.id, "Пароль успешно удалён!")
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так...")


bot.polling()
