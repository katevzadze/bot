from telebot import TeleBot
from telebot.types import Message
from dotenv import load_dotenv
import os
from datetime import datetime

# загрузка переменных окружения
load_dotenv('.env')
TG_TOKEN = os.getenv('TG_TOKEN')

# сохраняем инициализированный объект бота
bot = TeleBot(TG_TOKEN)

# хранилище данных пользователей
tasks: list[list[str]] = []

# Task class


class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        self.tags = []
    def add_tag(self, tag):
        self.tags.append(tag)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message) -> None:
    """
    Отправляет приветственное сообщение
    """
    welcome_text = """
    Привет! Я бот для управления задачами. Вот как со мной работать:
    - Чтобы добавить задачу, отправьте /add_task Номер. Название. Описание. Тег (при необходимости)
    - Чтобы посмотреть ваши задачи, отправьте /show_tasks
    - Чтобы удалить задачу, отправьте /delete_task Номер задачи
    - Чтобы удалить все задачи, отправьте /delete_all_tasks
    - Чтобы посмотреть эту памятку снова, отправьте /help
"""
    user_id: int = message.from_user.id
    bot.send_message(user_id, welcome_text)


@bot.message_handler(commands=['add_task'])
def add_task(message: Message) -> None:
    """Обрабатывает команду добавления задачи"""
    user_id: int = message.chat.id
    text: str = message.text[9:].strip()  # берем слайс после "/add_task"
    title = message.text.split(" ", 1)[1]
    description = message.text.split(" ", 2)[2]
    if not text:
        bot.send_message(user_id, 'Вы не ввели текст задачи. Памятка: /help')
        return
    else:
        tags = message.text.split("/tag")[1]
        tags = tags.split()
        task = Task(title, description)
        for tag in tags:
            task.add_tag(tag)
        time_message = f'{task.time} - {task}'
        bot.send_message(user_id, 'Задача добавлена!')

        tasks_parts = time_message.split('.')
        tasks.append(tasks_parts)


@bot.message_handler(commands=['show_tasks'])
def show_tasks(message: Message) -> None:
    """Выводит все текущие задачи пользователя"""
    user_id: int = message.chat.id
    message_text = 'Ваши задачи:\n'
    for i, task in enumerate(tasks, start=1):
        message_text += f"{i+1}. {task.title}\n{task.description}\n\n"
        if task.tags:
          message_text += "Теги:\n"
          for tag in task.tags:
             message_text += f"- {tag}\n"
    
    message_text += "\n"

    bot.send_message(user_id, message_text)


@bot.message_handler(commands=['delete_task'])
def delete_task(message: Message) -> None:
    """Удаляет задачу по номеру"""
    user_id: int = message.chat.id
    task_number: int = int(message.text[12:].strip())
    if task_number < 1 or task_number > len(tasks):
        bot.send_message(user_id, 'Вы ввели неверный номер задачи.')
        return
    else:
        del tasks[task_number - 1]
        bot.send_message(user_id, 'Задача удалена!')
        return


@bot.message_handler(commands=['delete_all_tasks'])
def delete_all_tasks(message: Message) -> None:
    """Удаляет все задачи пользователя"""
    user_id: int = message.chat.id
    tasks.clear()
    bot.send_message(user_id, 'Все задачи удалены!')
    return


if __name__ == '__main__':
    bot.infinity_polling()
