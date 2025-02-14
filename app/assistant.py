from app.llm import get_llm
from langchain.prompts import PromptTemplate

def get_assistant_response(user_message):
    llm = get_llm()

    prompt_template = PromptTemplate(
        input_variables=["question"],
        template="Ты дружелюбный помощник. Ответь на вопрос пользователя:\n{question}"
    )

    chain = prompt_template | llm

    response = chain.invoke({"question": user_message})
    return response.content if hasattr(response, 'content') else response
