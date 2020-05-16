import telebot
from config import token
from user import User, get_user_props, getuser, users, instance_type
from telebot import types


bot = telebot.TeleBot(token)


def build_markup(currentSubs=None, currentLevel=None, row_width=3):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    buttons = [types.InlineKeyboardButton(callback_data=b['callback'], text=b['name']) for b in currentSubs]
    if currentSubs:
        for n in range(0, len(buttons), 2):
            try:
                markup.add(buttons[n], buttons[n+1])
            except IndexError:
                markup.add(buttons[n])

    # buttons = [types.InlineKeyboardButton(callback_data=b['callback'], text=b['name']) for b in currentSubs]
    # mp = []
    # while buttons:
    #     mp.append(buttons[:2])
    #     try:
    #         buttons.pop(0)
    #         buttons.pop(0)
    #     except IndexError:
    #         break

    if currentLevel != 'Main':
        markup.row(types.InlineKeyboardButton(callback_data='go_back',
                                              text='⇠ Назад'))
    return markup


def build_lists_mp(user, prefix):
    markup = types.InlineKeyboardMarkup(row_width=3)
    if prefix == 'select=':
        for item in user.lists.keys():
            markup.add(types.InlineKeyboardButton(callback_data=f'{prefix}'+item,
                                                  text=item))
    elif prefix == 'wish=':
        for item in user.lists[user.selected_list]:
            markup.add(types.InlineKeyboardButton(callback_data=f'{prefix}' + item,
                                                  text=item))
    if user.menu.currentLevel() != 'Main':
        markup.add(types.InlineKeyboardButton(callback_data='go_back',
                                              text='⇠ Назад'))
    return markup


def send_payload(call_type, text, markup, next_func=None):
    print('_')
    call = instance_type(call_type)
    message = bot.edit_message_text(text=text,
                                    chat_id=call.chat.id,
                                    message_id=call.message_id)
    bot.edit_message_reply_markup(chat_id=call.chat.id,
                                  message_id=call.message_id,
                                  reply_markup=markup)
    if next_func is not None:
        print('handler step', text)
        bot.register_next_step_handler(message, next_func, bot, call_type, markup)


@bot.message_handler(commands=['start'])
def start(message):
    text = ''
    if message.chat.id not in users:
        user = User(*get_user_props(message))
        users[user.user_id] = user
        text = f'Добро пожаловать, {user.first_name if user.first_name else user.username}\n'
    else:
        user = users.get(message.chat.id)
    text = text+'Меню'
    markup = build_markup(user.menu.currentSubs(), user.menu.currentLevel())
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(commands=['menu'])
@getuser
def menu(message, user):
    print(user)
    markup = build_markup(user.menu.currentSubs(), user.menu.currentLevel())
    bot.send_message(message.chat.id, user.menu.entry.text(), reply_markup=markup)
    user.menu.previous(main_menu=True)


@bot.callback_query_handler(func=lambda call: True)
@getuser
def base(call, user):
    print('called', call.data)
    if call.data == 'my_lists':
        text = f'Выберите список:'
        user.menu.next(0, text)
        markup = build_lists_mp(user, 'select=')
        send_payload(call, text, markup)

    elif call.data == 'create_list':
        text = f'Введите название для вашего списка:'
        user.menu.next(1, text)
        markup = build_markup(user.menu.currentSubs(), user.menu.currentLevel())
        send_payload(call, text, markup, next_func=user.create_new_list)

    elif call.data == 'add_wish':
        text = f'Введите желание:'
        user.menu.next(0, text)
        markup = build_markup(user.menu.currentSubs(), user.menu.currentLevel())
        send_payload(call, text, markup, next_func=user.add_to_list)

    elif call.data == 'rm_wish':
        text = f'Выберите какое желание хотите удалить.'
        user.menu.next(2, text)
        markup = build_lists_mp(user, prefix='wish=')
        send_payload(call, text, markup)

    elif call.data == 'list_content':
        text = '\n'.join(['- ' + x for x in user.lists.get(user.selected_list)])
        content_list = f'{user.selected_list}:\n' + text
        user.menu.next(1, text)
        markup = build_markup(user.menu.currentSubs(), user.menu.currentLevel())
        send_payload(call, content_list, markup)

    elif call.data == 'rename_list':
        text = f'Введите новое название для списка \'{user.selected_list}\''
        user.menu.next(3, text)
        markup = build_markup(user.menu.currentSubs(), user.menu.currentLevel())
        send_payload(call, text, markup, next_func=user.rename_list)

    elif call.data == 'remove_list':
        text = f'Confirm deleting \'{user.selected_list}\'?'
        user.menu.next(4, text)
        markup = build_markup(user.menu.currentSubs(), user.menu.currentLevel())
        send_payload(call, text, markup)

    elif call.data == 'confirm_rm':
        text = f'Список \'{user.selected_list}\' удален.'
        user.menu.previous(-3)
        user.remove_list()
        markup = build_markup(user.menu.currentSubs(), user.menu.currentLevel())
        send_payload(call, text, markup)
        bot.answer_callback_query(call.id, text=f'{user.selected_list} удален!', cache_time=5)

    elif call.data == 'abort_rm':
        user.menu.previous()
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        send_payload(call, user.menu.currentLevel(),
                     build_markup(user.menu.currentSubs(),
                                  user.menu.currentLevel()))
    elif call.data.startswith('select='):
        user.selected_list = call.data.split('=')[1]
        text = f'Выбранный список: \'{user.selected_list}\'.'
        user.menu.next(0, text)
        markup = build_markup(user.menu.currentSubs(), user.menu.currentLevel())
        send_payload(call, text, markup)
    elif call.data.startswith('wish='):
        text = f'Выберите какое желание хотите удалить.'
        wish = call.data.split('=')[1]
        user.remove_wish(wish)
        markup = build_lists_mp(user, 'wish=')
        bot.answer_callback_query(call.id, f'\'{wish}\' удален!', cache_time=5)
        send_payload(call, text, markup)
    elif call.data == 'go_back':
        # print(user.menu.entry.superLevel[-1])
        if user.menu.superEnd is False:
            user.menu.previous()
            print('Now', user.menu.currentLevel(), user.menu.currentSubs()[0]['callback'])
            if user.menu.currentSubs()[0]['callback'] == 'options':
                markup = build_lists_mp(user, 'select=')
            else:
                markup = build_markup(user.menu.currentSubs(), user.menu.currentLevel())
                print(user.menu.entry.text)
            bot.edit_message_text(text=user.menu.entry.text,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=markup)
        else:
            pass
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)


bot.polling(none_stop=True, timeout=1000)

