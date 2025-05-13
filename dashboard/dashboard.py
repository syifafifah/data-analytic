import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# helper function untuk dataframe
def create_monthly_data_df(df):
    monthly_data_df = df.resample(rule='ME', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    monthly_data_df.index = monthly_data_df.index.strftime('%b %Y')
    # monthly_data_df_ly = monthly_data_df[monthly_data_df['dteday'].str.contains('2012')]
    monthly_data_df_ly = monthly_data_df.reset_index()
    monthly_data_df_ly.rename(columns={
        "dteday": "period",
        "instant": "count_of_rental",
        "cnt": "total_of_sharing_bike"
    }, inplace = True)
    
    return monthly_data_df_ly

def create_season_data_df(df):
    monthly_season_df = df.groupby(['year_month', 'season_name'])['cnt'].sum().reset_index()
    monthly_season_df['year_month'] = monthly_season_df['year_month'].astype(str)

    return monthly_season_df
# end helper

# load cleaned data
all_df = pd.read_csv("https://raw.githubusercontent.com/syifafifah/data-analytic/refs/heads/main/dashboard/data_df.csv")

dteday = ["dteday"]
all_df.sort_values(by="dteday")
all_df.reset_index(inplace=True)

for column in dteday:
    all_df[column] = pd.to_datetime(all_df[column])

# filter feature
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    
    st.text('Filter berdasarkan tanggal sewa')
    
    start_date, end_date = st.date_input(
        label = 'Rentang Waktu',
        min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

    main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# call helper
monthly_data_df = create_monthly_data_df(main_df)
monthly_season_df = create_season_data_df(main_df)

# main view
st.title('Project Analisis Data - Sharing Bike')

with st.container():
    st.subheader("Performa Penyewaan Sepeda")
    
    col1, col2 = st.columns(2)
    with col1:
        total_sharing = monthly_data_df.total_of_sharing_bike.sum()
        st.metric("Total Penyewaan Sepedah", value=total_sharing)
     
    with col2:
        count_day = monthly_data_df.period.nunique()
        st.metric("Jumlah bulan", value=count_day)

    fig, ax = plt.subplots(figsize=(16, 8))
    
    sns.barplot(
        y = "total_of_sharing_bike", 
        x = "period",
        data = monthly_data_df,
        # palette = "pink",
        ax = ax
    )
    ax.set_title("Performa Penyewaan Sepedah", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis = 'x', labelsize = 20, rotation=90)
    ax.tick_params(axis = 'y', labelsize = 15)
    st.pyplot(fig)

    st.subheader("Trend Penyewaan Sepeda Berdasarkan Musim")
    
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.lineplot(
        data = monthly_season_df,
        x = 'year_month',
        y = 'cnt',
        hue = 'season_name',
        marker = 'o'
    )
    
    ax.set_title('Trend Penyewaan Sepeda Berdasarkan Musim (Season)', fontsize=16)
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.tick_params(rotation = 45)
    ax.legend(title = 'Musim')
    ax.grid(True)
    # ax.tight_layout()
    st.pyplot(fig)

st.write("by Syifa Afifah Fitriani")
# end main view
