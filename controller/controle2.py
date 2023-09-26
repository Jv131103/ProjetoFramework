import sys
import os
sys.path.append(os.getcwd())   # Substitua pelo caminho real

from model import modelo2
import mysql.connector

class VerificacaoLab(modelo2.LabCrud):

    def verificar_usuario_existe(self, id_usuario: int) -> bool: #Método verificar_usuario_existe, que verifica se um usuário existe por meui de seu ID
        try:
            # Verifique se o usuário existe na tabela de usuários
            comando_verificacao = f'SELECT COUNT(*) FROM Usuario WHERE id={id_usuario}'
            self.cursor.execute(comando_verificacao) #Executa o comando
            resultado = self.cursor.fetchone() #Puxa um dado inserido

            # Se o resultado for maior que 0, significa que o usuário existe
            return resultado[0] > 0
        except mysql.connector.Error as err: #Erro de SQL
            # Trate qualquer erro de banco de dados aqui
            print(f"Erro ao verificar a existência do usuário: {err}")
            return False


    def _elemento_existe(self, id: int) -> int: #Método protegido elemento_existe que verifica se um lab existe por meio de seu id 
        try:
            comando = f'SELECT COUNT(*) FROM Labs WHERE id={id}' #Valida e verifica existencia do lab
            self.cursor.execute(comando) #Executa o comando de validação
            resultado = self.cursor.fetchone()[0] #Pega o dado retornado
            return resultado > 0
        except mysql.connector.Error as err: #Erro de execução MySQL
            return False
    
    def Read_By_Id(self, id: int) -> dict: #método Read_By_Id que nos permite ler e verificar dados de um Lab e retorna um Dict
        try:
            if self._elemento_existe(id): #Verifica a existência do elemento
                comando = f'SELECT * FROM Labs WHERE id={id}' #Execução SQL que puxa todos os dados de Lab por meio de seu ID
                self.cursor.execute(comando) #Executa o comando
                resultado = self.cursor.fetchone() #Extrai os dados do Lab
                if resultado: #Se existir dados
                    if resultado[2] == 2: #Caso o Lab esteja desativado, o valor padrão é 2
                        self.atividade = "Desativado"
                    elif resultado[2] == 1: #Caso o Lab esteja ativado, o valor padrão é 1
                        self.atividade = "Ativado"
                    else: #Caso contrário, retornará um erro
                        return {"status": False, "msg": "Valor Inexistente para Atividade do LAB"}

                    if resultado[3] == 0: #Caso o Lab esteja indisponível para o usuário o seu valor padrão é 0
                        self.disponibilidade = "Indisponível"
                    elif resultado[3] == 1: #Caso o Lab esteja disponível para o usuário o valor padrão é 1
                        self.disponibilidade = "Disponível"
                    else: #Caso contrário, retorna um erro
                        return {"status": False, "msg": "Valor Inexistente para Disponibilidade do LAB"}

                    #Retorna o dicionário com os dados
                    data = {"ID": resultado[0], "Nome": resultado[1], "Atividade": resultado[2], "Status de Atividade": self.atividade, "Disponibilidade": self.disponibilidade, "Status de Disponibilidade": self.disponibilidade}
                    return {"status": True, "data": data}
                else: #Caso não exista dados, ele retorna que nenhum dado foi encontrado
                    return {"status": False, "msg": f"Nenhum dado encontrado para o ID {id}"}
            else: #Caso o elemento não exista, retorna um erro
                return {"status": False, "msg": "Elemento inexistente"}
        except mysql.connector.Error as err: #Erro que pode ocorrer por meio de banco de dados
            return {"status": False, "msg": f"Erro ao ler dados: {err}"}
    
    def desativar_lab(self, id_lab: int) -> dict: #Método desativar_lab que nos permite inativar um Lab por meio de seu ID
        try:
            if self._elemento_existe(id_lab): #Se o elemento existir
                # Obtenha o ID de Uso_Lab correspondente ao status "desativado" (0)
                id_uso_lab_desativado = 2

                # Atualize a coluna "tipo_status" na tabela "Labs" com o ID de Uso_Lab correto
                comando = f'UPDATE Labs SET tipo_status={id_uso_lab_desativado} WHERE id={id_lab}'
                self.cursor.execute(comando) #Executa o comando
                self.conex.commit() #Atualiza os dados no registro do Banco de Dados
                return {"status": True, "msg": f"Lab de ID {id_lab} desativado com sucesso"}
            else: #Caso não haja dados ele retorna um Msg indicando que o elemento não existe
                return {"status": False, "msg": "Elemento inexistente"}
        except mysql.connector.Error as err: #Erro de execução MySQL
            return {"status": False, "msg": f"Erro ao desativar Lab: {err}"}

    def ativar_lab(self, id_lab: int) -> dict: #Método desativar_lab que nos permite ativar um Lab por meio de seu ID e retorna um Dict
        try:
            if self._elemento_existe(id_lab): #Se o elemento existir
                # Obtenha o ID de Uso_Lab correspondente ao status "ativado" (1)
                id_uso_lab_ativado = 1

                # Atualize a coluna "tipo_status" na tabela "Labs" com o ID de Uso_Lab correto
                comando = f'UPDATE Labs SET tipo_status={id_uso_lab_ativado} WHERE id={id_lab}'
                self.cursor.execute(comando) #Executa o comando SQL
                self.conex.commit() #Atualiza o registro no Bnaco de dados
                return {"status": True, "msg": f"Lab de ID {id_lab} ativado com sucesso"}
            else: #Caso não haja elementos, retorna um msg de erro de elemento não encontrado
                return {"status": False, "msg": "Elemento inexistente"}
        except mysql.connector.Error as err: #Erro de execução MySQL
            return {"status": False, "msg": f"Erro ao ativar Lab: {err}"}

    def disponibilizar_lab_para_usuario(self, id_lab: int, id_usuario: int) -> dict: #Método disponibilizar_lab_para_usuario, que nos permite liberar um Lab para um usuário específico
        try:
            # Verifique se o laboratório existe e está disponível
            comando_verificacao_lab = f'SELECT disponibilidade FROM Labs WHERE id={id_lab}' #Execução do banco de dados
            self.cursor.execute(comando_verificacao_lab) #Executa o SQL
            disponibilidade_lab = self.cursor.fetchone() #Extrai os dados

            if not disponibilidade_lab: #Se o lab não existir
                return {"status": False, "msg": f"Lab de ID {id_lab} não existe"}
            
            if disponibilidade_lab[0] == 0: #Se o lab não estiver disponível
                return {"status": False, "msg": f"Lab de ID {id_lab} não está disponível"}

            # Verifique se o usuário existe
            if not self.verificar_usuario_existe(id_usuario): 
                return {"status": False, "msg": f"Usuário de ID {id_usuario} não existe"}

            # Marque o laboratório como indisponível
            comando_atualizacao_lab = f'UPDATE Labs SET disponibilidade=0 WHERE id={id_lab}' #Registra para o uusário especificado
            self.cursor.execute(comando_atualizacao_lab) #Executa o UPDATE MySQL
            self.conex.commit() #Registra no banco de dados
            
            return {"status": True, "msg": f"Lab de ID {id_lab} disponibilizado para usuário de ID {id_usuario}"}
        except mysql.connector.Error as err:
            return {"status": False, "msg": f"Erro ao disponibilizar lab: {err}"}

    def tornar_lab_disponivel(self, id_lab: int) -> dict: #Método tornar_lab_disponivel, que nos permite liberar um acesso a um lab por meio de seu ID
        try:
            # Verifique se o laboratório existe e não está disponível
            comando_verificacao = f'SELECT disponibilidade FROM Labs WHERE id={id_lab}'
            self.cursor.execute(comando_verificacao) #Executa o comando
            disponibilidade = self.cursor.fetchone() #Puxa os dados
            if not disponibilidade: #Se o Lab existir
                return {"status": False, "msg": f"Lab de ID {id_lab} não existe"}

            if disponibilidade[0] == 1: #Se o lab já estiver disponível
                return {"status": False, "msg": f"Lab de ID {id_lab} já está disponível"}

            # Marque o laboratório como disponível
            comando = f'UPDATE Labs SET disponibilidade=1 WHERE id={id_lab}'
            self.cursor.execute(comando) #Executa o comando SQL
            self.conex.commit() #Altera o registro do banco de dados
            return {"status": True, "msg": f"Lab de ID {id_lab} tornou-se disponível novamente"}
        except mysql.connector.Error as err: #Erro MySQL
            return {"status": False, "msg": f"Erro ao tornar lab disponível: {err}"}

if __name__ == "__main__":
    labx = VerificacaoLab()
    #print(labx.create("labx", 1))
    print(labx.Read_By_Id(1))
    print(labx.disponibilizar_lab_para_usuario(2, 3))
    #print(labx.read())
