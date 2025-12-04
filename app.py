import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for
from sqlalchemy.testing.pickleable import User
from db import db
from models_equipamentos import EquipamentosTecnicos, EquipamentosTi, EquipamentosGamer, NotasFiscais, EquipamentosConsumo, RelatorioAtividade, Usuario
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash



# inicializa a app
app = Flask(__name__, instance_relative_config=True)
os.makedirs(app.instance_path, exist_ok=True)

# configurações
app.config.from_mapping(
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'labmaker.db').replace(os.sep, '/')}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# inicializa a extensão sem criar ciclo
db.init_app(app)

#inicia o login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso.", "info")
    return redirect(url_for('index.html'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            flash("Login realizado com sucesso.")
            next_page = request.args.get("next")
            return redirect(next_page or url_for('home'))
        else:
            flash("Email ou senha inválidos.")
    return render_template("login.html")


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('login'))
        perfil = request.form['perfil']
        novo_usuario = Usuario(nome=nome, email=email, senha=senha, perfil=perfil)
    return render_template('cadastro.html')


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/maker", methods=["GET", "POST"])
def maker():
    if request.method == "POST":
        try:
            now = EquipamentosConsumo(
                nome=request.form.get('nome', ''),
                garantia=request.form.get('garantia', ''),
                cor=request.form.get('cor', ''),
                fabricante_marca=request.form.get('fabricante_marca', ''),
                modelo=request.form.get('modelo', ''),
                numero_serie=request.form.get('numero_serie', ''),
                data_fabricacao=request.form.get('data_fabricacao', ''),
                validade=request.form.get('validade') in ('on', '1', 'true', 'True'),
                condicao=request.form.get('condicao_localizacao', ''),
                localizacao=request.form.get('condicao_localizacao', ''),
                patrimonio=request.form.get('patrimonio', ''),
                quantidade=int(request.form.get('quantidade') or 0)
            )
            db.session.add(now)
            db.session.commit()
            flash("Registro salvo com sucesso", "success")
            return redirect("/maker")
        except Exception:
            db.session.rollback()
            import traceback; traceback.print_exc()
            flash("Erro ao salvar registro, veja o console", "error")
            return redirect("/maker")

    equipamentos = EquipamentosConsumo.query.all()
    return render_template("maker.html", maker="LabMaker", dados=equipamentos)

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == "POST":
        try:
            relatorio = RelatorioAtividade(
                aluno=request.form.get('aluno', '').strip(),
                atividade=request.form.get('atividade', '').strip(),
                professor_responsavel=request.form.get('professor_responsavel', '').strip(),
                data=request.form.get('data', '').strip(),
                observacao=request.form.get('observacao', '').strip()
            )
            db.session.add(relatorio)
            db.session.commit()
            flash("Relatório enviado com sucesso!", "success")
            return redirect("/formulario")
        except Exception:
            db.session.rollback()
            import traceback; traceback.print_exc()
            flash("Erro ao enviar relatório", "error")
            return redirect("/formulario")

    relatorios = RelatorioAtividade.query.all()
    return render_template("formulario.html", relatorios=relatorios)


@app.route('/gamer', methods=['GET', 'POST'])
def gamer():
    if request.method == 'POST':
        try:
            novo = EquipamentosGamer(
                nome=request.form.get('nome',''),
                categoria=request.form.get('categoria',''),
                quantidade=int(request.form.get('quantidade') or 0)
            )
            db.session.add(novo)
            db.session.commit()
            return redirect('/gamer')
        except Exception:
            db.session.rollback()
            flash("Erro ao inserir gamer", "error")
            return redirect('/gamer')

    equipamentos = EquipamentosGamer.query.all()
    return render_template('gamer.html', dados=equipamentos)


@app.route('/tecnicos', methods=['GET', 'POST'])
def tecnicos():
    if request.method == 'POST':
        try:
            novo = EquipamentosTecnicos(
                nome=request.form.get('nome',''),
                garantia=request.form.get('garantia',''),
                fabricante_marca=request.form.get('fabricante_marca',''),
                modelo=request.form.get('modelo',''),
                numero_serie=request.form.get('numero_serie',''),
                data_fabricacao=request.form.get('data_fabricacao',''),
                validade=request.form.get('validade') in ('on','1','true','True'),
                condicao=request.form.get('condicao',''),
                localizacao=request.form.get('localizacao',''),
                patrimonio=request.form.get('patrimonio',''),
                quantidade=int(request.form.get('quantidade') or 0)
            )
            db.session.add(novo)
            db.session.commit()
            return redirect('/tecnicos')
        except Exception:
            db.session.rollback()
            flash("Erro ao inserir técnico", "error")
            return redirect('/tecnicos')

    equipamentos = EquipamentosTecnicos.query.all()
    dados = [e.__dict__ for e in equipamentos]
    for d in dados:
        d.pop('_sa_instance_state', None)  # remove metadado interno do sqlachemy
    return render_template('tecnicos.html', dados=dados)


@app.route('/ti', methods=['GET', 'POST'])
def ti():
    if request.method == 'POST':
        try:
            data_raw = request.form.get('data_fabricacao','').strip()
            try:
                data_fab = datetime.strptime(data_raw, '%Y-%m-%d').date() if data_raw else None
            except Exception:
                data_fab = None

            novo = EquipamentosTi(
                nome=request.form.get('nome',''),
                garantia=float(request.form.get('garantia') or 0),
                fabricante_marca=request.form.get('fabricante_marca',''),
                modelo=request.form.get('modelo',''),
                numero_serie=request.form.get('numero_serie',''),
                data_fabricacao=data_fab,
                validade=request.form.get('validade') in ('on','1','true','True'),
                condicao=request.form.get('condicao',''),
                localizacao=request.form.get('localizacao',''),
                patrimonio=request.form.get('patrimonio',''),
                quantidade=int(request.form.get('quantidade') or 0)
            )
            db.session.add(novo)
            db.session.commit()
            return redirect('/ti')
        except Exception:
            db.session.rollback()
            flash("Erro ao inserir TI", "error")
            return redirect('/ti')

    equipamentos = EquipamentosTi.query.all()
    return render_template('ti.html', dados=equipamentos)


@app.route('/notasFiscais', methods=['GET', 'POST'])
def notas_fiscais():
    if request.method == 'POST':
        try:
            novo = NotasFiscais(
                descricao_itens=request.form.get('descricao_itens',''),
                numero_nf=request.form.get('numero_nf',''),
                data_emissao=datetime.strptime(request.form.get('data_emissao',''), '%Y-%m-%d') if request.form.get('data_emissao') else None,
                fornecedor=request.form.get('fornecedor',''),
                cnpj=request.form.get('cnpj',''),
                quantidade=int(request.form.get('quantidade') or 0),
                valor_total=float(request.form.get('valor_total') or 0.0)
            )
            db.session.add(novo)
            db.session.commit()
            return redirect('/notasFiscais')
        except Exception:
            db.session.rollback()
            flash("Erro ao inserir nota fiscal", "error")
            return redirect('/notasFiscais')

    equipamentos = NotasFiscais.query.all()
    dados = [e.__dict__ for e in equipamentos]
    for d in dados:
        d.pop('_sa_instance_state', None)
    return render_template('notasFiscais.html', dados=dados)


# @app.route('/painel')
# @login_required
# def painel():
#     return render_template('painel.html')


# ponto de entrada
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)