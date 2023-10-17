import sys
import os
sys.path.append(os.getcwd())   # Substitua pelo caminho real

from model import modelo

import mysql.connector

class LabCrud(modelo.BancoCrud):
    '''Class LabCrud que executa o controle do banco Lab
    e recebe o BancoCrud como configurador SQL'''
    def __init__(self) -> None: #Método construtor da classe que não possui retorno e defini os dados do Modelo
        super().__init__() #Método especial que nos permite puxar todos os dados da classe Mãe(BancoCrud)
        self.nome = "" #atributo nome que nos permite definir o nome a ser inserido no banco Lab, e recebe uma string vazia
        self.tipo_status = 0 #Atributo tipo_status que nos permite definir o status do LAB (1[Desabilitado] | 2[Habilitado])
        self.atividade = "" #Atributo atividade que nos permite definir se o a atividade do Lab será Habilitado ou Não
        self.disponibilidade = 0 #Atributo disponibilidade que nos permite definir se um lab está disponível ou não (1[Disponível] | 2[Indisponível])
        self.resposta = "" #Atributo resposta que nos permite definir a resposta de disponibilidade do Lab, ou seja, se ele vai estar disponível ou não

    
    def CheckDuplicate(self, nome: str) -> str: #Método ChackDuplicate que nos permite verificar se os dados não estão duplicados
        try:
            comando_verificar = f'SELECT COUNT(*) FROM Labs WHERE nome="{nome}"' #Comando que nos permite validar a existência do LAB
            self.cursor.execute(comando_verificar) #Faz a execução do verificador
            total_registros = self.cursor.fetchone()[0] #Puxa o dado de verificação
            return total_registros > 0
        except mysql.connector.Error as err: #Erro de execução SQL
            print(f"Erro ao verificar duplicidade: {err}")
            return False


    def create(self, nome: str, tipo_status: int) -> dict: #Método CREATE que nos permite criar e cadastrar um Lab
        try:
            if self.CheckDuplicate(nome): #Verifica se o Lab já não foi criado
                return {"status": False, "response": 403, "msg": "Registro já existe"}

            if not nome or not tipo_status: #Caso o usuário não insira o nome e nem o tipo_status
                  return {"status": False, "response": 403, "msg": "Itens de cadastro são obrigatórios"}

            self.nome = nome #O atributo nome vai receber o parâmetro nome, que é o valor inserido no cadastro
            self.tipo_status = tipo_status #O atributo tipo_status vai receber o parâmetro tipo_status que é o status recebido, ou seja, Habilitado(1), Desabilitado(0)
            self.disponibilidade = 0

            try:
                if tipo_status == 1: #Se o o status inserido for 1, ele estará ativado
                    self.atividade = "Ativo"
                elif tipo_status == 2: #Se o status inserido for 2, ele estará desativado
                    self.atividade = "Desativado"
                else: #Caso contrário, se for um valor inválido, não será inserido no banco e retornará uma msg de erro
                    return {"status": False, "response": 403, "msg": "Valor Inexistente para Atividade do lab"}
            
                if self.disponibilidade == 0: #Se o Lab estiver indisponível que por padrão será sempre após o uso do LAB, ele será retornado como 0
                    self.resposta = "Indisponível"
                elif self.disponibilidade == 1: #Se o Lab estiver disponível por padrão ele retronará 1
                    self.resposta = "Disponível"
                else: #Caso contrário, ele retornará um erro e não executará os dados no Banco
                     return {"status": False, "response": 403, "msg": "Valor Inexistente para Disponibilidade do lab"}
            except ValueError: #Csaso haja um erro de tipagem
                return {"status": False, "response": 500, "msg": "Valor deve ser um número válido"}

            #Vai fazer a inserção dos dados no banco de dados
            comando = f'INSERT INTO Labs(nome, tipo_status, disponibilidade) VALUES("{nome}", {tipo_status}, {self.disponibilidade})'
            self.cursor.execute(comando) #Executa o comando
            self.conex.commit() #Atera o registro no banco
            return {"status": True, "response": 200, "msg": "Lab Cadastrado com sucesso"}
        except mysql.connector.Error as err: #Erro de execução MySQL    
            return {"status": False, "response": 500, "msg": f"Erro ao cadastrar o Lab: {err}"}
    

    def read(self) -> dict: #Método read que nos permite e retorna uma lista de Jsons de todos os labs existentes
        try:
            #Seleciona o comando que lerá todos os labs
            comando = f'SELECT * FROM Labs'
            self.cursor.execute(comando) #Executa o comando
            resultado = self.cursor.fetchall() #Pucha todos os dados registrados
            if not resultado: #Se o banco estiver vazio
                return {"status": False, "response": 404, "msg": "Banco sem dados", "data": []}
            else: #Caso contrário, se existir dados no banco
                data = [] #Lista/Array que vai receber todos os dados do banco 
                for resul in resultado:
                    if resul[2] == 2: #Se o status inserido for 2, ele estará desativado
                        self.atividade = "Desativado"
                    elif resul[2] == 1: #Se o status inserido for 1, ele estará ativado
                        self.atividade = "Ativado"
                    else: #Caso contrário retorna um erro de inserção
                         return {"status": False, "response": 403, "msg": "Valor Inexistente para Atividade do Lab"}

                    if resul[3] == 0: #Se a disponibilidade inserido for 0, ele estará indisponível
                        self.resposta = "Indisponível"
                    elif resul[3] == 1: #Se a disponibilidade inserido for 1, ele estará disponível
                        self.resposta = "Disponível"
                    else: #Caso contrário retorna uma mensagem de erro
                        return {"status": False, "response": 403, "msg": "Valor Inexistente para Disponibilidade do Lab"}
                    data.append({"ID": resul[0], "Nome": resul[1], "Atividade": resul[2], "Status de Atividade": self.atividade, "Disponibilidade": resul[3], "Status de Diponibilidade": self.resposta}) #A lista adiciona o Json do respectivo dado
                return {"status": True, "response": 200, "data": data}
        except mysql.connector.Error as err: #Erro de execução MySQL
            return {"status": False, "response": 500, "msg": f"Erro ao ler dados: {err}"}


    def update(self, update_nome: str, update_tipo_status: int, update_disponibilidade: int, id: int) -> dict: #Método update que nos permite alterar os dados de um lab por meio do Id
        try:
            # Verificar se o usuário com o ID fornecido existe
            comando_verificar_existencia = f'SELECT COUNT(*) FROM Labs WHERE id={id}'
            self.cursor.execute(comando_verificar_existencia)
            total_registros = self.cursor.fetchone()[0]
            if total_registros == 0: #Se não houver registros, retorna um erro
                return {"status": False, "response": 404, "msg": "Usuário não encontrado"}
            
            self.nome = update_nome #Atributo nome recebe o update_nome que será o nome alterado
            self.tipo_status = update_tipo_status #Atributo tipo_status recebe update_tipo_status que será o status[1 ou 2] de ativação do Lab
            self.disponibilidade = update_disponibilidade #Atributo disponibilidade que recebe update_disponibilidade[0 ou 1] que nos permite verificar a diposnibilidade dos Labs 

            if update_tipo_status not in [1, 2]: #Se o novo tipo_status inserido não for 1 e nem 2
                return {"status": False,"response": 403, "msg": "Valor inválido para Status de atividade"}

            if update_disponibilidade not in [0, 1]: #Se a nova disponibilidade inserida não for 0 e nem 1
                return {"status": False, "response": 403, "msg": "Valor inválido para Disponibilidade"}

            #Fará a atualização de registro de LABS
            comando = f'UPDATE Labs SET nome="{update_nome}", tipo_status={update_tipo_status}, disponibilidade={update_disponibilidade} WHERE id={id}'
            self.cursor.execute(comando) #Executa o comando
            self.conex.commit() #Altera o registro no Banco de dados

            return {"status": True, "response": 200, "msg": "Dados atualizados com sucesso"}
        except mysql.connector.Error as err: #Erro de MySQL
            return {"status": False, "response": 500, "msg": f"Erro ao atualizar dados: {err}"}


    def delete(self, id: int) -> dict: #Método delete que nos permite remover um lab no registro de banco de dados e retorna um dict de alteração
        try:
            comando = f'DELETE FROM Labs WHERE id={id}' #Comando SQL de execução
            self.cursor.execute(comando) #Executa o comando
            self.conex.commit() #Altera o registro no Banco de dados
            
            return {"status": True, "response": 200, "msg": "Registro deletado com sucesso"}
        except mysql.connector.Error as err: #Erro de execução MySQL
            return {"status": False, "response": 500, "msg": f"Erro ao deletar registro: {err}"}


if __name__ == "__main__":
    lab1 = LabCrud()
    #print(lab1.create("Sala", 1))
    #print(lab1.read())
    #print(lab1.update("Sala", 2, 0, 2))
    #print(lab1.read())
    #print(lab1.delete(1))
