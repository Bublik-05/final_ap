bad_words = {"мат", "плохое_слово", "ругательство"}

def contains_bad_words(text):
    words = text.lower().split()
    for word in words:
        if word in bad_words:
            return True
    return False


from app.llm import get_llm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def check_for_bad_words(text):
    llm = get_llm()

    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="Проверь, есть ли в этом тексте нецензурная лексика. Ответь 'Да' или 'Нет':\n{text}"
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)

    response = chain.run(text=text)
    return "да" in response.lower()
