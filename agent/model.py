from langchain_openai import ChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI

llm = ChatOpenAI(model="deepseek-chat",
                 temperature=0,
                 base_url="https://api.deepseek.com",
                 api_key="sk-73adeeaec0ba47b3aa4e0834f1c54f7e")
