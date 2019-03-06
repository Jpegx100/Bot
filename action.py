import pickle
import nltk
import re


class Action(object):
    
    def __init__(self):
        self.tagger = pickle.load(open('tagger.pkl', 'rb'))
        self.tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')

    def activate(self, frame):
        if frame.keys() == self.activation_fields.keys():
            for key in frame.keys():
                if not(set(frame[key]) & set(self.activation_fields[key])):
                    return False
            return True
        return False
    
    def likeness_rate(self, text):
        tagged_words = self.tagger.tag(nltk.word_tokenize(text))
        tagged_words = ['{};{}'.format(a, b) for a, b in  tagged_words]
        tagged_words = ' '.join(tagged_words)
        pattern = (
            r'(\S+;VERB )?(?P<action>\S+;VERB) '
            r'(((\S+;ADP )?\S+;DET)|\S+;PRON) '
            r'(?P<object>\S+;NOUN)'
        )
        result = re.search(pattern, tagged_words)
        import pdb;pdb.set_trace()
    