from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database

router = Router()

class QarzState(StatesGroup):
    mijoz_id = State()
    summa = State()
    izoh = State()

class QarzTolashState(StatesGroup):
    qarz_id = State()
    summa = State()

def qarzdorlik_inline_menu():
    kb = [
        [InlineKeyboardButton(text="➕ Qarz yozish", callback_data="add_debt")],
        [InlineKeyboardButton(text="📋 Qarzdorlar", callback_data="view_debts")],
        [InlineKeyboardButton(text="💸 Qarzni uzish", callback_data="pay_debt")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@router.message(F.text == "💳 Qarzdorlik")
async def qarzdorlik_menu(message: types.Message):
    await message.answer("💳 Qarzdorlik bo'limi.", reply_markup=qarzdorlik_inline_menu())

@router.callback_query(F.data == "view_debts")
async def view_debts_handler(call: CallbackQuery):
    debts = database.get_all_debts()
    if not debts:
        await call.message.answer("🎉 Qarzdorlar yo'q.")
    else:
        text = "📋 **Qarzdorlar:**\n\n"
        for q_id, ism, tel, sum, izoh, _ in debts:
            text += f"ID: {q_id} | {ism}\n💰 {sum:,.0f} so'm\n📌 {izoh}\n---\n"
        await call.message.answer(text)
    await call.answer()

@router.callback_query(F.data == "add_debt")
async def add_debt_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Mijoz ID sini yozing (Ro'yxatdan qarab):")
    await state.set_state(QarzState.mijoz_id)
    await call.answer()

@router.message(QarzState.mijoz_id)
async def process_debt_customer(message: types.Message, state: FSMContext):
    await state.update_data(mijoz_id=int(message.text))
    await message.answer("💰 Qarz summasini raqamda kiriting:")
    await state.set_state(QarzState.summa)

@router.message(QarzState.summa)
async def process_debt_sum(message: types.Message, state: FSMContext):
    await state.update_data(summa=float(message.text))
    await message.answer("📌 Izoh yozing:")
    await state.set_state(QarzState.izoh)

@router.message(QarzState.izoh)
async def process_debt_desc(message: types.Message, state: FSMContext):
    data = await state.get_data()
    database.add_debt(data['mijoz_id'], data['summa'], message.text)
    await message.answer("✅ Qarz yozildi!")
    await state.clear()

@router.callback_query(F.data == "pay_debt")
async def pay_debt_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Qaysi Qarz ID ga to'lov qilyapsiz?")
    await state.set_state(QarzTolashState.qarz_id)
    await call.answer()

@router.message(QarzTolashState.qarz_id)
async def process_pay_debt_id(message: types.Message, state: FSMContext):
    await state.update_data(qarz_id=int(message.text))
    await message.answer("Qancha to'ladi?")
    await state.set_state(QarzTolashState.summa)

@router.message(QarzTolashState.summa)
async def process_pay_debt_sum(message: types.Message, state: FSMContext):
    data = await state.get_data()
    success, msg = database.pay_debt(data['qarz_id'], float(message.text))
    await message.answer(msg)
    await state.clear()