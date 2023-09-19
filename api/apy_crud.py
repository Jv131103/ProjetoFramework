import sys
sys.path.append('/home/joao/Documentos/ProjetoQuinta/')
from flask import Flask, request, jsonify
from model import modelo
from model import modelo2
from controller import controle
from controller import controle2

app = Flask(__name__) #Define o objeto Flask
app.config["SECRET_KEY"] = 'minha-chave' #Palavra chave, que será utilizado nas confs

# Página de acesso a API
@app.route("/")
@app.route("/cadastro")
@app.route("/api")
def ola():
    d = {"msg": "Olá, seja bem vindo a nossa API",
         "Dados": "Verifique a nossa documentação para mais informações"}
    return d #Retorna um Json dando boas vindas

# Página de acesso a informações  
@app.route("/cadastro/api/info")
def info():
    return """### APIs<br>

As rotas API estão disponíveis em `http://localhost:5001/cadastro/api`.<br>

- **`POST /cadastro ou labs/api/insert`**: Crie um novo usuário. Envie os dados do usuário no corpo da solicitação como um JSON.<br>

- **`GET /cadastro ou labs/api/read`**: Leia todos os usuários registrados.<br>

- **`GET /cadastro ou labs/api/read/<int:id>`**: Leia os detalhes de um usuário específico com base no ID.<br>

- **`PUT /cadastro ou labs/api/update/<int:id>`**: Atualize os detalhes de um usuário existente. Envie os novos dados do usuário no corpo da solicitação como um JSON.<br>

- **`DELETE /cadastro ou labs/api/delete/<int:id>`**: Exclua um usuário do banco de dados com base no ID.""" #Retorna infomações da API (Ainda a ser atualizado)

# Página de acesso ao cadastro do CRUD: 
# CREATE: [POST]
@app.route("/cadastro/api/insert", methods=["POST"])
def create():   
    data = request.json

    # Caso não tenha inserido os dados para o cadastro
    if not data:
        return jsonify({"status": False, "msg": "Dados ausentes no corpo da solicitação"})

    nome = data.get("nome") #Nome do Usuário
    email = data.get("email") #Email do usuário: Necessita ser tipo email
    senha = data.get("senha") #Senha do usuário
    cpf = data.get("cpf") #cpf do usuário: Necessita ser CPF Válido
    telefone = data.get("telefone") #telefone: Indicado ser telefone válido
    id_tipo = data.get("id_tipo") #Tipo de Status: Se é Professor ou Aluno
    atividade = data.get("atividade") #Se o usuário está Ativado ou Desativado

    # Caso um dos valores não forem inseridos
    if nome is None or email is None or senha is None or cpf is None or telefone is None or id_tipo is None or atividade is None:
        return jsonify({"status": False, "msg": "Itens de cadastro são obrigatórios"})

    crud = modelo.BancoCrud() #Objeto instanciado do Model do BancoCrud que nos dá acesso ao cadastro
    result = crud.Create(nome, email, senha, cpf, telefone, id_tipo, atividade)
    return jsonify(result) #Retorna um Json com a validação completa caso tenha funcionado tudo ok


# Página de acesso a todos os dados
# READ: [GET]
@app.route("/cadastro/api/read", methods=["GET"])
def read():
    crud = modelo.BancoCrud() #Objeto instanciado do Model do BancoCrud que nos dá acesso a leitura dos dados
    result = crud.Read()
    return jsonify(result) #Retorna uma lista de Jsons com todos os usuários cadastrados


# Página de acesso a um usuário
# READ_by_ID(ID - Usuário): [GET]
@app.route("/cadastro/api/read/<int:id>", methods=["GET"])
def read_by_id(id):
    crud = controle.VerificacaoCrud() #Objeto instanciado do Controller do BancoCrud que nos dá acesso a leitura e controle de um usário
    result = crud.read_by_id(id)
    return result #Retorna um Json com as informações de um usuário


# Página de acesso para atualizar dados de usuário
# UPDATE: [PUT]
@app.route("/cadastro/api/update/<int:id>", methods=["PUT"])
def update(id):
    data = request.get_json() #Indico que para cadastrar precisa ser do tipo Json
    nome = data.get("nome") #Novo nome para atualização
    email = data.get("email") #Novo email para atualização
    senha = data.get("senha") #Nova senha para atualização
    cpf = data.get("cpf") #Novo cpf para atualização
    telefone = data.get("telefone") #Novo telefone para atualização
    atividade = data.get("atividade") #Nova atividade para ativação "0"(Desativado) ou "1"(Ativado)

    crud = modelo.BancoCrud() #Objeto instanciado do Model do BancoCrud que nos dá acesso ao update dos dados
    result = crud.Update(nome, email, senha, cpf, telefone, atividade, id)
    return jsonify(result) #Retorna uma msg revelando se a atualização foi ou não bem sucedida

# Página de acesso para deletar um usuário [APENAS PARA TESTES!!!!!!]
# Isso é um teste, e faz parte do CRUD
# DELETE: [DELETE]
@app.route("/cadastro/api/delete/<int:id>", methods=["DELETE"])
def delete(id):
    crud = modelo.BancoCrud() #Objeto instanciado do Model do BancoCrud que nos dá acesso ao dados que serão removidos
    result = crud.Delete(id)
    return result #Retorna uma validação indicando se o  usuário foi ou não removido

# Página de acesso que nos permite ativar um usuário a qualquer momento pelo seu ID
# UPDATE: [GET]
@app.route("/cadastro/api/ativar/<int:id>")
def ativar_user(id):
    crud = controle.VerificacaoCrud() #Objeto instanciado do Controller do BancoCrud que nos dá acesso a leitura e controle de ativação de um usário
    result = crud.ativar_usuario(id)
    return jsonify(result) #Retorna a msg indicando se ele está ativado ou se existe ou não

# Página de acesso que nos permite desativar um usuário a qualquer momento pelo seu ID
# UPDATE: [GET]
@app.route("/cadastro/api/desativar/<int:id>")
def desativar_user(id):
    crud = controle.VerificacaoCrud() #Objeto instanciado do Controller do BancoCrud que nos dá acesso a leitura e controle de desativação de um usário
    result = crud.inativar_usuario(id)
    return jsonify(result) #Retorna a msg indicando se ele está desativado ou se existe ou não


# Página de acesso ao cadastro de um lab
# CREATE: [POST]
@app.route("/labs/api/insert", methods=["Post"])
def criar():
    data = request.json

    # Caso não tenha inserido os dados para o cadastro
    if not data:
        return jsonify({"status": False, "msg": "Dados ausentes no corpo da solicitação"})

    nome = data.get("nome") # Nome da Lab
    tipo_status = data.get("tipo_status") #Seu status: (1)Ativo/(2)Inativo

    # Caso um dos dados não for inserido retorna um erro de acesso
    if nome is None or tipo_status is None:
        return jsonify({"status": False, "msg": "Itens de cadastro são obrigatórios"})

    crud = modelo2.LabCrud() #Objeto instanciado do Model do LabCrud que nos dá acesso ao modelo de inserção de um lab
    result = crud.create(nome, tipo_status)
    return jsonify(result) #Retorna se o objeto foi ou não criado


# Página de acesso a leitura de todos os labs existentes
# READ: [GET]
@app.route("/labs/api/read", methods=["GET"])
def ler():
    crud = modelo2.LabCrud() #Objeto instanciado do Model do LabCrud que nos dá acesso ao modelo de leitura de todos os lab
    result = crud.read()
    return jsonify(result) #Retorna uma lista de Jsons informando todos os Labs existentes

# Página de acesso a leitura de um único lab especificado pelo seu ID
# READ_by_ID(ID do lab no banco de dados): [GET]
@app.route("/labs/api/read/<int:id>", methods=["GET"])
def ler_id(id):
    crud = controle2.VerificacaoLab() #Objeto instanciado do Controller do LabCrud que nos dá acesso a leitura de um único lab
    result = crud.Read_By_Id(id)
    return result # Retrona um Json com os dados de um lab, caso ele exista


# Página de acesso a atualização de dados de um lab
# UPDATE: [PUT]
@app.route("/labs/api/update/<int:id>", methods=["PUT"])
def atualizar(id):
    data = request.get_json() #Estou informando que precisa ser um JSON
    nome = data.get("nome") #Novo nome para o LAB
    tipo_status = data.get("tipo_status") #Novo Status para o Lab 1(Ativado) ou 2(Desativado)
    disponibilidade = data.get("disponibilidade") #Nova disponibilidade, ou seja, se o lab está ou não em uso -> 0(Indisponível) ou 1(Disponível)

    crud = modelo2.LabCrud() #Objeto instanciado do Model do LabCrud que nos dá acesso ao modelo de atualização de um lab
    result = crud.update(nome, tipo_status, disponibilidade, id)
    return jsonify(result) #Retorna um Json indicando se o UPDATE foi realizado ou não com sucesso

# Página de acesso que nos permite deletar um lab pelo seu ID
# Isso é um teste, e faz parte do CRUD
# DELETE: [DELETE]
@app.route("/labs/api/delete/<int:id>", methods=["DELETE"])
def deletar(id):
    crud = modelo2.LabCrud() #Objeto instanciado do Model do LabCrud que nos dá acesso ao modelo de deletar um lab
    result = crud.delete(id)
    return result #Retorna um Json informando se foi ou não deletado


# Página de acesso que nos permite ativar um Lab pelo seu ID
# UPDATE: [GET]
@app.route("/labs/api/ativar/<int:id>")
def ativ(id):
    crud = controle2.VerificacaoLab() #Objeto instanciado do Controller do LabCrud que nos dá acesso ao controle de habilitar um lab
    result = crud.ativar_lab(id)
    return jsonify(result) #Retorna um Json que nos informa de sele foi ativado ou não

# Página de acesso que nos permite desativar um Lab pelo seu ID
# UPDATE: [GET]
@app.route("/labs/api/desativar/<int:id>")
def desativ(id):
    crud = controle2.VerificacaoLab() #Objeto instanciado do Controller do LabCrud que nos dá acesso ao controle de desabilitar um lab
    result = crud.desativar_lab(id)
    return jsonify(result) #Retorna um Json que nos informa de sele foi desativado ou não


# Página de acesso que nos permite disponibilizar um Lab pelo seu ID para um usuário cadastrado
# UPDATE: [GET]
@app.route("/labs/api/disponibilizar/<int:id_lab>/<int:id_user>")
def habilitar(id_lab, id_user):
    crud = controle2.VerificacaoLab() #Objeto instanciado do Controller do LabCrud que nos dá acesso ao controle de habilitar um acesso a um lab para um usuário
    result = crud.disponibilizar_lab_para_usuario(id_lab, id_user)
    return jsonify(result) #Retorna um Json informando que o Lab foi ou não disponível para o usuário


# Página de acesso que nos permite disponibilizar um Lab para acesso
# UPDATE: [GET]
@app.route("/labs/api/disponibilizar/<int:id_lab>")
def desabilitar(id_lab):
    crud = controle2.VerificacaoLab() #Objeto instanciado do Controller do LabCrud que nos dá acesso ao controle de habilitar e remover um acesso de um lab a usuário e mantê-lo livre para outro acesso
    result = crud.tornar_lab_disponivel(id_lab)
    return jsonify(result) #Retorna um Json deixando o LAB disponível para qualquer acesso

#Configurações de acesso ao servidor da API
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
