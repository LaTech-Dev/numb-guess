import streamlit as st
import time
import requests
from datetime import datetime, timezone, timedelta

st.set_page_config(layout="wide")

# -------------------------------
# TIME
# -------------------------------
x = datetime.now()

# -------------------------------
# WEATHER DEFAULTS
# -------------------------------
temp = 0
cloud_cover = 0
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
    col1, col2, col3, col4 = st.columns([3,3,3,3])

    col1.markdown("# This is a Header version 3/5")
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
# WEATHER FUNCTION (CACHED)
# -------------------------------
@st.cache_data(ttl=300)
def get_weather(city, api_key):

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=imperial"
    )

    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()


# -------------------------------
# WEATHER PARSER
# -------------------------------
def parse_weather(data):

    api_dt = data["dt"]
    tz_offset = data["timezone"]

    utc_time = datetime.fromtimestamp(api_dt, tz=timezone.utc)
    local_time = utc_time + timedelta(seconds=tz_offset)

    return {
        "time": local_time.strftime("%Y-%m-%d %I:%M:%S %p"),
        "temp": data["main"]["temp"],
        "clouds": data["clouds"]["all"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "wind_dir": data["wind"].get("deg", "N/A"),
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
    }


# -------------------------------
# OPENWEATHER CONFIG
# -------------------------------
CITY = "Addicks"
API_KEY = st.secrets["OPENWEATHER_KEY"]

# -------------------------------
# FETCH WEATHER
# -------------------------------
try:
    raw_weather = get_weather(CITY, API_KEY)
    weather = parse_weather(raw_weather)

except Exception as e:
    st.warning(f"Weather service temporarily unavailable: {e}")
    weather = None


# -------------------------------
# SESSION STATE
# -------------------------------
if "photo" not in st.session_state:
    st.session_state["photo"] = "not done"


def change_photo_state():
    st.session_state["photo"] = "done"


# simulate upload trigger
change_photo_state()

# -------------------------------
# AFTER PHOTO UPLOAD
# -------------------------------
if st.session_state["photo"] == "done":

    progress_bar = col2.progress(0)

    for perc_completed in range(100):
        time.sleep(0.0005)
        progress_bar.progress(perc_completed + 1)

    col2.success("Photo uploaded successfully!")

    # -------------------------------
    # WEATHER DISPLAY
    # -------------------------------
    if weather:

        col3.text("Weather Data From openweathermap.org")

        col3.metric(f"Weather Time in {CITY}", weather["time"])
        col3.metric("Temperature", f'{weather["temp"]} °F')
        col3.metric("Cloud Cover", f'{weather["clouds"]} %')
        col3.metric("Humidity", f'{weather["humidity"]} %')
        col3.metric("Wind Speed", f'{weather["wind_speed"]} MPH')
        col3.metric("Wind Direction", f'{weather["wind_dir"]} °')
        col3.metric("Latitude", weather["lat"])
        col3.metric("Longitude", weather["lon"])

    # -------------------------------
    # TEXT INPUT
    # -------------------------------
    md3 = st.text_area("Enter in Column 3! :balloon:")
    md4 = st.text_area("Enter in Column 4! :balloon:")

    col3.markdown(md3)

    col4.markdown(
        "this is the fourth column 12345 67890 12345 67890 "
        "12345 67890 12345 67890"
    )
    col4.markdown(md4)

    # -------------------------------
    # EXPANDER
    # -------------------------------
    with st.expander("Click to read more"):
        st.write(
            "Hello! Here are more details on this topic that you were interested in."
        )