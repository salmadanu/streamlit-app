import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengambil data dari sumber data main_data.csv
main_df = pd.read_csv("https://raw.githubusercontent.com/salmadanu/bangkit-ml/main/proyek_analisis_data/submission/dashboard/main_data.csv")

# Judul page dan penjelasan
st.subheader('Proyek Akhir Analisis Data :rain_cloud:')
st.header('AQI Levels in Huairou, Beijing :national_park:')
st.subheader('This dashboard displays quarterly data of AQI values throughout the years 2013-2017')
st.write(':one: First, choose the year and quarter of AQI data to be displayed.')
st.write(':two: Secondly, use the sidebar to choose which AQI values to be displayed.')

# --------------------- HELPER FUNCTIONS --------------------- #

# Function berikut digunakan untuk membuat pilihan input tahun dan quarter
def create_quarter_options(year):
    if year == '2013':
        return ['Q2', 'Q3', 'Q4']
    elif year == '2017':
        return ['Q1']
    else:
        return ['Q1', 'Q2', 'Q3', 'Q4']

# Function berikut digunakan untuk membuat data fram bernama quarterly_aqi_df
    # Data frame tersebut adalah kumpulan data harian seluruh parameter dari quarter yang dipilih
    # Data point harian diambil dari rata-rata nilai parameter per jam pada hari i
def create_quarterly_aqi_df(df):
    quarterly_aqi_df = df.groupby(['year', 'quarter']).agg({
        'PM2.5' : 'mean',
        'PM10' : 'mean',
        'SO2' : 'mean',
        'NO2' : 'mean',
        'CO' : 'mean',
        'O3' : 'mean',
        'TEMP' : 'mean',
        'PRES' : 'mean',
        'DEWP' : 'mean',
        'RAIN' : 'mean',
        'WSPM' : 'mean'
    }).reset_index()
    quarterly_aqi_df.columns = ['year', 'quarter', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    return quarterly_aqi_df

# Function berikut mengambil data berdasarkan pilihan tahun dan quarter, lalu menghitung rata-rata harian
    # seluruh nilai AQI selama quarter yang dipilih
def get_selected_quarter_data(main_df, year_select, quarter_select):
    selected_period_data = main_df[(main_df['year'] == int(year_select))]
    if quarter_select == 'Q1':
        selected_period_data = selected_period_data[(selected_period_data['month'] >= 1) & (selected_period_data['month'] <= 3)]
    elif quarter_select == 'Q2':
        selected_period_data = selected_period_data[(selected_period_data['month'] >= 4) & (selected_period_data['month'] <= 6)]
    elif quarter_select == 'Q3':
        selected_period_data = selected_period_data[(selected_period_data['month'] >= 7) & (selected_period_data['month'] <= 9)]
    elif quarter_select == 'Q4':
        selected_period_data = selected_period_data[(selected_period_data['month'] >= 10) & (selected_period_data['month'] <= 12)]
    else:
        return pd.DataFrame()
    
    # Agregasi nilai AQI yang dapat dihitung mean nya
    agg_dict = {
        'PM2.5': 'mean',
        'PM10': 'mean',
        'SO2': 'mean',
        'NO2': 'mean',
        'CO': 'mean',
        'O3': 'mean',
        'TEMP': 'mean',
        'PRES': 'mean',
        'DEWP': 'mean',
        'RAIN': 'mean',
        'WSPM': 'mean'
    }

    daily_data = selected_period_data.groupby(['year', 'month', 'day']).agg(agg_dict).reset_index()
    return daily_data
    
# Function tersebut adalah untuk membuat data frame yang berisi nilai mean, max, dan min nilai PM2.5 pada setiap quarter (2013-2017)
def create_quarterly_PM25_df(df):
    quarterly_PM25_df = df.groupby(['year', 'quarter']).agg({
        'PM2.5': ['mean', 'max', 'min']
    }).reset_index()
    quarterly_PM25_df.columns = ['year', 'quarter', 'mean_PM25', 'max_PM25', 'min_PM25']
    return quarterly_PM25_df

# Function tersebut adalah untuk mengambil data mean, max, dan min nilai PM2.5 masing-masing dari quarter yang dipilih
def get_PM25_metrics(quarterly_PM25_df, year_select, quarter_select):
    # Year dan quarter menjadi index pada data frame. Pengambilan dilakukan berdasarkan indeksnya
    quarterly_PM25_df.set_index(['year', 'quarter'], inplace=True)
    if (year_select, quarter_select) in quarterly_PM25_df.index:
        mean_PM25 = quarterly_PM25_df.loc[(year_select, quarter_select), 'mean_PM25']
        max_PM25 = quarterly_PM25_df.loc[(year_select, quarter_select), 'max_PM25']
        min_PM25 = quarterly_PM25_df.loc[(year_select, quarter_select), 'min_PM25']
        return mean_PM25, max_PM25, min_PM25
    else:
        return None, None, None
    
# Function tersebut adalah untuk membuat data frame yang berisi nilai mean, max, dan min temperatur pada setiap quarter (2013-2017)
def create_quarterly_temperature_df(df):
    quarterly_temp_df = df.groupby(['year', 'quarter']).agg({
        'TEMP': ['mean', 'max', 'min']
    }).reset_index()
    quarterly_temp_df.columns = ['year', 'quarter', 'mean_temp', 'max_temp', 'min_temp']
    return quarterly_temp_df

# Function tersebut adalah untuk mengambil data mean, max, dan min temperatur masing-masing dari quarter yang dipilih
def get_temperature_metrics(quarterly_temp_df, year_select, quarter_select):
    # Year dan quarter menjadi index pada data frame. Pengambilan dilakukan berdasarkan indeksnya
    quarterly_temp_df.set_index(['year', 'quarter'], inplace=True)
    if (year_select, quarter_select) in quarterly_temp_df.index:
        mean_temp = quarterly_temp_df.loc[(year_select, quarter_select), 'mean_temp']
        max_temp = quarterly_temp_df.loc[(year_select, quarter_select), 'max_temp']
        min_temp = quarterly_temp_df.loc[(year_select, quarter_select), 'min_temp']
        return mean_temp, max_temp, min_temp
    else:
        return None, None, None
    
# Terakhir, kedua fungsi yang sama untuk curah hujan
def create_quarterly_rain_df(df):
    quarterly_rain_df = df.groupby(['year', 'quarter']).agg({
        'RAIN': ['mean', 'max', 'min']
    }).reset_index()
    quarterly_rain_df.columns = ['year', 'quarter', 'mean_rain', 'max_rain', 'min_rain']
    return quarterly_rain_df

def get_rain_metrics(quarterly_rain_df, year_select, quarter_select):
    # Year and quarter become the index in the DataFrame. Retrieval is based on the index
    quarterly_rain_df.set_index(['year', 'quarter'], inplace=True)
    if (year_select, quarter_select) in quarterly_rain_df.index:
        mean_rain = quarterly_rain_df.loc[(year_select, quarter_select), 'mean_rain']
        max_rain = quarterly_rain_df.loc[(year_select, quarter_select), 'max_rain']
        min_rain = quarterly_rain_df.loc[(year_select, quarter_select), 'min_rain']
        return mean_rain, max_rain, min_rain
    else:
        return None, None, None
    

 # --------------------- HELPER FUNCTIONS --------------------- #   

# --------------------- SIDE BAR --------------------- #
# Side bar menampilkan check boxes berupa seluruh parameter AQI
    # Parameter yang diceklis akan disimpan dalam list selected_options untuk ditampilkan pada line chart
with st.sidebar:
    st.header(':round_pushpin: Huairou, Beijing')
    options = (
    'PM2.5', 
    'PM10', 
    'SO2',
    'NO2',
    'CO',
    'O3',
    'TEMP',
    'PRES',	
    'DEWP',
    'RAIN',
    'WSPM'
)
    selected_options = [st.checkbox(option, key=option) for option in options]
# --------------------- SIDE BAR --------------------- #
    
# --------------------- MAIN PAGE --------------------- #
# Dalam layour expander, user dapat memasukkan tahun dan quarter yang diinginkan untuk kemudian ditampilkan data AQI nya
with st.expander("Select Year and Quarter"):
    year_select = st.selectbox(
    label="Choose year",
    options=(
        '2013',
        '2014',
        '2015',
        '2016',
        '2017'
        )
    )
    quarter_options = create_quarter_options(year_select)
    quarter_select = st.selectbox(
        label="Choose a quarter",
        options=quarter_options
    )
st.write('Chosen period:', year_select, ' ', quarter_select)

# Pemanggilan helper function yang sudah dibuat di atas
quarterly_temp_df = create_quarterly_temperature_df(main_df)
quarterly_temp_df['year'] = quarterly_temp_df['year'].astype(str)
quarterly_temp_df['quarter'] = quarterly_temp_df['quarter'].astype(str)

quarterly_PM25_df = create_quarterly_PM25_df(main_df)
quarterly_PM25_df['year'] = quarterly_PM25_df['year'].astype(str)
quarterly_PM25_df['quarter'] = quarterly_PM25_df['quarter'].astype(str)

quarterly_RAIN_df = create_quarterly_rain_df(main_df)
quarterly_RAIN_df['year'] = quarterly_RAIN_df['year'].astype(str)
quarterly_RAIN_df['quarter'] = quarterly_RAIN_df['quarter'].astype(str)

quarterly_aqi_df = create_quarterly_aqi_df(main_df)

# Untuk menampilkan line chart pertama
selected_params = [param for param, selected in zip(options, selected_options) if selected]
selected_params_data = quarterly_aqi_df[['year', 'quarter'] + selected_params]
grouped_data = selected_params_data.groupby(['year', 'quarter']).mean().reset_index()
st.subheader('Line chart of selected AQI parameters by quarter (2013-2017)')
st.text('Data points are based on mean values of selected AQI parameters of each quarter throughout 2013-2017')
st.write(':grey_question: Empty line chart means no parameters have been chosen')
st.write('X-Axis : Quarter (2013 Q2 to 2017 Q1)')
st.write('Y-Axis : Quarterly mean value of selected AQI parameter)')
st.line_chart(grouped_data[selected_params])


st.subheader('Quarterly Statistics')
# PM2.5 container horizontal
st.subheader(':microscope: PM2.5')
mean_PM25, max_PM25, min_PM25 = get_PM25_metrics(quarterly_PM25_df, year_select, quarter_select)
mean_PM25 = round(mean_PM25, 2)
row1 = st.columns(3)
with row1[0]:  
    st.metric(label="Average PM2.5", value=f"{mean_PM25} µg/m³" if mean_PM25 is not None else "N/A")
with row1[1]: 
    st.metric(label="Maximum PM2.5", value=f"{max_PM25} µg/m³" if max_PM25 is not None else "N/A")
with row1[2]: 
    st.metric(label="Minimum PM2.5", value=f"{min_PM25} µg/m³" if min_PM25 is not None else "N/A")

# Temperature container horizontal
st.subheader(':thermometer: Temperature')
mean_temp, max_temp, min_temp = get_temperature_metrics(quarterly_temp_df, year_select, quarter_select)
mean_temp= round(mean_temp, 2) 
row1 = st.columns(3)
with row1[0]:
    st.metric(label="Average temperature", value=f"{mean_temp} °C" if mean_temp is not None else "N/A")
with row1[1]:  
    st.metric(label="Maximum temperature", value=f"{max_temp} °C" if max_temp is not None else "N/A")
with row1[2]: 
    st.metric(label="Minimum temperature", value=f"{min_temp} °C" if min_temp is not None else "N/A")

# Rain container horizontal
st.subheader(':umbrella_with_rain_drops: Rainfall')
mean_rain, max_rain, min_rain = get_rain_metrics(quarterly_RAIN_df, year_select, quarter_select)
mean_rain = round(mean_rain, 2)

row2 = st.columns(3)
with row2[0]:
    st.metric(label="Average rainfall", value=f"{mean_rain} mm" if mean_rain is not None else "N/A")
with row2[1]:
    st.metric(label="Maximum rainfall", value=f"{max_rain} mm" if max_rain is not None else "N/A")
with row2[2]:
    st.metric(label="Minimum rainfall", value=f"{min_rain} mm" if min_rain is not None else "N/A")


st.subheader('Daily means of all AQI parameters during selected quarter')
selected_quarter_data = get_selected_quarter_data(main_df, year_select, quarter_select)
st.write(selected_quarter_data)

# Untuk menampilkan line chart berdasarkan quarter yang terpilih dan parameter AQI yang terpilih
st.subheader('Line chart of selected AQI parameters during selected quarter')
st.text('Data points are based on daily means of AQI parameters throughout the chosen quarter')
st.write(':grey_question: Empty line chart means no parameters have been chosen')
st.write('X:Axis : Days throughout chosen quarter')
st.write('Y-Axis : Daily mean value of selected AQI parameter)')
selected_options_names = [option for option, selected in zip(options, selected_options) if selected]
selected_quarter_data_selected_options = selected_quarter_data[selected_options_names]
st.line_chart(selected_quarter_data_selected_options)

# --------------------- MAIN PAGE --------------------- #

st.caption('Made by Salma Nadhira Danuningrat for Bangkit ML 2024')




    


    


