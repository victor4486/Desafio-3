from flask import Flask, render_template


app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Tratamentos')
def Tratamentos():
    return render_template('Tratamentos.html')

@app.route('/Sobre')
def Sobre():
    return render_template('Sobre.html')

@app.route('/contato')
def Contato():
    return render_template('contato.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)