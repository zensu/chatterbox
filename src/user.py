import telebot
from menu import MenuEntry, Menu, menu_scheme
from db_orm import OrmUsers, Lists, session


class User:
    def __init__(self, user_id=None, first_name=None, username=None):
        self.username = username
        self.first_name = first_name
        self.user_id = user_id
        self.menu = Menu()
        self.selected_list = None
        self.db = self._addUser()

    def _addUser(self):
        props = {}
        props.update({'first_name': self.first_name}) if self.first_name else props
        props.update({'username': self.username}) if self.username else props
        if not session.query(OrmUsers).filter_by(user_id=self.user_id, **props).first():
            db = OrmUsers(user_id=self.user_id, **props)
        else:
            db = session.query(OrmUsers).filter_by(user_id=self.user_id,
                                                   **props).first()
        return db

    def addList(self, message, bot, call, markup):
        self.db.addList(message.text)
        bot.edit_message_text(text=f'Список \'{message.text}\' создан',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markup)
        bot.delete_message(chat_id=message.chat.id,
                           message_id=message.message_id)

    def renameList(self, message, bot, call, markup):
        self.db.renameList(self.selected_list, message.text)
        bot.edit_message_text(text=f'\'{self.selected_list.list_name}\' переименован в \'{message.text}\'',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markup)
        bot.answer_callback_query(call.id,
                                  f'\'{self.selected_list.list_name}\' переименован в \'{message.text}\'',
                                  cache_time=5)
        bot.delete_message(chat_id=message.chat.id,
                           message_id=message.message_id)

    def removeList(self):
        self.db.removeList(self.selected_list)

    def addContent(self, message, bot, call, markup):
        self.selected_list.addContent(message.text)
        bot.edit_message_text(text=f'\'{message.text}\' добавлен в список \'{self.selected_list.list_name}\'',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markup)
        bot.delete_message(chat_id=message.chat.id,
                           message_id=message.message_id)

    def selectList(self, list_id):
        return session.query(Lists).filter_by(user_id=self.user_id, list_id=list_id).first()


def instance_type(teletype):
    if isinstance(teletype, telebot.types.Message):
        return teletype
    elif isinstance(teletype, telebot.types.CallbackQuery):
        return teletype.message


users = {}


def getuser(func):
    def wrap(*args):
        message = instance_type(args[0])
        if message.chat.id in users:
            user = users.get(message.chat.id)
        else:
            user = None
        func(args[0], user)
    return wrap


def setUserProps(teletype):
    message = instance_type(teletype)
    props = dict()
    props.update({'username': message.chat.username}) if message.chat.username else props
    props.update({'first_name': message.chat.first_name}) if message.chat.first_name else props
    props.update({'user_id': message.chat.id})
    return props



#
# users = {}
#
#
# def instance_type(teletype):
#     if isinstance(teletype, telebot.types.Message):
#         message = teletype
#     elif isinstance(teletype, telebot.types.CallbackQuery):
#         message = teletype.message
#     return message
#
#
# def get_user_props(teletype):
#     message = instance_type(teletype)
#     username = message.chat.username
#     first_name = message.chat.first_name
#     user_id = message.chat.id
#     return user_id, first_name, username
#
#
# def userwrap(func):
#     def wrap(*args):
#         if isinstance(args[0], telebot.types.Message):
#             user = users[args[0].chat.id]
#         elif isinstance(args[0], telebot.types.CallbackQuery):
#             user = users[args[0].message.chat.id]
#         func(args[0], user)
#     return wrap
#
#
# # class User(UserObject):
# #     def __init__(self, user_id=None, first_name=None, username=None):
# #         self.username = username
# #         self.first_name = first_name
# #         self.user_id = user_id
# #         self.menu = Menu()
# #         self.selected_list = None
#
#
# class Userok:
#     def __init__(self, user_id=None, first_name=None, username=None):
#         self.username = username
#         self.first_name = first_name
#         self.user_id = user_id
#         self.menu = Menu()
#         self.selected_list = None
#         self.lists = {'Default': ['PlayStation 4'], 'Example': ['Audi A5', 'Mazda CX-5']}
#
#     def user_props(self):
#         return f'{self.user_id}, {self.first_name}, {self.username}'
#
#     def add_to_list(self, message, bot, call, markup):
#         self.lists[self.selected_list].append(message.text)
#         bot.edit_message_text(text=f'\'{message.text}\' добавлен в список {self.selected_list}',
#                               chat_id=call.message.chat.id,
#                               message_id=call.message.message_id)
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id,
#                                       message_id=call.message.message_id,
#                                       reply_markup=markup)
#
#     def create_new_list(self, message, bot, call, markup):
#         if message.text.lower() not in [x.lower() for x in self.lists.keys()]:
#             self.lists[message.text] = []
#             bot.edit_message_text(text=f'Список \'{message.text}\' создан.',
#                                   chat_id=call.message.chat.id,
#                                   message_id=call.message.message_id)
#             bot.edit_message_reply_markup(chat_id=call.message.chat.id,
#                                           message_id=call.message.message_id,
#                                           reply_markup=markup)
#         else:
#             bot.edit_message_text(text=f'\'{message.text}\' уже существует.',
#                                   chat_id=call.message.chat.id,
#                                   message_id=call.message.message_id)
#             bot.edit_message_reply_markup(chat_id=call.message.chat.id,
#                                           message_id=call.message.message_id,
#                                           reply_markup=markup)
#
#     def remove_list(self):
#         if self.selected_list.lower() in [x.lower() for x in self.lists.keys()]:
#             self.lists.pop(self.selected_list)
#             self.selected_list = None
#
#     def rename_list(self, message, bot, call, markup):
#         if self.selected_list.lower() in [x.lower() for x in self.lists.keys()]:
#             temp = self.lists[self.selected_list]
#             self.lists[message.text] = temp
#             self.lists.pop(self.selected_list)
#             bot.edit_message_text(text=f'\'{self.selected_list}\' переименован в \'{message.text}\'',
#                                   chat_id=call.message.chat.id,
#                                   message_id=call.message.message_id)
#             bot.edit_message_reply_markup(chat_id=call.message.chat.id,
#                                           message_id=call.message.message_id,
#                                           reply_markup=markup)
#             bot.answer_callback_query(call.id, f'\'{self.selected_list}\' переименован в \'{message.text}\'')
#             self.selected_list = message.text
#
#     def remove_wish(self, wish):
#         wish_index = self.lists[self.selected_list].index(wish)
#         self.lists[self.selected_list].pop(wish_index)
#
#     def __str__(self):
#         return str(self.user_id)
