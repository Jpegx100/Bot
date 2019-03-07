import pickle
import nltk
import re


class Action(object):
    is_done = False
    request_fields = list()
    fields = dict()
    activation_fields = dict()
    _req_fds = None

    def __init__(self):
        self.tagger = pickle.load(open('tagger.pkl', 'rb'))
        self.tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')

    @staticmethod
    def load_frame(text, tagger=None, tokenizer=None):
        if tagger is None:
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
        return frame

    def likeness_rate(self, frame):
        likeness = 0
        if frame.keys() == self.activation_fields.keys():
            for key in frame.keys():
                if set(frame[key]) & set(self.activation_fields[key]):
                    likeness = likeness + 1
        return likeness

    @property
    def request_field_names(self):
        if self._req_fds is None:
            sorted_req_fields = sorted(self.request_fields, key=lambda k:k.pop('order',0))
            self._req_fds = [field['name'] for field in sorted_req_fields]
        return self._req_fds

    @property
    def can_perform(self):
        return set(self.request_field_names) == set(self.fields.keys())

    def get_request_frame(self):
        for field_name in self.request_field_names:
            if field_name not in self.fields.keys():
                result = [
                    field for field in self.request_fields
                    if field['name'] == field_name
                ]
                return result[0]

    def perform_action(self):
        raise NotImplementedError()

    def perform(self):
        self.perform_action()
        self.is_done = True

    def get_ngrams(self, text, n):
        ngrams = [w for w in nltk.ngrams(text.split(), n)]
        return [' '.join(ngram) for ngram in ngrams]

    def get_bigrams(self, text):
        return self.get_ngrams(text, 2)

    def get_threegrams(self, text):
        return self.get_ngrams(text, 3)

    def feed(self, req_frame, text):
        name = req_frame['name']
        valid_function_name = 'valid_'+name
        if valid_function_name in dir(self):
            value, passed = getattr(self, valid_function_name)(text)
        else:
            value, passed = text, True

        if passed:
            self.fields[name] = value
