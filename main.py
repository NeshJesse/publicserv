from flask import Flask, render_template, g
import sqlite3
import json

app = Flask(__name__, template_folder="templates")

DATABASE = 'mp_data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT id, name, role, description, image, socials FROM profiles')
    profiles = cur.fetchall()
    profiles = [{'id': row[0], 'name': row[1], 'role': row[2], 'description': row[3], 'image': row[4], 'socials': json.loads(row[5])} for row in profiles]
    return render_template('index.html', profiles=profiles)

@app.route('/profile/<int:profile_id>')
def profile(profile_id):
    db = get_db()
    cur = db.execute('SELECT name, role, description, image, socials FROM profiles WHERE id = ?', (profile_id,))
    profile = cur.fetchone()
    if profile:
        profile = {'name': profile[0], 'role': profile[1], 'description': profile[2], 'image': profile[3], 'socials': json.loads(profile[4])}
    return render_template('profile.html', profile=profile)

if __name__ == '__main__':
    app.run(debug=True)
