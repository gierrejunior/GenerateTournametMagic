# list_manager.py
import streamlit as st


class DataManager:

    def addPlayer(self, player: str):
        if not st.session_state.get("players"):
            st.session_state["players"] = []

        existing_players = st.session_state["players"]

        if player.strip():
            new_players = [player.strip().upper()
                           for player in player.split(",")]
            # Adiciona os jogadores à lista
            existing_players.extend(new_players)
            # Remove jogadores duplicados mantendo a ordem original
            existing_players = list(dict.fromkeys(existing_players))
            st.success(
                f"Magiqueiro(s) {existing_players}(s) adicionado(s) com sucesso!")

    def addCommonDeck(self, common_deck: str):
        if not st.session_state.get("players_and_decks"):
            st.session_state["players_and_decks"] = {}
        if not st.session_state.get("common_decks"):
            st.session_state["common_decks"] = []

        players_and_decks = st.session_state["players_and_decks"]
        existing_common_decks = st.session_state["common_decks"]

        if common_deck.strip():
            new_common_decks = [common_deck.strip().upper()
                                for common_deck in common_deck.split(",")]
            # Adiciona os decks à lista
            existing_common_decks.extend(new_common_decks)
            # Remove decks duplicados mantendo a ordem original
            existing_common_decks = list(dict.fromkeys(existing_common_decks))

            # Inicializa a lista de decks individuais para cada jogador
            for player in st.session_state["players"]:
                if player not in players_and_decks:
                    players_and_decks[player] = {}

                # Adiciona os decks comuns à lista de decks individuais
                for deck in existing_common_decks:
                    if deck not in players_and_decks[player]:
                        players_and_decks[player][deck] = True

            st.success(
                f"Deck(s) Comunal(is) {existing_common_decks}(s) adicionado(s) com sucesso!")

    def addIndividualDecks(self, player: str, individual_deck: str):
        if not st.session_state.get("players_and_decks"):
            st.session_state["players_and_decks"] = {}

        players_and_decks = st.session_state["players_and_decks"]

        # Inicializa a lista de decks individuais para o jogador, se necessário
        if player not in players_and_decks:
            players_and_decks[player] = {}

        existing_individual_decks = players_and_decks[player]

        if individual_deck.strip():
            new_individual_decks = [individual_deck.strip().upper(
            ) for individual_deck in individual_deck.split(",")]
            # Adiciona os decks à lista
            for deck in new_individual_decks:
                # Adiciona o deck ao dicionário
                existing_individual_decks[deck] = True

            st.success(
                f"Deck(s) individual(is) {new_individual_decks}(s) do Magiqueiro {player} adicionado(s) com sucesso!")

    def removeLastPlayer(self):
        if st.session_state.get("players"):
            players = st.session_state.get("players")
            if players:
                removed_player = players.pop()
                if st.session_state.get("players_and_decks"):
                    players_and_decks = st.session_state["players_and_decks"]
                    # Verifica se o jogador existe em players_and_decks e, se existir, remove
                    if removed_player in players_and_decks:
                        del players_and_decks[removed_player]

                st.success(
                    f"Magiqueiro {removed_player} removido com sucesso!")
            else:
                st.warning("Nenhum jogador para remover.")
        else:
            st.warning("Nenhum jogador adicionado ainda.")

    def removeLastIndividualDeck(self, player: str):
        if st.session_state.get("players_and_decks"):
            players_and_decks = st.session_state.get("players_and_decks")
            if players_and_decks.get(player):
                deck_player_dict = players_and_decks.get(player)
                removed_individual_deck = list(deck_player_dict.keys())[-1]
                del deck_player_dict[removed_individual_deck]

                st.success(
                    f"Deck individual {removed_individual_deck} do Magiqueiro"
                    " {player} removido com sucesso!"
                )
            else:
                st.warning(
                    f"Nenhum deck individual para o Magiqueiro {player}.")
        else:
            st.warning("Nenhum jogador e deck adicionado ainda.")

    def removeLastCommonDeck(self):
        players = st.session_state.get("players")
        players_and_decks = st.session_state.get("players_and_decks")
        if st.session_state.get("common_decks"):
            common_decks = st.session_state.get("common_decks")
            removed_common_deck = common_decks.pop()
            for player in players:
                deck_player_dict = players_and_decks.get(player)
                if removed_common_deck in deck_player_dict:
                    del deck_player_dict[removed_common_deck]
                    st.success(
                        f"Deck Comunal {removed_common_deck} removido com sucesso!")
        else:
            st.warning("Nenhum deck comunal para remover.")

    def removeDeck(self, player, deck_to_be_removed):
        players_and_decks = st.session_state.get("players_and_decks")
        if player in players_and_decks:
            decks_player = players_and_decks.get(player)
            if deck_to_be_removed in decks_player:
                del decks_player[deck_to_be_removed]
                st.success(
                    f'Deck {deck_to_be_removed} do Magiqueiro {player} removido com sucesso!')
            else:
                st.warning("Deck não encontrado.")
        else:
            st.warning("Jogador não encontrado.")

    def deactivateDeck(self, player, deck_to_be_deactivate):
        players_and_decks = st.session_state.get("players_and_decks")
        if player in players_and_decks:
            decks_player = players_and_decks.get(player)
            if deck_to_be_deactivate in decks_player:
                if decks_player[deck_to_be_deactivate] == False:
                    st.warning(
                        f'Deck {deck_to_be_deactivate} ja está desativado')
                else:
                    decks_player[deck_to_be_deactivate] = False
                    st.success(
                        f'Deck {deck_to_be_deactivate} do Magiqueiro {player} desativado com sucesso!')
            else:
                st.warning("Deck não encontrado.")
        else:
            st.warning("Jogador não encontrado.")

    def activateDeck(self, player, deck_to_be_activate):
        players_and_decks = st.session_state.get("players_and_decks")
        if player in players_and_decks:
            decks_player = players_and_decks.get(player)
            if deck_to_be_activate in decks_player:
                if decks_player[deck_to_be_activate] == True:
                    st.warning(f'Deck {deck_to_be_activate} ja está ativo')
                else:
                    decks_player[deck_to_be_activate] = True
                    st.success(
                        f'Deck {deck_to_be_activate} do Magiqueiro {player} ativado com sucesso!')
            else:
                st.warning("Deck não encontrado.")
        else:
            st.warning("Jogador não encontrado.")

    def updateDeckStatus(self, player: str, deck: str, status: bool):
        if not st.session_state.get("players_and_decks"):
            st.session_state["players_and_decks"] = {}

        players_and_decks = st.session_state["players_and_decks"]

        # Verifica se o jogador existe em players_and_decks e, se existir, atualiza o status do deck
        if player in players_and_decks and deck in players_and_decks[player]:
            players_and_decks[player][deck] = status
