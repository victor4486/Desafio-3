from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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
        
        flash('Contato adicionado com sucesso!')
        return redirect(url_for('contato'))
        
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

@app.route('/Clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    filtro = request.args.get('filtro', 'todos')
    
    cur = mysql.connection.cursor()
    if filtro == 'visualizado':
        cur.execute("SELECT * FROM contatos WHERE visualizado = TRUE")
    elif filtro == 'nao_visualizado':
        cur.execute("SELECT * FROM contatos WHERE visualizado = FALSE")
    else:
        cur.execute("SELECT * FROM contatos")
    mensagens = cur.fetchall()
    cur.close()
    
    return render_template('clientes.html', mensagens=mensagens, filtro=filtro)

@app.route('/delete_message/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_message(id):
    if not current_user.is_admin:
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contatos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    
    flash('Mensagem excluída com sucesso!')
    return redirect(url_for('clientes'))

@app.route('/mark_as_viewed/<int:id>', methods=['POST', 'GET'])
@login_required
def mark_as_viewed(id):
    if not current_user.is_admin:
        return redirect(url_for('index'))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE contatos SET visualizado = TRUE, data_de_visualizacao = %s WHERE id = %s", (datetime.now(), id))
    mysql.connection.commit()
    cur.close()
    
    flash('Mensagem marcada como visualizada!')
    return redirect(url_for('clientes'))

@app.route('/agenda')
@login_required
def agenda():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    return render_template('agenda.html')

@app.route('/fornecedores')
@login_required
def fornecedores():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    return render_template('fornecedores.html')

if __name__ == '__main__':
    app.run(debug=True)
