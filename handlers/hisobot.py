from aiogram import Router, F, types
import database

# Router orqali botga ulanadi
router = Router()

@router.message(F.text == "📊 Kunlik/Oylik Hisobot")
async def hisobot_handler(message: types.Message):
    # Bazadan hisobot ma'lumotlarini olish
    kunlik_savdo, oylik_savdo = database.get_reports()
    
    text = (
        "📊 **MOLIYAVIY HISOBOT** 📊\n"
        "========================\n\n"
        f"📅 **Bugungi savdo aylanmasi:**\n"
        f"💰 {kunlik_savdo:,.0f} so'm\n\n"
        f"📆 **Shu oydagi umumiy savdo:**\n"
        f"💰 {oylik_savdo:,.0f} so'm\n\n"
        "========================"
    )
    
    await message.answer(text, parse_mode="Markdown")