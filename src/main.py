from bot_handlers import *
from db_orm import OrmUsers, Lists, ListContent, session
from user import User, setUserProps, users

"""
Logging Block here!
"""

# import logging
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)

[users.update({uq.user_id: User(uq.user_id,
                                uq.first_name,
                                uq.username)}) for uq in session.query(OrmUsers).all()]


@bot.message_handler(commands=['start'])
def start(message):
    text = str()
    if message.chat.id in users:
        user = users.get(message.chat.id)
    else:
        user_props = setUserProps(message)
        user_query = session.query(OrmUsers).filter_by(**user_props).first()
        if user_query:
            print('Existing user')
            user = User(user_query.user_id, user_query.first_name, user_query.username)
            users.update({message.chat.id: user})
        else:
            print('New user. Commit...')
            user = User(**user_props)
            session.add(user.db)
            session.commit()
            users.update({message.chat.id: user})
    text = text + 'Меню'
    markup = build_markup(user.menu)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(commands=['menu'])
@getuser
def menu(message, user):
    print(user)
    user.menu.previous(main_menu=True)
    markup = build_markup(user.menu)
    bot.send_message(message.chat.id, user.menu.entry.text, reply_markup=markup)

# user.selected_list = session.query(Lists).filter_by(user_id=person['user_id'], list_id=2).first()


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=123)

test_user = {'user_id': 1245555, 'first_name': 'sdfsf'}
