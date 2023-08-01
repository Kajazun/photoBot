import telebot
import sqlite3
from telebot import types

db = sqlite3.connect('server.db', check_same_thread=False)
sql = db.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER,
            photo VARCHAR(255) )''')
db.commit()


bot = telebot.TeleBot('5834768113:AAEG9EDL9oqkWzN2i41myi5KvJLxRrbA2HA')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('watch')
    btn2 = types.KeyboardButton('delete picture')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, 'This bot is designed to keep your pictures safe. Send your picture.',reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def qcel(message):
    sql.execute("INSERT INTO users (user_id, photo) VALUES (?, ?)", (message.chat.id, message.photo[0].file_id))
    db.commit()
    bot.send_message(message.chat.id,'The picture has been successfully saved with us.')
    

@bot.message_handler(content_types=['text'])
def tesnel(message):
   if message.text.lower() == 'watch':
    res = sql.execute(f"SELECT id, photo FROM users WHERE user_id = {message.chat.id}" )
    if res.fetchone() is None:
        bot.send_message(message.chat.id,"You don't have a picture yet. Upload a picture to use this feature")
    else:    
        for id,photos in sql.execute(f"SELECT id, photo FROM users WHERE user_id = {message.chat.id}" ):
                bot.send_photo(message.chat.id,photos)
                bot.send_message(message.chat.id,id)
   elif message.text.lower() == 'delete picture':
       s =  bot.send_message(message.chat.id,'Write the picture of the number you want to delete. You can write one number here.')
       bot.register_next_step_handler(s,dell)
    
     
def dell(message):
    try:
        id = int(message.text)
        sql.execute(f'DELETE FROM users WHERE id = {id}')
        db.commit()
        bot.send_message(message.chat.id,'The picture for this number has been deleted')
    except:
          bot.send_message(message.chat.id,"I'm sorry. Here you need to enter a number. Click on the delete picture button to try again")  
bot.infinity_polling()  

