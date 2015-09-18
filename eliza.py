import re
import pprint

input_file = open('input.txt', 'r' )

language = {
    'initial': '',
    'final': '',
    'pre': dict(),
    'post': dict(),
    'sair': [],
    'synon': [],
    'keys': []
}

# Dado uma string e um dicionario, associa a primeira palavra da string a segunda no dicionario
def InsereDicionario(string,dicionario):
    assert dicionario is not None
    palavra = string.split()
    # Se tem só uma palavra, deve associar à uma string vazia
    if len(palavra) == 1:
        dicionario[palavra[0]] = ''
    # Se tem duas palavras, associa a primeira à segunda
    elif len(palavra) == 2:
        dicionario[palavra[0]] = palavra[1]
    # Senao, tem zero ou mais de duas palavras. Simplesmente ignora a linha
    else:
        print("AVISO: Problema de sintaxe, linha {0}".format(linha_atual))

linha_atual = 1
while True:
    line = input_file.readline().rstrip()
    if not line:
        break
    formatted_line = line.split(':')
    if formatted_line[0] == 'initial':
        language['initial'] = formatted_line[1]
    elif formatted_line[0] == 'final':
        language['final'] = formatted_line[1]
    elif formatted_line[0] == 'sair':
        language['sair'].append(formatted_line[1])
    elif formatted_line[0] == 'pre':
        InsereDicionario(formatted_line[1],language['pre'])
    elif formatted_line[0] == 'post':
        InsereDicionario(formatted_line[1],language['post'])
    elif formatted_line[0] == 'synon':
        language['synon'].append(formatted_line[1])
    elif formatted_line[0] == 'key':
        key = []
        key.append(formatted_line[1])

        next_line = input_file.readline().rstrip()
        token = next_line.split(':')[0]
        decomp = []

        while (token in [' decomp', ' reasmb']):
            if token == ' decomp':
                if ( len(decomp) > 0 ):
                    key.append(decomp)
                decomp = []
                decomp.append(next_line.split(':')[1])
                decomp.append([])
            else:
                decomp[1].append(next_line.split(':')[1])

            next_line = input_file.readline().rstrip()
            token = next_line.split(':')[0]

        if ( len(decomp) > 0 ):
            key.append(decomp)
        language['keys'].append(key)
    linha_atual+= 1

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(language)

input_file.close()
