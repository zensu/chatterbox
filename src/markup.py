from telebot import types


def build_markup(menu=None, row_width=3):
    currentSubs = menu.currentSubs()
    currentLevel = menu.currentLevel()
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    buttons = [types.InlineKeyboardButton(callback_data=b['callback'], text=b['name']) for b in currentSubs]
    if currentSubs:
        for n in range(0, len(buttons), 2):
            try:
                markup.add(buttons[n], buttons[n+1])
            except IndexError:
                markup.add(buttons[n])
    if currentLevel != 'Main':
        markup.row(types.InlineKeyboardButton(callback_data='go_back',
                                              text='⇠ Назад'))
    return markup


def build_lists_mp(user, prefix):
    markup = types.InlineKeyboardMarkup(row_width=3)
    if prefix == 'lists':
        for item in user.db.lists:
            markup.add(types.InlineKeyboardButton(callback_data=f'{prefix}={str(item.list_id)}',
                                                  text=item.list_name))
    elif prefix == 'list_content':
        for item in user.selected_list.list_content:
            markup.add(types.InlineKeyboardButton(callback_data=f'{prefix}={str(item.content_id)}',
                                                  text=item.content))

    if user.menu.currentLevel() != 'Main':
        markup.add(types.InlineKeyboardButton(callback_data='go_back',
                                              text='⇠ Назад'))
    return markup
