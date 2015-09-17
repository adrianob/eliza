import re

input_file = open('input.txt', 'r' )


language = {
    'initial': '',
    'final': '',
    'post': [],
    'sair': [],
    'synon': [],
    'pre': [],
    'chaves': [
                #['sorry', [ ['*', [] ] ] ],
            ]

}


for line in input_file:
    formatted_line = line.split(':')
    if formatted_line[0] == 'initial':
        language['initial'] = formatted_line[1]
    elif formatted_line[0] == 'final':
        language['final'] = formatted_line[1]
    elif formatted_line[0] == 'sair':
        language['sair'].append(formatted_line[1])
    elif formatted_line[0] == 'pre':
        language['pre'].append(formatted_line[1])
    elif formatted_line[0] == 'post':
        language['post'].append(formatted_line[1])
    elif formatted_line[0] == 'synon':
        language['synon'].append(formatted_line[1])
    elif formatted_line[0] == 'key':
        chave = []
        chave[0] = formatted_line[1]
        chave[1] = []

        key_line = input_file.readline()

        while(key_line[0] == ' '):
            formatted_key_line = line.split(':')

            if formatted_key_line[0] == 'decomp':
                chave[1][0] = formatted_line[1]
                key_line = input_file.readline()
                formatted_key_line = line.split(':')
                while(formatted_key_line[0] == ' reasmb'):
                    chave[1][1] = append(formatted_key_line[1])
                    key_line = input_file.readline()
                    formatted_key_line = line.split(':')

            key_line = input_file.readline()










for x in language['sair']:
    print x,

input_file.close()
