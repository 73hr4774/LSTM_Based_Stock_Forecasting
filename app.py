import streamlit as st
import pandas as pd
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
import yfinance as yf

st.title('Stock Price Predictor App')

stock=st.text_input("Enter the Stock ID", 'HDB')

from datetime import datetime
end = datetime.now()
start=datetime(end.year-10, end.month, end.day)

hdfc_data=yf.download(stock,start,end)

model=load_model('Latest_stock_price_model.keras')
st.subheader('Stock Data')
st.write(hdfc_data)

splitting_len=int(len(hdfc_data)*0.7)
x_test=pd.DataFrame(hdfc_data.Close[splitting_len:])

def plot_graph(figsize,values, full_data, extra_data=0, extra_dataset=None):
    fig=plt.figure(figsize=figsize)
    plt.plot(values, 'Orange')
    plt.plot(full_data.Close, 'b')
    if extra_data:
        plt.plot(extra_dataset)
    return fig

st.subheader('Original Close Price and MA for 250 days')
hdfc_data['MA_for 250_days']=hdfc_data.Close.rolling(250).mean()
st.pyplot(plot_graph((15,6),hdfc_data['MA_for 250_days'],hdfc_data,0))

st.subheader('Original Close Price and MA for 200 days')
hdfc_data['MA_for 200_days']=hdfc_data.Close.rolling(200).mean()
st.pyplot(plot_graph((15,6),hdfc_data['MA_for 200_days'],hdfc_data,0))

st.subheader('Original Close Price and MA for 100 days')
hdfc_data['MA_for 100_days']=hdfc_data.Close.rolling(100).mean()
st.pyplot(plot_graph((15,6),hdfc_data['MA_for 100_days'],hdfc_data,0))

st.subheader('Original Close Price and MA for 100 days and MA for 250 days' )
st.pyplot(plot_graph((15,6),hdfc_data['MA_for 100_days'],hdfc_data,1,hdfc_data['MA_for 250_days']))

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(x_test)


x_data=[]
y_data=[]

for i in range(100, len(scaled_data)):
    x_data.append(scaled_data[i-100:i])
    y_data.append(scaled_data[i])

import numpy as np
x_data, y_data=np.array(x_data), np.array(y_data)

predictions=model.predict(x_data)

inv_pre=scaler.inverse_transform(predictions)
inv_y_test=scaler.inverse_transform(y_data)

ploting_data=pd.DataFrame(
    {
    'original_test_data':inv_y_test.reshape(-1),
     'predictions':inv_pre.reshape(-1)
    },
        index=hdfc_data.index[splitting_len+100:]
)
st.subheader('Original values VS Predicted values')
st.write(ploting_data)

st.subheader('Original Close price vs Predicted Close price')
fig=plt.figure(figsize=(15,6))
plt.plot(pd.concat([hdfc_data.Close[:splitting_len+100],ploting_data],axis=0))
plt.legend(['Data-not used', 'Original Test data', 'Predicted Test data'])
st.pyplot(fig)