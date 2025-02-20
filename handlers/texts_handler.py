from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.texts_menu import texts_menu_kb
from keyboards.main_menu import main_menu_kb
from utils.text_manager import get_user_texts, add_user_text

router = Router()

class AddTextState(StatesGroup):
    waiting_for_text = State()

class TextsState(StatesGroup):
    waiting_for_text_number = State()

@router.message(F.text == "Список текстов")
async def show_texts_menu(message: types.Message):
    await message.answer(
        "Выберите действие:",
        reply_markup=texts_menu_kb()
    )

@router.message(F.text == "Вернуться в меню")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu_kb())

@router.message(F.text == "добавить текст")
async def add_text(message: types.Message, state: FSMContext):
    await message.answer("📄 Отправь текст, который хочешь выучить:")
    await state.set_state(AddTextState.waiting_for_text)

@router.message(AddTextState.waiting_for_text)
async def receive_text(message: types.Message, state: FSMContext):
    add_user_text(message.from_user.id, message.text)
    await message.answer("✅ Текст добавлен!", reply_markup=main_menu_kb())
    await state.clear()

@router.message(F.text == "перейти по текстам")
async def list_texts(message: types.Message, state: FSMContext):
    texts = get_user_texts(message.from_user.id)
    if not texts:
        await message.answer("📭 У вас пока нет добавленных текстов.")
        return

    response = "📄 <b>Ваши тексты:</b>\n"
    for idx, text_data in enumerate(texts, 1):
        first_line = text_data['text'].split('\n')[0]
        response += f"{idx}. {first_line}\n"

    await message.answer(response)
    await message.answer("Введите номер текста, чтобы открыть его.")
    await state.set_state(TextsState.waiting_for_text_number)

@router.message(AddTextState.waiting_for_text, F.text == "Вернуться в меню")
async def cancel_adding_text(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Добавление текста отменено.", reply_markup=main_menu_kb())

@router.message(TextsState.waiting_for_text_number)
async def show_selected_text(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Пожалуйста, введите корректный номер текста.")
        return

    selected_number = int(message.text) - 1
    texts = get_user_texts(message.from_user.id)

    if 0 <= selected_number < len(texts):
        selected_text = texts[selected_number]['text']
        await message.answer(f"📄 <b>Текст {selected_number + 1}:</b>\n\n{selected_text}")
        await state.clear()
    else:
        await message.answer("❌ Текст с таким номером не найден. Попробуйте снова.")
