from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='static')
mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'F@rofa123'
app.config['MYSQL_DB'] = 'formulario_contato'

mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Tratamentos')
def Tratamentos():
    return render_template('Tratamentos.html')

@app.route('/Sobre')
def Sobre():
    return render_template('Sobre.html')

@app.route('/contato', methods=['GET', 'POST'])
def Contato():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['number']
        nascimento = request.form['nascimento']
        sexo = request.form['sexo']
        tipo = request.form['tipo']
        descricao = request.form['descricao']
    
        # Cria um cursor para a conexão MySQL
        cur = mysql.connection.cursor()
        
        # Executa a inserção no banco de dados
        cur.execute("""
            INSERT INTO contatos (nome, email, telefone, nascimento, sexo, tipo, descricao) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, email, telefone, nascimento, sexo, tipo, descricao))
        
        # Confirma a transação
        mysql.connection.commit()
        
        # Fecha o cursor
        cur.close()
        
    return render_template('contato.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port='')