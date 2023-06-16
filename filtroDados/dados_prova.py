from utils import pd, colPresenca

# DF de presença
dfPresenca = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=colPresenca)
print(dfPresenca.head())
print(dfPresenca.isnull().sum())
print(dfPresenca.isna().sum())

