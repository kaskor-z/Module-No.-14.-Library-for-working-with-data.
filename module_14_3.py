from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "7060077173:AAEBkb9YrPhdpYYV1i8IyxDx2fzQi1WNE8o"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Рассчитать"),
            KeyboardButton(text="Информация"),
            KeyboardButton(text="Купить")
        ]
    ], resize_keyboard=True, row_width=3
)

kb_2 = InlineKeyboardMarkup()
Button_3 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
Button_4 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
kb_2.row(Button_3, Button_4)

kb_3 = InlineKeyboardMarkup()
Button_1_3 = InlineKeyboardButton(text="Product_1", callback_data="product_buying")
Button_2_3 = InlineKeyboardButton(text="Product_2", callback_data="product_buying")
Button_3_3 = InlineKeyboardButton(text="Product_3", callback_data="product_buying")
Button_4_3 = InlineKeyboardButton(text="Product_4", callback_data="product_buying")
kb_3.row(Button_1_3, Button_2_3, Button_3_3, Button_4_3)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Расчёт индивидуальной калорийности продуктов:", reply_markup=kb_1)


@dp.message_handler(text=["Рассчитать"])
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb_2)


@dp.callback_query_handler(text=["formulas"])
async def get_formulas(call):
    await call.answer("для мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x 1.2")
    await call.answer()


@dp.callback_query_handler(text=["calories"])
async def set_age(call):
    await call.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age_=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth_=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_caloris(message, state):
    await state.update_data(weight_=message.text)
    data = await state.get_data()
    calorie_norms = (10.0 * float(data['weight_']) +
                     6.25 * float(data['growth_']) -
                     5.0 * float(data['age_']) + 5.0) * 1.2
    await message.answer(f'Ваша норма калорийности питания: \n\t\t{calorie_norms} ккал/день')
    await state.finish()


@dp.message_handler(text=["Купить"])
async def get_beyin_list(message):
    for i in range(1, 5):
        with open(f'Витамины/{i}.png', "rb") as img:
            await message.answer_photo(img, f'Название: Product_{i} | Описание: описание {i} | Цена: {i * 100}')
    await message.answer("Выберите продукт для покупки:", reply_markup=kb_3)


@dp.callback_query_handler(text=["product_buying"])
async def send_confirm_message(call):
    await call.answer("Вы успешно приобрели продукт!")
    await call.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
