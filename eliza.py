import re
import pprint

input_file = open('input.txt', 'r' )

language = {
    'initial': '',
    'final': '',
    'post': [],
    'sair': [],
    'synon': [],
    'pre': [],
    'keys': []

}

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
        language['pre'].append(formatted_line[1])
    elif formatted_line[0] == 'post':
        language['post'].append(formatted_line[1])
    elif formatted_line[0] == 'synon':
        language['synon'].append(formatted_line[1])
    elif formatted_line[0] == 'key':
        key = []
        key.append(formatted_line[1])

        next_line = input_file.readline().rstrip()
        token = next_line.split(':')[0].strip()
        decomp = []

        while (token in ['decomp', 'reasmb']):
            if token == 'decomp':
                if ( len(decomp) > 0 ):
                    key.append(decomp)
                decomp = []
                decomp.append(next_line.split(':')[1])
                decomp.append([])
            else:
                decomp[1].append(next_line.split(':')[1])

            next_line = input_file.readline().rstrip()
            token = next_line.split(':')[0].strip()

        if ( len(decomp) > 0 ):
            key.append(decomp)
        language['keys'].append(key)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(language)

input_file.close()
