from flask import Flask, render_template
import sqlite3

app = Flask(__name__, static_folder='static', template_folder='templates')

def get_db_connection():
    conn = sqlite3.connect('profile_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    profiles = conn.execute('SELECT * FROM profiles').fetchall()
    conn.close()
    return render_template('index.html', profiles=profiles)

@app.route('/profile/<int:profile_id>')
def profile(profile_id):
    conn = get_db_connection()
    profile = conn.execute('SELECT * FROM profiles WHERE id = ?', (profile_id,)).fetchone()
    conn.close()
    if profile is None:
        return "Profile not found!", 404
    return render_template('profile.html', profile=profile)

if __name__ == '__main__':
    app.run(debug=True)
