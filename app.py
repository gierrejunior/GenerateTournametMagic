import base64
import os
import random

import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.stoggle import stoggle

from magic_modules.generator_magic_duels import DuelsType
from repositories.data_manager import DataManager


def autoplay_loop_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
    <audio controls autoplay loop>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)


def listar_arquivos(diretorio):
    lista_de_arquivos = []
    for filename in os.listdir(diretorio):
        lista_de_arquivos.append(f'{diretorio}/{filename}')
    return lista_de_arquivos


image_screen_top = 'images/general/01.jpeg'
autoplay_loop_audio("sound/YuGiOh-Full.mp3")
st.image(image_screen_top, use_column_width=True)
add_logo('images/general/02.jpg')


if __name__ == "__main__":
    yes_or_no = ["Sim", "Não"]
    is_random_decks = False
    imgs_yugioh = listar_arquivos('images/yu_gi_oh')
    imgs_general = listar_arquivos('images/general')
    imgs_magic = listar_arquivos('images/magic_the_gathering')
    imgs_embaralhando = listar_arquivos('images/embaralhando')
    imgs_alone = listar_arquivos('images/alone')
    players_last_duel = []

    # Adiciona jogadores
    player_name_input = st.text_input(label="Digite o nome do Magiqueiro(s):")

    col1, col2 = st.columns(2)

    if col1.button("Adicionar Magiqueiro(s)"):
        DataManager().addPlayer(player_name_input)

    if st.session_state.get("players"):
        if col2.button("Remover Último nome"):
            DataManager().removeLastPlayer()

        players_string = ', '.join(st.session_state.players)
        stoggle("Lista de Magiqueiros:", players_string)

        if len(st.session_state.get("players")) >= 2:  # type: ignore
            # Da a opção de randomizar os decks, sim ou não
            randomize_decks = st.radio(
                label="Sortear os Decks ?",
                options=yes_or_no,
                horizontal=True,
                index=1,
            )

            if randomize_decks == yes_or_no[0]:
                is_random_decks = True
            else:
                is_random_decks = False

            # adiciona decks para serem aleatorizados
            if is_random_decks:
                if st.checkbox("Registrar deck(s) Communal(is)"):
                    # Adiciona decks Comunais
                    common_deck_input = st.text_input(
                        label="Digite os decks em comum:")
                    col1, col2 = st.columns(2)

                    if col1.button("Adicionar Deck(s) Comunal(is)"):
                        DataManager().addCommonDeck(common_deck_input)
                        st.write(st.session_state.players_and_decks)

                    if col2.button("Remover Último deck em comum"):
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

                    col1, col2 = st.columns(2)

                    if col1.button("Adicionar Deck(s) Individual(is)"):
                        DataManager().addIndividualDecks(
                            selected_player, individual_decks_input
                        )
                        st.write(st.session_state.players_and_decks)

                    if col2.button("Remover Último deck individual"):
                        DataManager().removeLastIndividualDeck(selected_player)
                        st.write(st.session_state.players_and_decks)

                if st.session_state.get('players_and_decks'):
                    # Obtém todos os decks de todos os jogadores
                    all_decks = [deck for player_decks in st.session_state['players_and_decks'].values(
                    ) for deck in player_decks]

                    # Verifica se há pelo menos dois decks diferentes
                    if len(set(all_decks)) >= 2:
                        repeat_deck = st.radio(
                            "Pode repetir o deck?",
                            ('Sim', 'Não')
                        )
                        can_repeat_deck = True if repeat_deck == 'Sim' else False

            # if not is_random_decks:
            #     # Pergunta se quer adicioanr os jogadores do ultimo duelo
            #     is_add_last_duel = st.checkbox(
            #         "Gostaria de adicionar os jogadores do ultimo duelo?"
            #     )

            #     # Adiciona uma janela para selecionar os dois players do último duelo
            #     if is_add_last_duel:
            #         players_last_duel = st.multiselect(
            #             label="Último duelo", options=st.session_state.players
            #         )
            #         if len(players_last_duel) > 2:
            #             st.error(
            #                 "Por favor, selecione no máximo dois players"
            #                 " que duelaram no último jogo"
            #             )
            #         elif len(players_last_duel) == 2:
            #             st.write(
            #                 f"Último duelo: {', '.join(players_last_duel)}")
            #     else:
            #         if st.session_state.get('players_last_duel'):
            #             players_last_duel = st.session_state.get(
            #                 'players_last_duel')
            #         else:
            #             players_last_duel = []

            if is_random_decks and st.session_state.get('players_and_decks'):

                # # Pergunta se quer adicioanr os jogadores do ultimo duelo
                # is_add_last_duel = st.checkbox(
                #     "Gostaria de adicionar os jogadores do ultimo duelo?"
                # )
                # # Adiciona uma janela para selecionar os dois players do último duelo
                # if is_add_last_duel:
                #     players_last_duel = st.multiselect(
                #         label="Último duelo", options=st.session_state.players
                #     )
                #     if len(players_last_duel) > 2:
                #         st.error(
                #             "Por favor, selecione no máximo dois players"
                #             " que duelaram no último jogo"
                #         )
                #     elif len(players_last_duel) == 2:
                #         st.write(
                #             f"Último duelo: {', '.join(players_last_duel)}")
                # else:
                #     if st.session_state.get('players_last_duel'):
                #         players_last_duel = st.session_state.get(
                #             'players_last_duel')
                #     else:
                #         players_last_duel = []

                is_deactivate_deck = st.checkbox(
                    "Gostaria de ativar ou desativar algum deck?")
                if is_deactivate_deck:
                    selected_player = st.selectbox(
                        "Escolha o Magiqueiro:", st.session_state.players)

                    # Obtém os decks do jogador selecionado
                    player_decks = st.session_state.players_and_decks.get(
                        selected_player)

                    # Verifica se o jogador tem mais de um deck ativo
                    active_decks = [
                        deck for deck, is_active in player_decks.items() if is_active]
                    if len(active_decks) > 1:
                        # Cria uma lista de verificação para os decks
                        for deck, is_active in player_decks.items():
                            is_checked = not is_active  # O deck está marcado se estiver desativado
                            # Cria um identificador único
                            unique_key = f"{selected_player}_{deck}"
                            new_checked_value = st.checkbox(
                                deck, value=is_checked, key=unique_key)

                            # Atualiza o status do deck com base no valor da caixa de seleção
                            player_decks[deck] = not new_checked_value
                    else:
                        st.warning(
                            'Não é possivel desativar deck, pois vc só possui um deck ativo')

            # if not st.session_state.get('players_last_duel'):
            #     st.session_state['players_last_duel'] = players_last_duel
            # players_last_duel = st.session_state['players_last_duel']

            if not st.session_state.get('duel'):
                st.session_state['duel'] = {}
            duel = st.session_state['duel']

            if st.button("Gerar Duelo"):
                if not is_random_decks:
                    duel = DuelsType().singleDuel(
                        st.session_state.players,
                        players_last_duel,
                    )
                    st.session_state['duel'] = duel
                    st.write(duel)

                elif st.session_state.get('players_and_decks'):
                    duel = DuelsType().singleDuel(
                        st.session_state.players_and_decks,
                        players_last_duel,
                        can_repeat_deck,
                    )
                    st.session_state['duel'] = duel
                    st.write(duel)

                else:
                    st.warning(
                        'Opção de marcar decks selecionadoa porém não há decks cadastrados')

            if st.session_state.get('duel'):
                duel = st.session_state['duel']

                # Adiciona um botão para cada jogador sorteado para desativar o deck usado
                for i in range(1, 3):
                    player = duel.get(f'player_{i}')
                    player_decks = st.session_state.players_and_decks.get(
                        player)

                    # Verifica se o jogador tem mais de um deck ativo
                    active_decks = [
                        deck for deck, is_active in player_decks.items() if is_active]
                    if len(active_decks) > 1:
                        # Cria um identificador único para o botão
                        unique_key = f"Desativar deck usado por {player}_{i}"
                        if st.button(unique_key, key=unique_key):
                            used_deck = duel.get(f"deck_{i}")
                            st.session_state.players_and_decks[player][used_deck] = False
                            st.success(
                                f"Deck {used_deck} do Magiqueiro {player} desativado com sucesso!")
                    else:
                        st.warning(
                            'Não é possivel desativar deck, pois vc só possui um deck ativo')

                # st.write('Salvar esse Duelo, como Ultimo duelo realizado?')
                # col1, col2, col3, col4, col5 = st.columns(5)
                # if col3.button("Salvar Duelo"):
                #     if not is_random_decks:
                #         players_last_duel = [
                #             duel.get('player_1'), duel.get('player_2')
                #         ]
                #         if players_last_duel:
                #             st.success(
                #                 f'Ultimo duelo enter {players_last_duel[0]} e'
                #                 f' {players_last_duel[1]} foi salvo')

                #     else:
                #         players_last_duel = [
                #             duel.get('player_1'), duel.get('player_2')
                #         ]

                #         if players_last_duel:
                #             st.success(
                #                 f'Ultimo duelo entre {players_last_duel[0]} e'
                #                 f' {players_last_duel[1]} foi salvo')
                # st.write(players_last_duel)

            imgs_magic_yugioh = imgs_magic + imgs_yugioh + imgs_embaralhando
            choice_img = random.choice(imgs_magic_yugioh)
            st.image(choice_img, use_column_width=True)

        else:
            st.warning(
                "Você precisa ter mais de um jogador para gerar um duelo."
            )
            choice_img = random.choice(imgs_alone)
            st.image(choice_img, use_column_width=True)
