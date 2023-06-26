from utils import *

df_socioEconomico = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=col_socioEconomico)

print(df_socioEconomico.head())
print(df_socioEconomico.columns)

'''  MEMENTO ---
Q001 - Até que série seu pai, ou o homem responsável por você, estudou?
Q002 - Até que série sua mãe, ou a mulher responsável por você, estudou?
Q003 - Ocupação do seu pai, ou a homem responsável por você, estudou?
Q004 - Ocupação da sua mãe, ou a mulher responsável por você, estudou?
Q005 - Incluindo você, quantas pessoas moram atualmente em sua residência?
Q006 - Qual é a renda mensal de sua família? (Some a sua renda com a dos seus familiares.
Q025 - Na sua residência tem acesso à Internet?
'''
# Criação coluna eliminados, para todos os candidatos, com base em isna() em cada prova
df_socioEconomico['ELIMINADOS_CONC'] = np.where((df_socioEconomico['NU_NOTA_CN'].isna())\
                                         | (df_socioEconomico['NU_NOTA_CH'].isna())\
                                         | (df_socioEconomico['NU_NOTA_LC'].isna())\
                                         | (df_socioEconomico['NU_NOTA_MT'].isna())\
                                         | (df_socioEconomico['NU_NOTA_REDACAO'].isna()), 'Eliminado', 'Presente')

# Criação de coluna media geral dos alunos presentes nos dois dias de prova
df_socioEconomico.loc[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente', 'MEDIA_GERAL'] =\
   df_socioEconomico[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis=1)

#Como só existem 2 linhas com valor NaN na resposta social, irei associar o valor "1" e valor "A"
df_socioEconomico['Q001'].fillna(value = 'A', inplace = True)
df_socioEconomico['Q002'].fillna(value = 'A', inplace = True)
df_socioEconomico['Q003'].fillna(value = 'A', inplace = True)
df_socioEconomico['Q004'].fillna(value = 'A', inplace = True)
df_socioEconomico['Q005'].fillna(value = 1, inplace = True)
df_socioEconomico['Q006'].fillna(value = 'A', inplace = True)
df_socioEconomico['Q025'].fillna(value = 'A', inplace = True)


'''Consultas'''

# Principais características socioeconomicas dos candidatos
panoramaGeral_social = df_socioEconomico.groupby(['Q001','Q002','Q003','Q004','Q005','Q006','Q025'])\
                                 [['Q001','Q002','Q003','Q004','Q005','Q006','Q025']].count()

# relação entre o acesso à internet e desempenho no ENEM 2021
nota_internet = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                .groupby('Q025')['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_GERAL']\
                .agg(['mean'])

# print(nota_internet)


# panorama de renda com melhores médias no ENEM
renda_raca_notasENEM = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                       .loc[df_socioEconomico['TP_COR_RACA'].isin([1,2,3])]\
                       .groupby(['Q006','TP_COR_RACA'])['MEDIA_GERAL'].agg(['mean', 'count','median'])\
                       .rename(columns={'mean': 'nota_media', 'median':'mediana', 'count': 'quantidade'})

# print(renda_raca_notasENEM)

# Panorama renda com raça

renda_porRaca_geral = df_socioEconomico\
                .loc[df_socioEconomico['TP_COR_RACA'].isin([1,2,3])]\
                .groupby('Q006')['TP_COR_RACA'].value_counts()

renda_porRaca_presente = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                .loc[df_socioEconomico['TP_COR_RACA'].isin([1,2,3])]\
                .groupby('Q006')['TP_COR_RACA'].value_counts()

# print(renda_porRaca_geral)
# print(renda_porRaca_presente)

# Panorama pessoas morando na casa com raça e nota media
moradores_nota = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                      .groupby('Q005')['MEDIA_GERAL'].agg(['mean', 'count'])
# print(moradores_nota)


# relação nível escolaridade mãe/pai com nota média 
escolaridadePai_nota = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                      .groupby('Q001')['MEDIA_GERAL'].agg(['mean', 'count'])

escolaridadeMae_nota = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                      .groupby('Q002')['MEDIA_GERAL'].agg(['mean', 'count'])

# print(escolaridadePai_nota)
# print(escolaridadeMae_nota)

# relação nível grupo de trabalho mãe/pai com nota média 
ocupacaoPai_nota = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                      .groupby('Q003')['MEDIA_GERAL'].agg(['mean', 'count'])

ocupacaoMae_nota = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                      .groupby('Q004')['MEDIA_GERAL'].agg(['mean', 'count'])

print(ocupacaoPai_nota)
print(ocupacaoMae_nota)




'''Gráfico ocupação '''