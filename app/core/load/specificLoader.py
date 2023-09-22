from pandas import read_csv
from unidecode import unidecode
import os

class Loader:
    def __init__(self):
        """Docstring."""
        self.data_list: list = None 

    def loadData(self, *datasName: str):
        print(os.getcwd())
        path = 'app/resources/data/'
        data_list = list()
        for dataName in datasName:
            data = read_csv(path + dataName, sep=',', encoding='latin1', header=0)
            data = data.applymap(procesar_texto)
            if dataName == 'documentos.csv':
                #Drop useless columns
                data = data.drop(['fecha_limite',
                                  'clave',
                                  'modificado_por_id',
                                  'descripcion',
                                  'sector',
                                  'tipo_documento',
                                  'cve_direccion',
                                  'creado_por_id'], axis=1)
                #Rename variables
                new_names = {'n': 'sin asignar',
                             'a': 'asignado',
                             'e': 'notificado',
                             'ne': 'no notificado',
                             'p': 'pendiente'}
                data['estatus_documento_clave'] = data['estatus_documento_clave'].replace(new_names)
                
                #Rename columns names
                data = data.rename(columns={'estatus_documento_clave': 'estatus_documento',
                                            'cve_auditoria': 'clave_auditoria'})
                #Drop NA
                data = data.dropna(subset='nombre')
                # data.reset_index(drop=True, inplace=True)
                # data = data.iloc[0:3500]
            # if dataName == 'regimen.csv':
            #     data = data.iloc[0]
            data_list.append(data)
            setattr(self, dataName[:-4], data)
        self.data_list = data_list

# Función para poner en minúsculas y quitar acentos
def procesar_texto(entry):
    if isinstance(entry, str):
        return unidecode(entry.lower())
    return entry
                