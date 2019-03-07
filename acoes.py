import nltk
import re

import action


class VerMenu(action.Action):
    request_fields = []
    activation_fields = {
        'action': ['querer', 'ver', 'mostrar', 'enviar'],
        'object': ['cardapio', 'menu']
    }

    def perform_action(self):
        print("""
        -----------MENU-----------
        X-Burguer         R$ 12,50
        Egg-Burguer       R$ 12,50
        X-Ignorância      R$ 12,50
        X-Tudo            R$ 12,50
        """)


class ComprarHamburguer(action.Action):
    request_fields = [
        {
            'name': 'hamburguer',
            'text': 'Qual hamburguer gostaria?',
            'order': 1
        }, {
            'name': 'endereco',
            'text': 'Qual o endereço de entrega?',
            'order': 2
        }
    ]

    activation_fields = {
        'action': ['querer', 'comprar'],
        'object': ['hamburger', 'burguer']
    }

    hamburger = None
    quantidade = None

    def perform_action(self):
        if self.quantidade > 1:
            msg = 'Os seus {}s estão sendo preparados :)'
        else:
            msg = 'O seu {} está sendo preparado e será entregue em "{}" :)'
        print(msg.format(self.fields['hamburguer'], self.fields['endereco']))

    def valid_endereco(self, text):
        print('Você confirma a entrega em: "{}"?'.format(text))
        confirm = 'sim' in input().lower() or 'confirm' in input().lower()
        while not confirm:
            print('Por favor digite o endereço correto: ')
            text = input()
            print('Você confirma a entrega em: "{}"?'.format(text))
            confirm = 'sim' in input().lower() or 'confirm' in input().lower()

        return text, True

    def valid_quantidade(self, text):
        quant = re.search(r'\d+', text)
        if quant is not None:
            self.quantidade = int(quant)

        quantidades = {
            'um': 1, 'dois': 2, 'três': 3, 'quatro': 4, 'cinco': 5, 'seis': 6,
            'sete': 7, 'oito': 8, 'nove': 9, 'dez': 10, 'onze': 11, 'doze': 12,
            'treze': 13, 'quatorze': 14, 'quinze': 15, 'dezesseis': 16,
            'dezessete': 17, 'dezoito': 18, 'dezenove': 19, 'vinte': 20,
            'trinta': 30, 'quarenta': 40, 'cinquenta': 50, 'sessenta': 60
        }

        words = text.split()
        quantidade = 0
        for key in quantidades:
            for word in words:
                if nltk.edit_distance(key, word) <= 1:
                    quantidade = quantidade + quantidades[key]
        if quantidade > 0:
            self.quantidade = quantidade
        else:
            print('Quantos hamburguers você quer?')
            text = input()
            self.valid_quantidade(text)

    def valid_hamburguer(self, text):
        frame = self.load_frame(text)
        ver_menu = VerMenu()
        if ver_menu.likeness_rate(frame) > self.likeness_rate(frame):
            ver_menu.perform()
            return '', False
        else:
            ngrams = (
                text.split() +
                self.get_bigrams(text) +
                self.get_threegrams(text)
            )

            hamburguer_dist = []
            hamburguers = ['x-burguer', 'egg-burguer', 'x-ignorância', 'x-tudo']
            for w in ngrams:
                for h in hamburguers:
                    hamburguer_dist.append((w, h, nltk.edit_distance(w, h)))

            hamburguer_dist = sorted(hamburguer_dist, key=lambda k:k[2])
            if hamburguer_dist[0][2] <= (len(hamburguer_dist[0][1])/2):
                self.valid_quantidade(text)
                return hamburguer_dist[0][1], True
            else:
                print('Não consegui identificar seu pedido. Veja nosso menu: ')
                ver_menu.perform()
                return '', False
