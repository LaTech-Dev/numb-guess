import streamlit as st
import time
import requests
from datetime import datetime, timezone, timedelta
#from datetime import datetime, timezone
from zoneinfo import ZoneInfo
st.set_page_config(
    page_title="4 Column Page",      # This goes in the browser tab
    page_icon="🌤️",                  # This is the "favicon" in the tab
    layout="wide"                    # Optional: uses the full screen width
)

# -------------------------------
# TIME
# -------------------------------
x = datetime.now(ZoneInfo("America/Chicago"))

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
weather: dict | None = None

# -------------------------------
# OPENWEATHER CONFIG
# -------------------------------
CITY = "Addicks"
API_KEY = st.secrets["OPENWEATHER_KEY"]

# -------------------------------
# HEADER / COLUMNS
# -------------------------------
def before_call():
    col1, col2, col3, col4 = st.columns([3,3,3,3])

    col1.markdown("#### This is a Header \nversion 3/9.18:50")
    col1.markdown("Here :red[**red**] is some **bold** text and some *italics* text.")
    col1.markdown("---")
    col1.markdown("ISO format")
    col1.markdown(x.isoformat())
    col1.markdown(x)
    col1.markdown(x.year)
    col1.markdown(x.strftime("%B %d,%Y"))
    col1.markdown(x.strftime("%I:%M:%S %p"))
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
    wtime = datetime.fromtimestamp(data["dt"] + data["timezone"], tz=timezone.utc
    )
    wtime = wtime.strftime("%Y-%m-%d %I:%M:%S %p")

    return {
        "time": wtime,
        "temp": data["main"]["temp"],
        #"temp_max": data["main"]["temp_max"],
        #"temp_min": data["main"]["temp_min"],
        "clouds": data["clouds"]["all"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "wind_dir": data["wind"].get("deg", "N/A"),
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
    }




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

    col3.text("Weather Data From openweathermap.org")
    if weather is not None:
        col3.markdown(f"Weather Time in {CITY}")
        col3.markdown(f"###### {weather['time']}")
        col3.markdown(f"Temperature: {weather['temp']} °F")
        col3.markdown(f"Humidity: {weather['humidity']} %")
        col3.markdown(f"Cloud Cover: {weather['clouds']} %")
        col3.markdown(f"Wind Speed: {weather['wind_speed']} MPH")
        col3.markdown(f"Wind Direction: {weather['wind_dir']} °")
        col3.markdown(f"Latitude: {weather['lat']}")
        col3.markdown(f"Longitude: {weather['lon']}")

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