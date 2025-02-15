# -*- coding: utf-8 -*-
"""ride_suggestions.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fxSwdo85jl9NVbj-yhtvz8IIauFYZt_N
"""

# Install required libraries
!pip install flask flask-ngrok requests folium

import folium
from flask import Flask, jsonify
from flask_ngrok import run_with_ngrok

# Initialize Flask app
app = Flask(__name__)
run_with_ngrok(app)  # Run Flask with ngrok

# Mock data for women-friendly rideshare services
# In a real-world application, this data would come from APIs or databases
rideshare_services = [
    {"name": "Pink Cabs", "lat": 28.6139, "lon": 77.2090, "contact": "+91-12345-67890"},
    {"name": "SheSafe Rides", "lat": 28.6200, "lon": 77.2300, "contact": "+91-98765-43210"},
    {"name": "LadyLine Taxis", "lat": 28.6300, "lon": 77.2000, "contact": "+91-45678-12345"}
]

# Function to get user location
def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json").json()
        lat, lon = map(float, response["loc"].split(","))
        return lat, lon
    except:
        return None, None

# Route for women-only rideshare services
@app.route("/")
def rideshare_suggestions():
    user_lat, user_lon = get_user_location()

    if user_lat is None or user_lon is None:
        return "Could not determine location. Please check your internet connection."

    # Create map centered on user's location
    map_object = folium.Map(location=[user_lat, user_lon], zoom_start=14)

    # Add user location marker
    folium.Marker(
        [user_lat, user_lon],
        popup="You are here",
        icon=folium.Icon(color="red")
    ).add_to(map_object)

    # Add women-friendly rideshare service markers
    for service in rideshare_services:
        folium.Marker(
            [service["lat"], service["lon"]],
            popup=f"{service['name']}<br>Contact: {service['contact']}",
            icon=folium.Icon(color="pink", icon="car", prefix="fa")
        ).add_to(map_object)

    # Save map as HTML
    map_object.save("rideshare_map.html")

    # Read the HTML file and return it
    with open("rideshare_map.html", "r", encoding="utf-8") as file:
        return file.read()

# Run the Flask app
app.run()

