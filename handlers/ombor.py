from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database

router = Router()

class OmborState(StatesGroup):
    nomi = State()
    narxi = State()
    miqdori = State()

def ombor_inline_menu():
    kb = [
        [InlineKeyboardButton(text="➕ Mahsulot qo'shish", callback_data="add_product")],
        [InlineKeyboardButton(text="📋 Qoldiqni ko'rish", callback_data="view_products")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@router.message(F.text == "📦 Ombor")
async def ombor_menu_handler(message: types.Message):
    await message.answer("📦 Ombor bo'limi. Nima amaliyot bajaramiz?", reply_markup=ombor_inline_menu())

@router.callback_query(F.data == "view_products")
async def view_products_handler(call: CallbackQuery):
    products = database.get_all_products()
    if not products:
        await call.message.answer("Ombor hozircha bo'sh.")
    else:
        text = "📦 **Ombordagi mahsulotlar:**\n\n"
        for idx, nomi, narxi, miqdori in products:
            text += f"ID-{idx}: {nomi} - {narxi:,.0f} so'm | {miqdori} ta qolgan\n"
        await call.message.answer(text, parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "add_product")
async def add_product_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Yangi mahsulotning **nomini** kiriting:\n\n(Bekor qilish uchun /cancel yozing)", parse_mode="Markdown")
    await state.set_state(OmborState.nomi)
    await call.answer()

@router.message(OmborState.nomi)
async def process_product_name(message: types.Message, state: FSMContext):
    await state.update_data(nomi=message.text)
    await message.answer(f"✅ Qabul qilindi. Endi **{message.text}** ning narxini (raqamda) kiriting:", parse_mode="Markdown")
    await state.set_state(OmborState.narxi)

@router.message(OmborState.narxi)
async def process_product_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("⚠️ Iltimos, narxni faqat raqamlarda kiriting!")
    await state.update_data(narxi=float(message.text))
    await message.answer("✅ Narx qabul qilindi. Endi miqdorini kiriting:")
    await state.set_state(OmborState.miqdori)

@router.message(OmborState.miqdori)
async def process_product_quantity(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("⚠️ Miqdorni faqat raqamlarda kiriting!")
    
    data = await state.get_data()
    nomi = data['nomi']
    narxi = data['narxi']
    miqdori = int(message.text)

    success = database.add_product(nomi, narxi, miqdori)
    if success:
        await message.answer(f"🎉 **Mahsulot qo'shildi!**\nNomi: {nomi}\nNarxi: {narxi:,.0f} so'm\nMiqdori: {miqdori} ta", parse_mode="Markdown")
    else:
        await message.answer("⚠️ Bu nomdagi mahsulot allaqachon mavjud.")
    await state.clear()