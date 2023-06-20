from utils import pd, np, col_redacao


# DF de presença
dfRedacao = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=col_redacao)