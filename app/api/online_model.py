from app.core.load.specificLoader import Loader
from app.core.load.loadModel import PandasAIModel

#Load datas
Datas = Loader()
Datas.loadData('regimen.csv', 'documentos.csv')

#Save into json
Datas.documentos.to_json('./documents.json', orient = 'records')

model = PandasAIModel('openai', Datas)
