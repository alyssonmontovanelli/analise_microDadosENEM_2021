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
print(presenca)


presenca2 = dfPresenca.groupby(['TP_ESCOLA','ELIMINADOS_CONC'])['NU_INSCRICAO'].count().reset_index()
presenca2['TP_ESCOLA'] = presenca2['TP_ESCOLA'].replace(mapeamento_por_tipoEscola_rosca)

presenca2['ELIMINADOS_CONC'] = presenca2['ELIMINADOS_CONC'].replace(mapeamento_eliminados)
print(presenca2)

# Panorama por UF 
presenca3 = dfPresenca.groupby('TP_ESCOLA')['NU_INSCRICAO'].count().reset_index()
presenca3['TP_ESCOLA'] = presenca3['TP_ESCOLA'].replace(mapeamento_por_tipoEscola_rosca)



# # Média geral para alunos brancos e negros
# media_raca = dfPresenca[dfPresenca['ELIMINADOS_CONC'] == 'Presente']\
#             .loc[dfPresenca['TP_COR_RACA'].isin([0,1,2,3,4,5,6])]\
#             .groupby('TP_COR_RACA')['NU_INSCRICAO']\
#             .agg(['count']).reset_index()\
#             .rename(columns={'TP_COR_RACA':'Cor/Raça','count': 'Quantidade'})

# # Mapear os valores da coluna 'Cor/Raça' para os novos nomes
# media_raca['Cor/Raça'] = media_raca['Cor/Raça'].replace(mapeamento_cor_raca)

# cores2 = sns.color_palette("OrRd")

# plt.figure(figsize=(12, 6))
# # Desenhar o gráfico de pizza com as quantidades
# wedges, texts, autotexts = plt.pie(media_raca['Quantidade'], labels=media_raca['Cor/Raça'],
#                                    autopct='%1.1f%%', startangle=100,colors=cores2)
# # Configurar as propriedades dos textos
# plt.setp(autotexts, size=12, color='black')
# # Limpar o círculo central
# centre_circle = plt.Circle((0, 0), 0.85, fc='white')
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)
# # Calcular e exibir a quantidade total
# total = media_raca['Quantidade'].sum()
# plt.text(0, -0.4, 'Candidatos Presentes: {}'.format(total), ha='center', va='center', fontsize=10)
# plt.title('Proporção de Candidatos presentes por Cor/Raça', y=1.03)
# plt.show()












# print(presenca3)
""" PLOTAGEM """

# cores_categorias = ['#f77e52',
#                     '#898989',
#                     '#ed6044',]

# cores_subCategorias = ['#f9a181',
#                        '#f9a181',
#                        '#c6c0c0',
#                        '#c6c0c0',
#                        '#ea9283',
#                        '#ea9283',]

# #Plotagem
# fig, ax = plt.subplots(figsize=(16, 10))

# # Gráfico das categorias
# grafico1 = ax.pie(presenca3['NU_INSCRICAO'],
#                   radius=1,
#                   labels=presenca3['TP_ESCOLA'],
#                   wedgeprops=dict(edgecolor='white'),
#                   colors=cores_categorias,
#                   textprops={'fontweight': 'bold', 'fontsize':9})  # Define a cor do texto como branco e rotaciona em -30 graus

# # Colorir Labels de gráf
# for label, color in zip(grafico1[1], cores_categorias):
#     label.set_color(color)

# # Gráfico das subcategorias
# grafico2 = ax.pie(presenca2['NU_INSCRICAO'],
#                   radius=0.9,
#                   labels=presenca2['ELIMINADOS_CONC'],
#                   colors=cores_subCategorias,
#                   labeldistance=0.68,
#                   wedgeprops=dict(edgecolor='white'),
#                   pctdistance=0.53,
#                   rotatelabels=True,
#                   autopct=lambda pct: int(round(pct * sum(presenca2['NU_INSCRICAO']) / 100)),
#                   textprops={'color': 'black', 'fontsize': 7})  # Define a cor do texto como branco e rotaciona em -30 graus

# # Limpar o centro do círculo
# centre_circle = plt.Circle((0, 0), 0.6, fc='white')
# fig.gca().add_artist(centre_circle)

# # Rótulos e anotações
# plt.annotate(text='Total: 3.389.832', xy=(-0.3, 0), fontsize= 12, color = '#f77e52', fontweight='bold')
# plt.title('Total de Inscritos no ENEM/2021', fontsize=12)
# plt.show()

