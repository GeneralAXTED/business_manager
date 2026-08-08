from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database

router = Router()

class BuyurtmaState(StatesGroup):
    mijoz_id = State()
    mahsulot_id = State()
    miqdori = State()

def buyurtma_inline_menu():
    kb = [[InlineKeyboardButton(text="🛍 Yangi buyurtma", callback_data="new_order")]]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@router.message(F.text == "🛒 Buyurtmalar")
async def buyurtmalar_menu(message: types.Message):
    await message.answer("🛒 Buyurtmalar bo'limi.", reply_markup=buyurtma_inline_menu())

@router.callback_query(F.data == "new_order")
async def new_order_start(call: CallbackQuery, state: FSMContext):
    customers = database.get_all_customers()
    if not customers:
        return await call.message.answer("⚠️ Baza bo'sh! Mijoz qo'shing.")
    
    text = "👥 **Qaysi mijoz xarid qilyapti?** (ID ni yozing)\n\n"
    for m_id, ism, _ in customers: text += f"ID-{m_id}: {ism}\n"
    
    await call.message.answer(text, parse_mode="Markdown")
    await state.set_state(BuyurtmaState.mijoz_id)
    await call.answer()

@router.message(BuyurtmaState.mijoz_id)
async def process_order_customer(message: types.Message, state: FSMContext):
    if not message.text.isdigit(): return await message.answer("⚠️ Faqat ID kiriting!")
    
    mijoz_id = int(message.text)
    if not database.get_customer_by_id(mijoz_id): return await message.answer("⚠️ Mijoz topilmadi.")

    await state.update_data(mijoz_id=mijoz_id)
    products = database.get_all_products()
    
    text = "📦 **Qaysi mahsulot sotilyapti?** (ID ni yozing)\n\n"
    for p_id, nomi, narxi, miq in products: text += f"ID-{p_id}: {nomi} ({miq} ta bor)\n"
    
    await message.answer(text, parse_mode="Markdown")
    await state.set_state(BuyurtmaState.mahsulot_id)

@router.message(BuyurtmaState.mahsulot_id)
async def process_order_product(message: types.Message, state: FSMContext):
    if not message.text.isdigit(): return await message.answer("⚠️ ID kiriting!")
    
    prod = database.get_product_by_id(int(message.text))
    if not prod: return await message.answer("⚠️ Mahsulot topilmadi.")
    if prod[3] <= 0: return await message.answer("⚠️ Omborda qolmagan!")

    await state.update_data(mahsulot_id=prod[0], narxi=prod[2], nomi=prod[1], qoldiq=prod[3])
    await message.answer(f"Nechta sotyapsiz? (Maksimal: {prod[3]} ta)")
    await state.set_state(BuyurtmaState.miqdori)

@router.message(BuyurtmaState.miqdori)
async def process_order_quantity(message: types.Message, state: FSMContext):
    if not message.text.isdigit(): return await message.answer("⚠️ Raqam yozing!")
    qty = int(message.text)
    data = await state.get_data()
    
    if qty > data['qoldiq']: return await message.answer("⚠️ Omborda buncha yo'q!")

    total = qty * data['narxi']
    success, msg = database.create_order(data['mijoz_id'], data['mahsulot_id'], qty, total)
    
    if success:
        await message.answer(f"🧾 **CHEK**\n📦 {data['nomi']}\n🔢 {qty} ta\n💰 {total:,.0f} so'm\n✅ Saqlandi!", parse_mode="Markdown")
    else:
        await message.answer(f"❌ Xatolik: {msg}")
    await state.clear()