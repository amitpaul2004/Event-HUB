# TO run this server, use the command:   {    python server.py      }

import os
import google.generativeai as genai
# Import the 'send_from_directory' function
from flask import Flask, jsonify, send_from_directory
from dotenv import load_dotenv

# We no longer need flask_cors!
# from flask_cors import CORS 

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# We will serve files from the current directory ('.')
app = Flask(__name__, static_folder='.', static_url_path='')

AI_PROMPT = """
Suggest 5 creative and engaging event ideas for tech professionals.
For each event, provide a catchy name and a one-sentence description.
Format the response as a list.

Example:
- AI & Art Gala: An evening exploring generative AI's impact on digital art.
"""

def get_ai_suggestions():
    """Calls the Gemini API to get event suggestions."""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(AI_PROMPT)
        return response.text
    except Exception as e:
        print(f"Error calling Google AI: {e}")
        return "Error: Could not get AI suggestions. Check your API key and server."

# --- API Endpoint (Backend) ---
@app.route('/get-suggestions', methods=['GET'])
def suggest_events():
    """This is the URL our JavaScript will call."""
    suggestions = get_ai_suggestions()
    return jsonify({
        'suggestion': suggestions
    })

# --- NEW: Frontend Routes ---

# This route will serve your 'index.html' file
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# This route will automatically serve your 'app.js' and 'style.css'
# (This is handled by the static_folder='.' in the app = Flask(...) line)


# --- Run the Server ---
if __name__ == '__main__':
    # UPDATED: New instructions for you!
    print("=============================================================")
    print("Server is running!")
    print("DO NOT open index.html directly.")
    print("Instead, open this URL in your browser:")
    print("http://127.0.0.1:5000")
    print("=============================================================")
    app.run(port=5000, debug=True)