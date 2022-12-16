from telebot import TeleBot, types
from requests import get
from random import randint
from translate import Translator
from pyjokes import get_joke
from time import sleep

translator = Translator('ru')

call_data = {
    '🦊 Фурри': ['https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed', '.jpg'],
    '🌙 Ночь': ['https://firebasestorage.googleapis.com/v0/b/thisnightskydoesnotexist.appspot.com/o/images%2Fseed', '.jpg?alt=media'],
    '🏞 Берег': ['https://thisbeachdoesnotexist.com/data/seeds-075/', '.jpg'],
    '🌌 Картина': ['https://thisartworkdoesnotexist.com/', 'art.jpg'],
    '🏴 Флаг': ['https://thisflagdoesnotexist.com/images/', '.png'],
    '🐸 Пепе': ['http://www.thispepedoesnotexist.co.uk/out/pepe%20(', ').png'],
    '💡 Идея': 'https://thisideadoesnotexist.com/'
}

# Setting bot
bot = TeleBot("5752526717:AAHt_iHNQ8zaBlsF2PkyNpK1mlkP7kqbjtc", parse_mode=None)


def get_markup(names):

    markup = types.ReplyKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(name) for name in names]
    for button in buttons:
        markup.add(button)
    return markup

markup = types.ReplyKeyboardMarkup()
btn1 = types.InlineKeyboardButton('🦊 Фурри')
btn2 = types.InlineKeyboardButton('🌙 Ночь')
btn3 = types.InlineKeyboardButton('🏞 Берег')
btn4 = types.InlineKeyboardButton('🌌 Картина')
btn5 = types.InlineKeyboardButton('🏴 Флаг')
btn6 = types.InlineKeyboardButton('🐸 Пепе')
btn7 = types.InlineKeyboardButton('😂 Шутка')
btn8 = types.InlineKeyboardButton('💡 Идея')
markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    print('Got photo from ' + message.from_user.username + '...')
    print('Sending to Snakes3Ladders...')
    bot.forward_message(2045352843, message.from_user.id, message.id)
    print('Message sent!')
    print('--------------------------------')


@bot.message_handler(commands=['start', 'file', 'help', 'joke', 'idea'])
def get_commands(message):
    file_r = open('user_data.csv', 'r')
    file_a = open('user_data.csv', 'a')
    user_id = message.from_user.id
    lines = file_r.readlines()
    if f'{user_id},{message.from_user.username}\n' in lines:
        write = True
    else:
        write = False

    if not write:
        file_a.write(f'{user_id},{message.from_user.username}\n')
    if message.text == '/file':
        if message.from_user.id == 2045352843:
            for line in lines:
                bot.send_message(user_id, line)
        else:
            bot.reply_to(message, 'У вас нет прав для использования команд разработчика🖥')
    elif message.text == '/start':
        bot.send_message(user_id, 'Привет!')
        sleep(0.5)
        bot.send_message(user_id, 'Я бот для генерации картинок и шуток!')
        sleep(0.5)
        bot.send_message(user_id, 'Что хочешь сгенерировать?', reply_markup=markup)
    elif message.text == '/joke':
        bot.send_message(message.from_user.id, get_joke(category='all'))
    elif message.text == '/idea':
        response = get(call_data['💡 Идея'])
        # soup = BeautifulSoup(response.text, 'html.parser')
        # idea = soup.find('h2')
        idea = response.text.split('<h2>')[1].split('</h2>')[0]
        bot.send_message(user_id, f'Гениальная идея!\n{translator.translate(idea)}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = message.from_user.id
    try:
        print('started')
        if message.text == '😂 Шутка':
            bot.send_message(user_id, get_joke(category='all'))
        elif message.text == '💡 Идея':
            response = get(call_data['💡 Идея'], stream=True)
            idea = response.text.split('<h2>')[1].split('</h2>')[0]
            bot.send_message(user_id, f'Гениальная идея!\n{translator.translate(idea)}')
            print('ended')
        elif message.text == '🌌 Картина':
            response = get(call_data['🌌 Картина'][0], stream=True)
            print(call_data['🌌 Картина'][0])
            bot.send_photo(user_id, response.raw)
            print('ended \n--------------------------------')
        elif message.text == "🦊 Фурри":
            response = get(f"{call_data['🦊 Фурри'][0]}{randint(10000, 99999)}{call_data['🦊 Фурри'][1]}", stream=True)
            print(f"{call_data['🦊 Фурри'][0]}{randint(10000, 99999)}{call_data['🦊 Фурри'][1]}")
            bot.send_photo(user_id, response.raw)
            print('ended \n--------------------------------')
        elif message.text in call_data.keys():
            response = get(f"{call_data[message.text][0]}{randint(1000, 9999)}{call_data[message.text][1]}", stream=True)
            print(f"{call_data[message.text][0]}{randint(1000, 5001)}{call_data[message.text][1]}")
            bot.send_photo(user_id, response.raw)
            print('ended \n--------------------------------')
        else:
            bot.send_message(user_id, 'Я тебя не понял. Напиши /start')
    except:
        get_text_messages(message)


print('--------------------------------')
bot.infinity_polling()
