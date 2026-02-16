import streamlit as st
import random

st.set_page_config(page_title="Guess a Number", page_icon="🎯")

st.title("🎯 Guess the Number")

# -----------------------
# Initialize Session State
# -----------------------
def initialize_game():
    st.session_state.secret = random.randint(1, 100)
    st.session_state.tries = 0
    st.session_state.game_over = False
    st.session_state.last_low = 0
    st.session_state.last_high = 101
    st.session_state.message = ""

if "secret" not in st.session_state:
    initialize_game()

# -----------------------
# Compute Guess Range
# -----------------------
min_guess = st.session_state.last_low + 1
max_guess = st.session_state.last_high - 1

# -----------------------
# Layout Containers (Prevents Jumping)
# -----------------------
input_container = st.container()
feedback_container = st.container()
status_container = st.container()

# -----------------------
# INPUT SECTION
# -----------------------
with input_container:
    #st.write(f"Guess a number between **{min_guess}** and **{max_guess}**")

    if not st.session_state.game_over and min_guess <= max_guess:
        with st.form("guess_form", clear_on_submit=True):
            guess_input = st.text_input("Enter Your Guess")
            submitted = st.form_submit_button("Submit")

        if submitted:
            if guess_input.isdigit():
                guess = int(guess_input)

                if guess < min_guess or guess > max_guess:
                    st.session_state.message = f"⚠️ Enter a number between {min_guess} and {max_guess}"
                else:
                    st.session_state.tries += 1

                    if guess > st.session_state.secret:
                        st.session_state.message = "📈 Too High!"
                        st.session_state.last_high = min(st.session_state.last_high, guess)

                    elif guess < st.session_state.secret:
                        st.session_state.message = "📉 Too Low!"
                        st.session_state.last_low = max(st.session_state.last_low, guess)

                    else:
                        st.session_state.message = (
                            f"🎉 You got it in {st.session_state.tries} tries!\n"
                            f"The number was {st.session_state.secret}"
                        )
                        st.session_state.game_over = True
                        st.balloons()
            else:
                st.session_state.message = "⚠️ Please enter a valid number"

# -----------------------
# FEEDBACK SECTION
# -----------------------
with feedback_container:
    if st.session_state.message:
        if st.session_state.game_over:
            st.success(st.session_state.message)
        elif "High" in st.session_state.message:
            st.write(st.session_state.message)
            st.write(f"Guess a number between **{min_guess}** and **{guess - 1}**")
        elif "Low" in st.session_state.message:
            st.write(st.session_state.message)
            st.write(f"Guess a number between **{guess + 1}** and **{max_guess}**")
        else:
            st.info(st.session_state.message)

# -----------------------
# STATUS PANEL (Always Visible)
# -----------------------
with status_container:
    st.divider()
    st.subheader("Game Status")
    st.write(f"📉 Closest LOW guess: {st.session_state.last_low}")
    st.write(f"📈 Closest HIGH guess: {st.session_state.last_high}")
    st.write(f"🎯 Tries: {st.session_state.tries}")
    st.divider()

# -----------------------
# RESTART BUTTON
# -----------------------
if st.session_state.game_over:
    if st.button("Play Again"):
        initialize_game()
        st.rerun()
