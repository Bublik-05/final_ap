import streamlit as st
from app.assistant import get_assistant_response
from app.filter import contains_bad_words, check_for_bad_words
#from app.callbacks import send_telegram_alert

st.title("ИИ Ассистент с фильтром текста")

user_message = st.text_input("Введите ваш вопрос:")

if st.button("Отправить"):
    if contains_bad_words(user_message):  # или check_for_bad_words(user_message)
        st.error("Обнаружена ненормативная лексика. Пожалуйста, переформулируйте ваш вопрос.")
        #send_telegram_alert(f"Пользователь отправил плохой текст: {user_message}")
    else:
        response = get_assistant_response(user_message)
        st.write("Ответ ассистента:")
        st.write(response)
