from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import crud_functions
import asyncio

api = "7060077173:AAEBkb9YrPhdpYYV1i8IyxDx2fzQi1WNE8o"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Рассчитать"),
            KeyboardButton(text="Информация"),
            KeyboardButton(text="Купить"),
            KeyboardButton(text="Регистрация")
        ]
    ], resize_keyboard=True, row_width=3
)

kb_2 = InlineKeyboardMarkup()
Button_3 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
Button_4 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
kb_2.row(Button_3, Button_4)

kb_3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Product_1", callback_data="product_buying"),
            InlineKeyboardButton(text="Product_2", callback_data="product_buying"),
            InlineKeyboardButton(text="Product_3", callback_data="product_buying"),
            InlineKeyboardButton(text="Product_4", callback_data="product_buying")
        ]
    ], resize_keyboard=True, row_width=4
)
all_products = crud_functions.get_all_products()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age_usr = State()
    balans = State()


@dp.message_handler(text=["Регистрация"])
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if crud_functions.is_included(message["text"]):
        await message.answer("Пользователь существует, введите другое имя")
    else:
        await state.update_data(username_=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email_=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age_usr.set()


@dp.message_handler(state=RegistrationState.age_usr)
async def set_age(message, state):
    await state.update_data(age_usr_=message.text)
    data_usr = await state.get_data()
    crud_functions.add_user(data_usr["username_"],
                            data_usr["email_"],
                            data_usr["age_usr_"],
                            1000
                            )
    await message.answer("Регистрация прошла успешно")
    await state.finish()


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
    for i in range(4):
        with open(all_products[i][3], "rb") as img:
            await message.answer_photo(img, f'Название: {all_products[i][1]} | '
                                            f'Описание: описание {all_products[i][2]} | '
                                            f'Цена: {all_products[i][4]}')
    await message.answer("Выберите продукт для покупки:", reply_markup=kb_3)


@dp.callback_query_handler(text=["product_buying"])
async def send_confirm_message(call):
    await call.answer("Вы успешно приобрели продукт!")
    await call.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
