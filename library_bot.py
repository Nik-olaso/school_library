import aiogram
import pandas
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from collections import Counter


BOT_TOKEN = '6850075516:AAHYQ4GFzf6_gdONnQ1d5nUwHnp2mONVJyU'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


books = pandas.read_excel('Книга.xlsx', na_values=[' '], keep_default_na=False)
books_dict = books.to_dict(orient='records')


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ – бот для поиска книг по библиотеке 156-ой школы\nНапиши мне одну первую букву фамилии автора, а я выведу все подходящие')


@dp.message()
async def send_echo(message: Message):
    if len(message.text) == 1: 
        try:
            author_letter = []
            for author in books_dict:
                if author['Автор '][:1] == message.text.upper():
                    if author['Автор '] not in author_letter:
                        author_letter.append(author['Автор '])
            author_letter = sorted(author_letter)
            await message.reply(text='\n'.join(author_letter))
            await message.reply(text="Напишите имя автора, чьи книги вы хотите узнать так, как написано в строке выше!")
        except aiogram.exceptions.TelegramBadRequest:
            await message.reply(text="На эту букву не найдено ни одной фамилии. Попробуйте ввести другую.")
    else:
        try:
            books_name = []
            for book in books_dict:
                if book['Автор '] == message.text:
                    books_name.append(book['Название '])
            counted_books = Counter(books_name)
            books = []
            for book in books_name:
                books.append(f'{book} – {counted_books[book]} штук')
            books = sorted(list(set(books)))
            await message.reply(text='\n'.join(books))
            await message.reply(text="Хотите ли узнать книги какого-нибудь другого писателя? Просто снова введите одну первую букву фамилии автора и выберите подходящего!")
        except aiogram.exceptions.TelegramBadRequest:
            await message.reply(text="Вы ввели имя автора неправильно!\n\n Чтобы найти книги, надо ввести имя автора, как написано в строке после выбора буквы!")


if __name__ == '__main__':
    dp.run_polling(bot)