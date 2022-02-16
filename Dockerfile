FROM python:3.8-slim-buster

WORKDIR /project
COPY . .
RUN python -m pip install --upgrade pip \
           && pip install python-dotenv \
           && pip install pyTelegramBotAPI

CMD [ "python3", "app/bot.py"]