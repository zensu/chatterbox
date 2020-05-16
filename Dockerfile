FROM centos-pybase


RUN pip3.7 install pytelegrambotapi sqlalchemy
WORKDIR /chatterbox
COPY config.py .
COPY chatterbox.db .
COPY user.py .
COPY menu.py .
COPY db_orm.py .
COPY markup.py .
COPY bot_handlers.py .
COPY main.py .

CMD ["python3.7", "main.py"]

