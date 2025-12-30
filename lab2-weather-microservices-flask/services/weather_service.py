import os
from flask import Flask, request, jsonify
from multiprocessing import Process, Queue
from utils.weather_providers import openweather, mock_provider


app = Flask(__name__)

def fetch_weather(queue, source, func, *args):
    try:
        data = func(*args)
        queue.put((source, data))
    except Exception:
        queue.put((source, None))

@app.route("/weather")
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "city is required"}), 400

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return jsonify({"error": "API key not configured"}), 500
    
    queue = Queue()

    processes = [
        Process(
            target=fetch_weather,
            args=(queue, "openweather", openweather, city, api_key)
        ),
        Process(
            target=fetch_weather,
            args=(queue, "mock", mock_provider, city)
        )
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
    
    results = {}
    
    while not queue.empty():
        source, data = queue.get()
        results[source] = data

    if results.get("openweather"):
        return jsonify(results["openweather"])
    if results.get("mock"):
        return jsonify(results["mock"])
    
    return jsonify({"error": "all providers failed"}), 503