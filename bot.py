import asyncio
import logging
from aiogram import Bot, Dispatcher
import database

# Handlers papkasidagi barcha routerlarni chaqiramiz
# Faraz qilamizki, siz hamma fayllarni yaratib, kodlarini routerga o'rab chiqqansiz.
# (Masalan: ombor.py da router = Router() bor va biz uni import qilamiz)
from handlers import common, ombor, mijozlar, buyurtma, qarzdorlik, hisobot

BOT_TOKEN = "SIZNING_BOT_TOKENINGIZNI_SHU_YERGA_YOZING"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Barcha routerlarni dispetcherga ulaymiz
dp.include_router(common.router)
dp.include_router(ombor.router)
dp.include_router(mijozlar.router)
dp.include_router(buyurtma.router)
dp.include_router(qarzdorlik.router)
dp.include_router(hisobot.router)

async def main():
    # Bazani tekshirish va yaratish
    database.create_tables()
    print("Database tayyor!")
    
    print("Bot ishga tushirildi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())