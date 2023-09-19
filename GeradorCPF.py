from random import randint

#Função do quadro
def GerarString(string: str, tamanho: int) -> str:
    return string * tamanho

#Função que gerará os 8 primeiros dígitos do CPF
def gerar8digitos() -> int:
    l = []
    for _ in range(8):
        i = randint(0, 9)
        l.append(i)
    return l

#Função que gera o Nono dígitos segundo as normas do Governo
def gerarNonoDigito(escolher:dict=None) -> int:
    if escolher != None:
        D = {"DF": 1, "GO": 1, "MS": 1, "MT": 1, "TO": 1,
         "AC": 2, "AM": 2, "AP": 2, "PA": 2, "RO": 2, "RR": 2,
         "CE": 3, "MA": 3, "PI": 3,
         "AL": 4, "PB": 4, "PE": 4, "RN": 4,
         "BA": 5, "SE": 5,
         "MG": 6,
         "ES": 7, "RJ": 7,
         "SP": 8,
         "PR": 9, "SC": 9,
         "RS": 0}
        
        for chave, valor in D.items():
            if chave == escolher.upper():
                return valor
        else:
            print("Dado inválido, insira um signo estadual!\nEX: SP")
            return "!"
    else:
        x = randint(0, 9)
        return x

#Irá gerar o primeiro dígito verificador
def gerar_primeiro_digito(l: list) -> int:
    l_i = []
    for i in l:
        l_i.append(int(i))
    cont = 10
    s = 0
    for val in l_i:
        val *= cont
        s += val
        cont -= 1
    resto = s % 11
    if resto < 2:
        return 0
    else:
        sub = 11 - resto
        return sub
    
#Irá gerar o segundo dígito verificador
def gerar_segundo_digito(l: list, digito1: int) -> int:
    l_i = []
    for i in l:
        l_i.append(int(i))
    l_i.append(digito1)
    s = 0
    cont = 11
    for val in l_i:
        val *= cont
        s += val
        cont -= 1
    resto = s % 11
    if resto < 2:
        return 0
    else:
        sub = 11 - resto
        return sub

if __name__ == '__main__':
    l = gerar8digitos()
    while len(set(l)) == 1: #Enquanto os valores forem diferentes na contagem
        l = gerar8digitos()
    one = gerarNonoDigito()
    l.append(one)
    uniao = ""
    for valor in l:
        if str(valor).isdigit():
            uniao += str(valor)
        else:
            print("Não foi possível inserir dados, pois houve um erro na criação!")
            uniao = ''
            print("Dados criados removidos!")


    if uniao == "":
        print("Não foi possível inserir dados, pois houve um erro")
        print("Refaça Novamente!")
    else:
        d1 = str(gerar_primeiro_digito(uniao))
        d2 = str(gerar_segundo_digito(uniao, int(d1)))
        uniao += d1 + d2
        print(GerarString('==', 30))
        print("|                 CPF criado com êxito!                    |")
        print("|          Lembre-se, isso aqui é para fins acadêmicos     |")
        print(f'|{"==" * 29}|')
        print("|                                                          |")
        print("| LINHA DE GERADOR SEM PONTO:", uniao, "                 |")
        print(f'|{"__" * 29}|')
        print("|                                                          |")
        print("| LINHA DE GERADOR COM EDIÇÃO: ", end="")
        cont = 0
        for i in range(0, len(uniao)-3):
            print(uniao[i], end="")
            cont += 1
            if cont == 3:
                print(".", end="")
                cont = 0 
        print(f"{uniao[8]}-{uniao[-2]}{uniao[-1]}              |")
        print("|                                                          |")
        print(GerarString('==', 30))
