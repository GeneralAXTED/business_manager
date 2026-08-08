from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database

router = Router()

class MijozState(StatesGroup):
    ism = State()
    telefon = State()

def mijozlar_inline_menu():
    kb = [
        [InlineKeyboardButton(text="➕ Yangi mijoz qo'shish", callback_data="add_customer")],
        [InlineKeyboardButton(text="📋 Mijozlar ro'yxati", callback_data="view_customers")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@router.message(F.text == "👥 Mijozlar bazasi")
async def mijozlar_menu_handler(message: types.Message):
    await message.answer("👥 Mijozlar bo'limi. Nima amaliyot bajaramiz?", reply_markup=mijozlar_inline_menu())

@router.callback_query(F.data == "view_customers")
async def view_customers_handler(call: CallbackQuery):
    customers = database.get_all_customers()
    if not customers:
        await call.message.answer("Mijozlar bazasi bo'sh.")
    else:
        text = "👥 **Mijozlar ro'yxati:**\n\n"
        for m_id, ism, tel in customers:
            text += f"🆔 ID-{m_id}: **{ism}** | 📞 {tel}\n"
        await call.message.answer(text, parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "add_customer")
async def add_customer_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Mijozning **Ism-familiyasini** kiriting:\n\n(Bekor qilish: /cancel)", parse_mode="Markdown")
    await state.set_state(MijozState.ism)
    await call.answer()

@router.message(MijozState.ism)
async def process_customer_name(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("✅ Endi telefon raqamini kiriting:")
    await state.set_state(MijozState.telefon)

@router.message(MijozState.telefon)
async def process_customer_phone(message: types.Message, state: FSMContext):
    telefon = message.text.replace(" ", "")
    data = await state.get_data()
    
    success = database.add_customer(data['ism'], telefon)
    if success:
        await message.answer(f"🎉 **Mijoz saqlandi!**\nIsmi: {data['ism']}\nTelefon: {telefon}", parse_mode="Markdown")
    else:
        await message.answer("⚠️ Bu raqamli mijoz bazada mavjud!")
    await state.clear()