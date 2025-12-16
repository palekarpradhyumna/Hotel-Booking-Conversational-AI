from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your ngrok / live API URL
HOTEL_API_URL = "https://euphonic-springlike-braxton.ngrok-free.dev/searchHotels"


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    parameters = req.get("queryResult", {}).get("parameters", {})

    city = parameters.get("city")
    room_type = parameters.get("type")  # Entity in Dialogflow named "type"
    budget = parameters.get("budget")
    check_in = parameters.get("check_in")
    check_out = parameters.get("check_out")

    payload = {
        "city": city,
        "room_type": room_type,
        "budget": budget,
        "check_in": check_in,
        "check_out": check_out
    }

    try:
        response = requests.post(HOTEL_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        hotel_data = response.json()

        if hotel_data.get("hotels"):
            first = hotel_data["hotels"][0]

            message = (
                f"Great! I found a hotel in {city} matching your needs:\n\n"
                f"*{first['hotel_name']}*\n"
                f"Room Type: {first['room_type']}\n"
                f" Price: {first['price']} per night\n"
                f" Check-in: {first['check_in']}\n"
                f" Check-out: {first['check_out']}\n\n"
                f"Would you like to proceed with booking?"
            )
        else:
            message = (
                f"Sorry! No available {room_type} rooms in {city} "
                f"within your budget during selected dates."
            )

    except Exception as e:
        message = f"Error connecting to hotel booking service: {str(e)}"

    return jsonify({
        "fulfillmentMessages": [
            {"text": {"text": [message]}}
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
