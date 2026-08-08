from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

router = Router()

def main_menu():
    kb = [
        [KeyboardButton(text="🛒 Buyurtmalar"), KeyboardButton(text="👥 Mijozlar bazasi")],
        [KeyboardButton(text="📦 Ombor"), KeyboardButton(text="💳 Qarzdorlik")],
        [KeyboardButton(text="📊 Kunlik/Oylik Hisobot")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear() # Har ehtimolga qarshi barcha holatlarni tozalaymiz
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}!\n"
        f"📊 Telegram Business Manager tizimiga xush kelibsiz.\n"
        f"Quyidagi menyudan kerakli bo'limni tanlang:",
        reply_markup=main_menu()
    )

@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Amaliyot bekor qilindi.", reply_markup=main_menu())