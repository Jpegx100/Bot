import pickle
import nltk
import re

import acoes


def select_action(actions, frame):
    for action in actions:
        if action.activate(frame):
            return action

text = 'querer um burguer'

tagger = pickle.load(open('tagger.pkl', 'rb'))
tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')

tagged_words = tagger.tag(nltk.word_tokenize(text.lower()))
tagged_words = ['{};{}'.format(a, b) for a, b in  tagged_words]
tagged_words = ' '.join(tagged_words)
pattern = (
    r'(?P<action>\S+;VERB)|(?P<object>\S+;(NOUN|PRON))'
)
result_list = [i.groupdict() for i in re.finditer(pattern, tagged_words)]
frame = {}
for result in result_list:
    for key in result.keys():
        if result[key]:
            value = result[key].split(';')[0]
            if key in frame:
                frame[key].append(value)
            else:
                frame[key] = [value]


ver_menu = acoes.VerMenu()
comprar_burguer = acoes.ComprarHamburguer()
acoes_possiveis = [ver_menu, comprar_burguer]
acao_atual = None

for acao in acoes_possiveis:
    if acao.activate(frame):
        acao_atual = acao

import pdb;pdb.set_trace()