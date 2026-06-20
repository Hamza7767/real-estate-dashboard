from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Mock database jo har shehar ke mutabik dynamic areas ka data return karega
PROPERTY_DATABASE = {
    "islamabad": {
        "DHA Phase 2": 32.5,
        "G-11 Sector": 28.2,
        "E-11 Sector": 25.4,
        "Bahria Town": 19.8,
        "Bani Gala": 14.2
    },
    "lahore": {
        "DHA Phase 6": 45.0,
        "Johar Town": 26.5,
        "Gulberg III": 38.2,
        "Bahria Orchard": 12.4,
        "Wapda Town": 21.0
    },
    "karachi": {
        "Clifton": 55.2,
        "DHA Phase 8": 62.0,
        "Gulshan-e-Iqbal": 18.5,
        "North Nazimabad": 14.8,
        "Malir Cantt": 28.0
    }
}

def scrape_backup_logic(city):
    # Agar user koi aisa shehar search kare jo list mein nahi hai, to standard response
    url = f"https://www.zameen.com/Homes/{city.capitalize()}-3-1.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        # Background scraping call (for backend activity log check)
        requests.get(url, headers=headers, timeout=3)
    except:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/properties')
def properties_api():
    # Frontend se user ka search input nikalna (e.g., /api/properties?city=lahore)
    user_city = request.args.get('city', 'islamabad').lower().strip()
    
    # Back-end scraping simulation trigger karna
    scrape_backup_logic(user_city)
    
    # Agar data database mein mautood hai to woh bhejein, nahi to Islamabad ka data fallback
    if user_city in PROPERTY_DATABASE:
        data = PROPERTY_DATABASE[user_city]
    else:
        # Generic query simulation dynamic rates ke sath
        data = {
            f"{user_city.capitalize()} Area A": 22.5,
            f"{user_city.capitalize()} Area B": 17.1,
            f"{user_city.capitalize()} Center": 29.4,
            f"{user_city.capitalize()} Suburbs": 11.2
        }
        
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=8500)