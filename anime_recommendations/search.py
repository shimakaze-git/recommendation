import pandas as pd


def read_csv():
    anime = pd.read_csv('anime.csv')
    return anime


def anime_name_search_csv(anime_keyword=''):
    # アニメの名称を元に部分一致するアニメを返す

    anime_df = read_csv()

    # 特定の文字列を含む
    search_results = anime_df[anime_df['name'].str.contains(anime_keyword)]

    columns = anime_df.columns
    return search_results.values.tolist(), columns


def anime_name_search_rdb(anime_keyword=''):
    # アニメの名称を元に部分一致するアニメを返す
    anime_list = []
    columns = []
    return anime_list, columns


def anime_name_search(anime_keyword='', count=10, source='csv'):
    # アニメの名称を元に部分一致するアニメを返す
    # source : csv or rdb

    anime_list = []
    columns = []

    if source == 'csv':
        anime_list, columns = anime_name_search_csv(anime_keyword)
        anime_list = anime_list[:count]
    elif source == 'rdb':
        anime_list, columns = anime_name_search_rdb(anime_keyword)
        anime_list = anime_list[:count]
    return anime_list, columns


if __name__ == "__main__":
    keyword = 'Gundam'
    anime_datas, columns = anime_name_search(keyword, count=5)
    print(columns)

    for anime in anime_datas:
        print(anime)
