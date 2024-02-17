import streamlit as st

from interfaces.data_manager import DataManager
from magic_modules.generator_magic_duels import DuelsType

# from magic_modules.generator_magic_duels import DuelsType

if __name__ == "__main__":
    modo = ""
    # Adiciona jogadores
    player_name_input = st.text_input(label="Digite o nome do Magiqueiro(s):")
    if st.button("Adicionar Magiqueiro"):
        DataManager().addPlayer(player_name_input)
        st.write("Lista final de Magiqueiros:", st.session_state.players)
    if st.button("Remover Último nome"):
        DataManager().removeLastPlayer()
        st.write("Lista final de Magiqueiros:", st.session_state.players)

    if st.session_state.get("players"):

        # pergunta se quer aleatorizar os decks tambem
        is_random_decks = st.checkbox("Aleatorizar Decks tambem?")

        # adiciona decks para serem aleatorizados
        if is_random_decks:
            if st.checkbox("Registrar deck(s) Communal(is)"):
                # Adiciona decks Comunais
                common_deck_input = st.text_input(label="Digite os decks em comum:")
                if st.button("Adicionar Deck(s) Comunal(is)"):
                    DataManager().addCommonDeck(common_deck_input)
                    st.write(st.session_state.players_and_decks)

                if st.button("Remover Último deck em comum"):
                    DataManager().removeLastCommonDeck()
                    st.write(st.session_state.players_and_decks)

            # Verifica se há decks individuais a serem adicionados
            if st.checkbox("Registrar decks Individuais"):
                # Pergunta ao usuário qual jogador deseja associar os decks individuais
                selected_player = st.selectbox(
                    "Escolha o Magiqueiro:", st.session_state.players
                )

                individual_decks_input = st.text_input(
                    label="Digite os decks individuais:"
                )

                if st.button("Adicionar Deck(s) Individual(is)"):
                    DataManager().addIndividualDecks(
                        selected_player, individual_decks_input
                    )
                    st.write(st.session_state.players_and_decks)

                if st.button("Remover Último deck individual"):
                    DataManager().removeLastIndividualDeck(selected_player)
                    st.write(st.session_state.players_and_decks)

        # Decide se os decks dos adversarios podem ser o mesmo
        if is_random_decks:
            can_repeat_deck = st.checkbox(
                "Os Decks entre os adversários podem ser o mesmo?"
            )
        # define os modos que podem ser escolhidos a partir dos requisitos
        if len(st.session_state.players) > 1:

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
                    "O modo torneio só fica ativo se o número de jogadores for par."
                )
                st.write(f"Modo escolhido: {modo}")

        else:
            st.write(
                "Você precisa ter mais de um jogador para escolher o modo de jogo."
            )

        if (modo == "Duelo simples") and (not is_random_decks):
            # Pergunta se quer adicioanr os jogadores do ultimo duelo
            is_add_last_duel = st.checkbox(
                "Gostaria de adicionar os jogadores do ultimo duelo?"
            )

            # Adiciona uma janela para selecionar os dois players do último duelo
            players_last_duel = []
            if is_add_last_duel:
                players_last_duel = st.multiselect(
                    label="Último duelo", options=st.session_state.players
                )
                if len(players_last_duel) > 2:
                    st.error(
                        "Por favor, selecione no máximo dois players"
                        " que duelaram no último jogo"
                    )
                elif len(players_last_duel) == 2:
                    st.write(f"Último duelo: {', '.join(players_last_duel)}")

        if (modo == "Duelo simples") and (is_random_decks):

            # Pergunta se quer adicioanr os jogadores do ultimo duelo
            is_add_last_duel = st.checkbox(
                "Gostaria de adicionar os jogadores do ultimo duelo?"
            )
            # Adiciona uma janela para selecionar os dois players do último duelo
            players_last_duel = []
            if is_add_last_duel:
                players_last_duel = st.multiselect(
                    label="Último duelo", options=st.session_state.players
                )
                if len(players_last_duel) > 2:
                    st.error(
                        "Por favor, selecione no máximo dois players"
                        " que duelaram no último jogo"
                    )
                elif len(players_last_duel) == 2:
                    st.write(f"Último duelo: {', '.join(players_last_duel)}")

    # Botão Processar
    if st.button("Processar"):
        if modo == "Duelo simples":
            if not is_random_decks:
                st.write(
                    DuelsType().singleDuel(
                        st.session_state.players,
                        players_last_duel,
                    )
                )
            else:
                st.write(
                    DuelsType().singleDuel(
                        st.session_state.players_and_decks,
                        players_last_duel,
                        can_repeat_deck,
                    )
                )

    # # Botão processar
    # if st.button("Processar"):
    #     if modo == "Duelo simples":
    #         simple_duel = DuelsType().singleDuel(
    #             players=st.session_state["players"],
    #             decks=st.session_state["decks"],
    #             players_last_duel=last_duel,
    #             used_decks={},
    #             decks_can_repeat=repeat,
    #         )

    #         duel = simple_duel[0]
    #         # Escreve a saída formatada
    #         st.markdown(
    #             f"<center><h2>Magiqueiro: {duel.get('player1')}</h2><h2> com o Deck: {duel.get('deck1')}</h2><h1>VS</h1><h2> Magiqueiro: {duel.get('player2')}</h2><h2> com o Deck: {duel.get('deck2')}</h2></center>",
    #             unsafe_allow_html=True,
    #         )
    #         st.session_state["Duelo simples"] = duel

    #     elif modo == "Torneio":
    #         if "winners" not in st.session_state:
    #             st.session_state["winners"] = st.session_state["players"]

    #         if "used_decks" not in st.session_state:
    #             st.session_state["used_decks"] = {
    #                 player: [] for player in st.session_state["players"]
    #             }

    #         duels = DuelsType().tournamentDuel(
    #             players=st.session_state["winners"],
    #             decks=st.session_state["decks"],
    #             used_decks=st.session_state["used_decks"],
    #             decks_can_repeat=repeat,
    #         )

    #         st.session_state["torneio"] = duels

    # if "torneio" in st.session_state:
    #     duels = st.session_state["torneio"]
    #     # Imprime os duelos e pede ao usuário para escolher o vencedor de cada duelo
    #     winners = []
    #     for i, duel in enumerate(duels):
    #         st.markdown(
    #             f"## Duelo {i+1}\n\n**{duel['player1']}** usando **{duel['deck1']}** VS **{duel['player2']}** usando **{duel['deck2']}**"
    #         )
    #         winner = st.selectbox(
    #             f"Escolha o vencedor do duelo {i+1}",
    #             [duel["player1"], duel["player2"]],
    #             key=f"duel_{i}",
    #         )

    #         # Salva a seleção do vencedor no session_state
    #         st.session_state[f"winner_{i}"] = winner

    #     if st.button("Finalizar"):
    #         winners = [st.session_state[f"winner_{i}"] for i in range(len(duels))]

    #         # Atualiza o dicionário used_decks após cada duelo
    #         for i in range(len(duels)):
    #             winner = st.session_state[f"winner_{i}"]
    #             deck = (
    #                 duels[i]["deck1"]
    #                 if duels[i]["player1"] == winner
    #                 else duels[i]["deck2"]
    #             )
    #             st.session_state["used_decks"][winner].append(deck)

    #         # Realiza um novo torneio com os vencedores
    #         st.session_state["winners"] = winners

    #         if repeat:
    #             st.session_state["torneio"] = DuelsType().randomizeDecksCanRepeat(
    #                 decks=st.session_state["decks"],
    #                 players=st.session_state["winners"],
    #                 used_decks=st.session_state["used_decks"],
    #             )
    #         else:
    #             st.session_state["torneio"] = DuelsType().randomizeDecksNoRepeat(
    #                 decks=st.session_state["decks"],
    #                 players=st.session_state["winners"],
    #                 used_decks=st.session_state["used_decks"],
    #             )

    #         # Atualiza a variável duels para a próxima rodada de duelos
    #         duels = st.session_state["torneio"]
