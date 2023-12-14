import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf

# Função para obter dados
def obter_dados(ativos, num_candles, timeframe):
    dados_completos = pd.DataFrame()

    for ativo in ativos:
        dados_ativo = yf.download(tickers = ativo, interval = timeframe, period = num_candles)
        df_ativo = pd.DataFrame(dados_ativo)
        df_ativo['volatilidade'] = df_ativo['High'] - df_ativo['Low']
        df_ativo['timeframe'] = f'{ativo}_{timeframe}'

        dados_completos = pd.concat([dados_completos, df_ativo])

# Calculando a média e desvio padrão da volatilidade para cada ativo e período
    dados_completos['media_volatilidade'] = dados_completos['volatilidade'].mean()
    dados_completos['desvio_padrao_volatilidade'] = dados_completos['volatilidade'].std()
    dados_completos.reset_index(drop=True, inplace=True)

    return dados_completos

# Interface Streamlit
st.title("Coleta de Dados MT5")  

# Configurações do usuário
num_candles = st.selectbox("Escolha o período de visualização:", ['1d', '5d', '1mo', '3mo', '6mo','1y', '2y', '5y', '10y'])
ativo_escolhido = st.selectbox("Escolha o ativo:", ['EURUSD=X','USDBRL=X','^BVSP', 'USDJPY=X', 'GBPUSD=X', 'AUDUSD=X', 'USDCAD=X', 'NZDUSD=X', 'USDCHF=X', 'EURJPY=X', 'GBPJPY=X', 'AUDJPY=X'])
timeframe_escolhido = st.radio("Escolha o timeframe:", ['D1', 'W1', 'MN1'])
porcentagem_media_volatilidade = st.number_input('Digite o percentual da média da volatilidade', min_value = 1, max_value = 100, value = 50)

# Mapeando o timeframe escolhido para o formato correspondente do MetaTrader5
mapa_timeframes = {'D1': '1d', 'W1': '1wk', 'MN1': '1mo'}
timeframe_mt5 = mapa_timeframes[timeframe_escolhido]

# Obtendo dados com base nas escolhas do usuário
dados = obter_dados([ativo_escolhido], num_candles, timeframe_mt5)
dados['porcentagem_media_volatilidade'] = dados['media_volatilidade'] * porcentagem_media_volatilidade/100
dados['média da volatilidade + desvio padrão'] = dados['media_volatilidade'] + dados['desvio_padrao_volatilidade']
dados['média da volatilidade - desvio padrão'] = dados['media_volatilidade'] - dados['desvio_padrao_volatilidade']
print(dados)

# Plotando o gráfico de barras verticais da amplitude
plt.figure(figsize=(10, 6))
plt.bar(dados.index, dados['volatilidade'], color='blue', alpha=0.7, label='Volatilidade')

# Linhas horizontais
plt.plot(dados['media_volatilidade'], color='yellow', label='Média da Volatilidade')
plt.plot(dados['média da volatilidade + desvio padrão'], color='green', linestyle='-', label='Média + Desvio Padrão')
plt.plot(dados['média da volatilidade - desvio padrão'], color='red', linestyle='-', label='Média - Desvio Padrão')
plt.plot(dados['porcentagem_media_volatilidade'], color='pink', linestyle='-', label=f'{porcentagem_media_volatilidade}% da Média da Volatilidade')

plt.title(f"Amplitude do Candlestick - {ativo_escolhido} - {timeframe_escolhido}")
plt.xlabel("Tempo")
plt.ylabel("Amplitude do Candlestick")
plt.legend()

# Passando a figura para st.pyplot()
st.pyplot(plt.gcf()) 

# Fechar a figura do Matplotlib
plt.close()

# Exibindo os dados no Streamlit
st.dataframe(dados)