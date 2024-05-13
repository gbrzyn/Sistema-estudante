# Nome: Gabriel Souza Michaliszyn RA: 1112024101187
# Raciocínio Computacional (11100010563_20241_01) | Semana 8 } Atividade Somativa 2

import json

ESCAPE = "9" #Constante para definir string de escape dos menus

#Utilizei uma estrutura de dados com listas e dicionarios para simular propriedades de uma Classe e incluir validadores

#"Classe" Estudante
estudante_data = {
    "name": "Estudante",
    "file_name": "estudantes.json"}
estudante_params = [
    {"name": "código", "type": "int", "min_len": 1, "max_len": 4, "unique": True}, 
    {"name": "nome", "type": "str", "min_len": 3, "max_len": 200, "unique": False}, 
    {"name": "cpf", "type": "str", "min_len": 11, "max_len": 14, "unique": True}]

#"Classe" Professor
professor_data = {
    "name": "Professor",
    "file_name": "professores.json"}
professor_params = [
    {"name": "código", "type": "int", "min_len": 1, "max_len": 4, "unique": True}, 
    {"name": "nome", "type": "str", "min_len": 3, "max_len": 200, "unique": False}, 
    {"name": "cpf", "type": "str", "min_len": 11, "max_len": 14, "unique": True}]

#"Classe" Disciplina
disciplina_data = {
    "name": "Disciplina",
    "file_name": "disciplinas.json"}
disciplina_params = [
    {"name": "código", "type": "int", "min_len": 1, "max_len": 4, "unique": True}, 
    {"name": "nome", "type": "str", "min_len": 3, "max_len": 200, "unique": False},]

#"Classe" Turma
turma_data = {
    "name": "Turma",
    "file_name": "turmas.json"}
turma_params = [
    {"name": "código", "type": "int", "min_len": 1, "max_len": 4, "unique": True},
    {"name": "código_do_professor", "type": "int", "min_len": 1, "max_len": 4, "unique": True},
    {"name": "código_da_disciplina", "type": "int", "min_len": 1, "max_len": 4, "unique": True}]

#"Classe" Matrícula
matricula_data = {
    "name": "Matrícula",
    "file_name": "matriculas.json"}
matricula_params = [
    {"name": "código", "type": "int", "min_len": 1, "max_len": 4, "unique": True},
    {"name": "código_da_turma", "type": "int", "min_len": 1, "max_len": 4, "unique": True},
    {"name": "código_do_estudante", "type": "int", "min_len": 1, "max_len": 4, "unique": True}]

#Função para exibição do Menu Principal
def menu_principal():
    print("\n----- MENU PRINCIPAL -----\n")
    print("(1) Gerenciar estudantes.")
    print("(2) Gerenciar professores.")
    print("(3) Gerenciar disciplinas.")
    print("(4) Gerenciar turmas.")
    print("(5) Gerenciar matrículas.")
    print(f"({ESCAPE}) Sair.")

#Função para exibição do Menu de Operações
def menu_operacoes(opcao_name):
    print(f"\n***** [{str.upper(opcao_name)}] MENU DE OPERAÇÕES *****\n")
    print("(1) Incluir.")
    print("(2) Listar.")
    print("(3) Atualizar.")
    print("(4) Excluir.")
    print(f"({ESCAPE}) Voltar ao menu principal.")

#Função para formatar strings
def formatar(string: str, param):
    match param:
        case "param":
            if(string == "cpf"):
                return string.upper()
            else:
                string = string.replace("_", " ")
                return string.capitalize()
        
        case "nome":
            return string.title()
        
        case "cpf":
            string = string.replace(".","").replace("-","")

            new_string = ""
            for i in range(0, len(string), 3):
                for j in range(0, 3):
                    if(i+j < 11):
                        new_string += (string[i+j])
                if(i < 6):
                    new_string += "."
                elif(i < 9):
                    new_string += "-"
            return new_string
        
        case _:
            return string

#Função para cadastrar dados de uma "classe" (estudante, professor ...)
def cadastrar(opcao_data, opcao_params):
    item = {}

    for param in opcao_params:
        valid = False

        while(not valid):
            value = validar(opcao_data, param, input(f"Informe o(a) {formatar(param["name"], "param")} do(a) {opcao_data["name"]}: "))

            if(value):
                item[param["name"]] = formatar(value, param["name"])
                valid = True
                
    return item

#Função para validar o dado informado de acordo com os validadores do parametro
def validar(opcao_data, param, value, update = False):
    length = len(value)
    value = converter(param, value)

    if(value is None):
        return None
     
    elif(param["max_len"] < param["min_len"]):
        print("\nERRO DE VALIDAÇÃO: Propriedade com tamanho máximo < minimo!\n")
        return None
    
    elif((length < param["min_len"]) | (length > param["max_len"])):
        print(f"\nValor inválido! A propriedade [{formatar(param["name"], "param")}] precisar ter entre {param["min_len"]} e {param["max_len"]} caracteres\n")
        return None
    
    elif((param["unique"]) & (obter(value, param["name"], opcao_data) is not None) & (not update)):
        print(f"\nValor unico ja cadastrado! O valor {value} ja foi cadastrado para o(a) {formatar(param["name"], "param")} do(a) {opcao_data["name"]}\n")
        return None

    return value

#Função para converter um valor de um parametro conforme seu tipo
def converter(param, value):
    try:
        match param["type"]:
            case "int":
                return int(value)
            case "float":
                return float(value)
            case "str":
                return str(value)
            case "bool":
                return bool(value)
            case _:
                print("\nERRO DE VALIDAÇÃO: Propriedade com tipo não suportado!\n")
                return None
    except:
        print(f"\nValor inválido! A propriedade [{formatar(param["name"], "param")}] precisar ser do tipo {param["type"]}\n")
        return None

#Função para inserir um novo registro de uma "classe" (estudante, professor ...)
def inserir(item, opcao_data):
    itens = recuperar_data_json(opcao_data["file_name"])
    itens.append(item)

    salvar_data_json(itens, opcao_data["file_name"])

    if("nome" in item):
        print(f"\nInserção do(a) {opcao_data["name"]} - {item["nome"]} concluída!")
    else:
        print(f"\nInserção do(a) {opcao_data["name"]} concluída!")

#Função para atualizar um registro já existente de uma "classe" (estudante, professor ...)
def atualizar(item, novo_item, opcao_data):
    itens = recuperar_data_json(opcao_data["file_name"])
    itens.insert(itens.index(item), novo_item)
    itens.remove(item)

    #Outra forma de atualizar o item
    #itens[itens.index(item)] = novo_item

    salvar_data_json(itens, opcao_data["file_name"])

    if("nome" in item):
        print(f"\nAtualização do(a) {opcao_data["name"]} - {novo_item["nome"]} concluída!")
    else:
        print(f"\nAtualização do(a) {opcao_data["name"]} concluída!")

#Função para remover um registro já existente de uma "classe" (estudante, professor ...)
def remover(item, opcao_data):
    itens = recuperar_data_json(opcao_data["file_name"])
    itens.remove(item)

    salvar_data_json(itens, opcao_data["file_name"])

    if("nome" in item):
        print(f"\nRemoção do(a) {opcao_data["name"]} - {item["nome"]} concluída!")
    else:
        print(f"\nRemoção do(a) {opcao_data["name"]} concluída!")

#Função para pesquisar registros por termos de pesquisa (códigos, cpf ...)
def pesquisar(opcao_data, opcao_params):
    terms = []
    cont = 0

    print("\nPesquisar por:\n")
    for param in opcao_params:
        if(param["unique"]):
            terms.append(param)
            print(f"{cont + 1} - {formatar(param["name"], "param")}")
            cont += 1

    valid = False
    while(not valid):
        try:
            #Subtrair 1 do valor lido para normalizar o index de acordo com o range da lista
            index = int(input("\nInforme o número do termo para pesquisa: ")) - 1
        except:
            print("\nValor inválido! Informe um número relacionado ao termo\n")
            continue

        if((index < 0) | (index > cont)):
            print(f"\nValor do termo fora do intervalo (0 - {len(terms)})\n")
        else:
            valid = True

    valid = False
    while(not valid):
        value = validar(opcao_data, terms[index], input(f"\nInforme o valor do termo ({formatar(terms[index]["name"], "param")}): "), True)

        if(value is not None):
            valid = True

    item = obter(value, terms[index]["name"], opcao_data)

    if(not item):
        print(f"\n{opcao_data["name"]} com o {terms[index]["name"]} {value} não cadastrado")
        return None
    
    else:
        return item

#Função para obter um registro de uma "classe" (estudante, professor ...) por meio de um termo de pesquisa e o seu valor
def obter(value, term, opcao_data):
    itens = recuperar_data_json(opcao_data["file_name"])
    for item in itens:
        if value == item[term]:
            return item
    return None

#Função para listar todos os registros de uma "classe" (estudante, professor ...)
def listar(opcao_data, opcao_params):
    itens = recuperar_data_json(opcao_data["file_name"])
    cont = 1

    if(len(itens) != 0):
        for item in itens:
            print(f"{opcao_data["name"]} {cont}")
            print("----------")
            cont += 1

            for param in opcao_params:
                print(f"{formatar(param["name"], "param")} - {formatar(item[param["name"]], param["name"])}")
            print("----------\n")
    else:
        print(f"Não há registros de {opcao_data["name"]} disponíveis!")

#Função para salvar dados em um arquivo json
def salvar_data_json(itens, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        #Parametro indent > 0 para melhor visualização do json
        json.dump(itens, file, indent=2, ensure_ascii=False)

#Função para recuperar dados de um arquivo json
def recuperar_data_json(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []

#Função de operaçòes CRUD para todas as classes
def operacoes(opcao_data, opcao_params):
    fim = False

    while(not fim):
        menu_operacoes(opcao_data["name"])
        acao = input("\nInforme a ação desejada: ")

        match acao:
            case "1":
                print("\n===== INCLUSÃO =====\n")
                inserir(cadastrar(opcao_data, opcao_params), opcao_data)

            case "2":
                print("\n===== LISTAGEM =====\n")
                listar(opcao_data, opcao_params)

            case "3":
                print("\n===== ATUALIZAÇÃO =====\n")
                item = pesquisar(opcao_data, opcao_params)

                if(item is not None):
                    atualizar(item, cadastrar(opcao_data, opcao_params), opcao_data)

            case "4":
                print("\n===== EXCLUSÃO =====\n")
                item = pesquisar(opcao_data, opcao_params)
                
                if(item is not None):
                    remover(item, opcao_data)

            case _:
                if(acao == ESCAPE):
                    fim = True
                else:
                    print("\n===== VALOR INVÁLIDO =====")

# Função principal (main)
fim = False
while(not fim): 
    menu_principal()
    opcao = input("\nInforme a opção desejada: ")

    match opcao:
        case "1":
            operacoes(estudante_data, estudante_params)
        case "2":
            operacoes(professor_data, professor_params)
        case "3":
            operacoes(disciplina_data, disciplina_params)
        case "4":
            operacoes(turma_data, turma_params)
        case "5":
            operacoes(matricula_data, matricula_params)
        case _:
            if(opcao == ESCAPE):
                fim = True
            else:
                print("\n***** [VALOR INVÁLIDO] *****")

print("\nFinalizando aplicação...")