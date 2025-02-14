from langchain.memory import ConversationBufferMemory

short_term_memory = ConversationBufferMemory()

def save_to_long_term_memory(user_message, assistant_response):
    with open("long_term_memory.txt", "a", encoding="utf-8") as file:
        file.write(f"Пользователь: {user_message}\nИИ: {assistant_response}\n")

def load_long_term_memory():
    try:
        with open("long_term_memory.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""
