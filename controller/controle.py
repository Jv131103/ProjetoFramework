import sys
sys.path.append('/home/joao/Documentos/ProjetoQuinta/')  # Substitua pelo caminho real


from model import modelo
import mysql.connector
#import bcrypt
#import hashlib

class VerificacaoCrud(modelo.BancoCrud):
    '''Classe de verificação de dados do CRUD que herda
    os valores do Banco de Dados'''
    def __init__(self) -> None: #Método construtor que vai herdar de BancoCrud
        super().__init__() #Pega todo o método mãe de BancoCrud
    
    def _elemento_existe(self, id: int) -> int: #Método que vai verificar se os dados do cliente existem na tabela por meio de seu id
        try:
            comando = f'SELECT COUNT(*) FROM Usuario WHERE id={id}' #Comando do Banco que fará a validação
            self.cursor.execute(comando) #Comando que vai executar o comando
            resultado = self.cursor.fetchone()[0] #Comando que vai puxar o resultado da consulta
            return resultado > 0
        except mysql.connector.Error as err:
            return False
        
    def read_by_id(self, id: int) -> dict: #Método que vai verificar os dados de um usuário pelo seu id e retorna um dict
        try:
            if self._elemento_existe(id): # Se esse usuário existir
                comando = f'SELECT * FROM Usuario WHERE id={id}' #Comando do banco de dados que vai puxar o usuário
                self.cursor.execute(comando) #Vai executar o comando
                resultado = self.cursor.fetchone() #Vai puxar todos os dados referentes ao usuário
                if resultado: #Se tiver dados
                    if resultado[6] == 1: #Se o usuário digitar a opção 1, será um professor
                        self.tipo = "professor"
                    elif resultado[6] == 2: #Se o usuário digitar a opção 2, será um aluno
                        self.tipo = "aluno"
                    else: #Caso contrário, não será encontrado no Banco de dados
                        return {"status": False, "msg": "Valor Inexistente para tipo"}
                    
                    if resultado[7] == "0": #Caso ele eteja desativado o valor padrão é "0"
                        self.atividade = "Desativado"
                    elif resultado[7] == "1": #Caso ativado o valor padrão é "1"
                        self.atividade = "Ativado"
                    else: #Caso nehum e nem outro, retorna um erro
                        return {"status": False, "msg": "Valor Inexistente para Atividade"}
                    #Leitura de todos os dados do usuário
                    data = {"ID": resultado[0], "Nome": resultado[1], "Email": resultado[2], "Cpf": resultado[4], "Telefone": resultado[5], "Tipo": resultado[6], "Profissão": self.tipo, "Atividade": self.atividade}
                    return {"status": True, "data": data}
                else: #Caso não tenha registros, retorna que não existe nehum dado
                    return {"status": False, "msg": f"Nenhum dado encontrado para o ID {id}"}
            else: #Caso o elemento não exista, retorna um erro de dados inexistentes
                return {"status": False, "msg": "Elemento inexistente"}
        except mysql.connector.Error as err: #Este caso, é para caso um erro seja gerado por parte da execução do Banco de Dados
            return {"status": False, "msg": f"Erro ao ler dados: {err}"}


    def inativar_usuario(self, id: int) -> dict: #Método inativar_usuário que nos permite por meio do ID de usuário, inativá-lo e não permitir seu acesso
        try:
            if self._elemento_existe(id): #Verifica se o usuário existe no Banco de dados
                # Verifique se o usuário já está desativado
                comando_verificacao = f'SELECT atividade FROM Usuario WHERE id={id}'
                self.cursor.execute(comando_verificacao) #Executa o comando
                resultado_verificacao = self.cursor.fetchone() #Puxa os dados

                if resultado_verificacao: #Vai verificar se já está desativado
                    status_atual = resultado_verificacao[0]

                    if status_atual == "0":
                        return {"status": False, "msg": f"Usuário {id} já está desativado"}

                # Caso o usuário não esteja desativado, desative-o
                comando = f'UPDATE Usuario SET atividade="0" WHERE id={id}'
                self.cursor.execute(comando)
                self.conex.commit()
                return {"status": True, "msg": f"Usuário {id} inativado com sucesso"}
            else: #Caso não tenha dados
                return {"status": False, "msg": "Elemento inexistente"}
        except mysql.connector.Error as err: #Erros de execução MySQL
            return {"status": False, "msg": f"Erro ao inativar usuário: {err}"}


    def ativar_usuario(self, id: int) -> dict: #Método ativar_usuario que nos permite ativar um usuário cadastrado por meio do seu id
        try:
            if self._elemento_existe(id): #Se os dados existirem
                # Verifique se o usuário já está ativo
                comando_verificacao = f'SELECT atividade FROM Usuario WHERE id={id}' #Chamam o comando
                self.cursor.execute(comando_verificacao) #Executa o comando
                resultado_verificacao = self.cursor.fetchone() #Puxa um valor

                if resultado_verificacao: #Verifica se o usuário já está ativado
                    status_atual = resultado_verificacao[0]

                    if status_atual == "1":
                        return {"status": False, "msg": f"Usuário {id} já está ativo"}

                # Caso o usuário não esteja ativo, ative-o
                comando = f'UPDATE Usuario SET atividade="1" WHERE id={id}'
                self.cursor.execute(comando)
                self.conex.commit()
                return {"status": True, "msg": f"Usuário {id} ativado com sucesso"}
            else: #Caso não encontre dados
                return {"status": False, "msg": "Elemento inexistente"}
        except mysql.connector.Error as err: #Erro de execução do MySQL
            return {"status": False, "msg": f"Erro ao ativar usuário: {err}"}


if __name__ == "__main__":
    x = VerificacaoCrud()
    print(x.Read())
    print(x.read_by_id(2))
    print(x.inativar_usuario(2))
    print(x.ativar_usuario(2))
    x.fechar()

