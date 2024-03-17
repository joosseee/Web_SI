import json
from flask import Flask, render_template, request, redirect, url_for
import exercise_2
import exercise_3
import exercise_4
import matplotlib
app = Flask(__name__)


matplotlib.use('agg')
with open('data/users.json') as users_file:
    users_data = json.load(users_file)

with open('data/legal.json') as web_history_file:
    web_history_data = json.load(web_history_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/MIS_functions')
def MIS_functions():

    top5_pages = exercise_4.paginas_desactualizadas()
    politicasWeb = exercise_4.webs_politicas_privacidad_por_año()
    usuariosCriticos = exercise_4.tenUSERS()
    user_img, admin_img = exercise_4.meanPasswords()

    return render_template('exercise_4.html', top5_pages=top5_pages, politicasWeb=politicasWeb, usuarios_criticos_img=usuariosCriticos, user_img=user_img, admin_img=admin_img)


@app.route('/phishing_stats')
def stats():
    stats_df, passwords_df = exercise_3.stats_function()
    return render_template('exercise_3.html', stats_df=stats_df, passwords_df=passwords_df)


@app.route('/values_computation')
def values_computation():
    df_results = exercise_2.data_querys()
    return render_template('exercise_2.html', df_results = df_results)


if __name__ == '__main__':
    app.run(debug=True)
