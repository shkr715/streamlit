# 以下を「app.py」に書き込み
import streamlit as st
from astropy.cosmology import Planck15 as cosmo
import astropy.units as u
import datetime
import nasa_keys
import requests

def get_todays_photo(date):
    url = "https://api.nasa.gov/planetary/apod"
    params = {
              "api_key": nasa_keys.nasa_api_keys,  # NASA APIキーを設定
              "date": date
              }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("データの取得に失敗しました")
        return None

def get_cosmo_age(redshift):
    st.session_state['cosmo_age'] = cosmo.age(redshift)

st.session_state['cosmo_age'] = 0.0

# calc cosmo age
st.title("宇宙年齢計算")
redshift = st.text_input("redshiftを入力してください")
button = st.button("計算!", on_click=get_cosmo_age(float(redshift)), args=(st.session_state['cosmo_age']))

if button:
    st.write(f'unit : Planck15')
    st.write(f'redshift : {redshift}')
    st.write('宇宙年齢 : {}'.format(st.session_state['cosmo_age']))

# todays photo
#st.header(datetime.date.today())
todays_photo = get_todays_photo(datetime.date.today())
url = todays_photo['url']
exp = todays_photo['explanation']
st.image(url, caption=exp,use_column_width=True)
