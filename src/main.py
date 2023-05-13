import logging
from aiogram import Bot, Dispatcher, types, exceptions
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import bot_token
from data import get_faculties, get_directions_by_faculty_id, get_courses_by_direction_id, get_course_by_id, get_review_by_course_id, get_metrics, get_metric_name_by_id, get_metric_score_by_chat_id, get_metric_score_by_metric_id, add_or_replace_score, add_review

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

async def send_faculties_keyboard(chat_id):
    faculties = get_faculties()
    keyboard = InlineKeyboardMarkup()
    for faculty in faculties:
        button = InlineKeyboardButton(text=faculty['name'], callback_data='faculty_{}'.format(faculty['id']))
        keyboard.add(button)
    await bot.send_message(chat_id, 'Выберите факультет:', reply_markup=keyboard)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await send_faculties_keyboard(message.chat.id)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'faculties', state='*')
async def back_to_faculties(callback_query: types.CallbackQuery):
    await send_faculties_keyboard(callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('faculty_'), state='*')
async def process_callback_faculty(callback_query: types.CallbackQuery, state: FSMContext):
    faculty_id = int(callback_query.data[8:])
    await state.update_data(
        {
            'faculty_id': faculty_id
        }
    )
    directions = get_directions_by_faculty_id(faculty_id)
    keyboard = InlineKeyboardMarkup()
    for direction in directions:
        button = InlineKeyboardButton(text=direction['name'], callback_data='direction_{}'.format(direction['id']))
        keyboard.add(button)
    back_button = InlineKeyboardButton(text='Назад', callback_data='faculties')
    keyboard.add(back_button)
    await bot.send_message(callback_query.from_user.id, text='Выберите направление:', reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('direction_'), state='*')
async def process_callback_direction(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query.data)
    direction_id = int(callback_query.data[10:])
    await state.update_data(
        {
            'direction_id': direction_id
        }
    )
    keyboard = InlineKeyboardMarkup()
    courses = get_courses_by_direction_id(direction_id)
    for course in courses:
        button = InlineKeyboardButton(text=course['name'], callback_data='course_{}_'.format(course['id']))
        keyboard.add(button)
    user_data = await state.get_data()
    print(user_data)
    faculty_id = user_data.get('faculty_id')
    back_button = InlineKeyboardButton(text='Назад', callback_data='faculty_{}'.format(faculty_id))
    keyboard.add(back_button)
    await bot.send_message(callback_query.from_user.id, text='Выберите курс:', reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)

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
    course = get_course_by_id(course_id)
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
    direction_id = user_data.get('direction_id')
    back_button = InlineKeyboardButton(text='Назад', callback_data='direction_{}'.format(direction_id))
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
    course = get_course_by_id(course_id)
    metrics = get_metrics()
    text = f"""
<i><b>Курс: {course['name']} ({course['type']})
Преподаватель: {course['teacher']}</b></i>

Средние метрики:
Успеваемость: 3.5/5.0
"""
    for metric in metrics:
        text += f"""{metric['metric_name']}: {get_metric_score_by_metric_id(course_id, metric['metric_id'], chat_id)}\n"""

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
    course = get_course_by_id(course_id)
    review = get_review_by_course_id(course_id)
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
    course = get_course_by_id(course_id)
    metrics = get_metrics()
    keyboard = InlineKeyboardMarkup()
    button_for_first_metric = InlineKeyboardButton(text=metrics[0]['metric_name'], callback_data='estimate_metric-{}'.format(metrics[0]['metric_id']))
    button_for_second_metric = InlineKeyboardButton(text=metrics[1]['metric_name'], callback_data='estimate_metric-{}'.format(metrics[1]['metric_id']))
    keyboard.add(button_for_first_metric, button_for_second_metric)
    button_for_third_metric = InlineKeyboardButton(text=metrics[2]['metric_name'], callback_data='estimate_metric-{}'.format(metrics[2]['metric_id']))
    button_for_fourth_metric = InlineKeyboardButton(text=metrics[3]['metric_name'], callback_data='estimate_metric-{}'.format(metrics[3]['metric_id']))
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
    course = get_course_by_id(course_id)
    metric_id = user_data.get('metric_id')
    metric_name = get_metric_name_by_id(metric_id)
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text='Назад', callback_data='add_feedback')
    keyboard.add(back_button)
    text = f"""
<i><b>Курс: {course['name']} ({course['type']})
Преподаватель: {course['teacher']}</b></i>
    
Метрика: <b>{metric_name}</b>
""" 
    personal_score = get_metric_score_by_chat_id(course_id, metric_id, chat_id)
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
    add_or_replace_score(chat_id, metric_id, course_id, score)
    await bot.send_message(chat_id, text="Ваша оценка успешно сохранена")
    await show_feedback_for_course(chat_id, state)
    await bot.answer_callback_query(callback_query.id)



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'add_review', state='*')
async def process_callback_review_addition(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    course = get_course_by_id(course_id)
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
    add_review(course_id, review_text)
    chat_id = callback_query.from_user.id
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


    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


