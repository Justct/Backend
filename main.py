from flask import Flask, request, jsonify, escape
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app)
limiter = Limiter(app, key_func=get_remote_address)

# Load rooms data from "rooms.json" file
with open("rooms.json") as f:
    rooms = json.load(f)

# Set the rate limit for API endpoints
rate_limit = "100/hour"  # Adjust as per your requirements

@app.route("/ggg")
def pring():
  print("PING PONG")
  return "Kwell"

@app.route("/find/<string:room>")
def find_room_url(room):
  name_to_url = {item["name"]: item["api_url"] for item in rooms}

  return name_to_url[room]
  
@app.route("/get/<int:page>/<int:results_per_page>")
@limiter.limit(rate_limit)
def get_rooms(page, results_per_page):
    start_index = (page - 1) * results_per_page
    end_index = start_index + results_per_page

    # Return rooms based on pagination
    return jsonify(rooms[start_index:end_index])


@app.route("/search/<string:search_query>")
@limiter.limit(rate_limit)
def search_rooms(search_query):
    results = []
    for room in rooms:
        if search_query.lower() in room['name'].lower() or search_query.lower() in room['description'].lower():
            results.append(room)

    # Return search results
    return jsonify(results)


@app.route("/new", methods=["POST"])
@limiter.limit(rate_limit)
def create_room():
    name = escape(request.headers.get('name'))
    description = escape(request.headers.get('description'))
    api_url = escape(request.headers.get('url'))

    # Check if room already exists
    for room in rooms:
        if room['name'] == name and room['description'] == description and room['api_url'] == api_url:
            return "x"  # Room already exists

    # Check if the API URL is valid and accessible
    try:
        
      response = requests.get(api_url)

    except:
      return "n"

    try:
      if api_url.endswith("/"):
        api_ = api_url + "verify/if/it/a/chat/room/of/just/chat"
      else:
        api_ = api_url + "/verify/if/it/a/chat/room/of/just/chat"
        
      res = requests.get(api_).text
      if res == name:
        pass      
      else:
        return "n"
    except:
      return "n"
    # Create a new room
    new_room = {"name": name, "description": description, "api_url": api_url}
    rooms.append(new_room)
    
    # Save the updated rooms data back to "rooms.json" file
    with open("rooms.json", "w") as f:
        json.dump(rooms, f)
      
    requests.get(api_)
  
    return "s"  # Room created successfully


if __name__ == "__main__":
    app.run("0.0.0.0")
