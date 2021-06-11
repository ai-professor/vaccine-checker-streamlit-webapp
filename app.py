import streamlit as st
from PIL import Image
from fake_useragent import UserAgent
import requests
import pandas as pd

ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

def run():
    img1 = Image.open('./sources/vac1.jpg')
    img1 = img1.resize((800,400))
    st.image(img1,use_column_width=False)
    st.title("Vaccination Center Checker")

    ## Area Pin
    area_pin = st.text_input('Enter your area Pincode')

    ## Date
    vac_date = st.date_input("Date")


    if st.button("Search"):
        try:
            vac_date = str(vac_date).split('-')
            new_date = vac_date[2]+'-'+vac_date[1]+'-'+vac_date[0]
            response = requests.get(
                f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={area_pin}&date={new_date}",
                headers=header)
            data = response.json()
            centers = pd.DataFrame(data.get('centers'))
            if centers.empty:
                st.warning("No Vaccines are available for "+new_date+' in '+str(area_pin)+' Check Later! or Try Another Centre')
            else:
                session_ids = []
                for j, row in centers.iterrows():
                    session = pd.DataFrame(row['sessions'][0])
                    session['center_id'] = centers.loc[j, 'center_id']
                    session_ids.append(session)

                sessions = pd.concat(session_ids, ignore_index=True)
                av_centeres = centers.merge(sessions, on='center_id')
                av_centeres.drop(columns=['sessions', 'session_id', 'lat', 'block_name', 'long', 'from', 'to'], inplace=True,errors='ignore')
                print(av_centeres)
                st.write(av_centeres)

        except Exception as e:
            st.error("Something went wrong!!")
            print(e)

run()