from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os


class GPTBase:
    def __init__(self, system_prompt, model_name="gpt-3.5-turbo-16k", temperature=0):
        self.default_model_name = model_name
        self.default_temperature = temperature

        self.chat = ChatOpenAI(
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            model_name=self.default_model_name,
            temperature=self.default_temperature,
            openai_api_base="https://openrouter.ai/api/v1",
        )
        self.system_message = SystemMessage(content=system_prompt)

    def generate_message(self, human_message, model_name=None, temperature=None):
        """Generates a system response message given a human message."""
        if model_name or temperature is not None:
            temporary_model_name = model_name if model_name else self.default_model_name
            temporary_temperature = (
                temperature if temperature is not None else self.default_temperature
            )
            temporary_chat = ChatOpenAI(
                openai_api_key=os.getenv("OPENROUTER_API_KEY"),
                openai_api_base="https://openrouter.ai/api/v1",
                model_name=temporary_model_name,
                temperature=temporary_temperature,
            )
        else:
            temporary_chat = self.chat

        messages = [
            self.system_message,
            HumanMessage(content=human_message),
        ]

        result = temporary_chat(messages)

        return result.content
