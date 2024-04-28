# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#
#
#
#
#
#
#
#
file = 'Data/egressos.csv'
df = pd.read_csv(file)
#
#
#
#
#
df = df[(df['Programa'] == 'PGCAP') | df['Programa'].str.startswith('ECO')]
#
#
#
#
#
#
#
df = df[df['Sit'] != 'n/r']
#
#
#
#
#
df['Adm'] = pd.to_datetime(df['Adm'], format='%Y-%m-%d')
df['Sit'] = pd.to_datetime(df['Sit'], format='%Y-%m-%d')
df['Nascimento'] = pd.to_datetime(df['Nascimento'], format='%Y-%m-%d')
#
#
#
#
#
#
df['AnoAdm'] = df['Adm'].dt.year
df['AnoGrad'] = df['Sit'].dt.year.astype(int)
df['MesesParaGrad'] = (df['Sit'] - df['Adm']).dt.days/30
df['IdadeNaGraduação'] = (df['Sit'] - df['Nascimento']).dt.days / 365.25 
#
#
#
#
#
#
#
#
#
# Primeiro contamos o número de graduados por ano e nível.
df_agg = df.groupby(['AnoGrad', 'Nivel']).size().reset_index(name='Número')
# Criamos o gráfico de barras acumuladas.
fig = px.bar(df_agg, x='AnoGrad', y='Número', color='Nivel', 
             title='Número de Graduados por Ano e Nível',
             labels={'AnoGrad': 'Ano da Graduação', 'count': 'Número'},
             category_orders={'Nivel': ['MESTRADO', 'DOUTORADO']},
             barmode='stack')
fig.update_layout(bargap=0.1)         
fig.update_xaxes(tickangle=90, dtick=1, tickfont=dict(size=8))               
fig.show()
#
#
#
#
#
#
#
#
#
#
#
# Separamos somente os egressos de mestrado.
dfMSc = df[df['Nivel'] == 'MESTRADO']
# Criamos o gráfico.
fig_master = px.violin(dfMSc, y='MesesParaGrad', box=True,  
                       points="all",
                       title='Tempo de Graduação para Mestrado',
                       labels={'MesesParaGrad': 'Meses'},
                       hover_data={'MesesParaGrad': True, 'Registro': True})
fig_master.add_shape(type="line", x0=0, x1=1, y0=24, y1=24, 
                     line=dict(color="green", width=2))
fig_master.add_annotation(x=0.5, y=24, text='24 meses',showarrow=False, 
                          bgcolor='rgba(255, 255, 255, 1)',
                          font=dict(color='green', size=12))
fig_master.add_shape(type="line", x0=0, x1=1, y0=36, y1=36, 
                     line=dict(color="red", width=2))
fig_master.add_annotation(x=0.5, y=36, text='36 meses',showarrow=False, 
                          bgcolor='rgba(255, 255, 255, 1)',
                          font=dict(color='red', size=12))
fig_master.show()
```
#
#
#
# Separamos somente os egressos de doutorado.
dfPhD = df[df['Nivel'] == 'DOUTORADO']
# Criamos o gráfico.
fig_phd = px.violin(dfPhD, y='MesesParaGrad', box=True, 
                    points="all",
                    title='Tempo de Graduação para Doutorado',
                    labels={'MesesParaGrad': 'Meses'},
                    hover_data={'MesesParaGrad': True, 'Registro': True})
fig_phd.add_shape(type="line", x0=0, x1=1, y0=48, y1=48, 
                  line=dict(color="green", width=2))
fig_phd.add_annotation(x=0.5, y=48, text='48 meses',showarrow=False, 
                       bgcolor='rgba(255, 255, 255, 1)',
                       font=dict(color='green', size=12))
fig_phd.add_shape(type="line", x0=0, x1=1, y0=60, y1=60, 
                  line=dict(color="red", width=2))
fig_phd.add_annotation(x=0.5, y=60, text='60 meses',showarrow=False, 
                       bgcolor='rgba(255, 255, 255, 1)',
                       font=dict(color='red', size=12))
fig_phd.show()
#
#
#
#
#
#
#
décadas = [(1970, 1980), (1980, 1990), (1990, 2000), (2000, 2010),
           (2010, 2020), (2020, 2030)]
cores = ['#1268AF', '#3F6C91', '#6C7173', '#997656', '#C67B38','#F3801B']
#
#
#
#
#
# Criamos a figura.
fig = go.Figure()
# Adicionamos um traço para cada década.
traços = 0
for i, (início,fim) in enumerate(décadas):
    dadosDec = dfMSc[(dfMSc['AnoGrad'] >= início) & 
                     (dfMSc['AnoGrad'] < fim)]
    if not dadosDec.empty:                     
        fig.add_trace(go.Violin(y=dadosDec['MesesParaGrad'], 
                      name=f'{início}-{fim}', box_visible=True,
                      meanline_visible=True,
                      line_color=cores[i]))
        traços += 1              
# Ajeitamos legendas e marcações.
fig.update_layout(title='Tempo de Graduação para Mestrado por Década',
                  xaxis_title='Década',
                  yaxis_title='Meses')
fig.add_shape(type="line", x0=0, x1=traços-1, y0=24, y1=24, 
              line=dict(color="green", width=2))
fig.add_annotation(x=(traços-1)/2, y=24, text='24 meses',showarrow=False, 
                   bgcolor='rgba(255, 255, 255, 1)',
                   font=dict(color='green', size=12))
fig.add_shape(type="line", x0=0, x1=traços-1, y0=36, y1=36, 
              line=dict(color="red", width=2))
fig.add_annotation(x=(traços-1)/2, y=36, text='36 meses',showarrow=False, 
                   bgcolor='rgba(255, 255, 255, 1)',
                   font=dict(color='red', size=12))                  
fig.show()
#
#
#
#
#
# Criamos a figura.
fig = go.Figure()
# Adicionamos um traço para cada década.
traços = 0
for i, (início,fim) in enumerate(décadas):
    dadosDec = dfPhD[(dfPhD['AnoGrad'] >= início) & 
                     (dfPhD['AnoGrad'] < fim)]
    if not dadosDec.empty:
        fig.add_trace(go.Violin(y=dadosDec['MesesParaGrad'], 
                      name=f'{início}-{fim}', box_visible=True,
                      meanline_visible=True,
                      line_color=cores[i]))
        traços += 1                     
# Ajeitamos legendas e marcações.
fig.update_layout(title='Tempo de Graduação para Doutorado por Década',
                  xaxis_title='Década',
                  yaxis_title='Meses')
fig.add_shape(type="line", x0=0, x1=traços-1, y0=48, y1=48, 
              line=dict(color="green", width=2))
fig.add_annotation(x=(traços-1)/2, y=48, text='48 meses',showarrow=False, 
                   bgcolor='rgba(255, 255, 255, 1)',
                   font=dict(color='green', size=12))
fig.add_shape(type="line", x0=0, x1=traços-1, y0=60, y1=60, 
              line=dict(color="red", width=2))
fig.add_annotation(x=(traços-1)/2, y=60, text='60 meses',showarrow=False, 
                   bgcolor='rgba(255, 255, 255, 1)',
                   font=dict(color='red', size=12))
fig.show()
#
#
#
#
#
#
#
# Agrupamos os mestres por ano e sexo.
df_grouped = dfMSc.groupby([df['AnoGrad'], 'Sexo']).size().reset_index(name='Número')
# Criamos o gráfico.
fig = px.bar(df_grouped, x='AnoGrad', y='Número', color='Sexo', 
             title='Graduados por Sexo e Ano -- Mestrado',
             labels={'Número': 'Número de Egressos', 'AnoGrad': 'Ano'})
fig.show()
#
#
#
#
#
# Agrupamos os doutores por ano e sexo.
df_grouped = dfPhD.groupby([df['AnoGrad'], 'Sexo']).size().reset_index(name='Número')
# Criamos o gráfico.
fig = px.bar(df_grouped, x='AnoGrad', y='Número', color='Sexo', 
             title='Graduados por Sexo e Ano -- Doutorado',
             labels={'Número': 'Número de Egressos', 'AnoGrad': 'Ano'})
fig.show()
#
#
#
#
#
#
#
fig_msc = px.histogram(dfMSc, x='IdadeNaGraduação', 
                       nbins=30, range_x=[0, 60],
                       title='Distribuição da Idade na Graduação (Mestrado)',
                       labels={'IdadeNaGraduação': 'Idade na Graduação'},
                       marginal='box')  
fig_msc.show()
#
#
#
#
fig_phd = px.histogram(dfPhD, x='IdadeNaGraduação', 
                       nbins=30, range_x=[0, 60],
                       title='Distribuição da Idade na Graduação (Doutorado)',
                       labels={'IdadeNaGraduação': 'Idade na Graduação'},
                       marginal='box') 
fig_phd.show()
#
#
#
#
#
# Separamos o dataframe:
dfMScM = dfMSc[dfMSc['Sexo'] == 'Masculino']
dfMScF = dfMSc[dfMSc['Sexo'] == 'Feminino']
# Criamos os gráficos:
violinM = go.Violin(y=dfMScM['IdadeNaGraduação'], side='positive', 
                    name='Masculino', marker_color='blue', 
                    box_visible=True, meanline_visible=True,
                    showlegend=False)
violinF = go.Violin(y=dfMScF['IdadeNaGraduação'], side='negative', 
                    name='Feminino', marker_color='red', 
                    box_visible=True, meanline_visible=True,
                    showlegend=False)
# Criamos a figura e adicionamos os traços.
fig = go.Figure()
fig.add_trace(violinM)
fig.add_trace(violinF)
# Ajustes no layout...
fig.update_layout(title='Idade na Graduação (MSc)',
                  yaxis_title='Idade em Anos',
                  violingap=0,
                  violinmode='overlay',
                  )
fig.show()
#
#
#
#
#
# Separamos o dataframe:
dfPhDM = dfPhD[dfPhD['Sexo'] == 'Masculino']
dfPhDF = dfPhD[dfPhD['Sexo'] == 'Feminino']
# Criamos os gráficos:
violinM = go.Violin(y=dfPhDM['IdadeNaGraduação'], side='positive', 
                    name='Masculino', marker_color='blue', 
                    box_visible=True, meanline_visible=True,
                    showlegend=False)
violinF = go.Violin(y=dfPhDF['IdadeNaGraduação'], side='negative', 
                    name='Feminino', marker_color='red', 
                    box_visible=True, meanline_visible=True,
                    showlegend=False)
# Criamos a figura e adicionamos os traços.
fig = go.Figure()
fig.add_trace(violinM)
fig.add_trace(violinF)
# Ajustes no layout...
fig.update_layout(title='Idade na Graduação (PhD)',
                  yaxis_title='Idade em Anos',
                  violingap=0,
                  violinmode='overlay',
                  )
fig.show()
#
#
#
#
#
#
#
#
#
# Agrupa por nome e nível. 
agrNomNiv = df.groupby('Nome')['Nivel'].nunique()
# Criamos um índice com os nomes dos alunos que completaram dois níveis.
doisNíveis = agrNomNiv[agrNomNiv == 2].index
# Filtra o dataframe original anotando o número de níveis cursados.
dfdoisNíveis = df[df['Nome'].isin(doisNíveis)]
# Criamos subsets. 
df2MSc = dfdoisNíveis[dfdoisNíveis['Nivel'] == 'MESTRADO']
df2PhD = dfdoisNíveis[dfdoisNíveis['Nivel'] == 'DOUTORADO']
# Juntamos por nome, mudando os nomes dos campos.
dfTemp = df2MSc.merge(df2PhD, on='Nome', suffixes=('_MSc', '_PhD'))
# Mantemos somente algumas colunas para evitar repetição.
dfAmbos = dfTemp[['Programa_MSc', 'Registro_MSc', 
                  'Nome', 'Adm_MSc', 'Sit_MSc', 'Adm_PhD', 'Sit_PhD', 
                  'Nascimento_MSc', 'Sexo_MSc']]
# Por organização renomeamos as colunas comuns.
dfAmbos = dfAmbos.rename(columns={'Programa_MSc': 'Programa', 
                                  'Registro_MSc': 'Registro',
                                  'Nascimento_MSc': 'Nascimento',
                                  'Sexo_MSc': 'Sexo'})
dfAmbos.to_csv("Data/DoisNiveis.csv")
#
#
#
#
#
dfAmbosS = dfAmbos.sort_values(by='Adm_MSc')
# Criamos a figura
fig = go.Figure()
# Adicionamos dois traços, um para cada nível que este estudante cursou.
index = 1
for _, row in dfAmbosS.iterrows():
    fig.add_trace(go.Scatter(x=[row['Adm_MSc'], row['Sit_MSc']],
                             y=[index+1]*2, 
                             mode='lines+markers',
                             line=dict(color='#4D97C9'), 
                             marker=dict(symbol=['triangle-right', 'triangle-left'],  
                                         color='#4D97C9', size=8),  
                             name=row['Nome'],
                             showlegend=False  
                            ))
    fig.add_trace(go.Scatter(x=[row['Adm_PhD'], row['Sit_PhD']],
                             y=[index+1]*2,  
                             mode='lines+markers',
                             line=dict(color='#0C416C'), 
                             marker=dict(symbol=['triangle-right', 'triangle-left'],  
                                         color='#0C416C', size=8),  
                             name=row['Nome'],
                             showlegend=False 
                            ))
    index += 1                        
# Ajustamos o layout.
fig.update_layout(title='Linha do Tempo para Egressos que Cursaram os Dois Níveis',
                  xaxis_title='Ano',xaxis_tickangle=90, 
                  yaxis_visible=False,
                  showlegend=False
                 )
# Mostramos a figura.
fig.show()
#
#
#
#
#
