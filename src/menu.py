from collections import OrderedDict

menu_scheme = OrderedDict()

menu_scheme = \
    {'name': 'Main', 'callback': 'home', 'text': 'Главное меню', 'index': 0, 'submenu': [
        {'name': 'Списки', 'callback': 'my_lists', 'text': '', 'index': 0, 'submenu': [
            {'name': 'Опции списка', 'callback': 'options', 'text': '', 'index': 0, 'submenu': [
                {'name': 'Добавить желание', 'callback': 'add_wish', 'text': '', 'index': 0, 'submenu': []},
                {'name': 'Показать список', 'callback': 'list_content', 'text': '', 'index': 1, 'submenu': []},
                {'name': 'Удалить желание', 'callback': 'rm_wish', 'text': '', 'index': 2, 'submenu': []},
                {'name': 'Переименовать список', 'callback': 'rename_list', 'text': '', 'index': 3, 'submenu': []},
                {'name': 'Удалить список', 'callback': 'remove_list', 'text': '', 'index': 4, 'submenu': [
                    {'name': 'Yes', 'callback': 'confirm_rm', 'text': 'да', 'index': 0, 'submenu': []},
                    {'name': 'No', 'callback': 'abort_rm', 'text': 'нет', 'index': 0, 'submenu': []}]}
                                                                                    ]
             }
                                                                            ]
         },
        {'name': 'Создать новый список', 'callback': 'create_list', 'index': 1, 'submenu': []},
        {'name': 'Узнать желания друга', 'callback': 'obtain_public', 'index': 2, 'submenu': [
            {'name': 'Списки друга', 'callback': 'obtain_lists', 'text': '', 'index': 0, 'submenu': [
                {'name': 'Желания друга', 'callback': 'obtain_wishes', 'text': '', 'index': 0, 'submenu': []}
            ]}
        ]}
                                                                ]
     }


class MenuEntry:
    def __init__(self, level, text, subLevel, superLevel=[]):
        self.level = level
        self.text = text
        self.subLevel = subLevel
        self.superLevel = superLevel

    def get_text(self):
        return self.text

    def __repr__(self):
        return f'<<<Entry - {self.level}>>>'


class Menu:
    def __init__(self):
        self.entry = MenuEntry(menu_scheme['name'], menu_scheme['text'], menu_scheme['submenu'])
        self.superEnd = False

    def next(self, ind, text=None):
        print(self.entry)
        if text:
            self.entry.subLevel[ind]['text'] = text
        else:
            self.entry.subLevel[ind]['text'] = self.entry.subLevel[ind]['name']
        print('Text in entry:', text)
        self.entry.superLevel.append(self.entry)
        self.entry = MenuEntry(self.entry.subLevel[ind]['name'],
                               self.entry.subLevel[ind]['text'],
                               self.entry.subLevel[ind]['submenu'],
                               self.entry.superLevel)
        print(self.entry)
        print(f'Current menu entry {self.entry.level}\n')

    def previous(self, step=-1, main_menu=False):
        if self.entry.superLevel:
            if step < -1:
                for s in range(-1, step, -1):
                    self.entry = self.entry.superLevel.pop(s)
            elif main_menu is True:
                self.entry = MenuEntry(menu_scheme['name'], menu_scheme['text'], menu_scheme['submenu'])
                self.superEnd = False
            else:
                self.entry = self.entry.superLevel.pop(step)
            print(f'Current menu entry {self.entry.level}\n')

    def currentSubs(self):
        return self.entry.subLevel

    def currentLevel(self):
        return self.entry.level

    def currentText(self):
        return self.entry




