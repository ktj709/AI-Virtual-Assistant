import streamlit as st
from nlp_processor import get_intent
from core_functions import (
    tell_time,
    calculate_expression,
    set_reminder,
    search_web,
    chat_response,
    get_weather,
    open_browser,
    get_due_reminders
)
from text_to_speech import speak
from speech_to_text import listen
from reminder_manager import check_due_reminders
from reminder_manager import check_due_reminders, init_db


init_db()


st.title("🎙️ Personal Assistant AI Agent")


due = check_due_reminders()
if due:
    for reminder in due:
        st.warning(reminder)
        speak(reminder)

mode = st.radio("Select Input Mode:", ["Text", "Voice"])


if mode == "Text":
    user_input = st.text_input("Enter your command:")
    if st.button("Run"):
        if user_input:
            intent = get_intent(user_input)

            if intent == "time":
                response = tell_time()
            elif intent == "math":
                response = calculate_expression(user_input)
            elif intent == "reminder":
                response = set_reminder(user_input)
            elif intent == "search":
                response = search_web(user_input)
            elif intent == "weather":
                city = user_input.split("in")[-1].strip() if "in" in user_input.lower() else "Delhi"
                response = get_weather(city)
            elif intent == "open_browser":
                response = open_browser()
            else:
                response = chat_response(user_input)

            st.success(response)
            speak(response)


elif mode == "Voice":
    if st.button("Start Listening"):
        st.info("Listening... Speak now.")
        user_input = listen()
        st.write(f"You said: {user_input}")

        intent = get_intent(user_input)

        if intent == "time":
            response = tell_time()
        elif intent == "math":
            response = calculate_expression(user_input)
        elif intent == "reminder":
            response = set_reminder(user_input)
        elif intent == "search":
            response = search_web(user_input)
        elif intent == "weather":
            city = user_input.split("in")[-1].strip() if "in" in user_input.lower() else "Delhi"
            response = get_weather(city)
        elif intent == "open_browser":
            response = open_browser()
        else:
            response = chat_response(user_input)

        st.success(response)
        speak(response)
