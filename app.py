import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


with open('data/users.json') as users_file:
    users_data = json.load(users_file)

with open('data/legal.json') as web_history_file:
    web_history_data = json.load(web_history_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':

        return redirect(url_for('index'))
    return render_template('report.html')

@app.route('/courses')
def courses():
    return render_template('courses.html', users=users_data, web_history=web_history_data)

if __name__ == '__main__':
    app.run(debug=True)
