import streamlit as st
import time
import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

#------------------------------
# GLOBAL VARIABLES
#------------------------------
Version = '3/13 15.20'
x = datetime.now(ZoneInfo("America/Chicago"))
st.set_page_config(
    page_title="4 Column Page",
    page_icon="🌤️",
    layout="wide"
)

# -------------------------------
# HEADER /DEFINE COLUMNS /COLUMN 1
# COLUMN1 USES A DIFFERENT NAME
# INSIDE THE FUNCTION
# THAN OUTSIDE
# -------------------------------
def before_call():

    cl1, cl2, cl3, cl4 = st.columns([3,3,3,3])


    return cl1, cl2, cl3, cl4

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
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "wind_dir": data["wind"].get("deg", "N/A"),
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
    }


#-----------------------------
# MAIN AREA
#-----------------------------
col1, col2, col3, col4 = before_call()

#-----------------------------
# COLUMN 1 LOAD
#-----------------------------
col1.markdown("##### This is a Header ")
col1.markdown(f"Version {Version}")
col1.markdown("Here :red[**red**] is some **bold** text and some *italics* text.")
col1.markdown("---")

col1.markdown("ISO format")
col1.markdown(x.isoformat())
col1.markdown(x)
col1.markdown(x.year)
# required to get spaces into date
formated_date = x.strftime("%A,   %B %d,  %Y")
# anything but text removes spaces
col1.text(formated_date)
# a better way to display is with .code
col1.code(x.strftime("%A,    %B %d,  %Y"))

col1.markdown(x.strftime("%I:%M:%S %p"))

# col1.markdown("You can even add a horizontal rule below \n\n ---")
col1.markdown(" \n\n ---")
col1.markdown("Above is one way for horizontal rule below is another")
col1.divider()

col1.markdown(":red[This text is red!]")
col1.markdown(":yellow[This text is yellow!]")
col1.markdown(":green[This text is green!]")
col1.markdown(":blue[This text is blue!]")

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


# -------------------------------
# WEATHER DISPLAY IN COLUMN 3
# -------------------------------
col3.text("Weather Data From openweathermap.org")

col3.markdown(
    f"Call Number: {st.session_state.w_call_count} Times"
)

if weather is not None:
    pressure_hpa = float(weather.get("pressure", 0))
    pressure_in_hg = round(pressure_hpa * 0.02953, 2)
    col3.markdown(f"""
    **Weather in {CITY}**

    Time: {weather['time']}

    Temperature: {weather['temp']} °F  
    Humidity: {weather['humidity']} %  
    Cloud Cover: {weather['clouds']} % 
     
    Pressure: {weather['pressure']} hPa  
    Pressure (inHg): {pressure_in_hg} inHg 
     
    Wind Speed: {weather['wind_speed']} MPH  
    Wind Direction: {weather['wind_dir']} °  

    Latitude: {weather['lat']}  
    Longitude: {weather['lon']}
    """)

# -------------------------------
# COLUMN 4 LOAD
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

#frame_height = st.slider("Adjust PDF Viewer Height", 200, 1000, 600)

