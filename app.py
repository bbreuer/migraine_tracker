from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'migraine_tracker.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        headache_severity = request.form['headache_severity']
        took_medicine = request.form['took_medicine']
        blood_pressure = request.form['blood_pressure']
        
        conn.execute('INSERT INTO migraines (headache_severity, took_medicine, blood_pressure) VALUES (?, ?, ?)',
                     (headache_severity, took_medicine, blood_pressure))
        conn.commit()
    
    migraines = conn.execute('SELECT * FROM migraines').fetchall()
    conn.close()
    return render_template('index.html', migraines=migraines)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        conn.execute('CREATE TABLE migraines (id INTEGER PRIMARY KEY, headache_severity TEXT, took_medicine TEXT, blood_pressure TEXT)')
        conn.close()
    app.run(debug=True)
