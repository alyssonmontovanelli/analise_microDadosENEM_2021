from utils import *

df_notaEscola = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=colEscola_nota)

'''
Testagem dos dados
'''
print(df_notaEscola.head())
print(df_notaEscola.describe())
print(df_notaEscola.isna().count())