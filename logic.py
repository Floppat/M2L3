from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

class Question:

    def __init__(self, text, answer_id, *options):
        self.__text = text
        self.__answer_id = answer_id
        self.options = options

    @property
    def get_text(self):
        return self.__text
    @property
    def get_answer_id(self):
        return self.__answer_id
    def gen_markup(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = len(self.options)

        for i, option in enumerate(self.options):
            if i == self.__answer_id:
                markup.add(InlineKeyboardButton(option, callback_data='correct'))
            else:
                markup.add(InlineKeyboardButton(option, callback_data='wrong'))

        return markup

class Multiple_Answer_Question(Question):
    def __init__(self, text, answer_id: list, *options):
        super().__init__(text, answer_id, *options)

    def gen_markup(self):  
        markup = InlineKeyboardMarkup()
        markup.row_width = len(self.options)

        for i, option in enumerate(self.options):
                if i in super().get_answer_id:
                    markup.add(InlineKeyboardButton(option, callback_data='correct'))
                else:
                    markup.add(InlineKeyboardButton(option, callback_data='wrong'))
                    
        return markup

quiz_questions = [
    Question("Что котики делают, когда никто их не видит?", 1, "Спят", "Пишут мемы"),
    Question("Как котики выражают свою любовь?", 0, "Громким мурлыканием", "Отправляют фото на Instagram", "Гавкают"),
    Question("Какие книги котики любят читать?", 3, "Обретение вашего внутреннего урр-мирения", "Тайм-менеджмент или как выделить 18 часов в день для сна", "101 способ уснуть на 5 минут раньше, чем хозяин", "Пособие по управлению людьми"),
    Multiple_Answer_Question("Вы любите котиков?",[0,1,2],"да","да","да")
]
