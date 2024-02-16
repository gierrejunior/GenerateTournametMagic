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
            simple_duel = DuelsType().singleDuel(
                players=st.session_state["players"],
                decks=st.session_state["decks"],
                players_last_duel=last_duel,
                used_decks={},
                decks_can_repeat=repeat,
            )

            duel = simple_duel[0]
            # Escreve a saída formatada
            st.markdown(
                f"<center><h2>Magiqueiro: {duel.get('player1')}</h2><h2> com o Deck: {duel.get('deck1')}</h2><h1>VS</h1><h2> Magiqueiro: {duel.get('player2')}</h2><h2> com o Deck: {duel.get('deck2')}</h2></center>", unsafe_allow_html=True
            )
            st.session_state["Duelo simples"] = duel

        elif modo == "Torneio":
            if "winners" not in st.session_state:
                st.session_state["winners"] = st.session_state["players"]

            if "used_decks" not in st.session_state:
                st.session_state["used_decks"] = {player: []
                                                  for player in st.session_state["players"]}

            duels = DuelsType().tournamentDuel(
                players=st.session_state["winners"],
                decks=st.session_state["decks"],
                used_decks=st.session_state["used_decks"],
                decks_can_repeat=repeat,
            )

            st.session_state["torneio"] = duels

    if "torneio" in st.session_state:
        duels = st.session_state["torneio"]
        # Imprime os duelos e pede ao usuário para escolher o vencedor de cada duelo
        winners = []
        for i, duel in enumerate(duels):
            st.markdown(
                f"## Duelo {i+1}\n\n**{duel['player1']}** usando **{duel['deck1']}** VS **{duel['player2']}** usando **{duel['deck2']}**")
            winner = st.selectbox(f'Escolha o vencedor do duelo {i+1}', [
                duel['player1'], duel['player2']], key=f"duel_{i}")

            # Salva a seleção do vencedor no session_state
            st.session_state[f"winner_{i}"] = winner

        if st.button("Finalizar"):
            winners = [st.session_state[f"winner_{i}"]
                       for i in range(len(duels))]

            # Atualiza o dicionário used_decks após cada duelo
            for i in range(len(duels)):
                winner = st.session_state[f"winner_{i}"]
                deck = duels[i]['deck1'] if duels[i]['player1'] == winner else duels[i]['deck2']
                st.session_state["used_decks"][winner].append(deck)

            # Realiza um novo torneio com os vencedores
            st.session_state["winners"] = winners

            if repeat:
                st.session_state["torneio"] = DuelsType().randomizeDecksCanRepeat(
                    decks=st.session_state["decks"],
                    players=st.session_state["winners"],
                    used_decks=st.session_state["used_decks"]
                )
            else:
                st.session_state["torneio"] = DuelsType().randomizeDecksNoRepeat(
                    decks=st.session_state["decks"],
                    players=st.session_state["winners"],
                    used_decks=st.session_state["used_decks"],
                )

            # Atualiza a variável duels para a próxima rodada de duelos
            duels = st.session_state["torneio"]
