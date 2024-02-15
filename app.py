import streamlit as st

from interfaces.list_manager import ListManager
from magic_random.generator_magic_duels import DuelsType

if __name__ == '__main__':
    item_digitado_player = st.text_input(label='Digite um player:')
    player_manager = ListManager("players", "player")
    if st.button(f"Adicionar {player_manager.item_label}"):
        player_manager.add_item(item_digitado_player)
    if st.button(f"Remover Último {player_manager.item_label}"):
        player_manager.remove_last_item()
    player_manager.display()

    item_digitado_deck = st.text_input(label='Digite um deck:')
    deck_manager = ListManager("decks", "deck")
    if st.button(f"Adicionar {deck_manager.item_label}"):
        deck_manager.add_item(item_digitado_deck)
    if st.button(f"Remover Último {deck_manager.item_label}"):
        deck_manager.remove_last_item()
    deck_manager.display()

    # Adiciona uma janela para selecionar múltiplos players para o último duelo
    ultimo_duelo = st.multiselect(
        label='Último duelo', options=st.session_state.players)
    if len(ultimo_duelo) > 2:
        st.error('Por favor, selecione no máximo dois players para o último duelo.')
    else:
        st.write(f"Último duelo: {', '.join(ultimo_duelo)}")

    # Adiciona a opção de escolher o modo de jogo
    # Verifica se há mais de um jogador e pelo menos dois decks adicionados
    if len(st.session_state.players) > 1 and len(st.session_state.decks) >= 2:
        # Verifica se o modo torneio é válido
        if len(st.session_state.players) % 2 == 0:
            # Cria duas bolinhas para o usuário clicar
            # Define o índice da opção de duelo simples como 0
            modo = st.radio(
                label='Escolha o modo:',
                options=['Duelo simples', 'Torneio'],
                index=0
            )
            st.write(f"Modo escolhido: {modo}")
        else:
            # Cria duas bolinhas para o usuário clicar
            # Define o índice da opção de duelo simples como 0
            # Desabilita a opção de torneio usando uma string
            modo = st.radio(
                label='Escolha o modo:',
                options=['Duelo simples'],
                index=0,
            )
            st.error(
                'O modo torneio só fica ativo se o número de jogadores for par.')
            st.write(f"Modo escolhido: {modo}")

    else:
        # Desabilita a opção de escolher o modo de jogo
        st.radio(label='Escolha o modo:', options=[
                 'Duelo simples', 'Torneio'], disabled=True)
        st.write(
            'Você precisa ter mais de um jogador e pelo menos dois decks adicionados para escolher o modo de jogo.')
