import keyboards as kb

import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, Bot, executor, types

from config import BOT_TOKEN, BOT_LINK

# import emoji

from fuzzywuzzy import fuzz

from Questions import *

from SQL import *

class StateGroup(StatesGroup):
    message_answer = State()
    bugs = State()
    notice = State()


bot = Bot(token = BOT_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage=MemoryStorage())

q = Questions()

sql = SQL()

logging.basicConfig(level=logging.ERROR)




sql.create_table()



@dp.message_handler(commands = "start")
async def registaration(message: types.Message):

    await bot.send_message(message.from_user.id, text = "Привет! Чтобы начать ботать, тебе нужно пройти регистрацию. Просто нажми кнопку ниже 👇", reply_markup=kb.registration_inline_markup)


@dp.message_handler(commands = "send", commands_prefix = "!", commands_ignore_caption=False, content_types=["any"])
async def send_message(message: types.Message):
    a = message.text
    msg = a.split("!")
    await bot.send_message(chat_id=msg[2], text = "Ответ на вашу проблему: \n\n" + msg[3].strip().capitalize() + "\n\nБлагодарим за сообщение, рады работать! 💖🤖")
    await bot.send_message(message.from_user.id, text = "Ваше сообщение успешно доставлено. 👨‍💻🤖")


@dp.message_handler(commands = "notice",  commands_prefix = "!")
async def notice(message: types.Message):
    await bot.send_message(message.from_user.id, text = "Что необходиимо написать <b>ВСЕМ</b> пользователям? 👨‍💻🤖")
    await StateGroup.notice.set()

@dp.message_handler(content_types=["any"], state=StateGroup.notice)
async def check(message: types.Message, state: FSMContext):
    async with state.proxy() as result:
        result["notice"] = message.text
    await state.finish()
    data = sql.get_id()
    for i in range(0, len(data)):
        await bot.send_message(chat_id=data[i][0], text = str(result["notice"]).capitalize() + "\n\nС уважением администрация. 💖🤖")
    await bot.send_message(message.from_user.id, text = "Сообщение отправлено <b>ВСЕМ</b> пользователям 👨‍💻🤖")

# @dp.message_handler(commands = "bugs")
# async def registaration(message: types.Message):
#     # await message.forward(chat_id=1012078689)
#     await bot.send_message(message.from_user.id, text = "Опишите вашу проблему ниже, по необходимости прикрепите фото...👇")
#     await StateGroup.bugs.set()

@dp.message_handler(commands = "киньБдПлиз")
async def bd(message: types.Message):
    f = open("users.db", "rb")
    await message.reply_document(f);


@dp.callback_query_handler(text="registration")
async def registration_handler(call: types.CallbackQuery):
    user_name = call.from_user.first_name
    user_id = call.from_user.id
    data = (str(user_name), int(user_id))
    print(data[1])
    if sql.add_in_table(con, data):
        await bot.send_message(call.from_user.id, text = "Регистрация прошла успешна. Поздравляю!", reply_markup=kb.start_markup)
    else: 
        await bot.send_message(call.from_user.id, text = "Вы уже зарегистрированы!", reply_markup=kb.start_markup)


@dp.message_handler(lambda message: message.text == "Начать ботать 📖")
async def vie_main_menu(message: types.Message):
    user_id = message.from_user.id
    result = sql.search_in_table(str(user_id))
    await bot.send_message(message.from_user.id, text = "Привет, <b>" + str(result[0][0]) + "</b>! \n\nЕсли <b>ВЫ</b> оказались здесь, значит <b>регистрация</b> прошла успешно. \nЯ вами горжусь!\n\nВ целях упрощения обучения информация представлена блоками. В скором времени будут добавлены и другие блоки.\n\n<b>Пожалуйста выберите блок...</b>", reply_markup=kb.main_menu_markup)

@dp.message_handler(lambda message: message.text == "Человек и общество 👥")
async def human_menu(message: types.Message):
    user_id = message.from_user.id
    q.set_mode(1)
    sql.set_mode(user_id, 1)
    await bot.send_message(message.from_user.id, text = "Выбранный блок: <b>Человек и общество 👥</b>\n\nКакой тип вопросов будем ботать?", reply_markup=kb.main_mode_markup)


@dp.message_handler(lambda message: message.text == "Экономика 👨‍💼📈")
async def economy_menu(message: types.Message):
    user_id = message.from_user.id
    q.set_mode(2)
    sql.set_mode(user_id, 2)
    await bot.send_message(message.from_user.id, text = "Выбранный блок: <b>Экономика 👨‍💼📈</b>\n\nКакой тип вопросов будем ботать?", reply_markup=kb.main_mode_markup)


@dp.message_handler(lambda message: message.text == "Политика 🗣📢")
async def policy_menu(message: types.Message):
    user_id = message.from_user.id
    q.set_mode(3)
    sql.set_mode(user_id, 3)
    await bot.send_message(message.from_user.id, text = "Выбранный блок: <b>Политика 🗣📢</b>\n\nКакой тип вопросов будем ботать?", reply_markup=kb.main_mode_markup)


@dp.message_handler(lambda message: message.text == "Право 🧑‍⚖️")
async def law_menu(message: types.Message):
    user_id = message.from_user.id    
    q.set_mode(4)
    sql.set_mode(user_id, 4)
    await bot.send_message(message.from_user.id, text = "Выбранный блок: <b>Право 🧑‍⚖️</b>\n\nКакой тип вопросов будем ботать?", reply_markup=kb.main_mode_markup)

@dp.message_handler(lambda message: message.text == "Социология 👨‍🏫")
async def sociology_menu(message: types.Message):
    user_id = message.from_user.id    
    q.set_mode(5)
    sql.set_mode(user_id, 5)
    await bot.send_message(message.from_user.id, text = "Выбранный блок: <b>Социология 👨‍🏫</b>\n\nКакой тип вопросов будем ботать?", reply_markup=kb.main_mode_markup)



@dp.message_handler(lambda message: message.text == "Профиль 👤")
async def profile(message: types.Message):
    user_id = message.from_user.id
    data = sql.search_in_table(user_id)
    if data[0][4] != 0:
        human_correct = int((data[0][5] / data[0][4]) * 100)
    else:
        human_correct = 0
    if data[0][6] != 0:
        economy_correct = int((data[0][7] / data[0][6]) * 100)
    else:
        economy_correct = 0
    if data[0][8] != 0:
        policy_correct = int((data[0][9] / data[0][8]) * 100)
    else:
        policy_correct = 0
    if data[0][10] != 0:
        law_correct = int((data[0][11] / data[0][10]) * 100)
    else:
        law_correct = 0
    if data[0][12] != 0:
        sociology_correct = int((data[0][13] / data[0][12]) * 100)
    else:
        sociology_correct = 0
    if data[0][2] != 0:
        percent = int((data[0][3] / data[0][2]) * 100)
    else:
        percent = 0 
    await bot.send_message(message.from_user.id, text = "<i>Имя: </i><b>" + str(data[0][0]) + "</b>\n\n<i>Статистика ответов по блокам:</i> \n\n<b>Человек и общество:</b>\n\t<i>Общее количество попыток: </i><b>" + str(data[0][4]) + "</b>\n\t<i>✅:</i><b> " + str(data[0][5]) + "</b>\n\t<i>Процент успешно выполненных:</i> <b>" + str(human_correct) + "%</b>\n\n<b>Экономика: </b>\n\t<i>Общее количество попыток: </i><b>" + str(data[0][6]) + "</b>\n\t<i>✅:</i><b> " + str(data[0][7]) + "</b>\n\t<i>Процент успешно выполненных: </i><b>" + str(economy_correct) + "%</b>\n\n<b>Политика: </b>\n\t<i>Общее количество попыток: </i><b>" + str(data[0][8]) + "</b>\n\t<i>✅:</i><b> " + str(data[0][9]) + "</b>\n\t<i>Процент успешно выполненных:</i> <b>" + str(policy_correct) + "%</b>\n\n<b>Право: </b>\n\t<i>Общее количество попыток: </i><b>" + str(data[0][10]) + "</b>\n\t<i>✅:</i><b> " + str(data[0][11]) + "</b>\n\t<i>Процент успешно выполненных:</i> <b>" + str(law_correct) + "%</b>\n\n<b>Социология: </b>\n\t<i>Общее количество попыток: </i><b>" + str(data[0][12]) + "</b>\n\t<i>✅:</i><b> " + str(data[0][13]) + "</b>\n\t<i>Процент успешно выполненных:</i> <b>" + str(sociology_correct) + "%</b>\n\t\n\n<b>Общая успеваемость по курсу: </b><b>" + str(percent) + "%</b>\n\n<i>Дата регистрации: </i><b>" + str(data[0][16]) +"</b>", reply_markup=kb.profile_menu_markup)

@dp.message_handler(lambda message: message.text == "Назад 🔙")
async def back(message: types.Message):
    await bot.send_message(message.from_user.id, text = "<b>Пожалуйста выберите блок...</b>", reply_markup=kb.main_menu_markup)


@dp.message_handler(lambda message: message.text == "Сообщить об ошибке 🐞")
async def bugs(message: types.Message):
    await bot.send_message(message.from_user.id, text = "Опишите вашу проблему ниже, по необходимости прикрепите фото...👇")
    await StateGroup.bugs.set()

@dp.message_handler(content_types=["any"], state=StateGroup.bugs)
async def check(message: types.Message, state: FSMContext):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    await message.forward(chat_id=1012078689)
    await message.forward(chat_id=770629236)
    await bot.send_message(chat_id=1012078689, text = "От: " + str(user_name) + ", <code>!send !" + str(user_id) + "!</code>")
    await bot.send_message(chat_id=770629236, text = "От: " + str(user_name) + ", <code>!send !" + str(user_id) + "!</code>")
    await bot.send_message(message.from_user.id, "Ваше сообщение доставлено разработчику! \nСпасибо за обратную связь! 💖💌", reply_markup=kb.profile_menu_markup)
    await state.finish()



@dp.message_handler(lambda message: message.text == "Сменить блок ♻️")
async def back_to_main_menu(message: types.Message):
    await bot.send_message(message.from_user.id, text = "<b>Пожалуйста выберите блок...</b>", reply_markup=kb.main_menu_markup)



@dp.message_handler(lambda message: message.text == "Определение 📝")
async def easy_question_human(message: types.Message):
    q.set_complexuty(1)
    await give_question(message =message)
    await StateGroup.message_answer.set()

@dp.message_handler(lambda message: message.text == "Сложный вопрос 🤔")
async def hard_question_human(message: types.Message):
    q.set_complexuty(2)
    await give_question(message =message)
    await StateGroup.message_answer.set()

@dp.message_handler(lambda message: message.text.lower(), state=StateGroup.message_answer)
async def check(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(user_id)
    async with state.proxy() as result:
        result['message_answer'] = message.text
    await state.finish()
    print(result["message_answer"])
    data = sql.search_in_table(user_id)
    if data[0][15] == 1:
        percent = fuzz.token_sort_ratio(str(result["message_answer"]), q.get_answer(message.from_user.id))
        result = sql.search_in_table(user_id)
        await bot.send_message(message.from_user.id, text = "Ваше определение схоже с моим на <b>" +str(percent) + "%</b>", reply_markup=kb.check_true_answer_markup)
        if percent >= 60:
            sql.change_totals_correct(user_id, result[0][14])
            sql.update_true_data_in_table(user_id)
        sql.change_is_anwering(user_id, 0)
    else: 
        await bot.send_message(message.from_user.id, text = "<b>Пожалуйста выберите блок...</b>", reply_markup=kb.main_menu_markup)
   
async def give_question(message: types.Message):
    user_id = message.from_user.id
    print(user_id)
    sql.update_all_total_in_table(user_id)
    q.set_question(user_id)
    sql.change_is_anwering(user_id, 1)
    await bot.send_message(message.from_user.id, text = "<b>" + str(q.get_question(message.from_user.id)).capitalize() + "- это...</b>\n\nОтвет напишите в чат 👇")


@dp.message_handler(lambda message: message.text == "Посмотреть правильный ответ ✅")
async def check_true_answer(message: types.Message):
    user_id = message.from_user.id
    result = sql.search_in_table(user_id)
    mode = ""
    if result[0][14] == 1:
        mode = "Человек и общество 👥"
    elif result[0][14] == 2:
        mode = "Экономика 👨‍💼📈"
    elif result[0][14] == 3:
        mode = "Политика 🗣📢"
    elif result[0][14] == 4:
        mode = "Право 🧑‍⚖️" 
    elif result[0][15] == 5:
        mode = "Социология 👨‍🏫"
    await bot.send_message(message.from_user.id, text = "Текущий блок: <b>" + str(mode) +"</b>\n\n<b>"+ str(q.get_question(message.from_user.id)) +"- это</b><i>" + str(q.get_answer(message.from_user.id)) + "</i>", reply_markup=kb.main_mode_markup) 




# #ПЕРЕДЕЛАТЬ НА МАШИНУ СОСТОЯНИЙ 
# @dp.message_handler(lambda message: message.text.lower())
# async def check(message: types.Message):
#     user_id = message.from_user.id
#     data = sql.search_in_table(user_id)
#     print(data)
#     print(data[0][15])
#     if data[0][15] == 1:
#         user_answer = message.text

# #ПЕРЕПИШИТЕ ЭТУ ХУЙНЮ ПОКА ВСЕ НЕ РАЗЪЕБАЛОСЬ НАХУЙ НИ В 
#         percent = fuzz.token_sort_ratio(user_answer, q.get_answer(message.from_user.id))
#         result = sql.search_in_table(user_id)
#         await bot.send_message(message.from_user.id, text = "Ваше определение схоже с моим на <b>" +str(percent) + "%</b>", reply_markup=kb.check_true_answer_markup)
#         if percent >= 60:
#             sql.change_totals_correct(user_id, result[0][14])
#             sql.update_true_data_in_table(user_id)
#         sql.change_is_anwering(user_id, 0)
#     else: 
#         await bot.send_message(message.from_user.id, text = "<b>Пожалуйста выберите блок...</b>", reply_markup=kb.main_menu_markup)
# #ЭТО НАХУЙ ОЧЕНЬ ПЛОХАЯ ПРАКТИКА ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


executor.start_polling(dp, skip_updates=True)


    




