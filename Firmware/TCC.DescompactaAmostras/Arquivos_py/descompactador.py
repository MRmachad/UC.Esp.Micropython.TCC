import pandas as pd
import socket
import struct
import datetime

from Arquivos_py.onSd import OnSd
from array import array


class Descompactador():

    sock = socket.socket()
    
    def __init__(self, dir = "/", ConjAmostra = 10):
        self.dir = dir
        self.ConjAmostra = ConjAmostra
        self.OB_Card = OnSd(self.dir)      
        
    def descompacta(self):

        _id=[]  
        _hora=[]
        _acx=[]
        _acy=[]
        _acz=[]
        _temperatura=[]

        for LoteX in self.OB_Card.contArq():

            print("\nLotex :", LoteX)

            try:
                pacBytes = ((170*3) + 15)
                input_file = open((self.dir + "/data/" + LoteX), 'r+b')
                nBytes = input_file.seek(0,2)
                input_file.seek(0)

          
                while input_file.tell() != nBytes:
                    
                    bytesfile = input_file.read(pacBytes*4)
                    float_array = array('f', struct.unpack((pacBytes*'f'), bytesfile))   
                    

                    id_, hora,  acx, acy, acz,temperatura = self.modelosStringJson(float_array)
                    
                    _id+=(id_)   
                    _hora+=(hora)
                    _acx+=(acx)
                    _acy+=(acy)
                    _acz+=(acz)
                    _temperatura+=(temperatura)
                    
            finally:
                input_file.close()

        print(hora)
        df = pd.DataFrame({"id":[0]*len(_id),"id_vaca":_id,"hora":_hora,"aceleracaox":_acx,"aceleracaoy":_acy,"aceleracaoz":_acz, "temperatura": _temperatura})
        print(df)

        df.to_excel('./amostras.xlsx', index = None)
        




    def modelosStringJson(self, float_array, temperatura = 0):

        _id=[]  
        _hora=[]
        _acx=[]
        _acy=[]
        _acz=[]
        _temperatura=[]

        date = []
        aux =  0

        data_inicial = datetime.datetime(int(float_array[1]),int(float_array[2]),int(float_array[3]),int(float_array[4]),int(float_array[5]),int(float_array[6]),int(float_array[7]/100))
        
        data_final = datetime.datetime(int(float_array[8]),int(float_array[9]),int(float_array[10]),int(float_array[11]),int(float_array[12]),int(float_array[13]),int(float_array[14]/100))

        lenraw_entreMeio = 170 - 1

        diferenca = (data_final - data_inicial) / lenraw_entreMeio

        date = [data_inicial.strftime("%Y-%m-%d %H:%M:%S.%f")]

        for i in range(lenraw_entreMeio-1):
            data_inicial = (data_inicial + diferenca)
            date.append(str(data_inicial))

        date.append(data_final.strftime("%Y-%m-%d %H:%M:%S.%f"))


        for cont in range(15,len(float_array), 3):

            _id.append(int(float_array[0]))   
            _hora.append(date[aux])
            _acx.append(float_array[cont])
            _acy.append(float_array[cont+1])
            _acz.append(float_array[cont+2])
            _temperatura.append(0)
            aux+=1


        return  _id, _hora, _acx, _acy,_acz,_temperatura
    
    