from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'seu_chave_secreta_aqui'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'farofa123'
app.config['MYSQL_DB'] = 'formulario-contato'

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, is_admin):
        self.id = id
        self.username = username
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(int(user[0]), user[1], user[3])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Tratamentos')
def Tratamentos():
    return render_template('Tratamentos.html')

@app.route('/Sobre')
def Sobre():
    return render_template('Sobre.html')

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    return render_template('admin.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        nascimento = request.form['nascimento']
        sexo = request.form['sexo']
        tipo = request.form['tipo']
        descricao = request.form['descricao']
    
        cur = mysql.connection.cursor()
        
        cur.execute("""
            INSERT INTO contatos (nome, email, telefone, nascimento, sexo, tipo, descricao) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, email, telefone, nascimento, sexo, tipo, descricao))
        
        mysql.connection.commit()
        
        cur.close()
        
    return render_template('contato.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[2], password):
            user_obj = User(int(user[0]), user[1], user[3])
            login_user(user_obj)
            return redirect(url_for('admin' if user[3] else 'index'))
        else:
            flash('Login não realizado. Verifique o nome de usuário e a senha.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
