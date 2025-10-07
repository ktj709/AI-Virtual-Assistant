import datetime, re, requests, os, webbrowser
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
from reminder_manager import add_reminder, check_due_reminders, init_db
from newsapi import NewsApiClient
import os

load_dotenv()  # Load .env variables


def tell_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}"


def calculate_expression(text):
    text = text.lower()
    text = (
        text.replace("plus", "+")
        .replace("add", "+")
        .replace("minus", "-")
        .replace("subtract", "-")
        .replace("times", "*")
        .replace("multiplied by", "*")
        .replace("into", "*")
        .replace("x", "*")
        .replace("divide", "/")
        .replace("divided by", "/")
        .replace("by", "/")
        .replace("over", "/")
    )
    expr = re.findall(r'[\d\.\+\-\*\/\(\)\s]+', text)
    if expr:
        try:
            result = eval("".join(expr))
            return f"The result is {result}"
        except:
            return "Sorry, I couldn't calculate that."
    return "Please provide a valid math expression."


def get_weather(city="Delhi"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Weather API key not found. Please add it to your .env file."

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    data = response.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    city_name = data["name"]
    return f"The weather in {city_name} is {desc} with a temperature of {temp}°C."


def set_reminder(text):
    init_db()
    return add_reminder(text)


def get_due_reminders():
    due = check_due_reminders()
    return "\n".join(due) if due else None


def search_web(query):
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return "News API key not found. Please add it to your .env file."

    newsapi = NewsApiClient(api_key=api_key)
    articles = newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=3)

    if not articles["articles"]:
        return "No news articles found."

    results = []
    for art in articles["articles"]:
        results.append(f"📰 {art['title']}\n🔗 {art['url']}\n")
    return "\n".join(results)



def open_browser():
    webbrowser.open("https://www.google.com", new=2)
    return "Opening Google in your browser."


def chat_response(prompt):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
