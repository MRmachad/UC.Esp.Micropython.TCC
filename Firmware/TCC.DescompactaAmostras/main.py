from Arquivos_py.descompactador import Descompactador


DIR_PADRAO = "./"

QTDACONJUNTO = 39

if __name__ == "__main__":
    descompactador = Descompactador(DIR_PADRAO, ConjAmostra = QTDACONJUNTO)                                                              
    descompactador.descompacta()