import base64
import os
import random

import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.stoggle import stoggle

from interfaces.data_manager import DataManager
from magic_modules.generator_magic_duels import DuelsType


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

                repeat_deck = st.radio(
                    label="Os oponentes podem possuir o mesmo deck ?",
                    options=yes_or_no,
                    horizontal=True,
                    index=1,
                )

                if repeat_deck == yes_or_no[1]:
                    can_repeat_deck = True

            st.session_state['last_duel'] = []
            players_last_duel = st.session_state['last_duel']
            if not is_random_decks:
                # Pergunta se quer adicioanr os jogadores do ultimo duelo
                is_add_last_duel = st.checkbox(
                    "Gostaria de adicionar os jogadores do ultimo duelo?"
                )

                # Adiciona uma janela para selecionar os dois players do último duelo
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
                        st.write(
                            f"Último duelo: {', '.join(players_last_duel)}")

            if is_random_decks:

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
                        st.write(
                            f"Último duelo: {', '.join(players_last_duel)}")

            if st.button("Gerar Duelo"):
                if not is_random_decks:
                    duel = DuelsType().singleDuel(
                        st.session_state.players,
                        players_last_duel,
                    )

                else:
                    duel = DuelsType().singleDuel(
                        st.session_state.players_and_decks,
                        players_last_duel,
                        can_repeat_deck,
                    )

                st.write(duel)

                if duel:
                    st.write(
                        'Salvar esse Duelo, como Ultimo duelo realizado?')
                    col1, col2, col3, col4, col5 = st.columns(5)
                    if col3.button("Salvar Duelo"):
                        if not is_random_decks:
                            st.write('dsfsdfds2')
                            players_last_duel = duel
                            if players_last_duel:
                                st.success(
                                    f'Ultimo duelo enter {players_last_duel[0]} e'
                                    f' {players_last_duel[1]} foi salvo')

                        else:
                            st.write('dsfsdfds3')
                            players_last_duel = [
                                duel.get('player_1'), duel.get('player_2')]

                            if players_last_duel:
                                st.success(
                                    f'Ultimo duelo enter {players_last_duel[0]} e'
                                    f' {players_last_duel[1]} foi salvo')

            imgs_magic_yugioh = imgs_magic + imgs_yugioh + imgs_embaralhando
            choice_img = random.choice(imgs_magic_yugioh)
            st.image(choice_img, use_column_width=True)

        else:
            st.warning(
                "Você precisa ter mais de um jogador para gerar um duelo."
            )
            choice_img = random.choice(imgs_alone)
            st.image(choice_img, use_column_width=True)
