# 以下を「app.py」に書き込み
import streamlit as st
import folium
from streamlit_folium import folium_static
import datetime
import nasa_keys
import requests
import pandas as pd 

def get_todays_photo():
    url = "https://api.nasa.gov/planetary/apod"
    params = {
              "api_key": st.secrets.NASAAIAPI.nasa_api_key,  # NASA APIキーを設定
              }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("データの取得に失敗しました")
        return None

def get_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latitude = data['iss_position']['latitude']
        longitude = data['iss_position']['longitude']
        return latitude, longitude
    else:
        st.error("データの取得に失敗しました")
        return None

def AreaMarker(df,m):
    for index, r in df.iterrows(): 

        # ピンをおく
        folium.Marker(
            location=[r.x, r.y],
            popup=index,
        ).add_to(m)

st.title("ISS Tracker")
st.subheader("現在のISSの位置情報を表示します")

# todays photo
st.sidebar.header(datetime.date.today())
st.sidebar.subheader('今日の写真')
todays_photo = get_todays_photo()
url = todays_photo['url']
exp = todays_photo['explanation']
st.sidebar.image(url, caption=exp,use_column_width=True)

# ISS location
iss_location = get_iss_location()
latitude = iss_location[0]
longitude = iss_location[1]

iss = pd.DataFrame(
    [[latitude, longitude]],
    columns=["x","y"])
m = folium.Map(location=[latitude,longitude], zoom_start=5) # 地図の初期設定
AreaMarker(iss,m) # データを地図渡す
folium_static(m) # 地図情報を表示
