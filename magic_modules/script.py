# from magic_modules.generator_magic_duels import DuelsType

# players = ["GR", "Gabs", "Bruno"]
# decks = [
#     "Agressão Arcana", "Arsenal Rebelde", "Assassinos Calculistas",
#     "Catadores Ferozes", "Dominação Aérea", "Esperança Crescente",
#     "Goblins pra Todo Lado", "Grande e Comande", "Legiões de Phyrexia",
#     "Manter a Paz", "Sacrificio Sucateado", "Segredos de Túmulo",
#     "Valor Voador", "Correndo em Frente", "Sabedoria Silvestre"]


# players_last_duel = ['GR', 'Gabs']

# used_decks = {
#     "GR": [
#         'Segredos de Túmulo',
#         "Valor Voador",
#         'Goblins pra Todo Lado',
#         'Correndo em Frente'
#     ],

#     "Gabs": [
#         'Sabedoria Silvestre',
#         'Segredos de Túmulo',
#         'Agressão Arcana',
#         'Legiões de Phyrexia'
#     ],

#     "Bruno": [
#         'Correndo em Frente',
#         'Goblins pra Todo Lado',
#         'Sabedoria Silvestre',
#         'Dominação Aérea',
#         'Catadores Ferozes'
#     ]
# }

# # duelo = DuelsType().singleDuel(
# #     players,
# #     decks,
# #     players_last_duel,
# #     used_decks,
# #     decks_can_repeat=False
# # )

# # print(duelo)

# tournament = DuelsType().tournamentDuel(
#     players,
#     decks,
#     used_decks,
#     decks_can_repeat=False
# )

# print(tournament)


import os
embaralhando = 'images/embaralhando'
general = 'images/general'
magic = 'images/magic_the_gathering'
yugioh = 'images/yu_gi_oh'
alone = 'images/alone'


def renomear_arquivos(diretorio):
    for count, filename in enumerate(os.listdir(diretorio)):
        # Divide o nome do arquivo e a extensão
        nome, ext = os.path.splitext(filename)
        # Formata o novo nome do arquivo
        novo_nome = "{:02d}{}".format(count+1, ext)
        # Cria o caminho completo para o arquivo original e o novo arquivo
        arquivo_original = os.path.join(diretorio, filename)
        novo_arquivo = os.path.join(diretorio, novo_nome)
        # Renomeia o arquivo
        os.rename(arquivo_original, novo_arquivo)


def excluir_arquivos(diretorio):
    for filename in os.listdir(diretorio):
        if filename.endswith(".identifier"):
            os.remove(os.path.join(diretorio, filename))

gierre, gabs, bruno

# # Substitua 'caminho_para_sua_pasta' pelo caminho do diretório que contém os arquivos que você deseja renomear
renomear_arquivos(alone)
# Substitua 'caminho_para_sua_pasta' pelo caminho do diretório que contém os arquivos que você deseja excluir
excluir_arquivos(alone)


    "Agressão Arcana", "Arsenal Rebelde", "Assassinos Calculistas",
    "Catadores Ferozes", "Dominação Aérea", "Esperança Crescente",
    "Goblins pra Todo Lado", "Grande e Comande", "Legiões de Phyrexia",
    "Manter a Paz", "Sacrificio Sucateado", "Segredos de Túmulo",
    "Valor Voador", "Correndo em Frente", "Sabedoria Silvestre"
