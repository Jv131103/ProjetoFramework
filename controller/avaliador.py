import bcrypt

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

class ProtegerSenha:
    '''Classe que nos permite Gerar Hashs de senha'''
    def __init__(self) -> None: #Método construtor da classe que tem seu retorno None
        self.__senha = "" #Atributo privado senha que recebe uma string vazia
        self.__hashed_password = "" #Atributo privado hashed_password que nos retornará o hash da senha, mas por padrão é uma string vazia

    def GerarHash(self, senha:str) -> str: #Método que nos permite Gerar o HASH da senha e recebe o parâmetro senha, que precisa ser inserido
        # Gerar um salt aleatório
        salt = bcrypt.gensalt()

        self.__senha = senha #O atributo privado senha recebe a senha inseida

        self.__hashed_password = bcrypt.hashpw(self.__senha.encode('utf-8'), salt) #O atributo privado hashed_password vai receber a criptografia da senha inserida

        return self.__hashed_password
    
    def ValidarSenhaHash(self, senha: str) -> str: #Método que nos permite validar e liberar o acesso ao cadastro
        if bcrypt.checkpw(senha.encode('utf-8'), self.__hashed_password): #Se a senha inserida corresponder ao salt de hash, ele será válido
            print("Acesso permitido!")
            return True
        else: #Caso contrário, não permitirá o acesso
            print("Acesso negado!")
            return False


# Testes
if __name__ == "__main__":
    c = ValidarCPF("433.783.648-90")
    print(c.validacao())
    print(c.analisar())

    senha = "123"
    gerar = ProtegerSenha()
    print(gerar.GerarHash(senha)) 
    print(gerar.ValidarSenhaHash(senha))

