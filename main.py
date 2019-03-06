import pickle
import nltk
import re

import acoes


def load_frame(tagger, tokenizer, text):
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
    return frame

def select_action(actions, frame):
    acao_likeness = [(acao, acao.likeness_rate(frame)) for acao in actions]
    acao_likeness.sort(key=lambda tup:tup[1])
    return acao_likeness[-1][0]


tagger = pickle.load(open('tagger.pkl', 'rb'))
tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')

ver_menu = acoes.VerMenu()
comprar_burguer = acoes.ComprarHamburguer()
acoes_possiveis = [ver_menu, comprar_burguer]
acao_atual = None

print('Olá, em que posso ajudar? ')
while acao_atual is None or not acao_atual.is_done:
    # text = 'querer comprar hamburguer'
    text = input()
    frame = load_frame(tagger, tokenizer, text)
    
    if acao_atual is None:
        acao_atual = select_action(acoes_possiveis, frame)
    else:
        acao_atual.feed(req_frame, text)
    
    if acao_atual.can_perform:
        acao_atual.perform()
    else:
        req_frame = acao_atual.get_request_frame()
        print(req_frame['text'])
