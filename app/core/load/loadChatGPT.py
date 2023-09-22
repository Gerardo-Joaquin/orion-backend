import openai

class chatGPT():
    def __init__(self, key) -> None:
        openai.api_key = key
    def get_completion(self, prompt, model="gpt-4"):

        messages = [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(

        model=model,

        messages=messages,

        temperature=0,

        )

        return response.choices[0].message["content"]