import sys
sys.path.append('/home/joao/Documentos/ProjetoQuinta/')
from flask import Flask, request, jsonify, render_template, url_for, session, redirect
from api import epy_crud
from model import modelo, modelo2
from controller import controle, controle2


app = Flask(__name__, template_folder='view')


@app.route('/login/<int:id>/<int:value>/<string:cpf>')
def ReturnToLogin(value, cpf, id):
    log = controle.VerificacaoCrud()
    logar = epy_crud.MyAPI()
    data = log.BuscarDadosDeLogin(cpf)
    i = log.BuscarIDporCPF(cpf)
    if i == id and log.BuscarTipoPorCPF(cpf) == value:
        id = log.BuscarIdPorEmail(data[0])
        resultado = logar.Login(data[0], data[1])
        if data:
            if value == 1:
                return render_template('professor.html', id=id, token=resultado['dado']['token'])
            elif value == 2:
                return render_template('aluno.html', id=id, token=resultado['dado']['token'])
            elif value == 3:
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
    #print(value)
    id = log.BuscarIdPorEmail(email)
    if value != False:
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


@app.route('/upgrade/<int:id>', methods=['GET', 'POST'])
def upgrade(id):
    up = epy_crud.MyAPI()
    value = controle.VerificacaoCrud().BuscarCPF(id)
    token = controle.VerificacaoCrud().BuscarEmaiSenhalPorID(id)
    data = epy_crud.MyAPI().Login(token[0], token[1])
    tipo = controle.VerificacaoCrud().BuscarTipoPorCPF(value)
    if request.method == 'POST':
        try:
            # Get request parameters
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            telefone = request.form.get('telefone')
        
            if value:
                # Call the Upgrade_User method
                result = up.Upgrade_User(id, nome, email, senha, telefone)
                resultado = epy_crud.MyAPI().Login(email, senha)
                # Render a template with the result
                return render_template('upgrade_result.html', id=id, result=result['msg'], tipo=tipo, cpf=value, token=resultado['dado']['token'])
            else:
                return render_template('error_acess.html', motivo="CPF não encontrado!")

        except Exception as e:
            error_message = f"Internal Server Error: {str(e)}"
            return render_template('error_acess.html', motivo=error_message)
    # If it's a GET request, render the form template
    return render_template('upgrade.html', id=id, cpf=value, tipo=tipo)


@app.route('/dados/<string:token>/<int:id>', methods=['GET'])
def area_do_aluno(id, token):
    data = epy_crud.MyAPI()
    try:
        result = data.Read_ID(id, token)
        if result['response'] == 200:
            return render_template("dados_pessoais.html", resultado=result['dado'], value=result['dado']['Tipo'], token=token, id=id)
        else:
            return render_template("error_acess.html", motivo=result['msg'], resp=result["response"])
    except Exception as e:
        return render_template("error500.html", motivo=e)


# Rota para lidar com erro 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


@app.route('/listar_usuarios/<int:id>/<string:token>')
def listar_usuarios(id, token):
    verificador = controle.VerificacaoCrud()
    tipo = verificador.BuscarTipoPorID(id)
    cpf = verificador.BuscarCPF(id)
    if tipo == 3:
        data = epy_crud.MyAPI()
        try:
            result = data.Read_all(token)
            if result['response'] == 200:
                return render_template("read_all.html", resultado=result['dado'], value=tipo, token=token, id=id, cpf=cpf)
        except Exception as e:
            return render_template("error500.html", motivo=e)
    else:
        return render_template("error_acess.html", motivo="Usuário não têm permissão de acesso!")

######################## FUNÇOES ADMIN #############################

@app.route('/cadastro_lab', methods=['GET', 'POST'])
def cadastro_lab():
    if request.method == 'POST':
        nome = request.form['nome']
        token = request.headers.get('Authorization')
       
      

        result = epy_crud.MyAPI().CadastrarLab(nome, token)  

    
        if result.get('status'):
         
            return render_template('cadastro_lab_ok', nome=nome) #coloquei o nome aqui para informar qual foi cadastrado
        else:
         
            erro = result.get('msg')
            return render_template('cadastro_lab_error.html', erro=erro)

    return render_template('cadastro_lab_form.html')


@app.route('/listar_laboratorios')
def listar_laboratorios():
   
    resultado = epy_crud.MyAPI().Read_all_Labs()

    if resultado.get('status'):
    
        laboratorios = resultado.get('data')
        return render_template('listar_laboratorios.html', laboratorios=laboratorios)
    else:
   
        erro = resultado.get('msg')
        return render_template('erro.html', erro=erro)
    
#         <body>
#     <h1>Lista de Laboratórios</h1>
#     <ul>
#         {% for laboratorio in laboratorios %}
#             <li>{{ laboratorio.nome }} - Status: {{ laboratorio.tipo_status }} - Disponibilidade: {{ laboratorio.disponibilidade }}</li>
#         {% endfor %}
#     </ul>
# </body> DICA PARA QUEM FOR FAZER O HTML

@app.route('/detalhes_laboratorio/<int:id>')
def detalhes_laboratorio(id):

    resultado = epy_crud.MyAPI().Read_Lab_ID(id)

    if resultado.get('status'):
     
        detalhes = resultado.get('data')
        return render_template('detalhes_laboratorio.html', detalhes=detalhes)
    else:
      
        erro = resultado.get('msg')
        return render_template('erro.html', erro=erro)
    
#  <script>
#         document.getElementById('lista-usuarios').addEventListener('click', function(event) {
#             // Verifica se o clique ocorreu em um elemento <li>
#             if (event.target.tagName === 'LI') {
#                 // Obtém o ID do usuário clicado
#                 var userId = event.target.dataset.id;

#                 // Aqui você pode enviar o ID para o seu backend usando uma solicitação AJAX ou algo similar
#                 // Exemplo de como enviar usando fetch:
#                 fetch(`/ativar_usuario/${userId}`, {
#                     method: 'GET',
#                     headers: {
#                         'Authorization': 'SeuTokenJWTAqui'
#                         // Adicione outros cabeçalhos necessários
#                     }
#                 })
#                 .then(response => response.text())
#                 .then(resultado => {
#                     // Exibe o resultado em um alerta
#                     alert(resultado);

#                     // Volta para a página anterior
#                     window.history.back();
#                 })
#                 .catch(error => console.error('Erro:', error));
#             }
#         });
#     </script>
   
@app.route('/ativar_usuario/<int:id>')
def ativar_user_painel(id):
    token = request.headers.get('Authorization')

    resultado = epy_crud.MyAPI.AtivarUser(id,token)
    return f'<script>alert("{resultado}"); window.history.back();</script>'

#  <script>
#         document.getElementById('lista-usuarios').addEventListener('click', function(event) {
#             // Verifica se o clique ocorreu em um elemento <li>
#             if (event.target.tagName === 'LI') {
#                 // Obtém o ID do usuário clicado
#                 var userId = event.target.dataset.id;

#                 // Aqui você pode enviar o ID para o seu backend usando uma solicitação AJAX ou algo similar
#                 // Exemplo de como enviar usando fetch:
#                 fetch(`/ativar_usuario/${userId}`, {
#                     method: 'GET',
#                     headers: {
#                         'Authorization': 'SeuTokenJWTAqui'
#                         // Adicione outros cabeçalhos necessários
#                     }
#                 })
#                 .then(response => response.text())
#                 .then(resultado => {
#                     // Exibe o resultado em um alerta
#                     alert(resultado);

#                     // Volta para a página anterior
#                     window.history.back();
#                 })
#                 .catch(error => console.error('Erro:', error));
#             }
#         });
#     </script>



@app.route('/desativar_user/<int:id>')
def desativar_user(id):
    token = request.headers.get('Authorization')
    resultado = epy_crud.MyAPI.Desativar(id,token)
    return f'<script>alert("{resultado}"); window.history.back();</script>'

#  <script>
#         document.getElementById('lista-usuarios').addEventListener('click', function(event) {
#             // Verifica se o clique ocorreu em um elemento <li>
#             if (event.target.tagName === 'LI') {
#                 // Obtém o ID do usuário clicado
#                 var userId = event.target.dataset.id;

#                 // Aqui você pode enviar o ID para o seu backend usando uma solicitação AJAX ou algo similar
#                 // Exemplo de como enviar usando fetch:
#                 fetch(`/ativar_usuario/${userId}`, {
#                     method: 'GET',
#                     headers: {
#                         'Authorization': 'SeuTokenJWTAqui'
#                         // Adicione outros cabeçalhos necessários
#                     }
#                 })
#                 .then(response => response.text())
#                 .then(resultado => {
#                     // Exibe o resultado em um alerta
#                     alert(resultado);

#                     // Volta para a página anterior
#                     window.history.back();
#                 })
#                 .catch(error => console.error('Erro:', error));
#             }
#         });
#     </script>

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
