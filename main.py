import time
import telebot
from telebot import types
import sorts
import hard

bot = telebot.TeleBot('6576286876:AAHqGq5RtJX0Iig8dcFiJPnCXR2UWRlpBxI')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(msg: types.Message):
    bot.send_message(msg.chat.id, "Привет! Я бот, который расскажет вам о сортировках.")

def menu(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row("Справка популярных сортировок")
    keyboard.row("Анализ сложности алгоритма")
    bot.send_message(msg.chat.id, "Выбери действие:", reply_markup=keyboard)
    bot.register_next_step_handler(msg, menu)

def menu_handler(msg: types.Message):
    if msg.text.endswith("Справка"):
        local_sorts(msg)
    elif msg.text.endswith("Анализ"):
        bot.send_message(msg.chat.id, "Отправь мне свой алгоритм, "
                                      "а я постараюсь посчитать его сложность по О-нотации.\n"
                                      "Внимание: анализ кода на сложность это сложный аналитический процесс. Результат "
                                      "может быть неверным!")
        bot.register_next_step_handler(msg, analyze_custom_algorithm)


def local_sorts(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    for sort in sorts.sort_dict:
        keyboard.row(sort[-3:])
    bot.send_message(msg.chat.id, "Выберите вид сортировки из меню ниже:", reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_sort_choice)


# Обработчик кнопок
def handle_sort_choice(msg: types.Message):
    sort_type = msg.text
    # В зависимости от выбора пользователя, отправьте информацию о соответствующей сортировке
    sort_info = sorts.sort(sort_type)
    bot.send_message(msg.chat.id, sort_info, "Markdown")
    time.sleep(2)
    menu(msg)

def analyze_custom_algorithm(msg: types.Message):
    a = hard.Analyze(msg.text)
    a.start()
    bot.send_message(msg.chat.id, a)
    time.sleep(2)
    menu(msg)


# Запуск бота
bot.infinity_polling()

