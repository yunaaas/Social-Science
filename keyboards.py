from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


registration_inline_button = InlineKeyboardButton(text = "Зарегистрироваться", callback_data="registration")
registration_inline_markup = InlineKeyboardMarkup(row_width=1).add(registration_inline_button)


start_button = KeyboardButton("Начать ботать 📖")
start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(start_button)

human_button = KeyboardButton("Человек и общество 👥")
economy_button = KeyboardButton("Экономика 👨‍💼📈")
policy_button = KeyboardButton("Политика 🗣📢")
law_button = KeyboardButton("Право 🧑‍⚖️")
sociology_button = KeyboardButton("Социология 👨‍🏫")
profile_button = KeyboardButton("Профиль 👤")
main_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(human_button).row(economy_button, policy_button).row(law_button, sociology_button).row(profile_button)

back_button = KeyboardButton("Назад 🔙")
bugs_report_button = KeyboardButton("Сообщить об ошибке 🐞")
profile_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(back_button, bugs_report_button)

easy_question_button = KeyboardButton("Определение 📝")
hard_question_button = KeyboardButton("Сложный вопрос 🤔")
change_mode = KeyboardButton("Сменить блок ♻️")
main_mode_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(easy_question_button, hard_question_button).row(change_mode)


check_true_answer_button = KeyboardButton("Посмотреть правильный ответ ✅")
check_true_answer_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(check_true_answer_button)