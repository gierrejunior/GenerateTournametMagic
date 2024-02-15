# list_manager.py
import streamlit as st


class ListManager:
    def __init__(self, key, item_label):
        self.key = key
        self.item_label = item_label

        # Inicializa a lista no estado da sessão, se ainda não existir
        if self.key not in st.session_state:
            st.session_state[self.key] = []

    def add_item(self, item):
        if item.strip():
            items = [item.strip().upper() for item in item.split(",")]
            # Adiciona os itens à lista
            st.session_state[self.key].extend(items)
            # Remove itens duplicados mantendo a ordem original
            st.session_state[self.key] = list(
                dict.fromkeys(st.session_state[self.key]))
            st.success(f"{self.item_label}(s) adicionado(s) com sucesso!")

    def remove_last_item(self):
        if st.session_state[self.key]:
            item_removed = st.session_state[self.key].pop()
            st.write(f"Último {self.item_label} removido: {item_removed}")

    def display(self):
        st.write(f"Lista final de {self.item_label}s:",
                 st.session_state[self.key])
