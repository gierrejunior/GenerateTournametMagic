import streamlit as st

from interfaces.list_manager import ListManager
from magic_random.generator_magic_duels import DuelsType

if __name__ == '__main__':
    # Adiciona jogadores
    item_digitado_player = st.text_input(label='Digite um player:')
    player_manager = ListManager("players", "player")
    if st.button(f"Adicionar {player_manager.item_label}"):
        player_manager.add_item(item_digitado_player)
    if st.button(f"Remover Último {player_manager.item_label}"):
        player_manager.remove_last_item()
    player_manager.display()

    # Adiciona decks
    item_digitado_deck = st.text_input(label='Digite um deck:')
    deck_manager = ListManager("decks", "deck")
    if st.button(f"Adicionar {deck_manager.item_label}"):
        deck_manager.add_item(item_digitado_deck)
    if st.button(f"Remover Último {deck_manager.item_label}"):
        deck_manager.remove_last_item()
    deck_manager.display()

    # Adiciona uma janela para selecionar múltiplos players do último duelo
    last_duel = st.multiselect(
        label='Último duelo',
        options=st.session_state.players
    )

    if len(last_duel) > 2:
        st.error(
            'Por favor, selecione no máximo dois players que duelaram no último jogo')
    elif len(last_duel) == 2:
        st.write(f"Último duelo: {', '.join(last_duel)}")
        # Aqui você pode adicionar os jogadores à sua variável ou fazer qualquer outra operação necessária

    # Adiciona a opção de escolher o modo de jogo
    if len(st.session_state.players) > 1 and len(st.session_state.decks) >= 2:
        # Verifica se o modo torneio é válido
        if len(st.session_state.players) % 2 == 0:
            modo = st.radio(
                label='Escolha o modo:',
                options=['Duelo simples', 'Torneio'],
                horizontal=True,
                index=0
            )
            st.write(f"Modo escolhido: {modo}")
        else:
            modo = st.radio(
                label='Escolha o modo:',
                options=['Duelo simples'],
                horizontal=True,
                index=0,
            )
            st.error(
                'O modo torneio só fica ativo se o número de jogadores for par.')
            st.write(f"Modo escolhido: {modo}")

    else:
        st.radio(
            label='Escolha o modo:',
            options=['Duelo simples', 'Torneio'],
            horizontal=True,
            disabled=True,
        )
        st.write(
            'Você precisa ter mais de um jogador e pelo menos dois'
            'decks adicionados para escolher o modo de jogo.'
        )

    # Seleção se os decks podem ser iguais
    if len(st.session_state.players) > 1 and len(st.session_state.decks) >= 2:
        repeat_deck = st.radio(
            label='Os Decks entre os adversarios podem ser o mesmo?:',
            options=['sim', 'nao'],
            horizontal=True,
            index=1
        )
    else:
        repeat_deck = st.radio(
            label='Os Decks entre os adversarios podem ser o mesmo?:',
            options=['sim', 'nao'],
            horizontal=True,
            disabled=True,
        )
        st.write(
            'Você precisa ter mais de um jogador e pelo menos dois decks'
            'adicionados para optar se os decks poderão se repetir.'
        )

    # if len(st.session_state.players) > 1 and len(st.session_state.decks) >= 2:
    #     if
    #     if modo == 'Duelo simples':
    #         duel = DuelsType().singleDuel(
    #             players=player_manager,
    #             decks=deck_manager

    #         )
