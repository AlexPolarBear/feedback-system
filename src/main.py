import logging
from aiogram import Bot, Dispatcher, types, exceptions
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import bot_token
from db_proxy_interface import DB_Proxy_Interface
from context import get_courses_by_user_request, get_tags_by_user_request 

logging.basicConfig(level=logging.INFO)


try:
    bot = Bot(token=bot_token)
except exceptions.ValidationError as e:
    print(e)
    print("Hint: set correct bot_token in ../data/config.json file before running up the bot")
    exit(0)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class user_message(StatesGroup):
    review = State()
    score = State()
    course_name = State()
    text_with_preferences = State()

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'main_page', state='*')
async def back_to_main_page(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    await show_main_page(callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)

async def show_main_page(chat_id):
    text = """
👋 Привет!

🤖 Это телеграм-бот "Система отзывов, оценок и рекомендаций"!

Тут ты cможешь:
1️⃣ Ознакомиться с оценками и отзывами по интересующему тебя курсу 📚
2️⃣ Оставить оценку или отзыв на пройденный тобою курс 📝
3️⃣ Подобрать курс на новый семестр согласно твоим предпочтениям 🎯
"""

    keyboard = InlineKeyboardMarkup()
    feedback_system_button = InlineKeyboardButton(text='Поиск курсов', callback_data='search_courses')
    keyboard.add(feedback_system_button)
    preferences_settings_button = InlineKeyboardButton(text='Редактировать свои предпочтения', callback_data='set_courses_preferences')
    keyboard.add(preferences_settings_button)
    reccomended_courses_button = InlineKeyboardButton(text='Получить релевантные курсы', callback_data='get_reсcomended_courses')
    keyboard.add(reccomended_courses_button)
    await bot.send_message(chat_id, text=text, reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'search_courses', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    text = '''
Введите назавание курса (при неточнотях в названии мы постараемся помочь вам найти его)

Также вы можете выбрать курс из списка,
нажав на кнопку <b>Выбрать курс из списка</b>
'''
    keyboard = InlineKeyboardMarkup()
    list_selection_button = InlineKeyboardButton(text='Выбрать курс из списка', callback_data='select_course_from_list')
    keyboard.add(list_selection_button)
    back_button = InlineKeyboardButton(text='Назад', callback_data='main_page')
    keyboard.add(back_button)
    await bot.send_message(callback_query.from_user.id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    await user_message.course_name.set()
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(state=user_message.course_name)
async def review_handler_text(message: types.Message, state: FSMContext):
    course_name = message.text
    await state.update_data(
        {
            'course_name': course_name
        }
    )
    await state.reset_state(with_data=False)
    # await get_courses_by_user_course_name(message.chat.id, state)
    user_data = await state.get_data()
    course_name = user_data.get('course_name')
    courses = get_courses_by_user_request(request=course_name)
    await state.update_data(
        {
            'course_list': courses
        }
    )
    await show_course_list(message.chat.id, state)

# @dp.callback_query_handler(lambda callback_query: callback_query.data == 'get_courses_by_user_request', state='*')
# async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
#     await get_courses_by_user_course_name(callback_query.from_user.id, state)
#     await bot.answer_callback_query(callback_query.id)


# async def get_courses_by_user_course_name(chat_id, state: FSMContext):
#     user_data = await state.get_data()
#     course_name = user_data.get('course_name')
#     courses = get_courses_by_user_request(request=course_name)
#     await state.update_data(
#         {
#             'course_list': courses
#         }
#     )
#     await show_course_list(chat_id, state)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await show_main_page(message.chat.id)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'select_course_from_list', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    course_list = DB_Proxy_Interface.get_all_courses()
    await state.update_data(
        {
            'course_list': course_list
        }
    )
    await show_course_list(callback_query.from_user.id, state)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'to_course_list', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await show_course_list(callback_query.from_user.id, state)
    await bot.answer_callback_query(callback_query.id)


async def show_course_list(chat_id, state: FSMContext):
    user_data = await state.get_data()
    course_list = user_data.get('course_list')
    keyboard = InlineKeyboardMarkup()
    for course in course_list:
        button = InlineKeyboardButton(text=course['name'], callback_data='course_{}_'.format(course['id']))
        keyboard.add(button)
    user_data = await state.get_data()
    back_button = InlineKeyboardButton(text='Назад', callback_data='search_courses')
    keyboard.add(back_button)
    await bot.send_message(chat_id, text='Выберите курс:', reply_markup=keyboard)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('course_'), state='*')
async def process_callback_course(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    start_index = 7
    end_index = callback_query.data.index("_", start_index)
    course_id = int(callback_query.data[7:end_index])
    await state.update_data(
        {
            'course_id': course_id
        }
    )
    course = DB_Proxy_Interface.get_course_by_id(course_id)
#     text = f"""
# Курс: {course['name']} ({course['type']})
# Преподаватель: {course['teacher']}
#     """
    text = f"""
<i><b>Курс: {course['name']} ({course['type']})
Преподаватель: {course['teacher']}</b></i>
"""

    keyboard = InlineKeyboardMarkup()
    # watch_review_button = InlineKeyboardButton(text='Посмотреть отзывы', callback_data='review_view')
    # keyboard.add(watch_review_button)
    watch_feedback_button = InlineKeyboardButton(text='Информация о курсе', callback_data='view_feedback')
    keyboard.add(watch_feedback_button)
    # add_review_button = InlineKeyboardButton(text='Оставить отзыв', callback_data='add_review')
    # keyboard.add(add_review_button)
    add_feedback_button = InlineKeyboardButton(text='Оставить обратную связь', callback_data='add_feedback')
    keyboard.add(add_feedback_button)
    user_data = await state.get_data()
    back_button = InlineKeyboardButton(text='Назад', callback_data='to_course_list')
    keyboard.add(back_button)
    print(callback_query.data)
    drop_new_message = not callback_query.data.endswith('_edit_last_message')
    chat_id = callback_query.from_user.id 
    if drop_new_message:
        print('True')
        message = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    else:
        print('False')
        message_to_edit_id = user_data.get('message_to_edit_id')
        message = await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    message_id = message.message_id
    await state.update_data(
        {
            'message_to_edit_id': message_id
        }
    )
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'view_feedback', state='*')
async def process_callback_feedback_view(callback_query: types.CallbackQuery, state: FSMContext):
    await show_feedback_for_course(callback_query.from_user.id, state, drop_new_message=False)
    await bot.answer_callback_query(callback_query.id)
    
async def show_feedback_for_course(chat_id, state: FSMContext, drop_new_message=True):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    course = DB_Proxy_Interface.get_course_by_id(course_id)
    metrics = DB_Proxy_Interface.get_all_metrics()
    text = f"""
<i><b>Курс: {course['name']} ({course['type']})
Преподаватель: {course['teacher']}</b></i>

Средние метрики:
Успеваемость: 3.5/5.0
"""
    for metric in metrics:
        text += f"""{metric['name']}: {DB_Proxy_Interface.get_metric_score_by_metric_id(course_id, metric['id'], chat_id)}\n"""

    text += f"""
Общий рейтинг курса: 73%
    """
    keyboard = InlineKeyboardMarkup()
    watch_review_button = InlineKeyboardButton(text='Посмотреть отзывы', callback_data='review_view')
    keyboard.add(watch_review_button)
    back_button = InlineKeyboardButton(text='Назад', callback_data='course_{}_edit_last_message'.format(course_id))
    keyboard.add(back_button)
    if drop_new_message:
        message = await bot.send_message(chat_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    else:
        message_to_edit_id = user_data.get('message_to_edit_id')
        message = await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    message_id = message.message_id
    await state.update_data(
        {
            'message_to_edit_id': message_id
        }
    )
    # message = await bot.send_message(chat_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    # message_id = message.message_id
    # await state.update_data(
    #     {
    #         'message_to_edit_id': message_id
    #     }
    # )

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'review_view', state='*')
async def process_callback_review_view(callback_query: types.CallbackQuery, state: FSMContext):
    await show_review_for_course(callback_query.from_user.id, state, drop_new_message=False)
    await bot.answer_callback_query(callback_query.id)

async def show_review_for_course(chat_id, state: FSMContext, drop_new_message=True):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    course = DB_Proxy_Interface.get_course_by_id(course_id)
    review = DB_Proxy_Interface.get_feedback_by_course_id(course_id)
    text = f"""
<i><b>Курс: {course['name']} ({course['type']})
Преподаватель: {course['teacher']}</b></i>   
"""
    for index, review_item in enumerate(review):
        text += f"""
Отзыв {index + 1}: 
{review_item['text']}
        """
    if len(review) == 0:
        text = "Отзывов пока нет!"
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text='Назад', callback_data='view_feedback')
    keyboard.add(back_button)
    # await bot.send_message(chat_id, text=text, reply_markup=keyboard)
    if drop_new_message:
        message = await bot.send_message(chat_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    else:
        message_to_edit_id = user_data.get('message_to_edit_id')
        message = await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    message_id = message.message_id
    await state.update_data(
        {
            'message_to_edit_id': message_id
        }
    )
     
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'add_feedback', state='*')
async def process_callback_feedback_addition(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    course = DB_Proxy_Interface.get_course_by_id(course_id)
    metrics = DB_Proxy_Interface.get_all_metrics()
    keyboard = InlineKeyboardMarkup()
    button_for_first_metric = InlineKeyboardButton(text=metrics[0]['name'], callback_data='estimate_metric-{}'.format(metrics[0]['id']))
    button_for_second_metric = InlineKeyboardButton(text=metrics[1]['name'], callback_data='estimate_metric-{}'.format(metrics[1]['id']))
    keyboard.add(button_for_first_metric, button_for_second_metric)
    button_for_third_metric = InlineKeyboardButton(text=metrics[2]['name'], callback_data='estimate_metric-{}'.format(metrics[2]['id']))
    button_for_fourth_metric = InlineKeyboardButton(text=metrics[3]['name'], callback_data='estimate_metric-{}'.format(metrics[3]['id']))
    keyboard.add(button_for_third_metric, button_for_fourth_metric)
    add_review_button = InlineKeyboardButton(text='Оставить отзыв', callback_data='add_review')
    keyboard.add(add_review_button)
    back_button = InlineKeyboardButton(text='Назад', callback_data='course_{}_edit_last_message'.format(course_id))
    keyboard.add(back_button)
    text = f""" 
<i><b>Курс: {course['name']} ({course['type']})
Преподаватель: {course['teacher']}</b></i>

Выберите метрику для оценивания или оставьте отзыв:
"""
    chat_id = callback_query.from_user.id
    # await bot.send_message(callback_query.from_user.id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    message_to_edit_id = user_data.get('message_to_edit_id')
    message = await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    message_id = message.message_id
    await state.update_data(
        {
            'message_to_edit_id': message_id
        }
    )
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('estimate_metric-'), state='*')
async def process_callback_metric_estimation(callback_query: types.CallbackQuery, state: FSMContext):
    metric_id = int(callback_query.data[16:])
    await state.update_data(
        {
            'metric_id': metric_id
        }
    )
    await suggest_estimate_metric(callback_query.from_user.id, state, drop_new_message=False)
    await bot.answer_callback_query(callback_query.id)

async def suggest_estimate_metric(chat_id, state: FSMContext, drop_new_message=True):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    course = DB_Proxy_Interface.get_course_by_id(course_id)
    metric_id = user_data.get('metric_id')
    metric_name = DB_Proxy_Interface.get_metric_name_by_id(metric_id)
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text='Назад', callback_data='add_feedback')
    keyboard.add(back_button)
    text = f"""
<i><b>Курс: {course['name']} ({course['type']})
Преподаватель: {course['teacher']}</b></i>
    
Метрика: <b>{metric_name}</b>
""" 
    personal_score = DB_Proxy_Interface.get_metric_score_by_chat_id(course_id, metric_id, chat_id)
    if personal_score != None:
        text += f"""\nВаша оценка: {personal_score} (новая оценка затрёт старую)\n"""
    text += """
Оцените по десятибальной шкале (1-10):"""
    if drop_new_message: 
        message = await bot.send_message(chat_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    else:
        message_to_edit_id = user_data.get('message_to_edit_id')
        message = await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    message_id = message.message_id
    await state.update_data(
        {
            'message_to_edit_id': message_id
        }
    )
    await user_message.score.set()
    

@dp.message_handler(state=user_message.score)
async def score_handler_text(message: types.Message, state: FSMContext):
    score_text = message.text
    await state.reset_state(with_data=False)
    def is_valid_score(score_text):
        try:
            score = int(score_text)
            return score >= 1 and score <= 10 
        except:
            return False
    if is_valid_score(score_text):
        score = int(score_text) 
        await state.update_data(
            {
                'score': score
            }
        )
        keyboard = InlineKeyboardMarkup()
        yes_button = InlineKeyboardButton(text='Да', callback_data='confirm_score')
        no_button = InlineKeyboardButton(text='Нет', callback_data='cancel_score')
        keyboard.add(yes_button, no_button)
        await message.answer(text="Подтвердить вашу оценку?", reply_markup=keyboard)
        pass
    else:
        await message.answer(text="Оценкой является натуральное число от 1 до 10")
        await suggest_estimate_metric(message.chat.id, state)
        pass 

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'cancel_score', state='*')
async def process_callback_score_cancellation(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    del user_data['score']
    await state.set_data(user_data)
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, text="Ваша оценка не будет сохранена")
    await suggest_estimate_metric(chat_id, state)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'confirm_score', state='*')
async def process_callback_score_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    metric_id = user_data.get('metric_id')
    print('course_id: ', str(course_id))
    score = user_data.get('score')
    print(score)
    chat_id = callback_query.from_user.id
    DB_Proxy_Interface.add_or_replace_score(chat_id, metric_id, course_id, score)
    await bot.send_message(chat_id, text="Ваша оценка успешно сохранена")
    await show_feedback_for_course(chat_id, state)
    await bot.answer_callback_query(callback_query.id)



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'add_review', state='*')
async def process_callback_review_addition(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    course = DB_Proxy_Interface.get_course_by_id(course_id)
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text='Отмена', callback_data='add_feedback')
    keyboard.add(back_button)
    text = f"""
<i><b>Курс: {course['name']} ({course['type']})
Преподаватель: {course['teacher']}</b></i>

Напишите ваш отзыв
"""
    chat_id = callback_query.from_user.id
    message_to_edit_id = user_data.get('message_to_edit_id')
    message = await bot.edit_message_text(chat_id=chat_id, message_id=message_to_edit_id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    message_id = message.message_id
    await state.update_data(
        {
            'message_to_edit_id': message_id
        }
    )
    # await bot.send_message(callback_query.from_user.id, text=text, reply_markup=keyboard)
    await user_message.review.set()
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(state=user_message.review)
async def review_handler_text(message: types.Message, state: FSMContext):
    review_text = message.text
    await state.reset_state(with_data=False)
    await state.update_data(
        {
            'review_text': review_text
        }
    )
    keyboard = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(text='Да', callback_data='confirm_review')
    no_button = InlineKeyboardButton(text='Нет', callback_data='cancel_review')
    keyboard.add(yes_button, no_button)
    await message.answer(text="Сохранить отзыв?", reply_markup=keyboard)
    
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'confirm_review', state='*')
async def process_callback_review_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    print('course_id: ', str(course_id))
    review_text = user_data.get('review_text')
    chat_id = callback_query.from_user.id
    DB_Proxy_Interface.add_feedback(course_id, chat_id, review_text)
    await bot.send_message(chat_id, text="Ваш отзыв успешно сохранён")
    await show_review_for_course(chat_id, state)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'cancel_review', state='*')
async def process_callback_review_cancellation(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    del user_data['review_text']
    await state.set_data(user_data)
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, text="Ваш отзыв не будет сохранён")
    await show_review_for_course(chat_id, state)
    await bot.answer_callback_query(callback_query.id)


### RECOMENDATION SECTION

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'set_courses_preferences', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    keyboard = InlineKeyboardMarkup()
    feedback_system_button = InlineKeyboardButton(text='Поиск подходящего тега по тексту', callback_data='search_tags_by_text')
    keyboard.add(feedback_system_button)
    preferences_settings_button = InlineKeyboardButton(text='Выбрать теги из предложенных', callback_data='select_tags_from_list')
    keyboard.add(preferences_settings_button)
    reccomended_courses_button = InlineKeyboardButton(text='Посмотреть ваши теги', callback_data='watch_user_tags')
    keyboard.add(reccomended_courses_button)
    back_button = InlineKeyboardButton(text='Назад', callback_data='main_page')
    keyboard.add(back_button)
    await bot.send_message(callback_query.from_user.id, text='...', reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'search_tags_by_text', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text='Назад', callback_data='set_courses_preferences')
    keyboard.add(back_button)
    await bot.send_message(callback_query.from_user.id, text='Введите текст, который максимально точно описывает ваши предпочтения и мы предложим вам выбрать теги', reply_markup=keyboard)
    await user_message.text_with_preferences.set()
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(state=user_message.text_with_preferences)
async def review_handler_text(message: types.Message, state: FSMContext):
    text_with_preferences = message.text
    await state.reset_state(with_data=False)
    # await get_courses_by_user_course_name(message.chat.id, state)
    # user_data = await state.get_data()
    # course_name = user_data.get('course_name')
    tags = get_tags_by_user_request(request=text_with_preferences)
    await state.update_data(
        {
            'tag_list': tags,
            'last_callback_data': 'search_tags_by_text'
        }
    )
    await show_tag_list(message.chat.id, state)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'select_tags_from_list', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    tags = DB_Proxy_Interface.get_all_tags()
    await state.update_data(
        {
            'tag_list': tags,
            'last_callback_data': 'set_courses_preferences'
        }
    )
    await show_tag_list(callback_query.from_user.id, state)
    await bot.answer_callback_query(callback_query.id)


async def show_tag_list(chat_id, state: FSMContext):
    user_data = await state.get_data()
    tag_list = user_data.get('tag_list')
    keyboard = InlineKeyboardMarkup()
    for tag in tag_list:
        button = InlineKeyboardButton(text=tag['title'], callback_data='save-tag-{}'.format(tag['id']))
        keyboard.add(button)
    user_data = await state.get_data()
    last_callback_data = user_data.get('last_callback_data')
    back_button = InlineKeyboardButton(text='Назад', callback_data=last_callback_data)
    keyboard.add(back_button)
    await bot.send_message(chat_id, text='Нажмите на теги, которые хотите сохранить', reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('save-tag-'), state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    tag_id = int(callback_query.data[9:])
    user_data = await state.get_data()
    if 'user_tags' in user_data:
        user_tags = user_data.get('user_tags')
    else:
        user_tags = []
    new_tag = DB_Proxy_Interface.get_tag_by_id(tag_id)
    user_tags.append(new_tag)
    tag_list = user_data.get('tag_list')
    tag_list = [tag for tag in tag_list if tag != new_tag]
    await state.update_data(
        {
            'user_tags': user_tags,
            'tag_list': tag_list
        }
    )
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, text='Тег успешно сохранен')
    await show_tag_list(chat_id, state)
    await bot.answer_callback_query(callback_query.id)



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'watch_user_tags', state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await show_user_tags(callback_query.from_user.id, state)
    await bot.answer_callback_query(callback_query.id)

async def show_user_tags(chat_id, state: FSMContext):
    user_data = await state.get_data()
    if 'user_tags' in user_data:
        user_tags = user_data.get('user_tags')
    else:
        user_tags = []
    text = 'Нажмите на теги, которые хотите удалить'
    if len(user_tags) == 0:
        text = 'У вас пока нет никаких тегов'
    keyboard = InlineKeyboardMarkup()
    for tag in user_tags:
        button = InlineKeyboardButton(text=tag['title'], callback_data='delete-tag-{}'.format(tag['id']))
        keyboard.add(button)
    back_button = InlineKeyboardButton(text='Назад', callback_data='set_courses_preferences')
    keyboard.add(back_button)
    await bot.send_message(chat_id, text=text, reply_markup=keyboard)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('delete-tag-'), state='*')
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    tag_id = int(callback_query.data[11:])
    user_data = await state.get_data()
    user_tags = user_data.get('user_tags')
    tag_to_delete = DB_Proxy_Interface.get_tag_by_id(tag_id)
    user_tags = [tag for tag in user_tags if tag != tag_to_delete]
    await state.update_data(
        {
            'user_tags': user_tags
        }
    )
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, text='Тег успешно удален')
    await show_user_tags(chat_id, state)
    await bot.answer_callback_query(callback_query.id)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


