import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
# Importei o Streamlit para fazer a interface gráfica, o yfinance pra baixar os dados das
# ações, o pandas pra transformar os dados em dataframes e o plotly para plotar os gráficos

st.set_page_config(layout="wide",
                   page_title='StockMonitor',
                   page_icon="📈")
# Configurei a página para abrir sempre em modo "wide", assim como título e ícone
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    .custom-title {
        font-family: 'Roboto', sans-serif;  /* Fonte Roboto */
        font-size: 30px;                     /* Tamanho da fonte */
        color: #FFFFFF;                      /* Cor da fonte */
        text-align: center;                  /* Alinhamento */
    }
    </style>
    <h1 class="custom-title">StockMonitor</h1>
    """, unsafe_allow_html=True)
# Usei um css simples para estilizar o título da página

acoes = ['ABEV3',  # Ambev
    'ITUB4',  # Itaú Unibanco
    'B3SA3',  # B3
    'PETR3',  # Petrobras
    'VALE3',  # Vale
    'BBAS3',  # Banco do Brasil
    'MGLU3',  # Magazine Luiza
    'LREN3',  # Lojas Renner
    'WEGE3',  # Weg
    'PSSA3',  # Porto Seguro
    'USIM5',  # Usiminas
    'GGBR4',  # Gerdau
    'BRFS3',  # BRF
    'RENT3',  # Localiza
    'KROT3',  # Kroton
    'COGN3',  # Cogna
    'CVCB3',  # CVC
    'VIVT3',  # Vivo
    'TIMP3',  # TIM
    'ENBR3',  # Energias do Brasil
    'EQTL3',  # Equatorial
    'CSNA3',  # Companhia Siderúrgica Nacional
    'SMLS3',  # Smiles
    'PINE4',  # Banco Pine
    'NTCO3',  # Natura
    'SEER3',  # Ser Educacional
    'CASH3',  # Assaí
    'CMIG4',  # Cemig
    'CVCB3',  # CVC Brasil
    'HGTX3',  # HGTX
    'BRKM3',  # Braskem
    'RAIL3',  # Rumo
    'LIGT3',  # Light
    'CSAN3',  # Cosan
    'PFRM3',  # Profarma
    'BBDC3',  # Bradesco
    'BBDC4',  # Bradesco
    'CGRA3',  # Cia. Brasileira de Distribuição
    'RNEW3',  # Renova
    'LREN3',  # Lojas Renner
    'JBSS3',  # JBS
    'FESA4',  # Ferbasa
    'TAEE11',  # Taesa
    'YDUQ3',  # Yduqs
]
# Listei as ações que iremos visualizar

acoes_selecionadas = st.multiselect("Selecione as ações que deseja visualizar:", acoes, default=acoes[:3])
# Usei o método st.multiselect para criar uma caixa de seleção

col1, col2 = st.columns(2)
# Criei duas colunas lado a lado para organizar melhor a página
if not acoes_selecionadas:
    st.warning("Por favor, selecione pelo menos uma ação para continuar.")
else:
    with col1:
        data_inicio = st.date_input("Data Inicial", value=pd.to_datetime('2022-01-01'), format="DD/MM/YYYY")
with col2:
    data_final = st.date_input("Data Final", value=pd.to_datetime('today'), format="DD/MM/YYYY")
# Em cada uma das colunas atribui um st.date_input a uma variavel e usei o pandas para
# formatar as datas

lista_metricas = []
# criei um dicionário para nossas métricas

with col1:
    for acao in acoes_selecionadas:
        ticker = f"{acao}.SA"
        dados = yf.download(ticker, start=data_inicio, end=data_final)
        # Dentro da coluna um criei um loop para baixar os dados de cada uma das ações, como estamos trabalhando com ações
        # brasileiras criei a variavel ticker e atribui a ela a variavel ação formatada como f string concatenado com .SA
        if not dados.empty:
            preco_atual = float(dados['Close'].iloc[-1])
            preco_inicio_periodo = dados['Close'].iloc[0]
            variacao_percentual = (preco_atual - preco_inicio_periodo) / preco_inicio_periodo * 100


            volume_total = dados['Volume'].sum()
            # Dentro de um If-else fiz uma breve validação dos dados e calculei as métricas que entrarão na nossa lista
            # abaixo
            lista_metricas.append({
                'Ação': acao,
                'Preço Atual': f'R$ {preco_atual:.2f}',
                'Variação Percentual': variacao_percentual,
                'Volume Total': volume_total
            })
        else:
            st.warning(f"Nenhum dado disponível para {acao}. Verifique o ticker.")

    # Converti a lista de métricas em um DataFrame
    df_metrica = pd.DataFrame(lista_metricas)

    st.write("### Métricas Comparativas das Ações Selecionadas")
    st.dataframe(df_metrica.sort_values(by='Preço Atual', ascending=True),
                 hide_index=True,
                 width=600
                 )
    # usei o st.write para dar título ao dataframe e exibi ele com st.dataframe, classifiquei os dados
    # por Preço atual de forma crescente para mostrar primeiro as ações que estão mais baratas no dia
    variacao_percentual = []
    for acao in acoes_selecionadas:
        if not dados.empty:
            var_perc = (dados['Close'].iloc[-1] - dados['Close'].iloc[0]) / dados['Close'].iloc[0] * 100
            variacao_percentual.append({'Ação': acao, 'Variação Percentual': var_perc})
    # Criei uma lista para variação percentual e en seguida um loop
    df_variacao = pd.DataFrame(variacao_percentual)

# Verificação da validade das datas dentro de uma estrutura if-else
if data_inicio < data_final:

    with col2:

        # Criei uma figura do plotly dentro da coluna 2
        fig = go.Figure()

        # Criei um loop pra buscar os dados
        for acao in acoes_selecionadas:
            # Incluí o '.SA' no ticker de cada ação
            ticker = yf.Ticker(acao + ".SA")
            dados_acao = ticker.history(start=data_inicio, end=data_final)

            # Adicionei uma linha para cada ação no gráfico
            fig.add_trace(go.Scatter(
                x=dados_acao.index,
                y=dados_acao['Close'],
                mode='lines',
                name=f"{acao}"
            ))

        # Formatei as datas para o título
        data_inicio_formatada = data_inicio.strftime("%d/%m/%Y")
        data_final_formatada = data_final.strftime("%d/%m/%Y")

        # Atualizei o layout do gráfico
        fig.update_layout(
            title=f'Preço de Fechamento ({data_inicio_formatada} a {data_final_formatada})',
            yaxis_title='Preço (R$)',
            template="plotly_dark",
            width=550
        )

        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f'Verifique as datas selecionadas acima')

with col1:
    variacao_percentual = []
    for acao in acoes_selecionadas:
        dados = yf.download(f"{acao}.SA", start=data_inicio, end=data_final)
        if not dados.empty:
            var_perc = (dados['Close'].iloc[-1] - dados['Close'].iloc[0]) / dados['Close'].iloc[0] * 100
            variacao_percentual.append({'Ação': acao, 'Variação Percentual': var_perc})

    df_variacao = pd.DataFrame(variacao_percentual)
# Dentro da coluna 1 criei uma lista para os valores de variação e busquei eles usando um loop com o yfinance
    # Após verificar se os dados estão vazios fazemos os calculos e adicionamos eles a variável que transformamos
    # em dataframe com o pandas


    fig_barra = go.Figure()
    # Criei o gráfico de barras horizontais com Plotly

    fig_barra.add_trace(go.Bar(
        x=df_variacao['Variação Percentual'],  # O eixo X será a variação percentual
        y=df_variacao['Ação'],  # O eixo Y será o nome das ações
        orientation='h',  # Barra horizontal
        marker=dict(color='salmon'),  # Cor das barras
    ))
    # Adicionei os dados ao gráfico

    fig_barra.update_layout(
        title='Variação Percentual das Ações Selecionadas',
        xaxis_title='Variação Percentual (%)',
        template='plotly_white',  # Estilo do gráfico
        xaxis=dict(showgrid=True),  # Adiciona grade ao eixo X
        yaxis=dict(autorange="reversed"),
        width=550
    )
    # Configurei os rótulos e o layout

    st.plotly_chart(fig_barra)

with col2:
    fig_barras = go.Figure()
    for acao in acoes_selecionadas:
        ticker = yf.Ticker(f"{acao}.SA")
        dados_acao = ticker.history(period="10y")
        # Dentro da col2 criei um grafico de barras e adicionei os dados
        # Adicionei uma barra para cada ação selecionada, com o valor máximo ('High')
        fig_barras.add_trace(go.Bar(
            x=[acao],
            y=[dados_acao['High'].max()],
            name=acao
        ))

    # Configurei o layout do gráfico
    fig_barras.update_layout(
        title='Valores Máximos (High) das Ações Selecionadas',
        yaxis_title='Valor Máximo (High)',
        template='plotly_white'  # Estilo do gráfico
    )


    st.plotly_chart(fig_barras)

media_movel_list = []
# Criei nossa lista de medias moveis
with col1:
    for  acao in acoes_selecionadas:
        dados = yf.download(f"{acao}.SA", start=data_inicio, end=data_final)
        # Dentro da col1 fiz um loop pra buscar os dados

        if dados is not None and len(dados) >= 100:  # Verificação pra ver se há pelo menos 100 dias de dados
            # Calculei as médias móveis
            media_movel_20 = dados['Close'].rolling(window=20).mean().iloc[-1]
            media_movel_50 = dados['Close'].rolling(window=50).mean().iloc[-1]
            media_movel_100 = dados['Close'].rolling(window=100).mean().iloc[-1]

            # Adicionei as médias móveis à lista
            media_movel_list.append({
                'Ação': acao,
                'Média Móvel (20 dias)': media_movel_20,
                'Média Móvel (50 dias)': media_movel_50,
                'Média Móvel (100 dias)': media_movel_100
            })
        else:
            st.warning(f"Ação {acao} não tem dados suficientes para calcular todas as médias móveis.")

        # Converti a lista em um DataFrame
        df_media = pd.DataFrame(media_movel_list)


    st.write("### Média Móvel")
    st.dataframe(df_media, hide_index=True, width=600)
