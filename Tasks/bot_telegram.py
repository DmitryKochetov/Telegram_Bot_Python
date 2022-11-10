import os
import sqlite3

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token_tg')


def sql_start():
    global db, cursor
    db = sqlite3.connect('data_base.db')
    cursor = db.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS personal(
    id_inp integer primary key AUTOINCREMENT,
    name_inp TEXT,
    last_name_inp TEXT,
    position TEXT,
    salary INT,
    bonus INT
    )'''
    )
    db.commit()


async def sql_add_string(state):
    async with state.proxy() as data:
        cursor.execute(
            'INSERT INTO personal VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
        db.commit()


async def sql_delete_string(state):
    async with state.proxy() as data:
        # print(data)
        cursor.execute(
            f'DELETE from personal WHERE id_inp = {data["id_inp"]};')
        db.commit()


storage = MemoryStorage()

bot = Bot(token)
dp = Dispatcher(bot, storage=storage)


class FSMAdmin(StatesGroup):
    id_inp = State()
    name_inp = State()
    last_name_inp = State()
    position_inp = State()
    salary_inp = State()
    bonus_inp = State()


class FSMdel(StatesGroup):
    id_inp = State()


class FSMfind(StatesGroup):
    id_inp = State()


async def on_startup(_):
    print('Бот в сети')
    sql_start()

b1 = KeyboardButton('/Посмотреть_базу')
b2 = KeyboardButton('/добавить_сотрудника')
b3 = KeyboardButton('/удалить_запись')
b4 = KeyboardButton('/найти_по_id')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)  # one_time_keyboard=True

kb_client.add(b1).insert(b2).add(b3).insert(b4)


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Главное меню:\n1 - посмотреть базу: \n2 - добавить сотрудника:\
         \n3 - удалить запись\n4 - найти по id\nвведите номер пункта меню: ', reply_markup=kb_client)
        # await message.delete()
    except:
        message.reply('Общение с ботом через ЛС')


@dp.message_handler(commands=['Посмотреть_базу'])
async def print_base(message: types.Message):
    for i in cursor.execute('SELECT * FROM personal;'):
        await bot.send_message(message.from_user.id, i)


@dp.message_handler(commands=['добавить_сотрудника'], state=None)
async def add_string(message: types.Message):
    await FSMAdmin.id_inp.set()
    await message.reply('Введите ID:')


@dp.message_handler(state=FSMAdmin.id_inp)
async def input_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_inp'] = int(message.text)
    await FSMAdmin.next()
    await message.reply('Теперь введите Имя:')


@dp.message_handler(state=FSMAdmin.name_inp)
async def input_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_inp'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь введите Фамилию:')


@dp.message_handler(state=FSMAdmin.last_name_inp)
async def input_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name_inp'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь введите должность:')


@dp.message_handler(state=FSMAdmin.position_inp)
async def input_position(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['position_inp'] = message.text
    await FSMAdmin.next()
    await message.reply('Теперь введите зарплату:')


@dp.message_handler(state=FSMAdmin.salary_inp)
async def input_salary(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['salary_inp'] = int(message.text)
    await FSMAdmin.next()
    await message.reply('Теперь введите бонус:')


@dp.message_handler(state=FSMAdmin.bonus_inp)
async def input_bonus(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bonus_inp'] = int(message.text)
    # print(state)
    await sql_add_string(state)
    await state.finish()


@dp.message_handler(commands=['удалить_запись'])
async def delete_string(message: types.Message):
    await FSMdel.id_inp.set()
    await bot.send_message(message.from_user.id, 'Введите id удаляемой записи:')


@dp.message_handler(state=FSMdel.id_inp)
async def input_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_inp'] = int(message.text)
    await sql_delete_string(state)
    await state.finish()


@dp.message_handler(commands=['найти_по_id'])
async def find_string(message: types.Message):
    await FSMfind.id_inp.set()
    await bot.send_message(message.from_user.id, 'Введите id записи, которую нужно найти:')


@dp.message_handler(state=FSMfind.id_inp)
async def input_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_inp'] = int(message.text)
        cursor.execute(
            f'SELECT * FROM personal WHERE id_inp = {data["id_inp"]};')
        one = cursor.fetchone()
    await bot.send_message(message.from_user.id, one)
    await state.finish()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
