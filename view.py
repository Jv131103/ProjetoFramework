import sys
sys.path.append('/home/joao/Documentos/ProjetoQuinta/')
from flask import Flask, request, jsonify, render_template, url_for, session, redirect, Blueprint
from flaskext.mysql import MySQL
from api import apy_crud
import requests

mysql = MySQL()
app = Flask(__name__, template_folder='view')
app.config["SECRET_KEY"] = 'minha-chave' #Palavra chave, que será utilizado nas confs

# Configurações do Banco de Dados
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Joao$131103'
app.config['MYSQL_DATABASE_DB'] = 'Projeto'
mysql.init_app(app)

apy_crud = Blueprint('apy_crud', __name__)
# Registre o Blueprint na aplicação principal com um prefixo
app.register_blueprint(apy_crud, url_prefix='/acessar/api')

# Função para verificar se o cadastro já existe pelo e-mail ou CPF
def verificar_cadastro_existente(email, cpf):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM Usuario WHERE email = %s OR cpf = %s", (email, cpf))
    user_id = cursor.fetchone()
    
    conn.close()
    
    return user_id
    
@app.route("/", methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def Acessar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        if email and senha:
            conn = mysql.connect()
            cursor = conn.cursor()
            
            # Verifica se o e-mail e senha correspondem a um usuário na tabela Usuario
            cursor.execute("SELECT id, atividade FROM Usuario WHERE email = %s AND senha = %s", (email, senha))
            user_data = cursor.fetchone()
            
            conn.close()
            
            if user_data:
                user_id, ativado = user_data
                if ativado == "1":
                    # Usuário autenticado e ativado, redireciona para a área pessoal
                    return render_template('area_pessoal.html')
                else:
                    # Usuário desativado, gera erro de cadastro informando que ele está desativado
                    return render_template("erro_user.html")
            else:
                # Credenciais inválidas, redireciona para a página de login com uma mensagem de erro
                return render_template("error_acess.html")

    return render_template('login.html', url_for=url_for)


@app.route('/gravar', methods=['GET', 'POST'])
def Cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha1 = request.form['senha1']  # Altere para 'senha1' para pegar a primeira senha
        senha2 = request.form['senha2']  # Altere para 'senha2' para pegar a segunda senha
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        tipo_registro = request.form['tipo_registro']  # Obtém o valor do radio button
        atividade = '1'

        # Verifique se as senhas coincidem
        if senha1 != senha2:
            return jsonify({'success': False, 'error': 'As senhas não coincidem. Por favor, tente novamente.'})

        # Verificando se o tipo_registro é uma opção válida (1 para Aluno, 2 para Professor)
        if tipo_registro not in ['1', '2']:
            return jsonify({'success': False, 'error': 'Tipo de registro inválido'})
        
        if atividade not in ["0", "1"]:
            return jsonify({'success': False, 'error': 'Registro de atividade inválido'})

        if nome and email and senha1 and cpf and tipo_registro and atividade:
            # Verifica se o cadastro já existe pelo e-mail ou CPF
            existing_user = verificar_cadastro_existente(email, cpf)
            if existing_user:
                return jsonify({'success': False, 'error': 'E-mail ou CPF já cadastrado'})

            conn = mysql.connect()
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO Usuario(nome, email, senha, cpf, telefone, id_tipo, atividade) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (nome, email, senha1, cpf, telefone, tipo_registro, atividade))
            conn.commit()
            conn.close()
            
            return render_template("area_pessoal.html")

    return render_template('cadastro.html')


@app.route('/habilitar_usuario/<int:user_id>', methods=['GET'])
def habilitar_usuario(user_id):
    user_id = str(user_id)
    conn = mysql.connect()
    cursor = conn.cursor()

    # Define o usuário como ativado (ativado = 1) na tabela Usuario
    cursor.execute("UPDATE Usuario SET atividade = '1' WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('Listar'))  # Redireciona para a página de lista de usuários



# Rota para desabilitar um usuário
@app.route('/desabilitar_usuario/<int:user_id>', methods=['GET'])
def desabilitar_usuario(user_id):
    user_id = str(user_id)
    conn = mysql.connect()
    cursor = conn.cursor()

    # Define o usuário como desativado (ativado = 0) na tabela Usuario
    cursor.execute("UPDATE Usuario SET atividade = '0' WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('Listar'))  # Redireciona para a página de lista de usuários


@app.route("/listar", methods=['POST','GET'])
def Listar():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, cpf, telefone, id_tipo, atividade from Usuario')
    data = cursor.fetchall()
    conn.commit()
    return render_template('lista.html', datas=data)

@app.route("/acessar/api")
def acessar_api():
    return 'Bem vindo a API!<br><br>Você pode acessá-la separadamente\nou\nTestar por aqui mesmo como teste:<br>-> Para acessar: /acessar/api/read_api<br><br>PS: Isso é apenas para testes, se quiser acessar nossa API acesse as informações para acessar nosso servidor de APIS!'

@app.route('/logout')
def logout():
    session.clear()  # Limpa todos os dados da sessão
    return redirect(url_for('Acessar'))  # Redireciona para a página de login

@app.errorhandler(404)
#Método erro404 que irá receber o parâmetro e
def error404(e):
    #Irá retornar a página de erro 404, alterado via HTML por meio do render_template
    return render_template('erro.html'), 404



@app.route('/acessar/api/read_api', methods=['GET'])
def listar_usuarios():
    # Envie uma solicitação GET para a rota correspondente no 'apy_crud'
    response = requests.get('http://localhost:5002/cadastro/api/read')
    
    # Verifique se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Parseie a resposta JSON
        data = response.json()
        usuarios = data.get('data', [])
        return jsonify(usuarios)
    else:
        # Trate erros, se necessário
        return jsonify({"error": "Erro ao listar usuários"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
