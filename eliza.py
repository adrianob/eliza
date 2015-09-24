#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import pprint
import sys

class LanguageDict(object):
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
            formatted_line = line.decode('utf-8').strip().split(':')
            token, data = formatted_line[0], formatted_line[1].strip()
            if token in ['initial', 'final']:
                self.language[token] = data
            elif token in ['pre', 'post']:
                self.insert_sub(data, self.language[token])
            elif token == 'key':
                self.read_key(data)
            elif token == 'quit':
                self.language['quit'].append(data)
            elif token == 'synon':
                self.read_synons(data, self.language['synon'])

    def read_next_line(self):
        line = next(self.input_file,'').decode('utf-8').strip()
        if line:
            token, data = line.split(':')[0].strip(), line.split(':')[1].strip()
        else: token,data = '',''
        return token, data

    def read_key(self, keyword):
        decomps = []

        keyword, weight = self.get_weight(keyword)
        decomps.append(weight)

        token, data = self.read_next_line()
        decomp = []

        while (token in ['decomp', 'reasmb']):
            if token == 'decomp':
                if ( len(decomp) > 0 ):
                    decomps.append(decomp)
                decomp = [data, []]
            else:
                decomp[1].append(data)

            token, data = self.read_next_line()

        if ( len(decomp) > 0 ):
            decomps.append(decomp)
        self.language['keys'][keyword] = decomps
        if (token == 'key'): self.read_key(data)

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

class Bot(object):
    def __init__(self, dictionary):
        self.__language = dictionary
        self.used_reasmb = []

    @property
    def language(self):
        return self.__language

    #realiza pre-substituicoes
    def substitute_pre(self, input_text):
        input_text = input_text.split()
        return [word if word not in self.language['pre'] else self.language['pre'][word] for word in input_text]

    #verifica se acabou o dialogo
    def check_for_end(self, input_text):
        if " ".join(input_text).decode('utf-8') in self.language['quit']:
            print self.language['final']
            sys.exit(0)

    def create_keywords_list(self, input_text):
        keywords = [word for word in input_text if word in self.language['keys']]
        for word in ( set(input_text) - set(keywords) ).intersection(self.language['synon']):
            for synon in self.language['synon'][word]:
                if synon in self.language['keys']:
                    keywords.append(synon)
        return sorted(keywords, reverse= True, key=lambda key: self.language['keys'][key][0])

    def decomp_used(self, key, decomp_regex):
        return [True for reasmb in self.used_reasmb if reasmb[0:2] == [key, decomp_regex]]

    def get_next_reasmb(self, key, decomp_group):
        decomp_regex = decomp_group[0]
        for index, reasmb in enumerate(self.used_reasmb):
            if reasmb[0:2] == [key, decomp_regex]:
                reasmb_index = reasmb[2] + 1
                if reasmb_index >= len(decomp_group[1]):
                    reasmb_index = 0
                self.used_reasmb[index] = [key, decomp_regex, reasmb_index]
                return reasmb_index

    #troca placeholders capturados na regex e realiza substituicoes post
    def format_result(self, input_match, decomp_group, key):
        decomp_regex = decomp_group[0]
        if self.decomp_used(key, decomp_regex):
            reasmb_index = self.get_next_reasmb(key, decomp_group)
        else:
            reasmb_index = 0
            self.used_reasmb.append([key, decomp_regex, reasmb_index])

        reasmb = decomp_group[1][reasmb_index]
        return re.sub('\((\d+)\)',
                lambda match: " ".join(
                    [word.decode('utf-8') if word not in self.language['post'] 
                          else self.language['post'][word] 
                          for word in input_match.group((int(match.group(1)))).split()]
                    ), reasmb, flags=re.IGNORECASE)

    def generate_decomp_regex(self, decomp_regex):
        regex = re.sub('(\s*\*\s*)', '*', decomp_regex)
        regex = regex.replace('*','(.*)')
        return re.sub('((@)(\w+))', lambda match: "(" + "|".join([synon for synon in self.language['synon'][match.group(3).lower()]]) + ")", regex )

    def generate_response(self, input_text):
        input_text = self.substitute_pre(input_text)
        self.check_for_end(input_text)
        keywords = self.create_keywords_list(input_text)

        done = False
        for key in keywords:
            decomps = self.language['keys'][key][1:]
            for decomp_group in decomps:
                decomp_regex = decomp_group[0]
                regex = self.generate_decomp_regex(decomp_regex)
                #procura uma decomposicao que aceita a regex
                input_match = re.search(regex, " ".join(input_text), flags=re.IGNORECASE)
                if input_match is not None:
                    print self.format_result(input_match, decomp_group, key)
                    done = True
                    break
            if done: break
        if not done:
            print self.language['keys']['xnone'][1][1][0]

input_file = open('script_bb.txt', 'r' )
dic = LanguageDict(input_file)
dic.build_dictionary()
bot = Bot(dic.language)

pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(bot.language)

input_file.close()

print bot.language['initial']
while True:
    input_text = raw_input('>')
    bot.generate_response(input_text.lower())
