from utils import *

df_notaEscola = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=colEscola_nota)

'''
Testagem dos dados
'''
print(df_notaEscola.columns)
print(df_notaEscola.describe())
print(df_notaEscola.isna().sum())

# Criar coluna com 'média geral'
# Criação de coluna generalista para "eliminados" e "presentes"
df_notaEscola['ELIMINADOS_CONC'] = np.where((df_notaEscola['NU_NOTA_CN'].isna())\
                                         | (df_notaEscola['NU_NOTA_CH'].isna())\
                                         | (df_notaEscola['NU_NOTA_LC'].isna())\
                                         | (df_notaEscola['NU_NOTA_MT'].isna())\
                                         | (df_notaEscola['NU_NOTA_REDACAO'].isna()), 'Eliminado', 'Presente')

# df_notaEscola['MEDIA_GERAL'] = df_notaEscola.loc[df_notaEscola['ELIMINADOS_CONC'] == 'Presente', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis=1)

# df_notaEscola['MEDIA_GERAL'] = 0
df_notaEscola.loc[df_notaEscola['ELIMINADOS_CONC'] == 'Presente', 'MEDIA_GERAL'] = df_notaEscola[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis=1)


print(df_notaEscola.head())

# df_notaEscola['MEDIA_GERAL'] = 


