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
    
    def feed(self, req_frame, text):
        name = req_frame['name']
        if 'valid_'+name in dir(self):
            import pdb;pdb.set_trace()
            value = ''
        else:
            value = text
        
        self.fields[name] = value
    