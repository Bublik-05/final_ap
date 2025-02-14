from langchain.chat_models import ChatOllama

def get_llm():
    return ChatOllama(model="llama3.2")  # или phi
