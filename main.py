import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = '''
    Привет! Чтобы начать работу, введите команду в следующем формате:\n
<валюта><валюта перевода><сумма>\n
Например: "Доллар Рубль 100" или "Новозеландский_доллар Рубль 100"\n
Хочешь увидеть список всех валют?:\n /values
    '''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Неверное число параметров')
        currency, currency_transfer, amount = values
        total_base = CurrencyConverter.get_price(currency, currency_transfer, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {currency} в {currency_transfer} = {round(total_base * float(amount))}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)