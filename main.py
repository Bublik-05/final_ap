import streamlit as st
from app.assistant import get_assistant_response
from app.filter import contains_bad_words
from app.memory import short_term_memory, save_to_long_term_memory, load_long_term_memory
from telegram import Bot
from app.callbacks import send_telegram_alert
import asyncio

if "test_message_sent" not in st.session_state:
    st.session_state.test_message_sent = False

if not st.session_state.test_message_sent:
    asyncio.run(send_telegram_alert("✅ Бот запущен! Это тестовое сообщение при старте приложения."))
    st.session_state.test_message_sent = True

token="7581453769:AAEBNxwmaqVUvq_AbP7p1JRhMEJFcCLLaP0"
chat_id="5768005834"

async def send_telegram_alert(message):
    bot = Bot(token)
    await bot.send_message(chat_id, text=message)


st.title("ИИ Ассистент с фильтром текста и памятью")

# Инициализация состояния сессии
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "chat_memory_type" not in st.session_state:
    st.session_state.chat_memory_type = {}

# Добавление нового чата
new_chat_name = st.sidebar.text_input("Название нового чата")
if st.sidebar.button("Создать чат"):
    if new_chat_name and new_chat_name not in st.session_state.chat_history:
        st.session_state.chat_history[new_chat_name] = []
        st.session_state.chat_memory_type[new_chat_name] = "Краткосрочная память"
        st.session_state.current_chat = new_chat_name

# Если чаты уже есть, даем выбрать
if st.session_state.chat_history:
    selected_chat = st.sidebar.radio(
        "История чатов",
        options=list(st.session_state.chat_history.keys()),
        index=list(st.session_state.chat_history.keys()).index(
            st.session_state.current_chat) if st.session_state.current_chat else 0
    )
    st.session_state.current_chat = selected_chat

if not st.session_state.current_chat:
    st.write("Создайте новый чат слева")
else:
    # Выбор памяти для текущего чата
    st.session_state.chat_memory_type[st.session_state.current_chat] = st.radio(
        "Выберите тип памяти:",
        ["Краткосрочная память", "Долгосрочная память"],
        index=0 if st.session_state.chat_memory_type[st.session_state.current_chat] == "Краткосрочная память" else 1
    )

    # Поле ввода сообщения
    user_message = st.text_input("Введите сообщение:")

    if st.button("Отправить"):
        if user_message:
            
            if contains_bad_words(user_message):
                st.error("Обнаружена ненормативная лексика. Пожалуйста, переформулируйте ваш вопрос.")
                asyncio.run(send_telegram_alert(f"⚠️ Пользователь отправил плохой текст: {user_message}"))
            else:
                memory_type = st.session_state.chat_memory_type[st.session_state.current_chat]

                if memory_type == "Краткосрочная память":
                    short_term_memory.save_context({"input": user_message}, {"output": "Ответ генерируется..."})
                    response = get_assistant_response(user_message)
                    short_term_memory.save_context({"input": user_message}, {"output": response})

                elif memory_type == "Долгосрочная память":
                    long_term_history = load_long_term_memory()
                    context_message = f"История диалога:\n{long_term_history}\nПользователь: {user_message}"
                    response = get_assistant_response(context_message)
                    save_to_long_term_memory(user_message, response)

                # Сохранение в историю чата
                st.session_state.chat_history[st.session_state.current_chat].append(f"Вы: {user_message}")
                st.session_state.chat_history[st.session_state.current_chat].append(f"ИИ: {response}")

    # Показать историю текущего чата
    st.write("История диалога:")
    for message in st.session_state.chat_history[st.session_state.current_chat]:
        st.write(message)
