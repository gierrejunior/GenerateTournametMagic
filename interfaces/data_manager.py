# list_manager.py
import streamlit as st


class DataManager:

    def addPlayer(self, player):
        if "players" not in st.session_state:
            st.session_state["players"] = []
        if player.strip():
            players = [player.strip().upper() for player in player.split(",")]
            # Adiciona os jogadores à lista
            st.session_state["players"].extend(players)
            # Remove jogadores duplicados mantendo a ordem original
            st.session_state["players"] = list(
                dict.fromkeys(st.session_state["players"])
            )
            st.success(f"Magiqueiro(s) {players}(s) adicionado(s) com sucesso!")

    def addCommonDeck(self, common_deck):
        if "players_and_decks" not in st.session_state:
            st.session_state["players_and_decks"] = {}
        if "common_decks" not in st.session_state:
            st.session_state["common_decks"] = []

        if common_deck.strip():
            common_decks = [
                common_deck.strip().upper() for common_deck in common_deck.split(",")
            ]
            st.session_state["common_decks"].extend(common_decks)
            st.session_state["common_decks"] = list(
                dict.fromkeys(st.session_state["common_decks"])
            )

            # Inicializa a lista de decks individuais para cada jogador
            for player in st.session_state["players"]:
                if player not in st.session_state["players_and_decks"]:
                    st.session_state["players_and_decks"][player] = []

                # Adiciona os decks comuns à lista de decks individuais do jogador
                st.session_state["players_and_decks"][player].extend(common_decks)

            st.success(
                f"Deck(s) Comunal(is) {common_decks}(s) adicionado(s) com sucesso!"
            )

    def addIndividualDecks(self, player, individual_deck):
        if "players_and_decks" not in st.session_state:
            st.session_state["players_and_decks"] = {}

        # Inicializa a lista de decks individuais para o jogador, se necessário
        if player not in st.session_state["players_and_decks"]:
            st.session_state["players_and_decks"][player] = []

        deck_player_list = st.session_state["players_and_decks"][player]
        if individual_deck.strip():
            individual_decks = [
                individual_deck.strip().upper()
                for individual_deck in individual_deck.split(",")
            ]
            deck_player_list.extend(individual_decks)
            deck_player_list = list(dict.fromkeys(deck_player_list))
            st.session_state["players_and_decks"][player] = deck_player_list

            st.success(
                f"Deck(s) individual(is) {individual_decks}(s) do Magiqueiro {player} adicionado(s) com sucesso!"
            )

    def removeLastPlayer(self):
        if "players" in st.session_state:
            if st.session_state["players"]:
                removed_player = st.session_state["players"].pop()
                st.success(f"Magiqueiro {removed_player} removido com sucesso!")
            else:
                st.warning("Nenhum jogador para remover.")
        else:
            st.warning("Nenhum jogador adicionado ainda.")

    def removeLastIndividualDeck(self, player):
        if "players_and_decks" in st.session_state:
            if player in st.session_state["players_and_decks"]:
                deck_player_list = st.session_state["players_and_decks"][player]
                if deck_player_list:
                    removed_individual_deck = deck_player_list.pop()
                    st.success(
                        f"Deck individual {removed_individual_deck} do Magiqueiro {player} removido com sucesso!"
                    )
                else:
                    st.warning(f"Nenhum deck individual para o Magiqueiro {player}.")
            else:
                st.warning(f"Magiqueiro {player} não encontrado.")
        else:
            st.warning("Nenhum deck individual adicionado ainda.")

    def removeLastCommonDeck(self):
        if "common_decks" in st.session_state:
            if st.session_state["common_decks"]:
                removed_common_deck = st.session_state["common_decks"].pop()
                for player in st.session_state["players"]:
                    deck_player_list = st.session_state["players_and_decks"].get(
                        player, []
                    )
                    if removed_common_deck in deck_player_list:
                        deck_player_list.remove(removed_common_deck)
                st.success(f"Deck Comunal {removed_common_deck} removido com sucesso!")
            else:
                st.warning("Nenhum deck comunal para remover.")
        else:
            st.warning("Nenhum deck comunal adicionado ainda.")
