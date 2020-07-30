import pandas as pd


def read_anime_rating_data(source='csv'):
    # csvからデーターを読みこむ
    anime = pd.read_csv('anime.csv')
    rating = pd.read_csv('rating.csv')
    return anime, rating
