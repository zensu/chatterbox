from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# engine = create_engine('sqlite:///chatterbox.db?check_same_thread=False', echo=True)
engine = create_engine('sqlite:///chatterbox.db?check_same_thread=False', echo=False)


Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


class OrmUsers(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String)
    username = Column(String)
    lists = relationship("Lists", backref="users", order_by="Lists.list_id")

    def showLists(self):
        return {l.list_name: l.list_content for l in self.lists}

    def addList(self, name):
        if isinstance(name, str):
            list_object = Lists(list_name=name)
            self.lists.append(list_object)
            session.commit()

    @staticmethod
    def renameList(selected_list, newName):
        if isinstance(selected_list, Lists) and isinstance(newName, str):
            selected_list.list_name = newName
            session.commit()

    @staticmethod
    def removeList(selected_list):
        if isinstance(selected_list, Lists):
            session.delete(selected_list)
            session.commit()

    def __repr__(self):
        return f'<User {self.user_id}, {self.first_name}, {self.username}>'


class Lists(Base):
    __tablename__ = 'lists'

    list_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    list_name = Column(String, nullable=False)
    list_content = relationship("ListContent", backref="lists")
    private = Column(Integer, default=0)

    def addContent(self, content):
        if isinstance(content, str):
            list_content = ListContent(content=content)
            self.list_content.append(list_content)
            session.commit()

    def removeContent(self, content_id, list_id=None):
        if isinstance(content_id, int):
            index = [c.content_id for c in self.list_content].index(content_id)
            content_delete = self.list_content.pop(index)
            session.delete(content_delete)
            session.commit()

    def getContent(self, content_id):
        if isinstance(content_id, int):
            cont = {c.content_id: c.content for c in self.list_content}
            if content_id in cont:
                return cont.get(content_id)
                
            

    def __repr__(self):
        return f'<Lists {self.list_id}, {self.user_id}, {self.list_name}>'


class ListContent(Base):
    __tablename__ = 'list_content'

    content_id = Column(Integer, primary_key=True, nullable=False)
    list_id = Column(ForeignKey('lists.list_id'), nullable=False)
    content = Column(String, nullable=True)

    def __repr__(self):
        return f'<ListContent, {self.content}, {self.content_id}>'


Base.metadata.create_all(engine)


def getUserObject(**kwargs):
    """
    :parameter
    *user_id: int(), first_name: string(), *username: string()
    """
    return session.query(OrmUsers).filter_by(**kwargs).first()


def getListObject(**kwargs):
    """
    :parameter
    *list_id: int(), *user_id: int(), *list_name: string()
    """
    return session.query(Lists).filter_by(**kwargs).first()





