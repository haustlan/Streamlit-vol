import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf

# Function to get data
def get_data(assets, num_candles, timeframe):
    complete_data = pd.DataFrame()

    for asset in assets:
        asset_data = yf.download(tickers=asset, interval=timeframe, period=num_candles)
        df_asset = pd.DataFrame(asset_data)
        df_asset['volatility'] = df_asset['High'] - df_asset['Low']
        df_asset['timeframe'] = f'{asset}_{timeframe}'

        complete_data = pd.concat([complete_data, df_asset])

    # Calculating the mean and standard deviation of volatility for each asset and period
    complete_data['volatility_mean'] = complete_data['volatility'].mean()
    complete_data['volatility_std_dev'] = complete_data['volatility'].std()
    complete_data.reset_index(drop=True, inplace=True)

    return complete_data

# Streamlit interface
st.title("MT5 Data Collection")  

# User settings
num_candles = st.selectbox("Choose the viewing period:", ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y'])
selected_asset = st.selectbox("Choose the asset:", ['EURUSD=X','USDBRL=X','^BVSP', 'USDJPY=X', 'GBPUSD=X', 'AUDUSD=X', 'USDCAD=X', 'NZDUSD=X', 'USDCHF=X', 'EURJPY=X', 'GBPJPY=X', 'AUDJPY=X'])
selected_timeframe = st.radio("Choose the timeframe:", ['D1', 'W1', 'MN1'])
volatility_mean_percentage = st.number_input('Enter the percentage of the volatility mean', min_value=1, max_value=100, value=50)

# Mapping the chosen timeframe to the corresponding MetaTrader5 format
timeframe_map = {'D1': '1d', 'W1': '1wk', 'MN1': '1mo'}
mt5_timeframe = timeframe_map[selected_timeframe]

# Getting data based on user choices
data = get_data([selected_asset], num_candles, mt5_timeframe)
data['volatility_mean_percentage'] = data['volatility_mean'] * volatility_mean_percentage / 100
data['volatility_mean + std_dev'] = data['volatility_mean'] + data['volatility_std_dev']
data['volatility_mean - std_dev'] = data['volatility_mean'] - data['volatility_std_dev']
print(data)

# Plotting the vertical bar chart of amplitude
plt.figure(figsize=(10, 6))
plt.bar(data.index, data['volatility'], color='blue', alpha=0.7, label='Volatility')

# Horizontal lines
plt.plot(data['volatility_mean'], color='yellow', label='Volatility Mean')
plt.plot(data['volatility_mean + std_dev'], color='green', linestyle='-', label='Mean + Std Dev')
plt.plot(data['volatility_mean - std_dev'], color='red', linestyle='-', label='Mean - Std Dev')
plt.plot(data['volatility_mean_percentage'], color='pink', linestyle='-', label=f'{volatility_mean_percentage}% of Volatility Mean')

plt.title(f"Candlestick Amplitude - {selected_asset} - {selected_timeframe}")
plt.xlabel("Time")
plt.ylabel("Candlestick Amplitude")
plt.legend()

# Passing the figure to st.pyplot()
st.pyplot(plt.gcf())

# Closing the Matplotlib figure
plt.close()

# Displaying data in Streamlit
st.dataframe(data)
