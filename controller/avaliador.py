import bcrypt
import jwt
import datetime

class ValidarCPF:
    '''Classe que nos permite verificar e validar um CPF'''
    def __init__(self, cpf: str) -> None: #Método construtor da classe que recebe o parâmetro CPF como entrada para atributo e seu retorno é None
        self.cpf = cpf.replace(".", "").replace("-", "") # Atributo de classe que recebe o CPF editado
        self.verificar = False #Atributo de classe verificador que nos permite gerar e verificar as leituras dos Jsons com o validador de CPF
        self.digitos = [] #Atributo de classe digitos que recebe uma lista que vai ler e calcular os dígitos do CPF
        self.erro = "" #Atributo de classe erro, que nos permitirá indicar ao usuário o erro posto na execução
    
    def validacao(self) -> str: #Método validacao que recebe todos os atributos de classe e nos retorna uma string caso as validações sejam corretas caso contrário, nos retorna um Dict
        if len(self.cpf)!= 11: # Verifica se o CPF não possuir exatamente 11 dígitos
            self.erro = "CPF inválido! Deve ter 11 dígitos."
            return self.gerar_erro(self.erro, self.cpf)
        elif not self.cpf.isdigit(): #Verifica se o CPF que está em formado string não são strings numéricas
            self.erro = "CPF inválido! Deve conter apenas dígitos numéricos."
            return self.gerar_erro(self.erro, self.cpf)
        else: #Caso contrário, nos permite verificar e terminar de validar
            self.verificar = True
            return self.verificar
        
    def analisar(self) -> str: #Método analisar que recebe todos os atributos de classe e nos retorna uma string caso os dados sejam bem validados, caso contrário, nos retorna um Dict
        if self.verificar == True: #Caso a 1° parte da validação for verdadeira
            uniao = "" #Var de classe união que vai funcionar como um concatenador que vai verificar os dados dos dígitos verificadores
            verificar = self.puxar_digitos(self.cpf) # Vai verificar e retornar os dígitos verificadores dos dados indicados
            if len(set(verificar)) == 1: # Verificar se todos os dígitos são iguais
                self.verificar = False
                self.erro = "CPF Não pode possuir valores iguais"
                return self.gerar_erro(self.erro, self.cpf)
            d1 = self.ValidarDigito1(verificar) #Fará a validação do primeiro dígito verificador
            d2 = self.ValidarDigito2(verificar, d1) #Fará a validação do segundo dígito verificador
            uniao += str(d1) + str(d2) # Concatenação dos dois dígitos
            if uniao == self.cpf[9:]: # Se a var de classe uniao for igual aos índices verificadores indicados pelo usuário
                return f"O CPF {self.cpf} é válido!"
            else: #Caso contrário
                self.erro = "O CPF é inválido"
                return self.gerar_erro(self.erro, self.cpf)
        else: # Caso o validador for falso
            self.erro = "O CPF não foi validado"
            return self.gerar_erro(self.erro, self.cpf)

    def puxar_digitos(self,cpf: str) -> list: #Método puxar_digitos que recebe o parâmetro CPF que vai nos permitir extrair os 8 primeiros dígitos do CPF e nos retorna uma lista com os dígitos
        for d in range(0, len(cpf) - 2):
            self.digitos.append(int(cpf[d]))
        return self.digitos #Retorna a lista com os 8 primeiros dígitos
    
    def gerar_erro(self, erro: str, cpf: str) -> dict: #Método gerar_erro que recebe os parâmetros erro(Mensagem de retorno do Json) e cpf(valor digiado pelo usuário) que nos retorna os erros em formato json caso os dados forme inválidos
        if erro:
            d = {"status": False,
                    f"Retorno user": cpf,
                    "Motivo": erro
                }
            return d
        else:
            return "Erro não cadastrado para gerar Dict"

    

    def ValidarDigito1(self, l: list, cont=10) -> int: #Método ValidarDigito1 que recebe os parâmetros l(Lista dos dados do CPF) e cont que por padrão recebe 10, e retorna o primeiro dígito verificador
        s = 0 #Variável de atribuição que somará o resultado dos dígitos vezes a contagem
        for val in l:
            val *= cont #Multiplica o valor de cada dígito pelo valor do contador EX: ((1*10)+(2*9)+(3*8)+(4*7)+(5*6)+(6*5)+(7*4)+(8*3)+(9*2))
            s += val #Soma o valor da multiplicação
            cont -= 1
        resto = s % 11 # Puxamos o resto da divisão para verificar se o valor é maior ou menor que 2
        if resto < 2: #Se o resultado for menor que 2, por padrão o primeiro dígito é 0
            return 0
        else: #Caso contrário, subtraimos o resto da divisão por 11 e obtemos o resultado do dígito verificador
            sub = 11 - resto
            return sub
    
    def ValidarDigito2(self, l: list, validacao1: int, cont=11) -> int: #Método ValidarDigito2 que recebe os parâmetros l(Lista dos dados do CPF), validacao1(Que é o valor do primeiro dígito encontrado) e cont que por padrão recebe 11, e retorna o segundo dígito verificador
        l.append(validacao1) #É adicionado a lista do dígitos o primeiro verificador
        s = 0 #Variável de atribuição que somará o resultado dos dígitos vezes a contagem
        for val in l:
            val *= cont #Multiplica o valor de cada dígito pelo valor do contador EX: ((1*10)+(2*9)+(3*8)+(4*7)+(5*6)+(6*5)+(7*4)+(8*3)+(9*2)+(1*1))
            s += val #Soma o valor da multiplicação
            cont -= 1
        resto = s % 11 # Puxamos o resto da divisão para verificar se o valor é maior ou menor que 
        if resto < 2:
            return 0 #Se o resultado for menor que 2, por padrão o segundo dígito é 0
        else: #Caso contrário, subtraimos o resto da divisão por 11 e obtemos o resultado do dígito verificador
            sub = 11 - resto
            return sub


class TokenManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_token(self, username, expiration_hours=24):
        # Dados do usuário que serão incluídos no token
        user_data = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours)
        }

        # Gere o token
        token = jwt.encode(user_data, self.secret_key, algorithm='HS256')
        return token

    def verify_token(self, token):
        try:
            decoded_data = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return decoded_data
        except jwt.ExpiredSignatureError:
            return {"error": "Token expirado"}
        except jwt.InvalidTokenError:
            return {"error": "Token inválido"}


