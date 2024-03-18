from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os

def fewshot_chain(prompt):
    os.environ["OPENAI_API_KEY"] = "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"
    examples = [
        {
            "question": 
            """
            example people info:
            [{'name': '조현우', 'applicant': '인그래디언트 주식회사', 'address': '경기도 고양시 일산서구 고양대로 633 동양아파트 103동 501호', 'start': '2011-02-23', 'end': '2011-02-23'}],
            [{'name': '조현우', 'applicant': 'Wips', 'address': '경기도 고양시 일산서구 고양대로 633 동양아파트 103동 501호', 'start': '2021-02-23', 'end': '2021-02-23'}],
            [{'name': '조현우', 'applicant': '인그래디언트 주식회사', 'address': '경기도 고양시 일산서구 고양대로 633 동양아파트 103동 501호', 'start': '2021-02-23', 'end': '2021-02-23'}],
            [{'name': '조현우', 'applicant': '인그래디언트 주식회사', 'address': '경기도 고양시 일산서구 고양대로 633 동양아파트 103동 501호', 'start': '2021-02-23', 'end': '2021-02-23'}] 

            input person info : 
            [{'name': '조현우', 'applicant': '삼성 전자', 'address': '경기도 고양시 일산서구 고양대로 633 동양아파트 103동 501호', 'date' : '2023-06-15'}] 
            
            """,
            
            "answer": """

            """
        },
        {
            "question": "Make the follow question more detailed to answer easier.'what is the biggest planet?'",
            "answer": """
            What is the biggest planet in the Solar system? The biggest means the biggest radius of planet, and 
            you don't have to think about rings of planet. Think and explain step by step.
            """
        },
        {
            "question": "Make the follow question more detailed to answer easier.'what is popular korean food?'",
            "answer": """
            I want to eat some Korean food, however I don't know which Korean food is exist. Find the most popular
            Korean food, and give me top 3 of that. Think and explain step by step.
            """
        },
    ]

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{question}"),
            ("ai", "{answer}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
                        You are a helpful assistant for distinguish person who have same name.
                        You should distinguish input person from example people.
                        The output should be information of one of the example people.
                        Answer nothing except the information of the example people, for exaple
                        'This is the answer you want'
                        I gave you some examples, so refer them.
                        """),
            few_shot_prompt,
            ("human", "{question}"),
        ]
    )

    model = ChatOpenAI(model="gpt-3.5-turbo")
    chain = final_prompt | model | StrOutputParser()

    return chain.invoke({"question":prompt})

    # final_answer = chain.invoke({"question": "what is the most yummy korea food?"}).content
    # print(final_answer)
