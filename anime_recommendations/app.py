import streamlit as st
import pandas as pd

from search import anime_name_search

"""
# anime_recommendations Sample Application.
anime_recommendationsのサンプルアプリケーション:
"""


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(
            f'<style>{f.read()}</style>',
            unsafe_allow_html=True
        )


def remote_css(url):
    st.markdown(
        f'<link href="{url}" rel="stylesheet">',
        unsafe_allow_html=True
    )


def icon(icon_name):
    st.markdown(
        f'<i class="material-icons">{icon_name}</i>',
        unsafe_allow_html=True
    )


local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')


def dataframe(frames, columns):
    df = pd.DataFrame(
        frames,
        columns=columns
    )
    return df


if __name__ == "__main__":
    """
    # アニメ検索.
    アニメの名前のキーワードを入れることでアニメを検索します:
    """
    icon("search")

    keyword = st.text_input('アニメ キーワード')
    if not keyword:
        st.write('キーワードが入力されていません')

    hit_count = st.text_input('検索ヒット数', 10)
    if not hit_count:
        st.write('検索ヒット数が入力されていません')

    # タイプを選択
    type_list = [
        '全て',
        'TV',
        'OVA',
        'Movie',
        'Special',
    ]
    selection = st.selectbox('タイプを選択', type_list)
    st.write(f'{selection} を選択')

    # マルチセレクト
    selected_targets = st.multiselect(
        'タイプを選択',
        type_list,
        default=type_list
    )

    if keyword and hit_count and st.button('検索'):
        anime_list, columns = anime_name_search(keyword, count=int(hit_count))

        df = dataframe(anime_list, columns)
        st.dataframe(df)
