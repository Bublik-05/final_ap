from app.llm import get_llm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def get_assistant_response(user_message):
    llm = get_llm()

    prompt_template = PromptTemplate(
        input_variables=["question"],
        template="Ты дружелюбный помощник. Ответь на вопрос пользователя:\n{question}"
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)

    response = chain.run(question=user_message)
    return response
