FROM python:3.7
WORKDIR /opt/chatterbox
COPY ./src/ /opt/chatterbox/
RUN pip install pytelegrambotapi sqlalchemy
CMD ["python3", "main.py"]