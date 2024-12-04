from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *


api = '1'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

menu = ReplyKeyboardMarkup([
    [KeyboardButton(text='Информация'), KeyboardButton(text='Рассчитать'),
        KeyboardButton(text='Купить')]
],
resize_keyboard=True)

inline_choices = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
         InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)

inline_products = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ретро-телефон', callback_data='product_buying'),
         InlineKeyboardButton(text='Ретро-холодильник', callback_data='product_buying'),
         InlineKeyboardButton(text='Ретро-компьютер', callback_data='product_buying'),
         InlineKeyboardButton(text='Ретро-плеер', callback_data='product_buying')]
    ]
)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for index, product in enumerate(get_all_products()):
        await message.answer(f'Название: {product[1]} | Описание: описание {product[2]} | Цена: {product[3]}')
        print(f'Название: {product[1]} | Описание: описание {product[2]} | Цена: {product[3]}')
        with open(f'image/image{index+1}.jpg', 'rb') as photo:
            await  message.answer_photo(photo)
            print(f'Отправлено изображение {index+1}')
    await message.answer("Выберите продукт для покупки:", reply_markup=inline_products)
    print("Выберите продукт для покупки:")

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    print("Вы успешно приобрели продукт!")


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_choices)
    print('Выберите опцию:')

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формулы расчета: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    print('Формулы расчета: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    print('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    print('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    print('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий составляет: {result}')
    print(f'Ваша норма калорий составляет: {result}')
    await state.finish()


@dp.message_handler(commands='start')
async def start(message):
    await message.answer('Привет! Какая техника тебя интересует?', reply_markup=menu)
    print('Привет! Какая техника тебя интересует?')

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')
    print('Введите команду /start, чтобы начать общение.')


@dp.message_handler()
async def send_confirm_message(message):
    print("Вы успешно приобрели продукт!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)