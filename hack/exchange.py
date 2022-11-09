import pandas as pd
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import altair as alt
import time

import glob

import os, sys

def fill_missing():
    path = "D:/SEM 5/hack/Currency_Conversion_Test_Data"
  
    # csv files in the path
    files = glob.glob(path + "/*.csv")
    for fname in files:
            print(fname)
            df = pd.read_csv(fname)
            print(df)
            for column in df:
        #print(df[column].values)
                df[column] = df[column].fillna(method='ffill')

            for column in df:
                if column == 'Date':
                    continue
                else:
            
        #print(df[column].values)
                    mean = df[column].mean()
                    df[column] = df[column].fillna(mean)
            print(df)
            df.to_csv(fname, index=False)


st.set_page_config(page_title="Dollar Conversion", page_icon=":bar_chart:", layout="wide")

fill_missing()

st.markdown("<h1 style='text-align: left; color: #041058;'><u>TEAM - 1</u></h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: black; background: #D296CA'><i>$ Currency Exchange Rate $</i></h1>", unsafe_allow_html=True)

st.markdown("<h6 style='text-align: center; color: black; background: #D296CA'>Adithya sree mohan<br>Aishwarya K<br>Akshara R<br>Angela Raj Chadha<br>Jaswanth Kunisetty<br></h6>", unsafe_allow_html=True)

df = pd.read_csv("D:/SEM 5/hack/Currency_Conversion_Test_Data/Exchange_Rate_Report_2012.csv")

columns1 = []
for rows in df:
    columns1.append(rows)

left_column, right_column = st.columns(2)
with left_column:
    st.markdown("<br><br><h3 style='text-align: left; color: black; background: #ADD296'>Select Currency-1</h3>", unsafe_allow_html=True)
    c1 = st.selectbox('From:', df.columns[1:])


with right_column:
    st.markdown("<br><br><h3 style='text-align: left; color: black; background: #ADD296'>Select Currency-2</h3>", unsafe_allow_html=True)
    c2 = st.selectbox('To:', df.columns[1:])

currency = pd.read_csv("D:/SEM 5/hack/Currency_Conversion_Test_Data/Exchange_Rate_Report_2021.csv")

cu = list(map(float, currency[c1]))
cu1 = list(map(float, currency[c2]))
temp = cu[5]
temp1 =cu1[5]
cal = (1/float(temp))*float(temp1)

left_column, right_column = st.columns(2)
with left_column:
    st.info(" 1 {} = ".format(c1))

with right_column:
    st.info("{0} {1}".format(cal,c2))

left_column, right_column = st.columns(2)
with left_column:
    st.markdown("<br><br><h3 style='text-align: left; color: black; background: #ADD296'> Currency-1</h3>", unsafe_allow_html=True)
    option1 = st.selectbox('From', df.columns[1:])


with right_column:
    st.markdown("<br><br><h3 style='text-align: left; color: black; background: #ADD296'> Currency-2</h3>", unsafe_allow_html=True)
    option = st.selectbox('To', df.columns[1:])

year = st.selectbox('Select year', ('2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'))

path = "D:/SEM 5/hack/Currency_Conversion_Test_Data/Exchange_Rate_Report_{}.csv".format(year)
df = pd.read_csv(path)

left_column, middle_column, right_column = st.columns(3)
with middle_column:
    st.markdown("<h4 style='text-align: center; color: black; background: #E09A7A'> Select time frame</h4>", unsafe_allow_html=True)
    time = st.radio(
            "",
            ["Weekly", "Monthly", "Quaterly","Yearly"],
            key="visibility",
            horizontal=True,
        )

def get_yearly_data(option):
    years = ['2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']

    values = []
    for i in range(len(years)):
        path = "D:/SEM 5/hack/Currency_Conversion_Test_Data/Exchange_Rate_Report_{}.csv".format(years[i])
        df = pd.read_csv(path)
        values.append(df[option].mean())
    values = pd.DataFrame(values, index = years,columns=[option])
    return values

def get_montly_data(option):
    data = df[[df.columns[0],option]].copy()
    data['month'] = pd.DatetimeIndex(data[data.columns[0]]).month
    avg = data.groupby(pd.PeriodIndex(data[data.columns[0]], freq="M"))[option].mean()
    avg = avg.to_frame()
    avg['mon'] = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

    avg = avg.set_index(avg['mon'])
    dat = avg[[option]].copy()
    return dat

def get_quaterly_data(option):
    data = df[[df.columns[0],option]].copy()
    data['month'] = pd.DatetimeIndex(data[data.columns[0]]).month
    avg = data.groupby(pd.PeriodIndex(data[data.columns[0]], freq="M"))[option].mean()
    avg = avg.to_frame()
    avg['mon'] = [0,1,2,3,4,5,6,7,8,9,10,11]
    avg = avg.set_index(avg['mon'])
    dat = avg[[option]].copy()
    temp = list(map(int, avg[option]))
    quarter = []
    sum = 0
    for x in avg['mon']:
        if x %4 == 0:
            if x == 0:
                sum = 0
            else:
                sum = sum / 4 
                quarter.append(sum)
                sum = 0
        sum = sum + temp[x]
    sum = sum / 4
    quarter.append(sum)
    quar = dat[option].copy()
    value = pd.DataFrame()
    value['val'] = quarter

    return value

if time == "Weekly":
    data = df[[df.columns[0],option]].copy()
    row = len(df.axes[0])
    data[data.columns[0]] =  pd.date_range(data[df.columns[0]].iloc[0],data[df.columns[0]].iloc[-1], periods=row)
    data = data.set_index(df.columns[0])
    minimum = data.min()
    maximum = data.max()
    l,r = st.columns(2)
    with l:
        st.info("MIN value: {}".format(minimum.iloc[0]))
    with r:
        st.info("MAX value: {}".format(maximum.iloc[0]))


    
    st.line_chart(data)

elif time == "Monthly":
    data_month = get_montly_data(option)
    minimum = data_month.min()
    maximum = data_month.max()
    l,r = st.columns(2)
    with l:
        st.info("MIN value: {}".format(minimum.iloc[0]))
    with r:
        st.info("MAX value: {}".format(maximum.iloc[0]))
    st.line_chart(data_month)

elif time == "Quaterly":
    data_quat = get_quaterly_data(option)
    minimum = data_quat.min()
    maximum = data_quat.max()
    l,r = st.columns(2)
    with l:
        st.info("MIN value: {}".format(minimum.iloc[0]))
    with r:
        st.info("MAX value: {}".format(maximum.iloc[0]))
    st.line_chart(data_quat)

elif time == "Yearly":
    data_year = get_yearly_data(option)
    minimum = data_year.min()
    maximum = data_year.max()
    l,r = st.columns(2)
    with l:
        st.info("MIN value: {}".format(minimum.iloc[0]))
    with r:
        st.info("MAX value: {}".format(maximum.iloc[0]))
    st.line_chart(data_year)




