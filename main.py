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
    if call.data == "correct":
        bot.answer_callback_query(call.id, "Answer is correct")
        points[call.message.chat.id] += 1
    elif call.data == "wrong":
        bot.answer_callback_query(call.id,  "Answer is wrong")

    user_responses[call.message.chat.id]+=1
    
    if user_responses[call.message.chat.id]>=len(quiz_questions):
        bot.send_message(call.message.chat.id, f"The end, {points[call.message.chat.id]}/{user_responses[call.message.chat.id]} points")
    else:
        send_question(call.message.chat.id)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in user_responses.keys():
        user_responses[message.chat.id] = 0
        send_question(message.chat.id)


bot.infinity_polling()
