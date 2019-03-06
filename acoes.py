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
        Egg Burguer       R$ 12,50
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
            'name': 'quantidade',
            'text': 'Quantos hamburguers você quer?',
            'order': 2
        }, {
            'name': 'endereco',
            'text': 'Qual o endereço de entrega?',
            'order': 3
        }
    ]

    activation_fields = {
        'action': ['querer', 'comprar'],
        'object': ['hamburger', 'burguer']
    }

    def quantidade_validator(self):
        return True
    
    def perform_action(self):
        print('O hamburguer está sendo preparado :)')
