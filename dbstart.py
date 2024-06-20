import sqlite3
import json

def init_db():
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    
    # Create profiles table (include 'county' column)
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 county TEXT NOT NULL,
                 constituency TEXT NOT NULL,
                 party TEXT NOT NULL,
                 image TEXT NOT NULL
             )''')
    
    # Create constituencies table (include 'gps' column)
    c.execute('''CREATE TABLE IF NOT EXISTS constituencies (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 county TEXT NOT NULL,
                 code TEXT NOT NULL,
                 constituency TEXT NOT NULL,
                 mp TEXT NOT NULL,
                 image TEXT NOT NULL,
                 party TEXT,
                 desc TEXT NOT NULL,
                 gps TEXT NOT NULL
             )''')
    
    # Load profiles data
    with open('mps.json', 'r') as f:
        mps_data = json.load(f)
    
    for mp in mps_data:
        name = mp['name']
        county = mp['county']
        constituency = mp['constituency']
        party = mp['party']
        image = mp['image']

        
        c.execute('INSERT INTO profiles (name, constituency, county, party, image) VALUES (?, ?, ?, ?, ?)',
                  (name, constituency, county, party, image))
    
    # Load constituencies data
    with open('constituencies.json', 'r') as f:
        constituencies_data = json.load(f)
    
    for county_data in constituencies_data:
        county = county_data['county']
        code = county_data['code']
        for constituency, details in county_data['constituencies'].items():
            mp = details['mp']
            image = details['image']
            party = details.get('party', 'Unknown')  # Use 'Unknown' if 'party' key is missing
            gps = json.dumps(details['gps'])  # Convert gps list to JSON string
            desc = json.dumps(details)  # Store details as JSON string
            
            c.execute('INSERT INTO constituencies (county, code, constituency, mp, image, party, desc, gps) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                      (county, code, constituency, mp, image, party, desc, gps))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()