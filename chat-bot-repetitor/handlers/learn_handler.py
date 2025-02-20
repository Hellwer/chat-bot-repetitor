from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from utils.text_manager import get_user_texts
from keyboards.learn_menu import learn_menu_kb
from keyboards.main_menu import main_menu_kb

router = Router()

class LearnTextState(StatesGroup):
    choosing_text = State()
    choosing_split = State()
    learning = State()

@router.message(F.text == "Учить")
async def choose_text_to_learn(message: types.Message, state: FSMContext):
    texts = get_user_texts(message.from_user.id)
    if not texts:
        await message.answer("У вас пока нет добавленных текстов.")
        return

    response = "📖 <b>Выберите текст для изучения:</b>\n"
    for idx, text_data in enumerate(texts, 1):
        first_line = text_data['text'].split('\n')[0]
        response += f"{idx}. {first_line}\n"

    await message.answer(response)
    await message.answer("Введите номер текста, который хотите учить:")
    await state.set_state(LearnTextState.choosing_text)

@router.message(F.text == "Вернуться в меню")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu_kb())

@router.message(LearnTextState.choosing_text, F.text.func(lambda text: text.isdigit()))
async def receive_text_choice(message: types.Message, state: FSMContext):
    selected_number = int(message.text) - 1
    texts = get_user_texts(message.from_user.id)

    if 0 <= selected_number < len(texts):
        await state.update_data(selected_text=selected_number)
        await message.answer("Как разбить текст?", reply_markup=learn_menu_kb())
        await state.set_state(LearnTextState.choosing_split)
    else:
        await message.answer("❌ Неверный номер текста. Попробуйте снова.")

@router.message(LearnTextState.choosing_split, F.text.in_(["по предложениям", "по абзацам"]))
async def start_learning(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    split_method = message.text
    selected_text_index = user_data['selected_text']
    texts = get_user_texts(message.from_user.id)
    selected_text = texts[selected_text_index]['text']

    # Разбиваем текст
    if split_method == "по предложениям":
        parts = selected_text.split('. ')
    else:
        parts = selected_text.split('\n\n')

    # Сохраняем части текста в состоянии
    await state.update_data(text_parts=parts, current_part=0)
    await message.answer("✅ Начинаем обучение!")
    await send_next_part(message, state)

    await state.set_state(LearnTextState.learning)

async def send_next_part(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    current_part = user_data['current_part']
    text_parts = user_data['text_parts']

    if current_part < len(text_parts):
        await message.answer(f"📚 {text_parts[current_part]}")
        await state.update_data(current_part=current_part + 1)
    else:
        await message.answer("🎉 Вы закончили изучение текста!", reply_markup=main_menu_kb())
        await state.clear()

@router.message(LearnTextState.choosing_text, F.text == "Вернуться в меню")
async def cancel_choosing_text(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выбор текста отменён.", reply_markup=main_menu_kb())

@router.message(LearnTextState.choosing_split, F.text == "Вернуться в меню")
async def cancel_choosing_split(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Выбор способа разбивки отменён.", reply_markup=main_menu_kb())

@router.message(LearnTextState.learning, F.text == "Вернуться в меню")
async def cancel_learning(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Обучение остановлено.", reply_markup=main_menu_kb())

@router.message(LearnTextState.learning)
async def continue_learning(message: types.Message, state: FSMContext):
    # Здесь можно проверить ответы пользователя и обновить прогресс
    await send_next_part(message, state)
