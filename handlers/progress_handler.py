from aiogram import Router, types, F
from utils.text_manager import get_user_texts
import datetime

router = Router()

@router.message(F.text == "Прогресс")
async def show_progress(message: types.Message):
    texts = get_user_texts(message.from_user.id)
    if not texts:
        await message.answer("У вас пока нет добавленных текстов.")
        return

    response = "📊 <b>Ваша статистика по каждому тексту:</b>\n"
    for idx, text_data in enumerate(texts, 1):
        learned_lines = text_data.get('learned_lines', 0)
        total_lines = text_data.get('total_lines', 0)
        time_started = text_data.get('time_started', '—')
        if time_started != '—':
            time_started = datetime.datetime.fromtimestamp(time_started).strftime('%Y-%m-%d %H:%M')

        response += (
            f"\n<b>Текст {idx}:</b>\n"
            f"Строк выучено: {learned_lines}\n"
            f"Строк не выучено: {total_lines - learned_lines}\n"
            f"Время начала изучения: {time_started}\n"
        )
    await message.answer(response)
