from utils import *

# DF de presença
dfPresenca = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=colPresenca)
# print(dfPresenca.head())
# print(dfPresenca.columns)

# Total de inscritos
inscritos = dfPresenca['NU_INSCRICAO'].count()
# print(inscritos)

# inscritos que faltaram em 1 dia e nos 2 dias
faltoso = dfPresenca.groupby(['TP_PRESENCA_LC', 'TP_PRESENCA_MT'])['NU_INSCRICAO'].count()

# Inscritos por sexo
inscritosSexo = dfPresenca.groupby('TP_SEXO')['NU_INSCRICAO'].count()
# print(inscritosSexo)
# Inscritos por raça
inscritosRaca = dfPresenca.groupby('TP_COR_RACA')['NU_INSCRICAO'].count()
# print(inscritosRaca)

# Criação de coluna generalista para "eliminados" e "presentes"
dfPresenca['ELIMINADOS_CONC'] = np.where((dfPresenca['TP_PRESENCA_LC'] == 0)\
                                         | (dfPresenca['TP_PRESENCA_LC'] == 2)\
                                         | (dfPresenca['TP_PRESENCA_MT'] == 0)\
                                         | (dfPresenca['TP_PRESENCA_MT'] == 2), 'Eliminado', 'Presente')


presenca = dfPresenca.groupby('ELIMINADOS_CONC')['NU_INSCRICAO'].count().reset_index()
# print(presenca)


presenca2 = dfPresenca.groupby(['TP_ESCOLA','ELIMINADOS_CONC'])['NU_INSCRICAO'].count().reset_index()
presenca2['TP_ESCOLA'] = presenca2['TP_ESCOLA'].replace(mapeamento_por_tipoEscola_rosca)

presenca2['ELIMINADOS_CONC'] = presenca2['ELIMINADOS_CONC'].replace(mapeamento_eliminados)
# print(presenca2)

# Panorama por UF 
presenca3 = dfPresenca.groupby('TP_ESCOLA')['NU_INSCRICAO'].count().reset_index()
presenca3['TP_ESCOLA'] = presenca3['TP_ESCOLA'].replace(mapeamento_por_tipoEscola_rosca)

# print(presenca3)
# Panorama faixa etária


# # Criando DF
# total_vendas_Cat_top12SubCat = dataFrame.groupby(['Categoria',
#                                                   'SubCategoria']).sum(numeric_only=True).sort_values('Valor_Venda',
#                                                                                                       ascending=False).head(12)

# # Convertendo coluna Valor_Venda em num inteiro e classificando por cat
# total_vendas = total_vendas_Cat_top12SubCat[['Valor_Venda']].astype(int).sort_values(by= 'Categoria').reset_index()

# # DatafRAME com totais por categoria para anel exterior
# total_vendas_Cat = total_vendas.groupby('Categoria').sum(numeric_only= True).reset_index()

# print(total_vendas)
# print(total_vendas_Cat)

# # Cores para categorias

cores_categorias = ['#f77e52',
                    '#898989',
                    '#ed6044',]

cores_subCategorias = ['#f9a181',
                       '#f9a181',
                       '#c6c0c0',
                       '#c6c0c0',
                       '#ea9283',
                       '#ea9283',]

#Plotagem
fig, ax = plt.subplots(figsize=(16, 10))

# Gráfico das categorias
grafico1 = ax.pie(presenca3['NU_INSCRICAO'],
                  radius=1,
                  labels=presenca3['TP_ESCOLA'],
                  wedgeprops=dict(edgecolor='white'),
                  colors=cores_categorias)

# Gráfico das subcategorias
grafico2 = ax.pie(presenca2['NU_INSCRICAO'],
                  radius=0.9,
                  labels=presenca2['ELIMINADOS_CONC'],
                  colors=cores_subCategorias,
                  labeldistance=0.7,
                  wedgeprops=dict(edgecolor='white'),
                  pctdistance=0.53,
                  rotatelabels=True,
                  autopct=lambda pct: int(round(pct * sum(presenca2['NU_INSCRICAO']) / 100)),
                  textprops={'color': 'black', 'fontsize': 9})  # Define a cor do texto como branco e rotaciona em -30 graus


# Limpar o centro do círculo
centre_circle = plt.Circle((0, 0), 0.6, fc='white')
fig.gca().add_artist(centre_circle)

# Rótulos e anotações
plt.annotate(text='Total de Inscritos: ' + str(int(sum(presenca2['NU_INSCRICAO']))), xy=(-0.3, 0), fontweight='bold')
plt.title('Total de Inscritos no ENEM/2021')
plt.show()

# fig, ax = plt.subplots(figsize=(16, 10))

# # Gráfico das categorias
# # Gráfico das categorias
# grafico1 = ax.pie(presenca3['NU_INSCRICAO'],
#                   radius=1,
#                   labels=presenca3['TP_ESCOLA'],
#                   wedgeprops=dict(edgecolor='white'),  # Limite das divisões
#                   colors=cores_categorias)

# # Gráfico das subcategorias
# grafico2 = ax.pie(presenca2['NU_INSCRICAO'],
#                   radius=0.9,
#                   labels=presenca2['ELIMINADOS_CONC'],
#                   colors=cores_subCategorias,
#                   labeldistance=0.7,
#                   wedgeprops=dict(edgecolor='white'),
#                   pctdistance=0.53,
#                   rotatelabels=True)  # Legendas inclinadas

# # Limpar o centro do círculo
# centre_circle = plt.Circle((0, 0), 0.6, fc='white')

# # Rótulos e anotações
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)
# plt.annotate(text='Total de Inscritos: ' + str(int(sum(presenca2['NU_INSCRICAO']))), xy=(-0.2, 0))
# plt.title('Total de Vendas Por Categoria e Top 12 Subcategorias')
# plt.show()