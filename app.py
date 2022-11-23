import telebot
from config import TOKEN, keys
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def cmd_start(message: telebot.types.Message):
    text = '''Приветствую!
Я умею конвертировать валюты.
Что бы начать работу введите команду в следующем формате: 
<имя валюты>  <в какую валюту перевести>  <сколько перевести>
Посмотреть список доступных вылют: /values
Напомнить о возможностях: /help'''
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def cmd_help(message: telebot.types.Message):
    text = '''Для конвертации введите команду боту в следующем формате: 
<имя валюты>  <в какую валюту перевести>  <сколько перевести>
Пример: доллар рубль 100
Посмотреть список доступных вылют: /values'''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def cmd_values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys:
        text += f'\n{key}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        if message.text.startswith("/"):
            raise APIException('Неизвестная команда.')

        params = message.text.lower().split()
        if len(params) != 3:
            raise APIException('Неверное количество параметров.')

        quote, base = params[:2]
        amount = CurrencyConverter.amount_transform(params[2])

        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {keys[quote]}  -  {total_base} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
