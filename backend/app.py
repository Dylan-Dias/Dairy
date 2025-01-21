from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import psycopg2
from scheduler import optimize_milking_schedule

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Database connection setup
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="root",
        password="root"
    )
    return conn

@app.route('/api/submit', methods=['POST'])
def submit_cow_data():
    data = request.get_json()
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Iterate through each row and insert the data into the database
    for row in data:
        cur.execute("""
            INSERT INTO "Cowlibrate" (cow_id, milk_yield, time_since_last_milk, daily_feed_quantity, enclosure_temp,
                                    outside_temp, feed_type, bovine_age, health, lactation_stage, breed, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row.get('cowId'),
            row.get('milkYield'),
            row.get('timeSinceLastMilk'),
            row.get('dailyFeedQuantity'),
            row.get('enclosureTemp'),
            row.get('outsideTemp'),
            row.get('feedType'),
            row.get('bovineAge'),
            row.get('health'),
            row.get('lactationStage'),
            row.get('breed'),
            row.get('country')
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'message': 'Data submitted successfully!'}), 200

    

@app.route('/api/schedule', methods=['GET'])
def generate_schedule():
    # Fetch data from database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT cow_id, milk_yield, health, lactation_stage, bovine_age, breed
        FROM "Cowlibrate"
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Convert database rows to a format suitable for the algorithm
    data = [
        {
            'Age_ID': row[0],
            'Yield': row[1],
            'Health': row[2],
            'Lactation_Stage': row[3],
            'Breed': row[4]
        }
        for row in rows
    ]

    # Run optimization
    schedule = optimize_milking_schedule(data)

    return jsonify(schedule)

if __name__ == '__main__':
    app.run(debug=True)
