#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pprint

language = {
    'initial': '',
    'final': '',
    'pre': dict(),
    'post': dict(),
    'quit': [],
    'synon': dict(),
    'keys': dict()
}

# Dado uma string e um dicionario, associa a primeira palavra da string ao restante no dicionario
def InsereDicionario(string,dicionario):
    assert dicionario is not None
    palavra = string.split()
    dicionario[palavra[0]] = " ".join(palavra[1:])

# Dado uma string com sinonimos, associa cada palavra dessa string com sua lista de sinonimos
def read_synons(string,dicionario):
    lista_sinonimos = []
    sinonimos = string.split()
    # Se não há palavras suficientes
    if len(sinonimos) <= 1:
        print("AVISO: Problema de sintaxe")
        return
    lista_sinonimos.append(sinonimos)
    # Para cada palavra, associa ela a sua lista de sinonimos
    for palavra in lista_sinonimos[-1]:
        dicionario[palavra] = lista_sinonimos[-1]

# Dado duas string, retorna True se elas são sinônimas, False se não são
def are_sinonims(string1,string2):
    l1 = language['synon'].get(string1)
    l2 = language['synon'].get(string2)
    return l1 is not None and l2 is not None and l1 == l2

def read_key(keyword):
    decomps = []

    #insere o peso da palavra chave no primeiro item do array, se não ouver usa 1
    if keyword.split()[-1].isdigit():
        decomps.append(int(keyword.split()[-1]))
    else:
        decomps.append(1)

    line = next(input_file).strip()
    token, data = line.split(':')[0].strip(), line.split(':')[1].strip()
    decomp = []

    while (token in ['decomp', 'reasmb']):
        if token == 'decomp':
            if ( len(decomp) > 0 ): decomps.append(decomp)
            decomp = []
            decomp.append(data)
            decomp.append([])
        else:
            decomp[1].append(data)

        line = next(input_file,'').strip()
        if line:
            token, data = line.split(':')[0].strip(), line.split(':')[1].strip()
        else: token = ''

    if ( len(decomp) > 0 ): decomps.append(decomp)
    if keyword.split()[-1].isdigit():
        keyword = keyword.split()
        keyword.pop()
        keyword = " ".join(keyword)
    language['keys'][keyword] = decomps
    if (token == 'key'):
        read_key(data)

def read_file(input_file):
    for line in input_file:
        formatted_line = line.strip().split(':')
        token, data = formatted_line[0], formatted_line[1].strip()
        if token == 'initial':
            language['initial'] = data
        elif token == 'final':
            language['final'] = data
        elif token == 'pre':
            InsereDicionario(data,language['pre'])
        elif token == 'post':
            InsereDicionario(data,language['post'])
        elif token == 'key':
            read_key(data)
        elif token == 'quit':
            language['quit'].append(data)
        elif token == 'synon':
            read_synons(data,language['synon'])

input_file = open('eliza.txt', 'r' )
read_file(input_file)
pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(language)

input_file.close()

print language['initial']
while True:
    input_text = raw_input()
    input_text = input_text.split()
    #realiza pre-substituicoes
    input_text[:] = [word if word not in language['pre'] else language['pre'][word] for word in input_text]
    if " ".join(input_text) in language['quit']:
        print language['final']
        break
    #acha keywords no input do usuario
    keywords = [word for word in input_text if word in language['keys']]
    keywords = sorted(keywords, reverse= True, key=lambda key: language['keys'][key][0])

    done = False
    for key in keywords:
        for decomp in language['keys'][key][1:]:
            regex = decomp[0].replace('*','(.*)')
            #procura uma decomposicao que aceita a regex
            input_match = re.search(regex, " ".join(input_text))
            if input_match is not None:
                #troca placeholders pelos grupos resultantes da regex
                print re.sub('\(\d+\)',
                        lambda match: input_match.group((int(match.group(0).replace('(','').replace(')','')))),
                        decomp[1][0])
                done = True
                break
        if done: break
