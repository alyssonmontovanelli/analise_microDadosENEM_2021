from utils import *

df_socioEconomico = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=col_socioEconomico)

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
                .agg(['mean']).reset_index()
nota_internet['Q025'] = nota_internet['Q025'].replace(mapeamento_internet)
nota_internet.rename(columns=mapeamento_nota_materia, inplace=True)

# panorama de renda com melhores médias no ENEM
renda_raca_notasENEM = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                       .loc[df_socioEconomico['TP_COR_RACA'].isin([1,2,3])]\
                       .groupby(['Q006','TP_COR_RACA'])['MEDIA_GERAL'].mean()\
                       .reset_index()\
                       .rename(columns={'MEDIA_GERAL': 'Nota Média'})
renda_raca_notasENEM['TP_COR_RACA'] = renda_raca_notasENEM['TP_COR_RACA'].replace(mapeamento_cor_raca)
renda_raca_notasENEM['Q006'] = renda_raca_notasENEM['Q006'].replace(mapeamento_renda)


# Panorama renda com raça
renda_porRaca_geral = df_socioEconomico\
                .loc[df_socioEconomico['TP_COR_RACA'].isin([1,2,3])]\
                .groupby('Q006')['TP_COR_RACA'].value_counts()

renda_porRaca_presente = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                .loc[df_socioEconomico['TP_COR_RACA'].isin([1,2,3])]\
                .groupby('Q006')['TP_COR_RACA'].value_counts().reset_index(name="Quantidade")
renda_porRaca_presente['TP_COR_RACA'] = renda_porRaca_presente['TP_COR_RACA'].replace(mapeamento_cor_raca)
renda_porRaca_presente['Q006'] = renda_porRaca_presente['Q006'].replace(mapeamento_renda)

# Panorama pessoas morando na casa com nota media
moradores_nota = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                      .groupby('Q005')['MEDIA_GERAL'].agg(['mean', 'count'])

# relação nível escolaridade mãe/pai com nota média 
escolaridadePai_nota = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                      .groupby('Q001')['MEDIA_GERAL'].agg(['mean']).reset_index()
escolaridadePai_nota['Q001'] = escolaridadePai_nota['Q001'].replace(mapeamento_escolaridade_responsavel)
escolaridadePai_nota.rename(columns={'Q001': 'Nível de Escolaridade'}, inplace=True)

escolaridadeMae_nota = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                      .groupby('Q002')['MEDIA_GERAL'].agg(['mean']).reset_index()
escolaridadeMae_nota['Q002'] = escolaridadeMae_nota['Q002'].replace(mapeamento_escolaridade_responsavel)
escolaridadeMae_nota.rename(columns={'Q002': 'Nível de Escolaridade'}, inplace=True)

# relação nível grupo de trabalho mãe/pai com nota média 
ocupacaoPai_nota = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                      .groupby('Q003')['MEDIA_GERAL'].agg(['mean'])\
                      .reset_index()\
                      .rename(columns={'Q003':'Ocupação','mean': 'Nota Media'})
ocupacaoPai_nota['Ocupação'] = ocupacaoPai_nota['Ocupação'].replace(mapeamento_ocupacao)


ocupacaoMae_nota = df_socioEconomico[df_socioEconomico['ELIMINADOS_CONC'] == 'Presente']\
                      .groupby('Q004')['MEDIA_GERAL'].agg(['mean'])\
                      .reset_index()\
                      .rename(columns={'Q004':'Ocupação','mean': 'Nota Media'})
ocupacaoMae_nota['Ocupação'] = ocupacaoMae_nota['Ocupação'].replace(mapeamento_ocupacao)

df_ocupacao = pd.merge(ocupacaoPai_nota, ocupacaoMae_nota, on='Ocupação', suffixes=('Q003', 'Q004'))
df_melted2 = df_ocupacao.melt(id_vars='Ocupação', var_name='Responsavel', value_name='Média da Nota')
df_melted2['Responsavel'] = df_melted2['Responsavel'].str.replace('Nota MediaQ003', 'Pai ou homem responsável')
df_melted2['Responsavel'] = df_melted2['Responsavel'].str.replace('Nota MediaQ004', 'Mãe ou mulher responsável')





'''
PLOTAGEM
'''




cores2 = sns.color_palette("Set2")



""" REGRESSÃO """
# # Plot sepal width as a function of sepal_length across days
# g = sns.lmplot(
#     data=penguins,
#     x="bill_length_mm", y="bill_depth_mm", hue="species",
#     height=5
# )

# # Use more informative axis labels than are provided by default
# g.set_axis_labels("Snoot length (mm)", "Snoot depth (mm)")

"""CATPLOT - Quantidade por faixa salarial / RAÇA - Quantidade"""
# g = sns.catplot(
#     data=renda_porRaca_presente, kind="bar",
#     x="Q006", y="Quantidade", hue="TP_COR_RACA",
#     errorbar="sd", palette="Set2", height=6,aspect=1.5
# )
# ax = g.facet_axis(0, 0)
# ax.set_xlabel(ax.get_xlabel(), fontweight='bold')
# ax.set_ylabel(ax.get_ylabel(), fontweight='bold')

# g.despine(left=True)
# g.set_axis_labels("Renda Mensal Familiar (R$)", "Qtde candidatos")
# plt.xticks(rotation=65)
# ax.xaxis.set_tick_params(labelsize=8)
# g.legend.set_title("Cor/Raça")
# plt.title("Relação Quantidade de Candidato/ Renda/ Raça", y=1.03)
# # Adicionar linhas de grade a cada 30.000 unidades no eixo Y
# step = 20000
# max_value = max(renda_porRaca_presente['Quantidade'])
# y_values = range(0, max_value + step, step)
# for y in y_values:
#     plt.axhline(y=y, color='gray', linestyle='-', linewidth=0.2)
#     plt.text(-0.6, y, str(y), color='gray', ha='right', va='center', fontsize=9)
# plt.yticks([])
# ax.yaxis.set_label_coords(-0.08, 0.5)  # Ajuste o valor conforme necessário
# plt.show()



"""CATPLOT - Quantidade por faixa salarial / RAÇA - Nota Média"""
# g = sns.catplot(
#     data=renda_raca_notasENEM, kind="bar",
#     x="Q006", y="Nota Média", hue="TP_COR_RACA",
#     errorbar="sd", palette="Set2", height=6,aspect=1.5
# )
# ax = g.facet_axis(0, 0)
# ax.set_xlabel(ax.get_xlabel(), fontweight='bold')
# ax.set_ylabel(ax.get_ylabel(), fontweight='bold')

# g.despine(left=True)
# g.set_axis_labels("Renda Mensal Familiar (R$)", "Nota Média")
# plt.xticks(rotation=65)
# # plt.yticks(color = 'grey')
# plt.ylim(400, 700)
# ax.xaxis.set_tick_params(labelsize=8)
# g.legend.set_title("Cor/Raça")
# plt.title("Média de notas por Cor/Raça e Renda", y=1.03)
# plt.yticks(range(400, 701, 25), color='grey')

# # Adicionar linhas de grade com intervalos de 25 em 25
# for y in range(400, 701, 25):
#     plt.axhline(y, color='lightgrey', linewidth=0.5, zorder = 0)

# ax.xaxis.set_tick_params(labelsize=8)
# g.legend.set_title("Cor/Raça")
# plt.title("Média de notas por Cor/Raça e Renda", y=1.03)

# ax.yaxis.set_label_coords(-0.08, 0.5)  # Ajuste o valor conforme necessário
# plt.show()


""" LINEPLOT - NOTA MÉDIA POR ACESSO A INTERNET -------------------------------------------"""
# # Transformar as colunas em linhas utilizando o melt
# df_melted = nota_internet.melt(id_vars='Q025', var_name='Nota', value_name='Valor')
# # Plotar o gráfico de linhas
# g = sns.lineplot(
#     data=df_melted, x='Nota', y='Valor', hue='Q025',
#     palette='Set2', markers=True, style='Q025'
# )
# for _, row in df_melted.iterrows():
#     g.annotate(round(row['Valor'], 2), (row['Nota'], row['Valor']),
#                textcoords="offset points",fontsize=8, xytext=(0,10), ha='center')

# plt.xticks(rotation=20, fontsize = 9, color = 'grey')
# plt.yticks(fontsize = 9, color = 'grey')
# plt.ylabel('Nota Média')
# plt.xlabel('Matérias')
# # # Borda top e right invisiveis
# g.spines['top'].set_visible(False)
# g.spines['right'].set_visible(False)
# g.spines['left'].set_visible(False)

# #Grid
# g.yaxis.grid(True, alpha=0.1)
# g.set_axisbelow(True)
# plt.ylim(400, 700)
# g.set_xlabel(g.get_xlabel(), fontweight='bold')
# g.set_ylabel(g.get_ylabel(), fontweight='bold')
# plt.title('Desempenho com base no acesso à internet', y = 1.03)
# plt.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')
# plt.show()


""" CATPLOT - NOTA MÉDIA COM BASE NA ESCOLARIDADE DOS PAIS"""

# df_merged = pd.merge(escolaridadePai_nota, escolaridadeMae_nota, on='Nível de Escolaridade', suffixes=('Q001', 'Q002'))

# df_melted = df_merged.melt(id_vars='Nível de Escolaridade', var_name='Variável', value_name='Média da Nota')

# df_melted['Variável'] = df_melted['Variável'].str.replace('meanQ001', 'Pai ou homem responsável')
# df_melted['Variável'] = df_melted['Variável'].str.replace('meanQ002', 'Mãe ou mulher responsável')

# g4 = sns.catplot(data=df_melted, x='Nível de Escolaridade', 
#                  y='Média da Nota', palette="OrRd",
#                  hue='Variável',aspect=1.5, kind='bar')

# ax = g4.facet_axis(0, 0)
# g4.despine(left=True)
# g4.set_axis_labels("Escolaridade dos responsáveis", "Nota Média")
# plt.xticks(rotation=40, color='grey')
# # plt.yticks(color = 'grey')
# plt.ylim(400, 626)
# ax.xaxis.set_tick_params(labelsize=8)
# g4.legend.set_title("Índice")
# plt.title("Nota Média por Nível de Escolaridade dos responsáveis", y=1.03)
# plt.yticks(range(400, 626, 25), color='grey', fontsize = 8)

# # Adicionar linhas de grade com intervalos de 25 em 25
# for y in range(400, 626, 25):
#     plt.axhline(y, color='lightgrey', linewidth=0.5, zorder = 0)

# plt.show()


""" CATPLOT - NOTA MÉDIA COM BASE NA OCUPAÇÃO DOS PAIS"""

# g5 = sns.catplot(data=df_melted2, x='Ocupação', 
#                  y='Média da Nota', palette="OrRd",
#                  hue='Responsavel',aspect=1.2, kind='bar')

# ax = g5.facet_axis(0, 0)
# g5.despine(left=True)
# g5.set_axis_labels("Ocupação dos responsáveis", "Nota Média")
# plt.xticks(rotation=40, color='grey')
# # plt.yticks(color = 'grey')
# plt.ylim(400, 626)
# ax.xaxis.set_tick_params(labelsize=8)
# g5.legend.set_title("Índice")
# plt.title("Nota Média por ocupação dos responsáveis", y=1.03)
# plt.yticks(range(400, 626, 25), color='grey', fontsize = 8)

# # Adicionar linhas de grade com intervalos de 25 em 25
# for y in range(400, 626, 25):
#     plt.axhline(y, color='lightgrey', linewidth=0.5, zorder = 0)

# plt.show()


''''''



# Load an example dataset with long-form data
# fmri = sns.load_dataset("fmri")

# Plot the responses for different events and regions
# g2 = sns.lineplot(x="Q006", y="Quantidade",
#              hue="TP_COR_RACA",
#              data=renda_porRaca_presente)
# #Grid
# g2.yaxis.grid(True, alpha=0.1)
# g2.set_axisbelow(True)
# plt.show()



