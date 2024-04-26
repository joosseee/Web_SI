import json
from flask import Flask, render_template, request, redirect, url_for, flash,  jsonify, send_from_directory
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
import uuid
import pdfkit
import os
import exercise_2
import exercise_3
import exercise_4
import matplotlib
import exercise_1and2_practica2
import p2_exercise_3
import sqlite3
from config import config
#Models
from models.ModelUser import ModelUser
#Entities
from models.entities.User import User

app = Flask(__name__)

matplotlib.use('agg')
with open('data/users.json') as users_file:
    users_data = json.load(users_file)

with open('data/legal.json') as web_history_file:
    web_history_data = json.load(web_history_file)


#Logueo de usuario
db = sqlite3.connect('bbdd.db',check_same_thread=False)
login_manager_app = LoginManager(app)
csrf = CSRFProtect(app)
@login_manager_app.user_loader
def load_user(username):
    return ModelUser.get_by_username(db,username)









#@app.route('/')
#def index():
#    #return render_template('index.html')


@app.route('/MIS_functions')
@login_required
def MIS_functions():
    top5_pages = exercise_4.paginas_desactualizadas()
    politicasWeb = exercise_4.webs_politicas_privacidad_por_año()
    usuariosCriticos = exercise_4.tenUSERS()
    user_img, admin_img = exercise_4.meanPasswords()

    return render_template('exercise_4.html', top5_pages=top5_pages, politicasWeb=politicasWeb,
                           usuarios_criticos_img=usuariosCriticos, user_img=user_img, admin_img=admin_img)


@app.route('/phishing_stats')
@login_required
def stats():
    stats_df, passwords_df = exercise_3.stats_function()
    return render_template('exercise_3.html', stats_df=stats_df, passwords_df=passwords_df)


@app.route('/values_computation')
@login_required
def values_computation():
    df_results = exercise_2.data_querys()
    return render_template('exercise_2.html', df_results=df_results)


# practica 2

#ejercicio 1
@app.route('/critical_users', methods=['GET', 'POST'])
@login_required
def xUsers():
    if request.method=='POST':
        num_users = int(request.form['num_users'])
        top_x_criticos, num_critical = exercise_1and2_practica2.xUsers(num_users)
    else:
        top_x_criticos, num_critical = exercise_1and2_practica2.xUsers(1)
        top_x_criticos = None

    return render_template('exercise_1_practica2.html', top_x_criticos=top_x_criticos, num_critical=num_critical)

@app.route('/critical_pages', methods=['GET', 'POST'])
@login_required
def xPages():
    if request.method=='POST':
        num_pages = int(request.form['num_pages'])
        top_x_pages, num_critical = exercise_1and2_practica2.xPages(num_pages)
    else:
        top_x_pages, num_critical = exercise_1and2_practica2.xPages(1)
        top_x_pages = None

    return render_template('exercise_1b_practica2.html', top_x_pages=top_x_pages, num_critical=num_critical)


#ejercicio 2

@app.route('/critical_users_ex2', methods=['GET', 'POST'])
@login_required
def users_ex2():
    if request.method=='POST':
        num_users = int(request.form['num_users'])
        clics = request.form['clics']
        top_x_users, num_critical = exercise_1and2_practica2.xUsersClics(num_users, clics)
    else:
        top_x_users, num_critical = exercise_1and2_practica2.xUsersClics(1, 'above')
        top_x_users = None
    return render_template('exercise_2_practica2.html', top_x_users=top_x_users, num_critical=num_critical)


# Practica 2 --> Ejercicio 3

@app.route('/vulnerabilities')
@login_required
def show_vulnerabilities():
    vulnerabilities = p2_exercise_3.get_latest_vulnerabilities()
    return render_template('p2_exercise_3.html', vulnerabilities=vulnerabilities[:10])


#Practica 3 --> Ejercicio 4 pdf

@app.route('/pdfs/<filename>')
@login_required
def pdfs(filename):
   
    return send_from_directory('pdfs/', filename)

@app.route('/generar_pdf', methods=['POST'])
@login_required
def generate_pdf():

    html_content = request.json['contenido_informe']
    pdf_filename = str(uuid.uuid4()) + '.pdf'

    # Construir la ruta completa del archivo PDF
    pdf_file_path = os.path.join('pdfs', pdf_filename)

    # Configurar wkhtmltopdf con la ruta al ejecutable
    wkhtmltopdf_path = os.path.join(os.getcwd(), 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')
    configure = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    pdfkit.from_string(html_content, pdf_file_path, configuration=configure)

    return jsonify({'pdf_path': pdf_file_path})
    

#Practica 3 --> Ejercicio 4 login
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = User(request.form['username'],None,request.form['password'])
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return render_template('index.html')
            else:
                flash("Invalid password...")
                return render_template('login.html')
        else:
            flash("User not found...")
            return render_template('login.html')
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user
    return redirect(url_for('login'))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>",404





if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
    csrf.init_app(app)
    app.register_error_handler(401,status_401())
    app.register_error_handler(404,status_404())
