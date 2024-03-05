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


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    def __str__(self):
        return f'{self.name} - {self.price} руб.- {self.date}'


class Client:
    def __init__(self, first_name, last_name, birthday, card_id):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.card_id = card_id
        self.products = []


clients = []


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message) -> None:
    """
    Отправляет приветственное сообщение
    """
    welcome_text = """
    Привет! Я бот для учета клиентов магазина. Вот как со мной работать:
    - Чтобы добавить клиента, отправьте /add_client Имя. Фамилия. Дата рождения. ID карты
    - Чтобы посмотреть всех клиентов, отправьте /show_clients
    - Чтобы добавить продукт клиенту, отправьте /add_product ID карты клиента. Название. Цена
    - Чтобы посмотреть продукты клиента, отправьте /show_products ID карты клиента
    - Чтобы удалить клиента, отправьте /delete_client ID карты клиента
    - Чтобы удалить все клиенты, отправьте /delete_all_clients
    - Чтобы посмотреть эту памятку снова, отправьте /help
"""
    user_id: int = message.from_user.id
    bot.send_message(user_id, welcome_text)


@bot.message_handler(commands=['add_client'])
def add_client(message: Message) -> None:
    user_id: int = message.chat.id
    client_info = message.text[12:].split('.')
    if len(client_info) != 4:
        bot.send_message(user_id, 'Вы ввели неверные данные.')
        return
    else:
        client = Client(client_info[0], client_info[1],
                        client_info[2], client_info[3])
        bot.send_message(user_id, 'Клиент добавлен!')
        clients.append(client)
        return


@bot.message_handler(commands=['show_clients'])
def show_clients(message: Message) -> None:
    user_id: int = message.chat.id
    message_text = 'Все клиенты:\n'
    for client in clients:
        message_text += f"{client.card_id} - {client.first_name} {client.last_name} - {client.birthday}\n"
    message_text += "\n"
    bot.send_message(user_id, message_text)


@bot.message_handler(commands=['add_product'])
def add_product(message: Message) -> None:
    user_id: int = message.chat.id
    product_info = message.text[13:].split('.')
    if len(product_info) != 3:
        bot.send_message(user_id, 'Вы ввели неверные данные.')
        return
    else:
        for client in clients:
            if client.card_id == product_info[0]:
                product = Product(product_info[1], product_info[2])
                client.products.append(product)
                bot.send_message(user_id, 'Продукт добавлен!')
                return
        bot.send_message(user_id, 'Клиента с таким ID карты не существует.')


@bot.message_handler(commands=['show_products'])
def show_products(message: Message) -> None:
    user_id: int = message.chat.id
    product_id = message.text[14:].strip()
    for client in clients:
        if client.card_id == product_id:
            message_text = f'{client.first_name} {client.last_name} - {client.birthday}\n'
            for product in client.products:
                message_text += f"{product}\n"
            message_text += "\n"
            bot.send_message(user_id, message_text)
            return
    bot.send_message(user_id, 'Клиента с таким ID карты не существует.')


@bot.message_handler(commands=['delete_client'])
def delete_client(message: Message) -> None:
    user_id: int = message.chat.id
    client_id = message.text[14:].strip()
    for client in clients:
        if client.card_id == client_id:
            clients.remove(client)
            bot.send_message(user_id, 'Клиент удален!')
            return
    bot.send_message(user_id, 'Клиента с таким ID карты не существует.')


@bot.message_handler(commands=['delete_all_clients'])
def delete_all_clients(message: Message) -> None:
    user_id: int = message.chat.id
    clients.clear()
    bot.send_message(user_id, 'Все клиенты удалены!')


if __name__ == '__main__':
    bot.infinity_polling()
