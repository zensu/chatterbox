from sqlalchemy import create_engine
import json

db_inst = create_engine("sqlite:///chatterbox.db")


# engine.execute("insert into employee_of_month (emp_name) values (:emp_name)",
#                emp_name='fred')

def insert_user(db, user_id, first_name, username):
    """
    insert into users
        (user_id, first_name, username)
    values
        (189885519, 'Thomas', 'flyclave')
    """
    statement = '''
    insert into users
        (user_id, first_name, username)
    values
        (:user_id, :first_name, :username)
                '''
    conn = db.connect()
    conn.execute(statement, user_id=user_id, first_name=first_name, username=username)
    conn.close()


def update_user(db):
    conn = db.connect()
    conn.execute()
    conn.close()


def insert_list(db, user_id, list_content, private=0):
    """
    insert into lists
        (name, content, user_id, private)
    values
        ('New', '{"New": ["First", "Second"]}', 189885519, 0)
    """
    content = json.dumps(list_content)
    name = next(list_content.keys().__iter__())
    statement = '''
        insert into lists (name, content, user_id, private)
        values            (:name, :content, :user_id, :private)
                '''
    conn = db.connect()
    conn.execute(statement, name=name, content=content, user_id=user_id, private=private)
    conn.close()


def update_list(db):
    conn = db.connect()
    conn.execute()
    conn.close()


