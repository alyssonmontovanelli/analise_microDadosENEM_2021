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

# Criação coluna eliminados, para todos os candidatos, com base em isna() em cada prova
df_notaEscola['ELIMINADOS_CONC'] = np.where((df_notaEscola['NU_NOTA_CN'].isna())\
                                         | (df_notaEscola['NU_NOTA_CH'].isna())\
                                         | (df_notaEscola['NU_NOTA_LC'].isna())\
                                         | (df_notaEscola['NU_NOTA_MT'].isna())\
                                         | (df_notaEscola['NU_NOTA_REDACAO'].isna()), 'Eliminado', 'Presente')

# Criação de coluna media geral dos alunos presentes nos dois dias de prova
df_notaEscola.loc[df_notaEscola['ELIMINADOS_CONC'] == 'Presente', 'MEDIA_GERAL'] = df_notaEscola[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis=1)


print(df_notaEscola.head())


# Média geral/UF - proporcional com a população

# Média geral para alunos brancos e negros

# Quantidade de alunos negros e brancos em escola publica/privada

# Inscritos por tipo/escola que faltaram ou estava presentes 

# Panorama tipo_escola com média geral

# Panorama tipo_escola com nota para cada disciplina

# Panorama tipo_escola por UF - média de notas 

# Verificar regressão de notas boas para escola publica

# Verificar regressão de notas boas para escola privada



