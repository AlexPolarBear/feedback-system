import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import bot_token
from data import get_faculties, get_directions_by_faculty_id, get_courses_by_direction_id, get_course_by_id, get_feedback_by_course_id, add_feedback

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class feedback(StatesGroup):
    text = State()

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
    direction_id = int(callback_query.data[10:])
    await state.update_data(
        {
            'direction_id': direction_id
        }
    )
    keyboard = InlineKeyboardMarkup()
    courses = get_courses_by_direction_id(direction_id)
    for course in courses:
        button = InlineKeyboardButton(text=course['name'], callback_data='course_{}'.format(course['id']))
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
    course_id = int(callback_query.data[7:])
    await state.update_data(
        {
            'course_id': course_id
        }
    )
    course = get_course_by_id(course_id)
    text = f"""
Курс: {course['name']}
Преподователь: {course['teacher']}
    """

    keyboard = InlineKeyboardMarkup()
    watch_feedback_button = InlineKeyboardButton(text='Посмотреть отзывы', callback_data='feedback_view')
    keyboard.add(watch_feedback_button)
    add_feedback_button = InlineKeyboardButton(text='Оставить отзыв', callback_data='add_feedback')
    keyboard.add(add_feedback_button)
    user_data = await state.get_data()
    direction_id = user_data.get('direction_id')
    back_button = InlineKeyboardButton(text='Назад', callback_data='direction_{}'.format(direction_id))
    keyboard.add(back_button)
    await bot.send_message(callback_query.from_user.id, text=text, reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'feedback_view', state='*')
async def process_callback_feedback_view(callback_query: types.CallbackQuery, state: FSMContext):
    await show_feedback_for_course(callback_query.from_user.id, state)
    await bot.answer_callback_query(callback_query.id)

async def show_feedback_for_course(chat_id, state: FSMContext):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    feedback = get_feedback_by_course_id(course_id)
    text = ""
    for index, feedback_item in enumerate(feedback):
        text += f"""
Отзыв {index + 1}: 
{feedback_item['text']}
        """
    if len(feedback) == 0:
        text = "Отзывов пока нет!"
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text='Назад', callback_data='course_{}'.format(course_id))
    keyboard.add(back_button)
    await bot.send_message(chat_id, text=text, reply_markup=keyboard)
    
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'add_feedback', state='*')
async def process_callback_feedback_addition(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    keyboard = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(text='Отмена', callback_data='course_{}'.format(course_id))
    keyboard.add(back_button)
    await bot.send_message(callback_query.from_user.id, text="Напишите ваш отзыв", reply_markup=keyboard)
    await feedback.text.set()
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(state=feedback.text)
async def feedback_handler_text(message: types.Message, state: FSMContext):
    feedback_text = message.text
    await state.update_data(
        {
            'feedback_text': feedback_text
        }
    )
    keyboard = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(text='Да', callback_data='confirm_feedback')
    no_button = InlineKeyboardButton(text='Нет', callback_data='cancel_feedback')
    keyboard.add(yes_button, no_button)
    await message.answer(text="Сохранить отзыв?", reply_markup=keyboard)
    
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'confirm_feedback', state='*')
async def process_callback_feedback_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    course_id = user_data.get('course_id')
    print('course_id: ', str(course_id))
    feedback_text = user_data.get('feedback_text')
    add_feedback(course_id, feedback_text)
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, text="Ваш отзыв успешно сохранён")
    await show_feedback_for_course(chat_id, state)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'cancel_feedback', state='*')
async def process_callback_feedback_cancellation(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    del user_data['feedback_text']
    await state.set_data(user_data)
    # course_id = user_data.get('course_id')
    # feedback_text = user_data.get('feedback_text')
    chat_id = callback_query.from_user.id
    await bot.send_message(chat_id, text="Ваш отзыв не будет сохранён")
    await show_feedback_for_course(chat_id, state)
    await bot.answer_callback_query(callback_query.id)


    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


