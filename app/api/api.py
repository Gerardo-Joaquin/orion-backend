from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.online_model import model
from fastapi import Request, Response
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:4200'],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post('/data')
async def get_data(req: Request):
    json_ = await req.json()
    question = json_['question']
    print(question)
    # return question
    response = model.run_model(question)
    print(response)

    return response