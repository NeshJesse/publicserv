# init_db.py
import sqlite3

def init_db():
    conn = sqlite3.connect('profile_data.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 role TEXT NOT NULL,
                 description TEXT NOT NULL,
                 image TEXT NOT NULL
             )''')
    
    profiles = [
        ('Julie Watson', 'UX / UI developer', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Pariatur delectus, mollitia tenetur libero quam recusandae alias in incidunt.', 'profile1.jpg'),
        ('Marc McKnew', 'Front-End developer', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Pariatur delectus, mollitia tenetur libero quam recusandae alias in incidunt.', 'profile2.jpg'),
        ('Jenny McKnew', 'Back-End developer', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Pariatur delectus, mollitia tenetur libero quam recusandae alias in incidunt.', 'profile3.jpg')
    ]
    
    c.executemany('INSERT INTO profiles (name, role, description, image) VALUES (?, ?, ?, ?)', profiles)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
