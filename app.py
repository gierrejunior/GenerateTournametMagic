import streamlit as st

from interfaces.list_manager import ListManager
from magic_modules.generator_magic_duels import DuelsType


if __name__ == "__main__":
    # Adiciona jogadores
    item_digitado_player = st.text_input(label="Digite um player:")
    player_manager = ListManager("players", "player")
    if st.button(f"Adicionar {player_manager.item_label}"):
        player_manager.add_item(item_digitado_player)
    if st.button(f"Remover Último {player_manager.item_label}"):
        player_manager.remove_last_item()
    player_manager.display()

    # Adiciona decks
    item_digitado_deck = st.text_input(label="Digite um deck:")
    deck_manager = ListManager("decks", "deck")
    if st.button(f"Adicionar {deck_manager.item_label}"):
        deck_manager.add_item(item_digitado_deck)
    if st.button(f"Remover Último {deck_manager.item_label}"):
        deck_manager.remove_last_item()
    deck_manager.display()

    # Adiciona a opção de escolher o modo de jogo
    if len(st.session_state.players) > 1 and len(st.session_state.decks) >= 2:
        # Verifica se o modo torneio é válido
        if len(st.session_state.players) % 2 == 0:
            modo = st.radio(
                label="Escolha o modo:",
                options=["Duelo simples", "Torneio"],
                horizontal=True,
                index=0,
            )
            st.write(f"Modo escolhido: {modo}")
        else:
            modo = st.radio(
                label="Escolha o modo:",
                options=["Duelo simples"],
                horizontal=True,
                index=0,
            )
            st.error(
                "O modo torneio só fica ativo se o número de jogadores for par.")
            st.write(f"Modo escolhido: {modo}")

    else:
        st.radio(
            label="Escolha o modo:",
            options=["Duelo simples", "Torneio"],
            horizontal=True,
            disabled=True,
        )
        st.write(
            "Você precisa ter mais de um jogador e pelo menos dois"
            "decks adicionados para escolher o modo de jogo."
        )

    if len(st.session_state.players) > 1 and len(st.session_state.decks) >= 2:
        if modo:
            if modo == "Duelo simples":
                # Adiciona uma janela para selecionar múltiplos players do último duelo
                last_duel = []
                if "players" in st.session_state and st.session_state.players:
                    last_duel = st.multiselect(
                        label="Último duelo", options=st.session_state.players
                    )

                if len(last_duel) > 2:
                    st.error(
                        'Por favor, selecione no máximo dois players'
                        ' que duelaram no último jogo'
                    )
                elif len(last_duel) == 2:
                    st.write(f"Último duelo: {', '.join(last_duel)}")

    # Seleção se os decks podem ser iguais
    if len(st.session_state.players) > 1 and len(st.session_state.decks) >= 2:
        repeat_deck = st.radio(
            label="Os Decks entre os adversarios podem ser o mesmo?:",
            options=["sim", "nao"],
            horizontal=True,
            index=1,
        )
    else:
        repeat_deck = st.radio(
            label="Os Decks entre os adversarios podem ser o mesmo?:",
            options=["sim", "nao"],
            horizontal=True,
            disabled=True,
        )
        st.write(
            "Você precisa ter mais de um jogador e pelo menos dois decks"
            "adicionados para optar se os decks poderão se repetir."
        )

    if repeat_deck == "sim":
        repeat = True
    else:
        repeat = False

    # Botão processar
    if st.button("Processar"):
        if modo == "Duelo simples":
            duel = DuelsType().singleDuel(
                players=st.session_state["players"],
                decks=st.session_state["decks"],
                players_last_duel=last_duel,
                used_decks={},
                decks_can_repeat=repeat,
            )

        elif modo == "Torneio":
            duel = DuelsType().tournamentDuel(
                players=st.session_state["players"],
                decks=st.session_state["decks"],
                used_decks={},
                decks_can_repeat=repeat,
            )

        st.write(duel)
