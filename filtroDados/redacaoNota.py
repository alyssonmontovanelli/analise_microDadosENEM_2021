from utils import pd, np, col_redacao


# DF de presença
df_Redacao = pd.read_csv("C:\Projetos Pessoais\DataScience\/0_dados_pesados\data\MICRODADOS_ENEM_2021.csv", sep= ";", encoding="ISO-8859-1", usecols=col_redacao)

# Criação coluna eliminados, para todos os candidatos, com base em isna() em cada prova
df_Redacao['ELIMINADOS_CONC'] = np.where(df_Redacao['TP_STATUS_REDACAO'].isna(), 'Eliminado', 'Presente') 

print(df_Redacao.columns)
print(df_Redacao.isna().sum())
print(df_Redacao)

# Panorama redação por tipo/ escola - com todas as competências
nota_porTipoEscola = df_Redacao[df_Redacao['ELIMINADOS_CONC'] == 'Presente']\
                  .loc[df_Redacao['TP_ESCOLA'].isin([2,3])]\
                  .groupby('TP_ESCOLA')['NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3',
       'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO']\
                  .agg(['mean'])

print(nota_porTipoEscola)

# Panorama média/geral por competencias

media_porCompetencia = df_Redacao[df_Redacao['ELIMINADOS_CONC'] == 'Presente']\
                   .groupby(['ELIMINADOS_CONC'])['NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3',
       'NU_NOTA_COMP4', 'NU_NOTA_COMP5', 'NU_NOTA_REDACAO'].agg(['mean']).reset_index()

print(media_porCompetencia)

# panorama de status da redação 

status_redacao = df_Redacao[df_Redacao['ELIMINADOS_CONC'] == 'Presente']\
                  .loc[df_Redacao['TP_ESCOLA'].isin([2,3])]\
                  .groupby(['TP_ESCOLA', 'TP_STATUS_REDACAO'])['TP_STATUS_REDACAO']\
                  .agg(['count']).rename(columns={'count': 'Qtde alunos'})
                 

print(status_redacao)
