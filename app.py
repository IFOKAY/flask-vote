from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret-key'

def init_db():
    with sqlite3.connect('votes.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS votes (candidate TEXT)')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    candidates = ['Alice', 'Bob', 'Charlie']
    if request.method == 'POST':
        if 'voted' in session:
            return redirect('/results')
        candidate = request.form['candidate']
        with sqlite3.connect('votes.db') as conn:
            conn.execute('INSERT INTO votes (candidate) VALUES (?)', (candidate,))
            conn.commit()
        session['voted'] = True
        return redirect('/results')
    return render_template('vote.html', candidates=candidates)

@app.route('/results')
def results():
    with sqlite3.connect('votes.db') as conn:
        cur = conn.execute('SELECT candidate, COUNT(*) FROM votes GROUP BY candidate')
        results = cur.fetchall()
    return render_template('results.html', results=results)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)