import sqlite3
import json

def init_db():
    # Connect to SQLite database
    conn = sqlite3.connect('mp_data.db')
    c = conn.cursor()
    
    # Create profiles table
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 role TEXT NOT NULL,
                 description TEXT NOT NULL,
                 image TEXT NOT NULL,
                 socials TEXT NOT NULL
             )''')

    # Load JSON data from files
    with open('mps.json', 'r') as f:
        mps_data = json.load(f)
    
    # Insert data into profiles table
    for mp in mps_data:
        name = mp['name']
        role = mp['constituency']  # Use constituency as role
        description = f"County: {mp['county']}, Party: {mp['party']}"  # Create a description using county and party
        image = mp['image']
        socials = json.dumps(mp.get('socials', {}))  # Assuming socials are empty
        
        c.execute('INSERT INTO profiles (name, role, description, image, socials) VALUES (?, ?, ?, ?, ?)',
                  (name, role, description, image, socials))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
