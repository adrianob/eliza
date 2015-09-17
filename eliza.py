import re

input_file = open('input.txt', 'r' )


language = {
    'initial': '',
    'final': '',
    'quit': [],
    'post': [],
    'synon': [],
    'pre': [],
    'keys': [
                ['sorry', {'decomp': [],'reasmb':[]} ],
                ['perhaps', {'decomp': [],'reasmb':[]} ],
            ]

}


for line in input_file:
    formatted_line = line.split(':')
    language[formatted_line[0]] = formatted_line[1]

print language['post']
input_file.close()
