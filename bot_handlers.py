import telebot
from config import token
from user import setUserProps, getuser, instance_type
from markup import *


bot = telebot.TeleBot(token)


def send_payload(call_type, text, markup, next_func=None):
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


@bot.callback_query_handler(func=lambda call: True)
@getuser
def base(call, user):
    print('called', call.data)
    if call.data == 'my_lists':
        text = f'Выберите список:'
        user.menu.next(0, text)
        markup = build_lists_mp(user, prefix='lists')
        send_payload(call, text, markup)

    elif call.data == 'create_list':
        text = f'Введите название для вашего списка:'
        user.menu.next(1, text)
        markup = build_markup(user.menu)
        send_payload(call, text, markup, next_func=user.addList)

    elif call.data == 'add_wish':
        text = f'Введите желание:'
        user.menu.next(0, text)
        markup = build_markup(user.menu)
        send_payload(call, text, markup, next_func=user.addContent)

    elif call.data == 'rm_wish':
        text = f'Выберите какое желание хотите удалить.'
        user.menu.next(2, text)
        markup = build_lists_mp(user, prefix='list_content')
        send_payload(call, text, markup)

    elif call.data == 'list_content':
        text = '\n'.join(['- ' + x.content for x in user.selected_list.list_content])
        content_list = f'{str(user.selected_list.list_name)}:\n' + text
        user.menu.next(1, text)
        markup = build_markup(user.menu)
        send_payload(call, content_list, markup)

    elif call.data == 'rename_list':
        text = f'Введите новое название для списка \'{user.selected_list.list_name}\''
        user.menu.next(3, text)
        markup = build_markup(user.menu)
        send_payload(call, text, markup, next_func=user.renameList)

    elif call.data == 'remove_list':
        text = f'Confirm deleting \'{user.selected_list.list_name}\'?'
        user.menu.next(4, text)
        markup = build_markup(user.menu)
        send_payload(call, text, markup)

    elif call.data == 'confirm_rm':
        text = f'Список \'{user.selected_list.list_name}\' удален.'
        user.menu.previous(-3)
        user.removeList()
        markup = build_markup(user.menu)
        send_payload(call, text, markup)
        bot.answer_callback_query(call.id, text=f'{user.selected_list.list_name} удален!', cache_time=5)

    elif call.data == 'abort_rm':
        user.menu.previous()
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        send_payload(call, user.menu.currentLevel(), build_markup(user.menu))

    elif call.data.startswith('lists='):
        list_id = int(call.data.split('=')[1])
        print(f'list_id={list_id}')
        user.selected_list = user.selectList(list_id=list_id)
        text = f'Выбранный список: \'{user.selected_list.list_name}\'.'
        user.menu.next(0)
        markup = build_markup(user.menu)
        send_payload(call, text, markup)

    elif call.data.startswith('list_content='):
        text = f'Выберите какое желание хотите удалить.'
        wish_id = int(call.data.split('=')[1])
        user.selected_list.removeContent(wish_id)
        wish_name = user.selected_list.getContent(wish_id)
        markup = build_lists_mp(user, 'list_content')
        bot.answer_callback_query(call.id, f'\'{wish_name}\' удален!', cache_time=5)
        send_payload(call, text, markup)

    elif call.data == 'go_back':
        if user.menu.superEnd is False:
            user.menu.previous()
            print('Now', user.menu.currentLevel(), user.menu.currentSubs()[0]['callback'])
            if user.menu.currentSubs()[0]['callback'] == 'options':
                markup = build_lists_mp(user, 'lists')
            else:
                markup = build_markup(user.menu)
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
