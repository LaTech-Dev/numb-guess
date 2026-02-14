import streamlit as st
import random

st.title("🎯 Guess the Number")

# -----------------------
# Initialize Session State
# -----------------------
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(1, 100)
    st.session_state.tries = 0
    st.session_state.game_over = False
    st.session_state.last_low = 0
    st.session_state.last_high = 101

# -----------------------
# Determine Valid Guess Range
# -----------------------
min_guess = st.session_state.last_low + 1
max_guess = st.session_state.last_high - 1

st.write(f"Guess a number between **{min_guess}** and **{max_guess}**")

# -----------------------
# Only show input if game is not over
# -----------------------
if not st.session_state.game_over and min_guess <= max_guess:

    with st.form("guess_form", clear_on_submit=True):
        guess_input = st.text_input("Enter Your Guess")  # starts blank
        submitted = st.form_submit_button("Submit")

    if submitted:
        # Validate input
        if guess_input.isdigit():
            guess = int(guess_input)

            # Check bounds
            if guess < min_guess or guess > max_guess:
                st.warning(f"Please enter a number between {min_guess} and {max_guess}")
            else:
                st.session_state.tries += 1

                if guess > st.session_state.secret:
                    st.warning("Too High!")
                    if st.session_state.last_low < guess < st.session_state.last_high:
                        st.session_state.last_high = guess


                elif guess < st.session_state.secret:
                    st.warning("Too Low!")
                    if st.session_state.last_low < guess < st.session_state.last_high:
                        st.session_state.last_low = guess

                else:
                    st.balloons()
                    st.success(f"🎉 You got it in {st.session_state.tries} tries!")
                    st.success(f"The number was  {st.session_state.secret}")
                    st.session_state.game_over = True
                st.code(f"************************")
                st.write(f"📉 ***Closest LOW guess: {st.session_state.last_low}")
                st.text(f"📈 +++Closest HIGH guess: {st.session_state.last_high}")
                st.code(f"************************")
                st.write(f"Tries: {st.session_state.tries}")

        else:
            st.warning("Please enter a valid number")

# -----------------------
# Restart Button
# -----------------------
if st.session_state.game_over:
    if st.button("Play Again"):
        for key in ["secret", "tries", "last_high", "last_low", "game_over"]:
            del st.session_state[key]
        st.rerun()
