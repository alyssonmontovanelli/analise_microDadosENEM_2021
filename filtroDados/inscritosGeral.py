from utils import pd, np, colPresenca

# DF de presença
dfPresenca = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=colPresenca)
# print(dfPresenca.head())
print(dfPresenca.columns)

# Total de inscritos
inscritos = dfPresenca['NU_INSCRICAO'].count()

# inscritos que faltaram em 1 dia e nos 2 dias
faltoso = dfPresenca.groupby(['TP_PRESENCA_LC', 'TP_PRESENCA_MT'])['NU_INSCRICAO'].count()

# Inscritos por sexo
inscritosSexo = dfPresenca.groupby('TP_SEXO')['NU_INSCRICAO'].count()

# Inscritos por raça
inscritosRaca = dfPresenca.groupby('TP_COR_RACA')['NU_INSCRICAO'].count()

# Criação de coluna generalista para "eliminados" e "presentes"
dfPresenca['ELIMINADOS_CONC'] = np.where((dfPresenca['TP_PRESENCA_LC'] == 0)\
                                         | (dfPresenca['TP_PRESENCA_LC'] == 2)\
                                         | (dfPresenca['TP_PRESENCA_MT'] == 0)\
                                         | (dfPresenca['TP_PRESENCA_MT'] == 2), 'Eliminado', 'Presente')

# Panorama por UF 
presentesUF = dfPresenca.groupby(['SG_UF_PROVA', 'ELIMINADOS_CONC'])['NU_INSCRICAO'].count()

# Panorama faixa etária


#



