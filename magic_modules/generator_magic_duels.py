import itertools
import random
from typing import Dict, List, Union


class DuelsType:

    def singleDuel(
        self,
        players_or_players_and_decks: Union[Dict[str, Dict[str, bool]], List[str]],
        players_last_duel: List = [],
        decks_can_repeat: bool = False,
    ) -> Union[Dict[str, str], List[str]]:

        if isinstance(players_or_players_and_decks, list):
            players = players_or_players_and_decks
            drawn_players = random.sample(players, 2)
            return drawn_players

        elif isinstance(players_or_players_and_decks, dict):
            players_and_decks = players_or_players_and_decks

            # Cria todas as combinações possíveis de 2 jogadores
            all_combinations = list(itertools.combinations(players_and_decks.keys(), 2))

            # Remove as combinações que incluem os jogadores do último duelo
            valid_combinations = [
                comb for comb in all_combinations if set(comb) != set(players_last_duel)
            ]

            # Seleciona aleatoriamente uma das combinações válidas
            drawn_players = random.choice(valid_combinations)

            drawn_players_and_decks: Dict[str, str] = {}
            for i, drawn_player in enumerate(drawn_players, start=1):
                available_decks = [
                    deck
                    for deck, is_active in players_and_decks[drawn_player].items()
                    if is_active  # only consider the deck if it is active
                ]
                if not decks_can_repeat:
                    # Remove os decks inativos para evitar repetições
                    available_decks = [
                        deck
                        for deck in available_decks
                        if deck not in drawn_players_and_decks.values()
                    ]
                drawn_deck = random.choice(available_decks)

                key_player = f"player_{i}"
                key_deck = f"deck_{i}"
                drawn_players_and_decks[key_player] = drawn_player
                drawn_players_and_decks[key_deck] = drawn_deck

        return drawn_players_and_decks
