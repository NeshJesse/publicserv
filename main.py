from flask import Flask,jsonify,request, render_template, g
import sqlite3
import json

app = Flask(__name__, template_folder="templates")

DATABASE = 'profiles.db'

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


@app.route('/consti')
def constituencies():
    db = get_db()
    cur = db.execute('SELECT county, code, constituency, mp, image, party, gps FROM constituencies')
    constituencies = cur.fetchall()
    constituencies = [{'county': row[0], 'code': row[1], 'constituency': row[2], 'mp': row[3], 'image': row[4], 'party': row[5], 'gps': json.loads(row[6])} for row in constituencies]
    return render_template('constis.html', constituencies=constituencies)

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT id, name, county,constituency, image ,party FROM profiles')
    profiles = cur.fetchall()
    profiles = [{'id': row[0], 'name': row[1], 'county': row[2], 'constituency': row[3], 'image': row[4],'party': row[5]} for row in profiles]
    return render_template('index.html', profiles=profiles)

@app.route('/profile/<int:profile_id>')
def profiled(profile_id):
    db = get_db()
    cur = db.execute('SELECT name, county,constituency, party, image FROM profiles WHERE id = ?', (profile_id,))
    profile = cur.fetchone()
    if profile:
        profile = {'name': profile[0], 'county': profile[1], 'constituency': profile[2], 'image': profile[3], 'party': profile[4]}
    return render_template('profile.html', profile=profile)


@app.route('/profile/<int:profile_id>')
def profile(profile_id):
    db = get_db()
    cur = db.execute('SELECT name, county, constituency,  image, party FROM profiles WHERE id = ?', (profile_id,))
    profile = cur.fetchone()  
    profile = {
            'name': profile[0],
            'county': profile[1],
            'constituency': profile[2],
            'image': profile[3],
            'party': profile[4]
        }
    return render_template('profile_detail.html', profile=profile)



@app.route('/counties')
def get_counties():
    conn = sqlite3.connect('profiles.db')
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT county FROM profiles')
    counties = [row[0] for row in cur.fetchall()]
    conn.close()
    return jsonify(counties)

@app.route('/constituencies/<county>')
def get_constituencies(county):
    conn = sqlite3.connect('profiles.db')
    cur = conn.cursor()
    cur.execute('SELECT constituency FROM profiles WHERE county = ?', (county,))
    constituencies = [row[0] for row in cur.fetchall()]
    conn.close()
    return jsonify(constituencies)

@app.route('/filter')
def filter_results():
    county = request.args.get('county')
    constituency = request.args.get('constituency')
    conn = sqlite3.connect('profiles.db')
    cur = conn.cursor()
    cur.execute('SELECT name, county, constituency, image, party FROM profiles WHERE county = ? AND constituency = ?', (county, constituency))
    results = [{'name': row[0], 'county': row[1], 'constituency': row[2], 'image': row[3], 'party': row[4]} for row in cur.fetchall()]
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
