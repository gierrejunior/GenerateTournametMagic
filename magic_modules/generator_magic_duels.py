import copy
import random
from typing import Dict, List


class RandomizeList:
    """_summary_"""

    def randomizeList(self, times: int, _list: list) -> list:
        """_summary_

        Args:
            times (_type_): _description_
            _list (_type_): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if not _list:
            raise ValueError(
                "RandomizeList: The list is empty."
                " You cannot randomize an empty list."
            )
        result_list = []
        for i in range(times):
            result = random.choice(_list)
            _list.remove(result)
            result_list.append(result)
        return result_list

    def randomizelists(self, *args: list) -> list:
        """_summary_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        result_list = []
        deck_choiced = ""
        for _list in args:
            if not _list:
                raise ValueError(
                    "RandomizeList: The list is empty."
                    " You cannot randomize an empty list."
                )
            if deck_choiced:
                if deck_choiced in _list:
                    _list.remove(deck_choiced)
            result = random.choice(_list)
            deck_choiced = result
            result_list.append(result)
        return result_list


class GeneratorMagicDuels(RandomizeList):

    def randomizePlayers(self, players: list, players_last_duel: list = []) -> List:
        temp_players = copy.deepcopy(players)
        temp_player_last_duel = copy.deepcopy(players_last_duel)
        if not temp_players:
            raise ValueError(
                "randomizePlayers: The list is empty."
                "You cannot randomize an empty list."
            )

        if temp_player_last_duel:
            excluded_player = random.choice(temp_player_last_duel)
            temp_players.remove(excluded_player)

        return self.randomizeList(2, temp_players)

    def randomizeDecksNoRepeat(
        self, decks: list, players: list, used_decks: dict = {}
    ) -> List:

        if not decks:
            raise ValueError(
                "randomizeDecks: The list is empty."
                " You cannot randomize an empty list."
            )

        decks_to_choose = []
        for player in players:
            temp_deck = copy.deepcopy(decks)
            if used_decks:
                player_used_decks = used_decks.get(player)
                if player_used_decks:
                    for player_used_deck in player_used_decks:
                        temp_deck.remove(player_used_deck)
            if not temp_deck:
                raise ValueError(
                    f"randomizeDecks: The list is empty."
                    f" the player: {player} has already played"
                    f" with all available decks."
                )
            decks_to_choose.append(temp_deck)
        final_result_decks = self.randomizelists(*decks_to_choose)

        return final_result_decks

    def randomizeDecksCanRepeat(
        self, decks: list, players: list, used_decks: dict = {}
    ) -> List:

        if not decks:
            raise ValueError(
                "randomizeDecks: The list is empty."
                "You cannot randomize an empty list."
            )

        final_result_decks = []
        choice_deck = []
        for player in players:
            temp_deck = copy.deepcopy(decks)
            if used_decks:
                player_used_decks = used_decks.get(player)
                if player_used_decks:
                    for player_used_deck in player_used_decks:
                        temp_deck.remove(player_used_deck)
            choice_deck = self.randomizeList(1, temp_deck)
            final_result_decks.append(choice_deck)

        return final_result_decks

    def generateDictDuel(self, players: List, decks: List) -> List[Dict]:
        if not players or not decks:
            raise ValueError(
                "generateDictDuel: The list is empty."
                " You cannot randomize an empty list."
            )

        duel = [
            {
                "player1": players[i],
                "deck1": decks[i],
                "player2": players[i + 1],
                "deck2": decks[i + 1],
            }
            for i in range(0, len(players), 2)
        ]
        return duel


class DuelsType(GeneratorMagicDuels):

    def singleDuel(
        self,
        players_or_players_and_decks: dict[str, list[str]] | list[str],
        players_last_duel: list = [],
        decks_can_repeat: bool = False,
    ) -> dict[str, str] | list[str]:
        if isinstance(players_or_players_and_decks, list):
            players = players_or_players_and_decks
            drawn_players = random.sample(players, 2)
            return drawn_players

        elif isinstance(players_or_players_and_decks, dict):
            players_and_decks = players_or_players_and_decks

            pd_last_duel_removed = {
                key: value
                for key, value in players_and_decks.items()
                if value not in players_last_duel
            }

            drawn_players = random.sample(pd_last_duel_removed.keys(), 2)
            drawn_players_and_decks: dict[str, str] = {}
            for i, drawn_player in enumerate(drawn_players, start=1):
                if decks_can_repeat:
                    drawn_deck = random.choice(players_and_decks[drawn_player])
                else:
                    # Remove o deck já sorteado para evitar repetições
                    available_decks = [
                        deck
                        for deck in players_and_decks[drawn_player]
                        if deck not in drawn_players_and_decks.values()
                    ]
                    drawn_deck = random.choice(available_decks)

                key_player = f"player_{i}"
                key_deck = f"deck_{i}"
                drawn_players_and_decks[key_player] = drawn_player
                drawn_players_and_decks[key_deck] = drawn_deck

            return drawn_players_and_decks


    def tournamentDuel(
        self,
        players: list,
        common_decks: list,
        decks_can_repeat: bool = False,
    ):
        pass
        # temp_players = copy.deepcopy(players)
        # tournament = []
        # n_players = len(players)
        # n_brackets = n_players // 2

        # for player in players:
        #     player_deck = {player: decks}

        # for bracket in range(n_brackets):

        #     f"bracket{n_brackets}": {}

        #     random_players = self.randomizePlayers(temp_players)
        #     if isinstance(random_players, ValueError):
        #         return random_players

        #     new_players_list = [
        #         player for player in temp_players if player not in random_players
        #     ]

        #     temp_players = new_players_list

        #     if decks_can_repeat:
        #         random_decks = self.randomizeDecksCanRepeat(
        #             decks, random_players, used_decks
        #         )
        #     else:
        #         random_decks = self.randomizeDecksNoRepeat(
        #             decks, random_players, used_decks
        #         )
        #     if isinstance(random_decks, ValueError):
        #         return random_decks

        #     match = self.generateDictDuel(random_players, random_decks)
        #     if isinstance(match, ValueError):
        #         return match

        #     # Adicione cada dicionário individualmente à lista do torneio
        #     tournament.extend(match)

        # return tournament
