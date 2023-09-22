from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from pandasai.llm.google_palm import GooglePalm
from pandasai.llm.falcon import Falcon
import datetime
import re
import os
from app.core.load.loadChatGPT import chatGPT
from app.core.load.specificLoader import Loader

class PandasAIModel:
    """Docstring."""

    def __init__(self, type_:str, data: Loader) -> None:
        """Docstring."""
        tokenOpenAi = os.getenv("OPENAITOKEN", "")
        if type_ == 'openai':
            llm = OpenAI(api_token=tokenOpenAi)
        elif type_ == 'google':
            llm = GooglePalm(api_token="YOUR_Google_API_KEY")
        elif type_ == 'falcon':
            llm = Falcon(api_token="hf_XDdnKDSemLVkpBbBaC")

        self.model = PandasAI(llm, conversational=False, enable_cache=False)
        
        self.chatGPT = chatGPT(tokenOpenAi)
        self.data = data
        
    def run(self, datas:list, question:str):
        """Docstring"""
        question = re.sub(r'\s+', ' ', question)
        if 'hoy' in question:
            currentDate = datetime.datetime.now()
            currentDate = currentDate.strftime('%d de %B del %Y')
            question = question.replace("hoy", currentDate)
        print(question)
        not_able = 'Unfortunately, I was not able to answer your question,'
        for i in range(2):
            response = str(self.model.run(datas, question))
            print(response)
            if not_able not in response:
                question = 'si el siguiente texto está en inglés regresa un "si": ' + response
                answer = self.chatGPT.get_completion(question)
                if answer in ['si', 'Sí', 'sí']:
                    response = 'Te enviaré el siguiente texto:\n' + response + '\n  pasa la respuesta al español'
                    response = self.chatGPT.get_completion(response)
                break
            else:
                response = 'Porfavor reformula tu pregunta porque no entendí bien el contexto'

        return str(response)

    def run_model(self, question: str):
        return self.run(self.data.data_list, question)

