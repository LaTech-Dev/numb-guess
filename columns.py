import streamlit as st
#from streamlit_pdf_viewer import pdf_viewer
import time
import requests
#import base64
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

#------------------------------
# GLOBAL VARIABLES
#------------------------------
Version = '3/12 09.47'
x = datetime.now(ZoneInfo("America/Chicago"))
st.set_page_config(
    page_title="4 Column Page",
    page_icon="🌤️",
    layout="wide"
)

# -------------------------------
# HEADER /DEFINE COLUMNS /COLUMN 1
# -------------------------------
def before_call():

    col1, col2, col3, col4 = st.columns([3,3,3,3])

    col1.markdown("##### This is a Header ")
    col1.markdown(f"Version {Version}")
    col1.markdown("Here :red[**red**] is some **bold** text and some *italics* text.")
    col1.markdown("---")

    col1.markdown("ISO format")
    col1.markdown(x.isoformat())
    col1.markdown(x)
    col1.markdown(x.year)

    col1.markdown(x.strftime("%B %d,%Y"))
    col1.markdown(x.strftime("%I:%M:%S %p"))

    #col1.markdown("You can even add a horizontal rule below \n\n ---")
    col1.markdown(" \n\n ---")
    col1.markdown("Above is one way for horizontal rule below another")
    col1.divider()

    col1.markdown(":red[This text is red!]")
    col1.markdown(":yellow[This text is yellow!]")
    col1.markdown(":green[This text is green!]")
    col1.markdown(":blue[This text is blue!]")

    return col1, col2, col3, col4

#-----------------------------------
#NUMBER OF TIMES CALLED WEATHER DATA
#-----------------------------------
def increment_counter():
    try:
        with open("weather_counter.txt", "r") as f:
            count = int(f.read())
    except (FileNotFoundError, ValueError):
        count = 0

    count += 1

    with open("weather_counter.txt","w") as f:
        f.write(str(count))

    return count

# -------------------------------
# WEATHER FUNCTION (CACHED)
# -------------------------------
@st.cache_data(ttl=10)
def get_weather(city, api_key):
    st.session_state.w_call_count = increment_counter()

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=imperial"
    )

    r = requests.get(url, timeout=5)
    r.raise_for_status()

    return r.json()

# -------------------------------
# WEATHER PARSER/SETUP PRINTING
# -------------------------------
def parse_weather(data):

    w_time = datetime.fromtimestamp(
        data["dt"] + data["timezone"],
        tz=timezone.utc
    )

    w_time = w_time.strftime("%Y-%m-%d %I:%M:%S %p")

    return {
        "time": w_time,
        "temp": data["main"]["temp"],
        "clouds": data["clouds"]["all"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "wind_dir": data["wind"].get("deg", "N/A"),
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
    }


#-----------------------------
# MAIN AREA
#-----------------------------
col1, col2, col3, col4 = before_call()

# -------------------------------
# SESSION STATE COUNTER
# -------------------------------
st.session_state.w_call_count = 10

# -------------------------------
# TIME
# -------------------------------

# -------------------------------
# WEATHER DEFAULTS
# -------------------------------
weather: dict | None = None

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
# PHOTO ACQUIRE
# -------------------------------
if "photo" not in st.session_state:
    st.session_state["photo"] = "not done"


def change_photo_state():
    st.session_state["photo"] = "done"


uploaded_file = col2.file_uploader(
    "Upload a TXT or PDF file",
    type=["txt", "pdf"]
)

#camera_photo = col2.camera_input(
#    "Take a photo",
#    on_change=change_photo_state
#)

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
col3.text("Weather Data From openweathermap.org")

col3.markdown(
    f"Call Number: {st.session_state.w_call_count} Times"
)

if weather is not None:

    col3.markdown(f"""
    **Weather in {CITY}**

    Time: {weather['time']}

    Temperature: {weather['temp']} °F  
    Humidity: {weather['humidity']} %  
    Cloud Cover: {weather['clouds']} %  

    Wind Speed: {weather['wind_speed']} MPH  
    Wind Direction: {weather['wind_dir']} °  

    Latitude: {weather['lat']}  
    Longitude: {weather['lon']}
    """)

# -------------------------------
# COLUMN 4 DISPLAY
# -------------------------------
col4.markdown(
    "this is the fourth column 12345 67890 "
    "12345 67890 12345 67890"
)

#-----------------------------
# BELOW THE COLUMNS DISPLAY
#-----------------------------

md3 = st.text_area("Enter in Column 3! :balloon:")
md4 = st.text_area("Enter in Column 4! :balloon:")

col3.write(md3)
col4.markdown(md4)

# -------------------------------
# EXPANDER CAN ADD INFORMATION
# AND A FILE BELOW THE COLUMNS
# -------------------------------

with st.expander("Click to read more"):

    if uploaded_file is not None:

        if uploaded_file.type == "application/pdf":

            st.pdf(uploaded_file)

        elif uploaded_file.type == "text/plain":

            file_contents = uploaded_file.read().decode("utf-8")
            st.text_area("Text File Contents", file_contents, height=300)