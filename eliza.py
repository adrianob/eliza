#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pprint

language = {
    'initial': '',
    'final': '',
    'pre': dict(),
    'post': dict(),
    'sair': [],
    'synon': dict(),
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
        print("AVISO: Problema de sintaxe")

# Dado uma string com sinonimos, associa cada palavra dessa string com sua lista de sinonimos
lista_sinonimos = []
def read_synons(string,dicionario):
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
    if l1 is not None and l2 is not None and l1 == l2:
        return True
    else:
        return False

def read_key(data):
    key = []
    key.append(data)

    line = next(input_file).strip()
    token, data = line.split(':')[0].strip(), line.split(':')[1].strip()
    decomp = []

    while (token in ['decomp', 'reasmb']):
        if token == 'decomp':
            if ( len(decomp) > 0 ): key.append(decomp)
            decomp = []
            decomp.append(data)
            decomp.append([])
        else:
            decomp[1].append(data)

        line = next(input_file,'').strip()
        if line:
            token, data = line.split(':')[0].strip(), line.split(':')[1].strip()
        else: token = ''

    if ( len(decomp) > 0 ): key.append(decomp)
    language['keys'].append(key)
    if (token == 'key'): read_key(data)

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
        elif token == 'sair':
            language['sair'].append(data)
        elif token == 'synon':
            read_synons(data,language['synon'])

input_file = open('script_bb.txt', 'r' )
read_file(input_file)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(language)

input_file.close()
