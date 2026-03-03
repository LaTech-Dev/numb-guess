import streamlit as st
import time
import requests
from datetime import datetime

st.set_page_config(layout="wide")

# -------------------------------
# TIME
# -------------------------------
x = datetime.now()

# -------------------------------
# WEATHER DEFAULTS
# -------------------------------
temp = 0
cloudcover = 0
humidity = 0
wind_speed = 0
wind_dir = 0
latitude = 0
longitude = 0
wtime = "N/A"

# -------------------------------
# HEADER / COLUMNS
# -------------------------------
def before_call():
    col1, col2, col3, col4 = st.columns([1,1,1,1])

    col1.markdown("# This is a Header")
    col1.markdown("Here :red[**red**] is some **bold** text and some *italics* text.")
    col1.markdown("---")
    col1.markdown("ISO format")
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

    return col1, col2, col3, col4


col1, col2, col3, col4 = before_call()

# -------------------------------
# OPENWEATHER CONFIG
# -------------------------------
CITY = "Addicks"
#API_KEY = st.secrets["OPENWEATHER_KEY"]
API_KEY = "3aee7873828cf0017c7f865836a4dd49"

url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={CITY}&appid={API_KEY}&units=imperial"
)

# -------------------------------
# FETCH WEATHER
# -------------------------------
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()

    # Extract OpenWeather fields
    wtime = datetime.fromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M:%S")
    temp = data["main"]["temp"]
    cloudcover = data["clouds"]["all"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    wind_dir = data["wind"].get("deg", "N/A")
    latitude = data["coord"]["lat"]
    longitude = data["coord"]["lon"]

except Exception as e:
    st.warning(f"Weather service temporarily unavailable: {e}")
    data = None

# -------------------------------
# SESSION STATE
# -------------------------------
if "photo" not in st.session_state:
    st.session_state["photo"] = "not done"


def change_photo_state():
    st.session_state["photo"] = "done"


# -------------------------------
# PHOTO INPUT
# -------------------------------
uploaded_photo = col2.file_uploader("Upload a photo", on_change=change_photo_state)
camera_photo = col2.camera_input("Take a photo", on_change=change_photo_state)

# -------------------------------
# AFTER PHOTO UPLOAD
# -------------------------------
if st.session_state["photo"] == "done":

    progress_bar = col2.progress(0)

    for perc_completed in range(100):
        time.sleep(0.005)
        progress_bar.progress(perc_completed + 1)

    col2.success("Photo uploaded successfully!")

    col3.text("Weather Data From openweathermap.org")
    col3.metric(label=f"Weather Time in {CITY}", value=wtime)
    col3.metric(label="Temperature is", value=f"{temp} °F")
    col3.metric(label="Cloud Cover is", value=f"{cloudcover} %")
    col3.metric(label="Humidity is", value=f"{humidity} %")
    col3.metric(label="Wind Speed is", value=f"{wind_speed} MPH")
    col3.metric(label="Wind Direction is", value=f"{wind_dir} °")
    col3.metric(label="Latitude is", value=f"{latitude} °")
    col3.metric(label="Longitude is", value=f"{longitude} °")

    md3 = st.text_area("Enter in Column 3! :balloon:")
    md4 = st.text_area("Enter in Column 4! :balloon:")

    col3.markdown(md3)

    col4.markdown("this is the fourth column")
    col4.markdown(md4)

    with st.expander("Click to read more"):
        st.write("Hello! Here are more details on this topic that you were interested in.")

        if uploaded_photo is None:
            if camera_photo:
                st.image(camera_photo)
        else:
            st.image(uploaded_photo)