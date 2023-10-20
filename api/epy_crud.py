import sys
import os
sys.path.append(os.getcwd()) 
from flask import Flask, request
from model import modelo
from model import modelo2
from controller import controle
from controller import controle2
import jwt
import mysql.connector
import datetime

class MyAPI:
    def __init__(self):
        self.jwt = None


    def GerarJson(self, status, response, msg, valor):
        d = {"status": status,
            "response": response,
            "msg": msg,
            "dado": valor}
        return d


    def CreateUser(self, nome, email, senha, cpf, telefone, id_tipo, atividade="1"): #Professor e Aluno
        try:
            # Caso um dos valores não forem inseridos
            if nome is None or email is None or senha is None or cpf is None or telefone is None or id_tipo is None or atividade is None:
                return self.GerarJson(False, 403, "Itens de cadstro são obrigatórios", {"nome": nome, "email": email, "senha": senha, "cpf": cpf, "telefone": telefone, "atividade": atividade})
        
            crud = modelo.BancoCrud()
            result = crud.Create(nome, email, senha, cpf, telefone, id_tipo, atividade)
            if result is not None:
                if result["status"]:
                    if id_tipo == 1:
                        return self.GerarJson(True, 200, "Dados Criados com sucesso!", "ALUNO")
                    elif id_tipo == 2:
                        return self.GerarJson(True, 200, "Dados Criados com sucesso!", "PROF")
                    elif id_tipo == 3:
                        return self.GerarJson(True, 200, "Dados Criados com sucesso!", "ADMIN")
                elif result["status"] is False and result["msg"] == "Registro já existe":
                    return self.GerarJson(False, 403, "Registro já existe", None)
                elif result["status"] is False and result["msg"] == "Valor Inexistente para tipo":
                    return self.GerarJson(False, 403, "Valor Inexistente para tipo", id_tipo)
            else:
                return self.GerarJson(False, 500, "Erro inesperado ao cadastrar usuário: retorno inesperado", None)
        except mysql.connector.Error as err:
            return self.GerarJson(False, 500, f"Erro de MySQL ao cadastrar usuário: {err}", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro inesperado em cadastrar usuário: {e}", None)


    def Login(self, email, senha): #Professor, Aluno, Admin
        control = controle.VerificacaoCrud()
        if control.ValidarEmailESenha(email, senha):

            if control.VerificarAtivo(email) != "1":
                return self.GerarJson(False, 401, "Acesso não autorizado, Usuário desativado", None)

            if control.ValidarEmailESenha(email, senha):
                # Configuração das informações que você deseja incluir no token
                payload = {
                    'email': email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expira em 1 dia
                }

                # Chave secreta usada para assinar o token
                chave_secreta = '123'

                # Gera o token
                token = jwt.encode(payload, chave_secreta, algorithm='HS256')

                value = control.BuscarTipoPorEmail(email)
                if value[0] == 1:
                    self.jwt = token
                    return self.GerarJson(True, 200, "Login bem-sucedido", {'token': token, "tipo": "Professor", "email_user": email})
                elif value[0] == 2:
                    self.jwt = token
                    return self.GerarJson(True, 200, "Login bem-sucedido", {'token': token, "tipo": "Aluno", "email_user": email})
                elif value[0] == 3:
                    self.jwt = token
                    return self.GerarJson(True, 200, "Login bem-sucedido", {'token': token, "tipo": "Admin", "email_user": email})
                else:
                    return self.GerarJson(False, 401, "Usuário não cadastrado", email)
            else:
                return self.GerarJson(False, 401, "Credenciais inválidas", None)
        else:
            return self.GerarJson(False, 404, "Usuário não cadstrado", {"email": email, "senha": senha})


    def Read_all(self, token): #Admin
        chave_secreta = '123'
        try:
            control = controle.VerificacaoCrud()
            # Verifica o token
            payload = jwt.decode(token, chave_secreta, algorithms=['HS256'])
            # Agora você pode acessar o email do usuário
            email_do_usuario = payload.get('email')

            # Verifica se o usuário é um administrador (ou implemente sua própria lógica de verificação)
            if control.VerificarAdmin(email_do_usuario) == 3:
                # Lógica para ler todos os dados (substitua isso com a sua própria lógica)
                crud = modelo.BancoCrud()
                result = crud.Read()
                return self.GerarJson(True, 200, "Operação bem-sucedida", result['data'])
            else:
                return self.GerarJson(False, 403, "Acesso proibido para usuários não administradores", None)
        except jwt.ExpiredSignatureError:
            return self.GerarJson(False, 401, "Token expirado", None)
        except jwt.InvalidTokenError:
            return self.GerarJson(False, 401, "Token inválido", None)
        except Exception as e:
            return self.GerarJson(False, 401, "Um erro inesperado aconteceu ao verificar usuários: e", None)


    def Read_ID(self, id, token): #Admin, professor daquele ID e aluno daquele ID
        chave_secreta = '123'
        try:
            control = controle.VerificacaoCrud()
            # Verifica o token
            payload = jwt.decode(token, chave_secreta, algorithms=['HS256'])

            # Agora você pode acessar o email do usuário
            email_do_usuario = payload.get('email')

            # Verifica se o usuário tem permissão para acessar o recurso identificado pelo ID
            if control.BuscarIdPorEmail(email_do_usuario) == id or control.VerificarAdmin(email_do_usuario) == 3:
                # Lógica para ler os dados associados ao ID (substitua isso com a sua própria lógica)
                crud = controle.VerificacaoCrud() #Objeto instanciado do Controller do BancoCrud que nos dá acesso a leitura e controle de um usuário
                result = crud.read_by_id(id)
                return self.GerarJson(True, 200, "Operação bem-sucedida", result['data'])
            else:
                return self.GerarJson(False, 403, "Acesso proibido para este recurso", None)
        except jwt.ExpiredSignatureError:
            return self.GerarJson(False, 401, "Token expirado", None)
        except jwt.InvalidTokenError:
            return self.GerarJson(False, 401, "Token inválido", None)
    

    def Upgrade_User(self, id, nome, email, senha, telefone, atividade="1"): #Admin, professor daquele ID e Usuário daquele ID
        try:
            # Caso um dos valores não forem inseridos
            if nome is None or email is None or senha is None or telefone is None or atividade is None:
                return self.GerarJson(False, 403, "Itens de cadstro são obrigatórios", {"nome": nome, "email": email, "senha": senha, "telefone": telefone, "atividade": atividade})

            crud = modelo.BancoCrud()
            result = crud.Update(nome, email, senha, telefone, atividade, id)
            if result["status"] == False and result["msg"] == "Valor inválido para atividade":
                return self.GerarJson(False, 403, "Valor inválido para atividade", atividade)
            if result["status"] == True:
                return self.GerarJson(True, 200, "Dados Atualizados com sucesso!", {"nome": nome, "email": email})
            elif result["status"] == False and result["msg"] == "Usuário não encontrado":
                return self.GerarJson(False, 404, "Usuário não encontrado", None)
                
        except mysql.connector.Error as err:
            return self.GerarJson(False, 500, f"Erro de MySQL ao Atualizar usuário: {err}", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro inesperado em atualizar usuário: {e}", None)


    def AtivarUser(self, id, token): #Admin
        chave_secreta = "123"
        try:
            control = controle.VerificacaoCrud()
            # Verifica o token
            payload = jwt.decode(token, chave_secreta, algorithms=['HS256'])

            # Agora você pode acessar o email do usuário
            email_do_usuario = payload.get('email')

            # Verifica se o usuário é um administrador (ou implemente sua própria lógica de verificação)
            if control.VerificarAdmin(email_do_usuario) == 3:
                result = control.ativar_usuario(id)
                return result
            else:
                return self.GerarJson(False, 401, f"Acesso não autorizado para usuário {email_do_usuario}", None)
        except jwt.ExpiredSignatureError:
            return self.GerarJson(False, 401, "Token expirado", None)
        except jwt.InvalidTokenError:
            return self.GerarJson(False, 401, "Token inválido", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro interno ao ativar usuário: {e}", id)



    def Desativar(self, id, token): #Admin
        chave_secreta = '123'
        try:
            control = controle.VerificacaoCrud()
            # Verifica o token
            payload = jwt.decode(token, chave_secreta, algorithms=['HS256'])

            # Agora você pode acessar o email do usuário
            email_do_usuario = payload.get('email')
            # Verifica se o usuário tem permissão para acessar o recurso identificado pelo ID
            if control.BuscarIdPorEmail(email_do_usuario) == id or control.VerificarAdmin(email_do_usuario) == 3:
                # Lógica para ler os dados associados ao ID (substitua isso com a sua própria lógica)
                resul = control.inativar_usuario(id)
                return resul
            else:
                return self.GerarJson(False, 403, "Acesso proibido para este recurso", None)
        except jwt.ExpiredSignatureError:
            return self.GerarJson(False, 401, "Token expirado", None)
        except jwt.InvalidTokenError:
            return self.GerarJson(False, 401, "Token inválido", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro interno ao ativar usuário: {e}", id)


    def CadastrarLab(self, nome, token, tipo_status=1): #Se quiser desativar, digite 2 em tipo_status    #Admin
        chave_secreta = '123'
        try:
            if nome is None or tipo_status is None:
                return self.GerarJson(False, 401, "Dados não inseridos", {"nome": nome, "tipo_status": tipo_status})
            control = controle.VerificacaoCrud()
            # Verifica o token
            payload = jwt.decode(token, chave_secreta, algorithms=['HS256'])

            # Agora você pode acessar o email do usuário
            email_do_usuario = payload.get('email')
            # Verifica se o usuário é um administrador (ou implemente sua própria lógica de verificação)
            if control.VerificarAdmin(email_do_usuario) == 3:
                crud = modelo2.LabCrud()
                result = crud.create(nome, tipo_status)
                if result['status'] == False and result['msg'] == "Valor Inexistente para Atividade do lab":
                    return self.GerarJson(False, 500, "Valor Inexistente para Atividade do lab", tipo_status)
                else:
                    return self.GerarJson(True, 200, "Lab Cadastrado com sucesso", {"nome": nome, "atividade": tipo_status})
            else:
                return self.GerarJson(False, 403, "Acesso proibido para usuários não administradores", None)
        except jwt.ExpiredSignatureError:
            return self.GerarJson(False, 401, "Token expirado", None)
        except jwt.InvalidTokenError:
            return self.GerarJson(False, 401, "Token inválido", None)
        except mysql.connector.Error as err:
            return self.GerarJson(False, 500, f"Erro de MySQL ao Cadastrar Lab: {err}", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro inesperado em Cadastrar Lab: {e}", None)


    def Read_all_Labs(self): #Admin, Aluno, Professor
        try:
            leitura = modelo2.LabCrud()
            result = leitura.read()
            if result["status"] == False and result["msg"] == "Banco sem dados":
                return self.GerarJson(False, 404, "Banco sem dados", result["data"])
            else:
                return self.GerarJson(True, 200, "Registros acessados", result["data"])
        except mysql.connector.Error as err:
            return self.GerarJson(False, 500, f"Erro de MySQL ao Ler os Lab: {err}", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro inesperado ao ler os Labs: {e}", None)


    def Read_Lab_ID(self, id): #Admin, Aluno, Professor
        try:
            ler = controle2.VerificacaoLab()
            resul = ler.Read_By_Id(id)
            if resul["status"] == False and resul["msg"] == f"Nenhum dado encontrado para o ID {id}":
                return self.GerarJson(False, 401, f"Nenhum dado encontrado para o ID {id}", id)
            elif resul["status"] == False and resul["msg"] == "Elemento inexistente":
                return self.GerarJson(False, 401, "Elemento inexistente", None)
            else:
                return self.GerarJson(True, 200, f"Dado de id {id} encontrado", resul["data"])
        except mysql.connector.Error as err:
            return self.GerarJson(False, 500, f"Erro de MySQL ao Ler o Lab: {err}", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro inesperado ao ler o Lab: {e}", None)


    def Update_Lab(self, nome, tipo_status, disponibilidade, id, token): #Admin
        chave_secreta = '123'
        try:
            if nome is None or tipo_status is None or disponibilidade is None:
                return self.GerarJson(False, 401, "Dados não inseridos", {"nome": nome, "tipo_status": tipo_status})
            control = controle.VerificacaoCrud()
            # Verifica o token
            payload = jwt.decode(token, chave_secreta, algorithms=['HS256'])

            # Agora você pode acessar o email do usuário
            email_do_usuario = payload.get('email')
            # Verifica se o usuário é um administrador (ou implemente sua própria lógica de verificação)
            if control.VerificarAdmin(email_do_usuario) == 3:
                crud = modelo2.LabCrud()
                if tipo_status not in [1, 2]:
                    return self.GerarJson(False, 403, "Valor inválido para Status de atividade", tipo_status)
                elif disponibilidade not in [0, 1]:
                        return self.GerarJson(False, 403, "Valor inválido para Disponibilidade", disponibilidade)
                resul = crud.update(nome, tipo_status, disponibilidade, id)
                return self.GerarJson(True, 200, "Lab atualizado com sucesso", {"id": id, "nome": nome, "tipo_status": tipo_status, "disponibilidade": disponibilidade})     
            else:
                return self.GerarJson(False, 403, "Acesso proibido para usuários não administradores", None)
        except mysql.connector.Error as err:
            return self.GerarJson(False, 500, f"Erro de MySQL ao Atualizar usuário: {err}", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro inesperado em atualizar usuário: {e}", None) 


    def DeastivarLab(self, id, token): #Admin
        chave_secreta = '123'
        try:
            control = controle.VerificacaoCrud()
            # Verifica o token
            payload = jwt.decode(token, chave_secreta, algorithms=['HS256'])

            # Agora você pode acessar o email do usuário
            email_do_usuario = payload.get('email')

            # Verifica se o usuário é um administrador (ou implemente sua própria lógica de verificação)
            if control.VerificarAdmin(email_do_usuario) == 3:
                contro = controle2.VerificacaoLab()
                result = contro.desativar_lab(id)
                return result
            else:
                return self.GerarJson(False, 403, "Acesso proibido para usuários não administradores", None)
        except jwt.ExpiredSignatureError:
            return self.GerarJson(False, 401, "Token expirado", None)
        except jwt.InvalidTokenError:
            return self.GerarJson(False, 401, "Token inválido", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro interno ao ativar usuário: {e}", id)
    

    def AtivarLab(self, id, token): #Admin
        chave_secreta = '123'
        try:
            control = controle.VerificacaoCrud()
            # Verifica o token
            payload = jwt.decode(token, chave_secreta, algorithms=['HS256'])

            # Agora você pode acessar o email do usuário
            email_do_usuario = payload.get('email')

            # Verifica se o usuário é um administrador (ou implemente sua própria lógica de verificação)
            if control.VerificarAdmin(email_do_usuario) == 3:
                contro = controle2.VerificacaoLab()
                result = contro.ativar_lab(id)
                return result
            else:
                return self.GerarJson(False, 403, "Acesso proibido para usuários não administradores", None)
        except jwt.ExpiredSignatureError:
            return self.GerarJson(False, 401, "Token expirado", None)
        except jwt.InvalidTokenError:
            return self.GerarJson(False, 401, "Token inválido", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro interno ao ativar usuário: {e}", id)


    def DispopnibilizarLabUser(self, id_lab, id_user, token): #Admin
        chave_secreta = '123'
        try:
            control = controle.VerificacaoCrud()
            # Verifica o token
            payload = jwt.decode(token, chave_secreta, algorithms=['HS256'])

            # Agora você pode acessar o email do usuário
            email_do_usuario = payload.get('email')

            # Verifica se o usuário é um administrador (ou implemente sua própria lógica de verificação)
            if control.VerificarAdmin(email_do_usuario) == 3:
                contro = controle2.VerificacaoLab()
                result = contro.disponibilizar_lab_para_usuario(id_lab, id_user)
                if result["status"] == False and result["msg"] == f"Lab de ID {id_lab} não existe":
                    return self.GerarJson(False, 404, f"Lab de ID {id_lab} não existe", id_lab)
                elif result["status"] == False and result["msg"] == f"Lab de ID {id_lab} não está disponível":
                    return self.GerarJson(False, 503, f"Lab de ID {id_lab} não está disponível", id_lab)
                elif result["status"] == False and result["msg"] == f"Usuário de ID {id_user} não existe":
                    return self.GerarJson(False, 404, f"Usuário de ID {id_user} não existe", id_user)
                else:
                    return self.GerarJson(True, 200, f"Lab de ID {id_lab} disponibilizado para usuário de ID {id_user}", {"lab": "sucess", "user": "sucess"})
            else:
                return self.GerarJson(False, 403, "Acesso proibido para usuários não administradores", None)
        except jwt.ExpiredSignatureError:
            return self.GerarJson(False, 401, "Token expirado", None)
        except jwt.InvalidTokenError:
            return self.GerarJson(False, 401, "Token inválido", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro interno ao ativar usuário: {e}", id)


    def DeixarLabDisponivel(self, id_lab, token): #Admin
        chave_secreta = '123'
        try:
            control = controle.VerificacaoCrud()
            # Verifica o token
            payload = jwt.decode(token, chave_secreta, algorithms=['HS256'])

            # Agora você pode acessar o email do usuário
            email_do_usuario = payload.get('email')

            # Verifica se o usuário é um administrador (ou implemente sua própria lógica de verificação)
            if control.VerificarAdmin(email_do_usuario) == 3:
                contro = controle2.VerificacaoLab()
                result = contro.tornar_lab_disponivel(id_lab)
                if result["status"] == False and result["msg"] == f"Lab de ID {id_lab} não existe":
                    return self.GerarJson(False, 404, f"Lab de ID {id_lab} não existe", )
                else:
                    return self.GerarJson(True, 200, f"Lab de ID {id_lab} tornou-se disponível para acesso", {"lab": "sucess"}) 
            else:
                return self.GerarJson(False, 403, "Acesso proibido para usuários não administradores", None)
        except jwt.ExpiredSignatureError:
            return self.GerarJson(False, 401, "Token expirado", None)
        except jwt.InvalidTokenError:
            return self.GerarJson(False, 401, "Token inválido", None)
        except Exception as e:
            return self.GerarJson(False, 500, f"Houve um erro interno ao ativar usuário: {e}", id)


    def Token(self):
        return self.jwt

