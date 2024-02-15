import ipywidgets as widgets
from IPython.display import display


class ListManager:
    def __init__(self, lista_inicial=None, descricao_caixa='Digite um item:'):
        # Crie uma lista para armazenar os itens
        self.lista = lista_inicial or []

        # Crie um widget Text para entrada de texto
        self.text = widgets.Text(
            value='',
            description=descricao_caixa
        )

        # Crie botões para adicionar, remover e finalizar
        self.button_adicionar = widgets.Button(
            description="Adicionar Item"
        )
        self.button_remover = widgets.Button(
            description="Remover Último Item"
        )

        # Associe as funções aos botões
        self.button_adicionar.on_click(self.adicionar_item)
        self.button_remover.on_click(self.remover_ultimo_item)

        # Exiba os widgets Text e os botões
        display(self.text)
        display(self.button_adicionar)
        display(self.button_remover)

    def adicionar_item(self, b):
        item_digitado = self.text.value.strip()
        print(item_digitado)

        if item_digitado:
            # Divide a string usando vírgulas como delimitador e remove espaços em branco
            items = [item.strip() for item in item_digitado.split(",")]
            

            # Adiciona cada item à lista
            self.lista.extend(items)

            # Limpa o conteúdo da caixa de texto após adicionar o(s) item(ns)
            self.text.value = ""

        print(self.lista)  # Exibe a lista após adicionar item

    def remover_ultimo_item(self, b):
        if self.lista:
            item_remover = self.lista.pop()
            print(f"Último item removido: {item_remover}")
        else:
            print("Lista vazia")

        print(self.lista)  # Exibe a lista após remover item

    def finalizar(self, b):
        return self.lista
