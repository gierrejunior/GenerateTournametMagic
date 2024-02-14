from generator_magic_duels import DuelsType

players = ["GR", "Gabs", "Bruno"]
decks = [
    "Agressão Arcana", "Arsenal Rebelde", "Assassinos Calculistas",
    "Catadores Ferozes", "Dominação Aérea", "Esperança Crescente",
    "Goblins pra Todo Lado", "Grande e Comande", "Legiões de Phyrexia",
    "Manter a Paz", "Sacrificio Sucateado", "Segredos de Túmulo",
    "Valor Voador", "Correndo em Frente", "Sabedoria Silvestre"]


players_last_duel = ['GR', 'Gabs']

used_decks = {
    "GR": [
        'Segredos de Túmulo',
        "Valor Voador",
        'Goblins pra Todo Lado',
        'Correndo em Frente'
    ],

    "Gabs": [
        'Sabedoria Silvestre',
        'Segredos de Túmulo',
        'Agressão Arcana',
        'Legiões de Phyrexia'
    ],

    "Bruno": [
        'Correndo em Frente',
        'Goblins pra Todo Lado',
        'Sabedoria Silvestre',
        'Dominação Aérea',
        'Catadores Ferozes'
    ]
}

# duelo = DuelsType().singleDuel(
#     players,
#     decks,
#     players_last_duel,
#     used_decks,
#     decks_can_repeat=False
# )

# print(duelo)

tournament = DuelsType().tournamentDuel(
    players,
    decks,
    used_decks,
    decks_can_repeat=False
)

print(tournament)
