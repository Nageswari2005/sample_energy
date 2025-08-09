import streamlit as st
from forecast import loaddata,predict_usage,train_forecast_model
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import pandas as pd
from analyzer import detect_anomalies
from recommender import generate_recomendatation

st.set_page_config(page_title="Restential Energy Analyzer")
st.title("Resitance Energy Analysis")
tab1,tab2=st.tabs(["Dashboard","Bot Assistant"])
with tab1:
    st.title("Dashboard of analysis")
    uploaded_file=st.file_uploader("upload csv file")
    if uploaded_file:
        df=loaddata(uploaded_file)
        if not {'timestamp','usage_kwh'}.issubset(df.columns):
            st.error("csv must contain timestamp,usage_kwh")
            st.stop()
        #chart 1: Line chart
        st.subheader("Usage over time")
        st.line_chart(df.set_index('timestamp')['usage_kwh'])
        #chart 2: Hourly usage bar chart
        st.subheader("Hourly Energy Usage")
        df_groupbyhour=df.groupby('hour')['usage_kwh'].sum().reset_index()
        bar_chart=alt.Chart(df_groupbyhour).mark_bar().encode(x='hour:O',y='usage_kwh:Q',tooltip=['hour','usage_kwh']).properties(height=300)
        st.altair_chart(bar_chart,use_container_width=True)
        #chart 3: Heatmap Day vs Hour
        st.subheader("Heatmap Day vs Hour")
        weekday_order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        df['day']=pd.Categorical(df['day'],categories=weekday_order,ordered=True)
        heatmap_data=df.pivot_table(index='day',columns='hour',values='usage_kwh',aggfunc='sum').fillna(0)
        fig,ax=plt.subplots(figsize=(12,5))
        sns.heatmap(heatmap_data,cmap='YlOrRd',annot=True,fmt=".1f",linewidths=0.3,ax=ax)
        st.pyplot(fig)
        #forecasting
        st.subheader("Forecasting Next 24 hours")
        model=train_forecast_model(df)
        forecast=predict_usage(model,list(range(24)))
        st.line_chart(forecast)
        
        st.subheader("Anomally Detection")
        anomalies=detect_anomalies(df)
        st.dataframe(anomalies[anomalies['anomaly']==-1])
        
        st.subheader("Recommendation for low usage")
        for rec in generate_recomendatation(df):
            st.info(rec)


with tab2:
    st.title("Bot Assistant")
    user_input=st.text_input("Ask question regarding energy save")
    st.subheader("Answer for the query")
    st.caption("@ copyrights by Nageswari 2025")
    