import os       # caminhos de arquivo
import pandas as pd
from flask import Flask, render_template     #render_template carrega arquivo html da pasta template

BASE = os.path.dirname(os.path.abspath(__file__))   #pega o caminho da pasta onde esta o app.py
TEMPLATES = os.path.join(BASE, 'templates')

print(">>> BASE DIR:", BASE)
print(">>> TEMPLATES DIR:", TEMPLATES)

app = Flask(__name__, template_folder=TEMPLATES)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/itens')         #le o arquivo csv e converte os dados p/ uma lista e envia a lista para itens.html
def itens():
    caminho_csv = os.path.join(BASE, 'data', 'itens.csv')
    df = pd.read_csv(caminho_csv)
    itens = df.to_dict(orient='records')
    return render_template('itens.html', itens=itens)
@app.route('/gamer', methods = ['GET', 'POST', 'DELETE'])
def gamer():
    caminho = os.path.join(BASE, 'data', 'cadastro_equipamentos_gamer.csv')
    df = pd.read_csv(caminho, encoding='latin1')
    dados = df.to_dict(orient='records')
    return render_template('gamer.html', dados=dados)

@app.route('/tecnicos', methods = ['GET', 'POST', 'DELETE'])
def tecnicos():
    caminho = os.path.join(BASE, 'data', 'cadastro_equipamentos_tecnicos.csv')
    df = pd.read_csv(caminho, encoding='latin1')
    dados = df.to_dict(orient='records')
    return render_template('tecnicos.html', dados=dados)

@app.route('/ti', methods = ['GET', 'POST', 'DELETE'])
def ti():
    caminho = os.path.join(BASE, 'data', 'cadastro_equipamentos_ti.csv')
    df = pd.read_csv(caminho, encoding='latin1')
    dados = df.to_dict(orient='records')
    return render_template('ti.html', dados=dados)

@app.route('/notasFiscais', methods = ['GET', 'POST', 'DELETE'])
def notasFiscais():
    caminho = os.path.join(BASE, 'data', 'cadastro_notas_fiscais.csv')
    df = pd.read_csv(caminho, encoding='latin1')
    dados = df.to_dict(orient='records')
    return render_template('notasFiscais.html', dados=dados)

@app.route('/maker', methods = ['GET', 'POST', 'DELETE'])
def maker():
    caminho = os.path.join(BASE, 'data', 'levantamento_maker.csv')
    df = pd.read_csv(caminho, encoding='latin1')
    dados = df.to_dict(orient='records')
    return render_template('maker.html', dados=dados)

@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)