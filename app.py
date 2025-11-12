from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

# --- Configuration ---
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configure your MySQL connection
db_config = {
    'host': 'localhost',
    'user': 'your_mysql_user',        # <-- UPDATE THIS
    'password': 'your_mysql_password',  # <-- UPDATE THIS
    'database': 'event_manager'
}

# --- Database Connection Helper ---
def create_db_connection():
    """Create and return a database connection."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# --- API Routes ---

# 1. GET: Browse all upcoming events
@app.route('/api/events', methods=['GET'])
def get_events():
    conn = create_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events WHERE start_time > NOW() ORDER BY start_time ASC")
    events = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(events)

# 2. GET: View detailed event information
@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    conn = create_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    event = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if event:
        return jsonify(event)
    else:
        return jsonify({'error': 'Event not found'}), 404

# 3. POST: Register for an event
@app.route('/api/register', methods=['POST'])
def register_for_event():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    event_id = data.get('event_id')

    if not all([name, email, event_id]):
        return jsonify({'error': 'Missing required fields (name, email, event_id)'}), 400

    conn = create_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)

    try:
        # Step 1: Find user or create a new one
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            user_id = user['user_id']
        else:
            # Create new user
            cursor.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)",
                           (name, email, phone))
            user_id = cursor.lastrowid

        # Step 2: Register the user for the event
        cursor.execute("INSERT INTO registrations (event_id, user_id) VALUES (%s, %s)",
                       (event_id, user_id))
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful!',
            'user_id': user_id,
            'event_id': event_id
        }), 201

    except mysql.connector.IntegrityError:
        # This triggers if the user is already registered (from UNIQUE KEY)
        return jsonify({'error': 'You are already registered for this event.'}), 409
    except Error as e:
        conn.rollback()
        return jsonify({'error': f'An error occurred: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)