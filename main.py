import telebot
from collections import defaultdict

from config import token
from logic import quiz_questions


bot = telebot.TeleBot(token)


user_responses = {} 
points = defaultdict(int)


def send_question(chat_id):
    bot.send_message(chat_id, quiz_questions[user_responses[chat_id]].get_text, reply_markup=quiz_questions[user_responses[chat_id]].gen_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    chat_id = call.message.chat.id

    if call.data == "correct":
        bot.answer_callback_query(call.id, "Answer is correct")
        points[chat_id] += 1
    elif call.data == "wrong":
        bot.answer_callback_query(call.id,  "Answer is wrong")

    bot.edit_message_reply_markup(chat_id=chat_id,message_id =call.message.message_id, reply_markup =None)

    user_responses[chat_id]+=1
    
    if user_responses[chat_id]>=len(quiz_questions):
        bot.send_message(chat_id, f"The end, {points[chat_id]}/{user_responses[chat_id]} points")
    else:
        send_question(chat_id)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in user_responses.keys():
        user_responses[message.chat.id] = 0
        send_question(message.chat.id)
    else:
        user_responses[message.chat.id] = 0
        points[message.chat.id] = 0
        send_question(message.chat.id)

bot.infinity_polling()
