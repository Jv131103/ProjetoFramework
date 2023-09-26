import mysql.connector
from flask import jsonify

class BancoCrud:
    '''Classe BancoCrud que faz um cadastro de um usuário 
    no banco de dados'''
    def __init__(self) -> None: #Método construtor que fará a conexão com o Banco de Dados
        self.conex = mysql.connector.connect(
            host="localhost",
            user="muniz",
            password="lmds2003",
            database="Projeto"
        ) #Faz a conexão com o MySQL
    
        self.cursor = self.conex.cursor() #Atributo cursor que recebe a conexão do Banco de dados
        self.nome = ""  #Atributo nome que é iniciado como uma stringa vazia, que vai nos permitir inserir o nome do usário no cadastro
        self.email = "" #Atributo email que é iniciado como uma string vazia, que vai nos permitir inserir o email do usuário no cadastro
        self.senha = "" #Atributo senha que é iniciado como uma string vazia, que vai nos permitir inserir a senha do usuário no cadastro
        self.cpf = "" #Atributo senha que é iniciado como uma string vazia, que vai nos permitir inserir o CPF do usuário no cadastro
        self.telefone = ""
        self.id_tipo = 0
        self.tipo = 0
        self.atividade = ""

    
    def CheckDuplicate(self, nome: str) -> str:
        try:
            comando_verificar = f'SELECT COUNT(*) FROM Usuario WHERE nome="{nome}"'
            self.cursor.execute(comando_verificar)
            total_registros = self.cursor.fetchone()[0]
            return total_registros > 0
        except mysql.connector.Error as err:
            print(f"Erro ao verificar duplicidade: {err}")
            return False


    def Create(self, nome: str, email: str, senha: str, cpf: str, telefone: str, id_tipo: int, atividade: str) -> dict:
        try:
            if self.CheckDuplicate(nome):
                return {"status": False, "msg": "Registro já existe"}

            if not nome or not email or not senha or not cpf or not telefone or not id_tipo:
                return {"status": False, "msg": "Itens de cadastro são obrigatórios"}
            
            self.nome = nome
            self.email = email
            self.senha = senha
            self.cpf = cpf
            self.telefone = telefone
            self.atividade = atividade #Digite "0" para Desativar e "1" para ativar
            
            try:
                id_tipo = int(id_tipo)
                if id_tipo == 1:
                    self.tipo = 1
                elif id_tipo == 2:
                    self.tipo = 2
                else:
                    return {"status": False, "msg": "Valor Inexistente para tipo"}
                if atividade == "0":
                    self.atividade = "Desativado"
                elif atividade == "1":
                    self.atividade = "Ativado"
                else:
                    return {"status": False, "msg": "Valor Inexistente para Atividade"}
            except ValueError:
                return {"status": False, "msg": "Valor deve ser um número válido"}

            comando = f'INSERT INTO Usuario(nome, email, senha, cpf, telefone, id_tipo, atividade) VALUES("{nome}", "{email}", "{senha}", "{cpf}", "{telefone}", {id_tipo}, "{atividade}")'
            self.cursor.execute(comando)
            self.conex.commit()
            
            return {"status": True, "msg": "Cadastro realizado com sucesso"}
        except mysql.connector.Error as err:
            return {"status": False, "msg": f"Erro ao cadastrar: {err}"}


    def Read(self) -> dict:
        try:
            comando = f'SELECT * FROM Usuario'
            self.cursor.execute(comando)
            resultado = self.cursor.fetchall()
            
            if not resultado:
                return {"status": True, "msg": "Banco sem dados", "data": []}
            else:
                data = []
                for resul in resultado:
                    if resul[6] == 1:
                        self.tipo = "professor"
                    elif resul[6] == 2:
                        self.tipo = "aluno"
                    elif resul[6] == 3:
                        self.tipo = "admin"
                    else:
                        return {"status": False, "msg": "Valor Inexistente para tipo"}
                    if resul[7] == "0":
                        self.atividade = "Desativado"
                    elif resul[7] == "1":
                        self.atividade = "Ativo"
                    else:
                        return {"status": False, "msg": "Valor Inexistente para atividade"}
                    data.append({"ID": resul[0], "Nome": resul[1], "Email": resul[2], "cpf": resul[4], "telefone": resul[5], "id_tipo": resul[6], "Profissão": self.tipo, "Atividade": self.atividade})
                return {"status": True, "data": data}
        except mysql.connector.Error as err:
            return {"status": False, "msg": f"Erro ao ler dados: {err}"}


    def Update(self, update_nome: str, update_email: str, update_senha: str, update_cpf: str, update_telefone: str, update_atividade: str, id: int) -> dict:
        try:
            # Verificar se o usuário com o ID fornecido existe
            comando_verificar_existencia = f'SELECT COUNT(*) FROM Usuario WHERE id={id}'
            self.cursor.execute(comando_verificar_existencia)
            total_registros = self.cursor.fetchone()[0]
            if total_registros == 0:
                return {"status": False, "msg": "Usuário não encontrado"}
            
            self.nome = update_nome
            self.email = update_email
            self.senha = update_senha
            self.cpf = update_cpf
            self.telefone = update_telefone
            self.atividade = update_atividade  # Digite "0" para inativar e "1" para Ativar

            # Verificar se o valor de atividade é válido
            if update_atividade not in ["0", "1"]:
                return {"status": False, "msg": "Valor inválido para atividade"}

            comando = f'UPDATE Usuario SET nome="{update_nome}", email="{update_email}", senha="{update_senha}", cpf="{update_cpf}", telefone="{update_telefone}", atividade="{update_atividade}" WHERE id={id}'
            self.cursor.execute(comando)
            self.conex.commit()

            return {"status": True, "msg": "Dados atualizados com sucesso"}
        except mysql.connector.Error as err:
            return {"status": False, "msg": f"Erro ao atualizar dados: {err}"}


    def Delete(self, id: int) -> dict:
        try:
            comando = f'DELETE FROM Usuario WHERE id={id}'
            self.cursor.execute(comando)
            self.conex.commit()
            
            return {"status": True, "msg": "Registro deletado com sucesso"}
        except mysql.connector.Error as err:
            return {"status": False, "msg": f"Erro ao deletar registro: {err}"}


    def fechar(self) -> None:
        self.cursor.close()
        self.conex.close()


if __name__ == "__main__":
    b = BancoCrud()
    #print(b.Create("nome", "email", "senha", "cpf", "telefone", 1, "1"))
    #print(b.Read())   
    #print(b.Update("nome", "email", "senha", "cpf", "telefone", "0", 1)) 
    #print(b.Delete(1))
    #print(b.Read()) 
