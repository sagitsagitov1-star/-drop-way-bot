import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

products = {
    "jordan3": {
        "name": "NIKE AIR JORDAN 3",
        "season": "Осень / весна",
        "sizes": "41–45",
        "price": "4 990 ₽"
    },
    "dunk": {
        "name": "NIKE DUNK LOW SP",
        "season": "Осень / весна",
        "sizes": "41–45",
        "price": "4 490 ₽"
    },
    "north": {
        "name": "THE NORTH FACE CORTEX",
        "season": "Осень / зима",
        "sizes": "41–46",
        "price": "5 490 ₽"
    }
}


@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="👟 Каталог", callback_data="catalog")
    keyboard.button(text="🔥 Новинки", callback_data="new")
    keyboard.button(text="📞 Связаться", callback_data="contact")

    keyboard.adjust(1)

    await message.answer(
        "👋 Добро пожаловать в DROP WAY!\n\n"
        "👟 Здесь вы можете посмотреть ассортимент кроссовок.",
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(lambda c: c.data == "catalog")
async def catalog(callback: types.CallbackQuery):
    keyboard = InlineKeyboardBuilder()

    for product_id, product in products.items():
        keyboard.button(
            text=product["name"],
            callback_data=f"product:{product_id}"
        )

    keyboard.adjust(1)

    await callback.message.edit_text(
        "👟 Каталог DROP WAY\n\nВыберите модель:",
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(lambda c: c.data.startswith("product:"))
async def product(callback: types.CallbackQuery):
    product_id = callback.data.split(":")[1]
    item = products[product_id]

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="🛒 Заказать",
        callback_data=f"order:{product_id}"
    )
    keyboard.button(
        text="⬅️ Назад",
        callback_data="catalog"
    )

    await callback.message.edit_text(
        f"👟 {item['name']}\n\n"
        f"🍂 Сезон: {item['season']}\n"
        f"📏 Размеры: {item['sizes']}\n"
        f"💰 Цена: {item['price']}\n\n"
        "Для заказа нажмите кнопку ниже.",
        reply_markup=keyboard.as_markup()
    )


@dp.callback_query(lambda c: c.data.startswith("order:"))
async def order(callback: types.CallbackQuery):
    product_id = callback.data.split(":")[1]
    item = products[product_id]

    await callback.message.answer(
        f"🛒 Заказ\n\n"
        f"👟 Модель: {item['name']}\n"
        f"💰 Цена: {item['price']}\n\n"
        "Напишите желаемый размер."
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "new")
async def new_products(callback: types.CallbackQuery):
    await callback.answer("🔥 Скоро здесь будут новинки!")


@dp.callback_query(lambda c: c.data == "contact")
async def contact(callback: types.CallbackQuery):
    await callback.message.answer(
        "📞 По вопросам заказа пишите менеджеру."
    )
    await callback.answer()


async def main():
    print("DROP WAY запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
