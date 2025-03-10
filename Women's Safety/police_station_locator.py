# Install required libraries
!pip install flask flask-ngrok requests folium

import requests
import folium
from flask import Flask, render_template, jsonify
from flask_ngrok import run_with_ngrok

# Initialize Flask app
app = Flask(__name__)
run_with_ngrok(app)  # Run Flask with ngrok

# Function to get user's IP-based location
def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json").json()
        lat, lon = map(float, response["loc"].split(","))
        return lat, lon
    except:
        return None, None

# Function to get nearby police stations using OpenStreetMap (Overpass API)
def get_police_stations(lat, lon, radius=5000):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node["amenity"="police"](around:{radius},{lat},{lon});
    out;
    """
    response = requests.get(overpass_url, params={"data": query})
    data = response.json()

    police_stations = []
    for element in data.get("elements", []):
        if "lat" in element and "lon" in element:
            police_stations.append({
                "name": element.get("tags", {}).get("name", "Unnamed Police Station"),
                "lat": element["lat"],
                "lon": element["lon"]
            })
    return police_stations

# Route for the main page
@app.route("/")
def home():
    user_lat, user_lon = get_user_location()

    if user_lat is None or user_lon is None:
        return "Could not determine location. Please check your internet connection."

    police_stations = get_police_stations(user_lat, user_lon)

    # Create map
    map_object = folium.Map(location=[user_lat, user_lon], zoom_start=14)

    # User Location Marker
    folium.Marker(
        [user_lat, user_lon], popup="You are here", icon=folium.Icon(color="red")
    ).add_to(map_object)

    # Police Stations Markers
    for station in police_stations:
        folium.Marker(
            [station["lat"], station["lon"]],
            popup=station["name"],
            icon=folium.Icon(color="blue")
        ).add_to(map_object)

    # Save map as HTML
    map_object.save("map.html")

    # Read the HTML file and return it
    with open("map.html", "r", encoding="utf-8") as file:
        return file.read()

# Run the Flask app
app.run()

