from flask import Flask, request, jsonify
from flask_cors import CORS
from core_functions import (
    tell_time, calculate_expression, set_reminder,
    search_web, chat_response, get_weather, open_browser
)
from nlp_processor import get_intent
from reminder_manager import init_db, check_due_reminders

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
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

    return jsonify({"response": response})

@app.route("/due_reminders", methods=["GET"])
def due_reminders():
    due = check_due_reminders()
    return jsonify({"reminders": due})

if __name__ == "__main__":
    app.run(debug=True)
