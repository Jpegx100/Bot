import pickle
import nltk
import re


class ComprarHamburguer(object):
    request_fields = ['hamburguer', 'quantidade', 'endereco']
    fields = list()

    def __init__(self):
        self.tagger = pickle.load(open('tagger.pkl', 'rb'))
        self.tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')

    def likeness_rate(self, text):

        #      !VERB ADP? DET !NOUN
        # VERB !VERB PRON !NOUN
        # VERB !VERB DET !NOUN
        pattern = r'(VERB)? (?P<action>VERB) (((ADP)? DET)| PRON) (?P<object>NOUN)'
        tagged_words = self.tagger.tag(nltk.word_tokenize(text))
        # Tranforma a lista de tuplas em duas listas
        words, tags = zip(*tagged_words)
        tags = ' '.join(tags)
        result = re.search(pattern, tags)
        import pdb;pdb.set_trace()


ch = ComprarHamburguer()
ch.likeness_rate('Quero uma pizza')
