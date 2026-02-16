import streamlit as st
import time

def get_data(user_text, slider_value):
    # Replace single newlines with Markdown-friendly line breaks
    formatted_text = user_text.replace("\n", "  \n")
    for char in formatted_text:
        yield char
        time.sleep(slider_value)

# Keyboard input: st.text_area allows multi-line input
user_input = st.text_area("Type your message here (Press Enter for new lines):", " ")

slider_value = st.slider("Typing Speed", 0.0, 0.2, value=0.05, step=0.01)

if st.button("Stream My Text"):
    # st.write_stream will process the generator char by char
    st.write_stream(get_data(user_input, slider_value))
