#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import pprint
import sys

class Language(object):
    def __init__(self, input_file):
        self.language = {
            'initial': '',
            'final': '',
            'pre': dict(),
            'post': dict(),
            'quit': [],
            'synon': dict(),
            'keys': dict()
        }
        self.input_file = input_file

    def build_dictionary(self):
        for line in self.input_file:
            formatted_line = line.strip().split(':')
            token, data = formatted_line[0], formatted_line[1].strip()
            if token == 'initial':
                self.language['initial'] = data
            elif token == 'final':
                self.language['final'] = data
            elif token == 'pre':
                self.insert_sub(data, self.language['pre'])
            elif token == 'post':
                self.insert_sub(data, self.language['post'])
            elif token == 'key':
                self.read_key(data)
            elif token == 'quit':
                self.language['quit'].append(data)
            elif token == 'synon':
                self.read_synons(data, self.language['synon'])


    # Dado duas string, retorna True se elas são sinônimas, False se não são
    def are_synonyms(self,string1,string2):
        l1 = self.language['synon'].get(string1)
        l2 = self.language['synon'].get(string2)
        return l1 is not None and l2 is not None and l1 == l2

    def read_next_line(self):
        line = next(self.input_file,'').strip()
        if line:
            token, data = line.split(':')[0].strip(), line.split(':')[1].strip()
        else: token,data = '',''
        return token, data

    @staticmethod
    def get_weight(keyword):
        weight = 1
        #insere o peso da palavra chave no primeiro item do array, se não ouver usa 1
        if keyword.split()[-1].isdigit():
            keyword = keyword.split()
            weight = int(keyword[-1])
            keyword.pop()
            keyword = " ".join(keyword)

        return keyword, weight

    def read_key(self, keyword):
        decomps = []

        keyword, weight = self.get_weight(keyword)
        decomps.append(weight)

        token, data = self.read_next_line()
        decomp = []

        while (token in ['decomp', 'reasmb']):
            if token == 'decomp':
                if ( len(decomp) > 0 ): decomps.append(decomp)
                decomp = []
                decomp.append(data)
                decomp.append([])
            else:
                decomp[1].append(data)

            token, data = self.read_next_line()

        if ( len(decomp) > 0 ): decomps.append(decomp)
        self.language['keys'][keyword] = decomps
        if (token == 'key'): self.read_key(data)

    def substitute_pre(self, input_text):
        input_text = input_text.split()
        #realiza pre-substituicoes
        input_text[:] = [word if word not in self.language['pre'] else self.language['pre'][word] for word in input_text]
        return input_text

    def check_for_end(self, input_text):
        if " ".join(input_text) in self.language['quit']:
            print self.language['final']
            sys.exit(0)

    def create_keywords_list(self, input_text):
        keywords = [word for word in input_text if word in self.language['keys']]
        return sorted(keywords, reverse= True, key=lambda key: self.language['keys'][key][0])

    #troca placeholders capturados na regex e realiza substituicoes post
    def format_result(self, input_match, decomp):
        return re.sub('\((\d+)\)',
                lambda match: " ".join(
                    [word if word not in self.language['post'] 
                          else self.language['post'][word] 
                          for word in input_match.group((int(match.group(1)))).split()]
                    ),
                decomp[1][0])

    def generate_response(self, input_text):
        input_text = self.substitute_pre(input_text)
        self.check_for_end(input_text)
        keywords = self.create_keywords_list(input_text)

        done = False
        for key in keywords:
            decomps = self.language['keys'][key][1:]
            for decomp in decomps:
                regex = decomp[0].replace('*','(.*)')
                #procura uma decomposicao que aceita a regex
                input_match = re.search(regex, " ".join(input_text))
                if input_match is not None:
                    print self.format_result(input_match, decomp)
                    done = True
                    break
            if done: break

    # Dado uma string e um dicionario, associa a primeira palavra da string ao restante no dicionario
    @staticmethod
    def insert_sub(string, dicionario):
        assert dicionario is not None
        palavra = string.split()
        dicionario[palavra[0]] = " ".join(palavra[1:])

    # Dado uma string com sinonimos, associa cada palavra dessa string com sua lista de sinonimos
    @staticmethod
    def read_synons(string, dicionario):
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

input_file = open('eliza.txt', 'r' )
bot = Language(input_file)
bot.build_dictionary()

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(bot.language)

input_file.close()

print bot.language['initial']
while True:
    input_text = raw_input()
    bot.generate_response(input_text)

