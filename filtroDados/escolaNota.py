from utils import *

df_notaEscola = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=colEscola_nota)

'''
Testagem dos dados
'''
print(df_notaEscola.columns)
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

# Média geral/UF - proporcional com a população
media_UF = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente'].groupby('SG_UF_PROVA')['MEDIA_GERAL'].mean().reset_index()

# Média geral para alunos brancos e negros
media_raca = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']\
            .loc[df_notaEscola['TP_COR_RACA'].isin([1,2,3,4,5])]\
            .groupby('TP_COR_RACA')['MEDIA_GERAL']\
            .agg(['mean','count']).reset_index()\
            .rename(columns={'TP_COR_RACA':'Cor/Raça','mean': 'Nota Média', 'count': 'Quantidade'})

# Mapear os valores da coluna 'Cor/Raça' para os novos nomes
mapeamento_cor_raca = {
    0: 'Não declarado',
    1: 'Branco',
    2: 'Preto',
    3: 'Pardo',
    4: 'Amarelo',
    5: 'Indígena'
}
media_raca['Cor/Raça'] = media_raca['Cor/Raça'].replace(mapeamento_cor_raca)
print(media_raca)

# Quantidade de alunos negros, brancos e pardos em escola publica/privada

raca_porEscola = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']\
                 .loc[df_notaEscola['TP_COR_RACA'].isin([1,2,3])]\
                 .groupby(['TP_ESCOLA', 'TP_COR_RACA'])['TP_COR_RACA'].count()
# print(raca_porEscola)

# Inscritos por tipo/escola que faltaram ou estava presentes 

inscritos_presentes = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']\
                 .loc[df_notaEscola['TP_COR_RACA'].isin([1,2,3])]\
                 .groupby(['TP_ESCOLA', 'TP_COR_RACA'])['TP_COR_RACA'].count()
# print(raca_porEscola)



# Panorama tipo_escola com média geral
media_tipoEscola = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']\
                  .loc[df_notaEscola['TP_ESCOLA'].isin([2,3])]\
                  .groupby(['TP_ESCOLA', 'TP_COR_RACA'])['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT','NU_NOTA_REDACAO','MEDIA_GERAL']\
                  .agg(['mean']).reset_index()
# print(media_tipoEscola)

# Panorama tipo_escola por UF - média de notas 

media_tipoEscola_porUF = df_notaEscola[df_notaEscola['ELIMINADOS_CONC'] == 'Presente']\
                  .loc[df_notaEscola['TP_ESCOLA'].isin([2,3])]\
                  .groupby(['SG_UF_PROVA','TP_ESCOLA'])['MEDIA_GERAL']\
                  .agg(['mean'])
# print(media_tipoEscola_porUF)
'''
PLOTAGEM
'''
cores2 = sns.color_palette("Set2")
""" Barplot - média por raça"""
plt.figure(figsize=(8, 4))
sns.barplot(x='Cor/Raça', y='Nota Média', data=media_raca)
sns.set_palette(cores2)
# Adicionar os valores das barras no gráfico
ax = sns.barplot(x='Cor/Raça', y='Nota Média', data=media_raca)
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
# Ajustar a estética do gráfico
sns.set(style='whitegrid')
plt.title('Média Geral por Cor/Raça')
plt.xlabel('Cor/Raça')
plt.ylabel('Nota Média')
plt.xticks(rotation = 20)
# Mostrar os grids
ax.yaxis.grid(True)
ax.set_axisbelow(True)
# Borda top e right invisiveis
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# Mostrar o gráfico
# plt.show()

""" Pie - Qtde por raça """
# Configurar a paleta de cores