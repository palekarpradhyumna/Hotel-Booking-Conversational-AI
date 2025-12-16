from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

HOTEL_DATA = [
    {
        "city": "Pune",
        "name": "Pune Grand Hotel",
        "hotel_id": "H-PUN-101",
        "rooms": [
            {
                "type": "Standard",
                "price": 3000,
                "availability": [
                    {"from": "2025-11-20", "to": "2025-11-30"},
                    {"from": "2025-12-10", "to": "2025-12-20"}
                ]
            },
            {
                "type": "Deluxe",
                "price": 4500,
                "availability": [
                    {"from": "2025-11-18", "to": "2025-11-25"},
                    {"from": "2025-12-01", "to": "2025-12-10"}
                ]
            }
        ]
    },{
        "city": "Pune",
        "name": " SunRise Hotel",
        "hotel_id": "H-PUN-122",
        "rooms": [
            {
                "type": "Standard",
                "price": 3000,
                "availability": [
                    {"from": "2025-11-20", "to": "2025-11-30"},
                    {"from": "2025-12-10", "to": "2025-12-20"}
                ]
            },
            {
                "type": "Deluxe",
                "price": 4500,
                "availability": [
                    {"from": "2025-11-18", "to": "2025-11-25"},
                    {"from": "2025-12-01", "to": "2025-12-10"}
                ]
            }
        ]
    },
    {
        "city": "Nagpur",
        "name": "Nagpur Comfort Stay",
        "hotel_id": "H-NGP-202",
        "rooms": [
            {
                "type": "Standard",
                "price": 2500,
                "availability": [
                    {"from": "2025-11-21", "to": "2025-11-29"},
                    {"from": "2025-12-03", "to": "2025-12-15"}
                ]
            },
            {
                "type": "Suite",
                "price": 5500,
                "availability": [
                    {"from": "2025-11-20", "to": "2025-11-26"},
                    {"from": "2025-12-05", "to": "2025-12-25"}
                ]
            }
        ]
    },
    {
        "city": "Mumbai",
        "name": "Mumbai Seaside View",
        "hotel_id": "H-MUM-303",
        "rooms": [
            {
                "type": "Deluxe",
                "price": 7000,
                "availability": [
                    {"from": "2025-11-19", "to": "2025-11-28"},
                    {"from": "2025-12-08", "to": "2025-12-20"}
                ]
            },
            {
                "type": "Suite",
                "price": 12000,
                "availability": [
                    {"from": "2025-11-22", "to": "2025-11-30"},
                    {"from": "2025-12-12", "to": "2025-12-25"}
                ]
            }
        ]
    }
]


def date_in_range(check_in, check_out, availability):
    """
    Return True if room availability supports requested dates
    """
    check_in_dt = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_dt = datetime.strptime(check_out, "%Y-%m-%d")

    for slot in availability:
        start = datetime.strptime(slot["from"], "%Y-%m-%d")
        end = datetime.strptime(slot["to"], "%Y-%m-%d")

        if start <= check_in_dt and check_out_dt <= end:
            return True

    return False


@app.route("/searchHotels", methods=["POST"])
def search_hotels():
    data = request.get_json()

    city = data.get("city")
    room_type = data.get("room_type")
    budget = data.get("budget")
    check_in = data.get("check_in")
    check_out = data.get("check_out")

    results = []

    for hotel in HOTEL_DATA:
        if hotel["city"].lower() == city.lower():
            for room in hotel["rooms"]:
                if room["type"].lower() == room_type.lower() and room["price"] <= budget:
                    if date_in_range(check_in, check_out, room["availability"]):
                        results.append({
                            "hotel_id": hotel["hotel_id"],
                            "hotel_name": hotel["name"],
                            "city": hotel["city"],
                            "room_type": room_type,
                            "price": f"{room['price']}",
                            "check_in": check_in,
                            "check_out": check_out
                        })

    return jsonify({"hotels": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
