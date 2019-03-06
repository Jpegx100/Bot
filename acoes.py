import action


class VerMenu(action.Action):
    request_fields = []
    fields = list()
    activation_fields = {
        'action': ['querer', 'ver', 'mostrar', 'enviar'],
        'object': ['cardapio', 'menu']
    }


class ComprarHamburguer(action.Action):
    request_fields = ['hamburguer', 'quantidade', 'endereco']
    fields = list()
    activation_fields = {
        'action': ['querer', 'comprar'],
        'object': ['hamburger', 'burguer']
    }
