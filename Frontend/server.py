import os
import google.generativeai as genai
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin  # Import cross_origin
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

AI_PROMPT = """
Suggest 5 creative and engaging event ideas for tech professionals.
For each event, provide a catchy name and a one-sentence description.
Format the response as a list.

Example:
- AI & Art Gala: An evening exploring generative AI's impact on digital art.
"""

# --- Set up the Flask server ---
app = Flask(__name__)
# UPDATED: Explicitly allow all origins, including 'null' for local files
CORS(app, resources={r"/get-suggestions": {"origins": "*"}})

# --- AI Generation Function ---
def get_ai_suggestions():
    """Calls the Gemini API to get event suggestions."""
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(AI_PROMPT)
        return response.text
    except Exception as e:
        print(f"Error calling Google AI: {e}")
        return "Error: Could not get AI suggestions. Check your API key and server."

# --- API Endpoint ---
@app.route('/get-suggestions', methods=['GET'])
@cross_origin()  # UPDATED: Add this decorator
def suggest_events():
    """This is the URL our JavaScript will call."""
    suggestions = get_ai_suggestions()
    
    # Return the suggestions as JSON
    return jsonify({
        'suggestion': suggestions
    })

# --- Run the Server ---
if __name__ == '__main__':
    print("Starting the AI suggestion server at http://127.0.0.1:5000")
    app.run(port=5000, debug=True)