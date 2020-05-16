from db_orm import OrmUsers, Lists, ListContent, session
from menu import Menu


class User:
    def __init__(self, user_id=None, first_name=None, username=None):
        self.db = session.query(OrmUsers).filter_by(user_id=user_id,
                                                    first_name=first_name,
                                                    username=username).first()
        self.username = username
        self.first_name = first_name
        self.user_id = user_id
        self.menu = Menu()
        self.selected_list = None


person = {'username': 'flyclave', 'first_name': 'Thomas', 'user_id': 189885519}

user_query = session.query(OrmUsers).filter_by(**person).first()
if user_query:
    user = User(user_query.user_id, user_query.first_name, user_query.username)
    print('Existing user')
else:

    user = User(**person)
    session.add(user)
    session.commit()
    print('New user. Commit...')

print(user)

user.selected_list = session.query(Lists).filter_by(user_id=person['user_id'], list_id=2).first()

# user.addList(Lists(user_id=user.user_id, list_name='Cars'))

# selected_list = session.query(Users).filter_by(user_id=user_id, list_id=1, list_name='Cars').first()

# selected_list.addContent('Mazda CX-5 2016 Restyle')

person = {'username': 'flyclave', 'first_name': 'Thomas', 'user_id': 189885519}

user_query = session.query(OrmUsers).filter_by(**person).first()

user = User(user_query.user_id, user_query.first_name, user_query.username)

