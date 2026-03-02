import streamlit as st
import time
#import datetime
import requests
from datetime import datetime, timedelta, timezone

st.set_page_config(layout="wide")


x = datetime.now()
temp = 0
cloud_cover = 0
humidity = 0
wind_speed = 0
wind_direction = 0
coord_lat = 0
coord_long = 0
forcast_time = 0

#API_KEY = "3aee7873828cf0017c7f865836a4dd49"
CITY = "Addicks"
url = f"https://wttr.in/{CITY}?format=j1"
#url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=imperial"

response = requests.get(url)
data = response.json()

if response.status_code == 200:
    wtime = data["current_condition"][0]["localObsDateTime"]
    temp = data["current_condition"][0]["temp_F"]
    cloudcover = data["current_condition"][0]["cloudcover"]
    humidity = data["current_condition"][0]["humidity"]
    wind_dir = data["current_condition"][0]["winddir16Point"]
    wind_speed = data["current_condition"][0]["windspeedMiles"]
    latitude = data["nearest_area"][0]["latitude"]
    longitude = data["nearest_area"][0]["longitude"]
else:
    st.error("Failed to fetch weather data. Please check API and city")
    local_dt = None

if "photo" not in st.session_state:
    st.session_state ["photo"]="not done"
    #st.session_state["photo"] = "done"

col1, col2, col3, col4 = st.columns([1,1,1,1])


col1.markdown("# This is a Header")
col1.markdown("Here :red[**red**] is some **bold** text and some *italics* text.")
col1.markdown("---")
col1.markdown('ISO format')
col1.markdown(x.isoformat())
col1.markdown(x.year)
col1.markdown(x.strftime("%B %d,%Y"))
col1.markdown(x.strftime("%H:%M:%S"))
col1.markdown("You can even add a horizontal rule below \n\n---")
col1.markdown(":red[latest streamlit method below and it should be used]")
col1.divider()
col1.markdown(":red[This text is red!]")
col1.markdown(":yellow[This text is yellow!]")
col1.markdown(":green[This text is green!]")
col1.markdown(":blue[This text is blue!]")


def change_photo_state():
    st.session_state["photo"]="done"

uploaded_photo = col2.file_uploader("Upload a photo", on_change=change_photo_state)
camera_photo = col2.camera_input("Take a photo", on_change=change_photo_state)

if st.session_state["photo"] == "done":
    progress_bar = col2.progress (0)

    for perc_completed in range (100):
        time.sleep (0.005)
        progress_bar.progress(perc_completed+1)

    col2.success ("Photo uploaded successfully!")
    col3.metric(label=f"Weather Time in {CITY}", value=f"{wtime} ")
    col3.metric(label=f"Temperature is ", value=f"{temp} °F")
    col3.metric(label=f"Cloud Cover is", value=f"{cloudcover} %")
    col3.metric(label=f"Humidity is", value=f"{humidity} %")
    col3.metric(label=f"Wind Speed is ", value=f"{wind_speed} MPH")
    col3.metric(label=f"Wind Direction is", value=f"{wind_dir} ")
    col3.metric(label=f"Latitude is", value=f"{latitude}  °")
    col3.metric(label=f"longitude is ", value=f"{longitude} °")

    md3 = st.text_area("Enter in Column 3! :balloon:")
    #md = st.text_area('Type in your markdown string (without outer quotes)',
    #                  "Happy Streamlit-ing! :balloon:")
    md4 = st.text_area("Enter in Column 4! :balloon:")

    #col3.code(f"""col3.markdown('''{md}''')""")

    col3.markdown(md3)

    col4.markdown("this is the fourth column")
    col4.markdown(md4)
    with (st.expander("Click to read more")):
        st.write("Hello! Here are more details on this topic that you were interested in.")

        if uploaded_photo is None:
          st.image(camera_photo)
          #col4.image(camera_photo)
        else:
            st.image(uploaded_photo)
            #col4.image(uploaded_photo)