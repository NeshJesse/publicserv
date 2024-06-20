import sqlite3
import json

def init_db():
    conn = sqlite3.connect('public_data.db')
    c = conn.cursor()
    
    # Create profiles table
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 role TEXT NOT NULL,
                 description TEXT NOT NULL,
                 image TEXT NOT NULL,
                 socials TEXT NOT NULL,
                 county TEXT NOT NULL
             )''')
    
    # Create constituencies table
    c.execute('''CREATE TABLE IF NOT EXISTS constituencies (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 county TEXT NOT NULL,
                 code TEXT NOT NULL,
                 constituency TEXT NOT NULL,
                 mp TEXT NOT NULL,
                 image TEXT NOT NULL,
                 party TEXT,
                 desc TEXT NOT NULL
             )''')
    
    # Load profiles data
    with open('mps.json', 'r') as f:
        mps_data = json.load(f)
    
    for mp in mps_data:
        name = mp['name']
        role = mp['constituency']
        description = f"County: {mp['county']}, Party: {mp['party']}"
        image = mp['image']
        county = mp['county']
        
        c.execute('INSERT INTO profiles (name, role, description, image, county) VALUES (?, ?, ?, ?, ?)',
                  (name, role, description, image, county))
    
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
            gps = json.dumps(details['gps'])
            
            c.execute('INSERT INTO constituencies (county, code, constituency, mp, image, party, gps) VALUES (?, ?, ?, ?, ?, ?, ?)',
                      (county, code, constituency, mp, image, party, gps))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()

