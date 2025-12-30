from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/recommendation", methods=["POST"])
def recommend():
    data = request.json
    weather = data.get("weather", {}).get("main", "")

    if weather == "Rain":
        rec = "Возьмите зонт"
    elif weather == "Clear":
        rec = "Отличная погода для прогулки"
    else:
        rec = "Погода обычная"
    
    return jsonify({"recommendation": rec})