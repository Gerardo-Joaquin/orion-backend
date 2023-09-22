from pandas import read_excel, ExcelFile
import os

class Loader():
    def __init__(self, dataPath:str) -> None:
        """Docstring."""
        self.load_datas(dataPath)
    
    def load_datas(self, dataPath:str):
        """Docstring."""
        datasName = os.listdir(dataPath)
        for name in datasName:
            # print('DATA ', name )
            if name != 'logs.txt':
                excelFile = ExcelFile(dataPath+name)
                sheetNames = excelFile.sheet_names
                if name == 'ori.xlsx':
                    for sheetName in sheetNames:
                        print('read ', sheetName )
                        if sheetName == 'regimen' or sheetName == 'documentos':
                            data = read_excel(dataPath+name, sheet_name=sheetName)
                            
                            setattr(self, sheetName, data)