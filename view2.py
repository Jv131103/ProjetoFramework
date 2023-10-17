import sys
sys.path.append('/home/joao/Documentos/ProjetoQuinta/')
from flask import Flask, request, jsonify, render_template, url_for, session, redirect
from api import epy_crud
from model import modelo, modelo2
from controller import controle, controle2
import requests
import jwt

app = Flask(__name__, template_folder='view')


@app.route('/login/<int:value>/<string:cpf>')
def ReturnToLogin(value, cpf):
    log = controle.VerificacaoCrud()
    logar = epy_crud.MyAPI()
    data = log.BuscarDadosDeLogin(cpf)
    if data:
        id = log.BuscarIdPorEmail(data[0])
        resultado = logar.Login(data[0], data[1])
        if resultado['status'] == True:
            if value == 1:
                return render_template('professor.html', id=id, token=resultado['dado']['token'])
            elif value == 2:
                return render_template('aluno.html', id=id, token=resultado['dado']['token'])
            else:
                return render_template('admin.html', id=id, token=resultado['dado']['token'])
        else:
            return render_template("error_acess.html", motivo="Erro! Usuário não liberado")
    else:
        return render_template("error_acess.html", motivo="Dados não encontrados")

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    log = controle.VerificacaoCrud()
    value = log.BuscarTipoPorEmail(email)
    id = log.BuscarIdPorEmail(email)
    if value[0] in [1, 2, 3]:
        logar = epy_crud.MyAPI()
        resultado = logar.Login(email, senha)
        if resultado['status'] == True:
            # Redireciona para a rota adequada com base no tipo de usuário
            if value[0] == 1:
                return render_template("professor.html", id=id, token=resultado['dado']['token'])
            elif value[0] == 2:
                return render_template('aluno.html', id=id, token=resultado['dado']['token'])
            elif value[0] == 3:
                return render_template('admin.html', id=id, token=resultado['dado']['token'])
            else:
                return render_template("error_acess.html", motivo="Usuário não encontrado!")
        else:
            return render_template("error_acess.html", motivo="Usuário não permitidido ou inativo!")
    else:
        return render_template("error_acess.html", motivo="Usuário não corresponde aos dados de cadastro")


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Obtenha os dados do formulário
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        cpf = request.form.get('cpf')
        telefone = request.form.get('telefone')
        id_tipo = request.form.get('tipoUsuario')
        
        # Check if the email already exists
        email_exists = controle.VerificacaoCrud().CadastroExistePorEmail(email)
        if not email_exists:
            # Chame o método CreateUser da sua classe
            result = epy_crud.MyAPI().CreateUser(nome, email, senha, cpf, telefone, id_tipo)

            # Verifique o tipo de usuário
            busc = controle.VerificacaoCrud().BuscarTipoPorEmail(email)

            # Trate os resultados
            if busc[0] == 1:
                # Se o cadastro for bem-sucedido, redirecione para a área de login
                return render_template("login.html")
            elif busc[0] == 2:
                return render_template("login.html")
            elif busc[0] == 3:
                return render_template("login.html")
            else:
                return render_template("error_acess.html", motivo="Acesso Negado para acesso!")
        else:
            return render_template("error_acess.html", motivo="Dados de usuário não encontrado!")

    # Se for um pedido GET ou qualquer outro método, renderize o formulário
    return render_template('cadastro.html')


@app.route('/dados/<string:token>/<int:aluno_id>', methods=['GET'])
def area_do_aluno(aluno_id, token):
    data = epy_crud.MyAPI()
    try:
        result = data.Read_ID(aluno_id, token)
        if result['response'] == 200:
            print(result)
            return render_template("dados_pessoais.html", resultado=result['dado'], value=result['dado']['Tipo'])
        else:
            return render_template("error_acessAluno.html", motivo=result['msg'], resp=result["response"])
    except Exception as e:
        return render_template("error500.html", motivo=e)


if __name__ == '__main__':
    app.run(debug=True)
