import pandas as pd
import numpy as np
import scipy as sp
import operator

from sklearn.metrics.pairwise import cosine_similarity

# %matplotlib inline

# アニメとユーザーの類似性を測定し、
# ユーザーが特定のアニメを楽しむかどうかを予測できるようにする簡単な推奨システムを作成する


def read_data():
    anime = pd.read_csv('anime.csv')
    rating = pd.read_csv('rating.csv')
    return anime, rating


def data_merge(anime, rating):
    # anime_id列の2つのデータフレームを結合する
    # anime_idをキーにして結合
    # merged.renameでrating_userからuser_ratingに項目名を変更

    merged = rating.merge(
        anime,
        left_on='anime_id',
        right_on='anime_id',
        suffixes=['_user', '']
    )
    merged.rename(
        columns={'rating_user': 'user_rating'},
        inplace=True
    )

    # 計算上の理由から、データフレームの長さを10,000ユーザーに制限
    # 3つのカラムのみ利用
    merged = merged[['user_id', 'name', 'user_rating']]
    merged = merged[merged.user_id <= 10000]
    # merged = merged[merged.user_id <= 30000]

    return merged


def data_cleaning(df):
    # データのクリーニング作業
    # 不要なデータを削っていく

    # 評点のついていない行を削除
    # 評点のついていない行に関しては推薦に利用できないので削除

    # 欠損値が1つでもある行を削除
    merged = df.dropna()

    # 推薦の精度を高めるために、評点平均より低い評点の行を削除

    # 同じ映画に対して、Aさんは6,Bさんが6と評価したとしても、
    # Aさんは甘口評価で、Bさんは辛口評価の人だとした場合、その6という評価の価値は異なります。
    # その辺りを公平にする意味でも、ユーザーごとに評点の平均より低い評点の行は削除してしまう

    # user_idごとの評点の平均を求める
    mean_rate = merged.groupby("user_id").mean()
    merged = merged.merge(
        mean_rate,
        left_on="user_id",
        right_on="user_id",
        suffixes=["", "_mean"]
    )

    # ユーザーごとに評点平均より低い評点の行を削除
    merged = merged[merged["user_rating"] >= merged["user_rating_mean"]]
    merged = merged.drop("user_rating_mean", axis=1)

    return merged


def pivot_table(merged):
    # user × itemのクロス集計表を作成

    # 協調フィルタリングでは、1つの軸にユーザーのピボットテーブルを作成し、もう1つの軸に沿ってテレビ番組名を作成する必要がある。
    # ピボットテーブルは、ユーザーとショーの類似性を定義するのに役立ち、誰が何を好きになるかをより正確に予測する。
    piv = merged.pivot_table(
        index=['user_id'],
        columns=['name'],
        values='user_rating'
    )
    return piv


def shaping_piv(piv):
    # 前処理と整形作業
    # 注：標準化するために各評価から平均を差し引いているので
    # 評価が1つだけのユーザー、または全てを同じに評価したすべてのユーザーは削除される.

    # 後の作業のために、正規化とNaNを0に変換する
    # (cos類似度計算時にエラーを吐かれる)
    # 値を正規化
    # Min-Max Scaling
    piv_norm = piv.apply(
        lambda x: (x-np.mean(x))/(np.max(x)-np.min(x)),
        axis=1
    )

    # 評価しなかったユーザーを表すゼロのみを含むすべての列を削除する
    piv_norm.fillna(
        0,
        inplace=True
    )
    # 転置化
    piv_norm = piv_norm.T
    piv_norm = piv_norm.loc[:, (piv_norm != 0).any(axis=0)]

    return piv_norm


def top_animes(anime_name, item_sim_df):
    # この関数は類似度が最も高い上位10のアニメを返す

    count = 1
    print('Similar shows to {} include:\n'.format(anime_name))

    top_ten_animes = []

    item_sim_df_sort_values = item_sim_df.sort_values(
        by=anime_name,
        ascending=False
    ).index[1: 11]

    for item in item_sim_df_sort_values:
        print('No. {}: {}'.format(count, item))
        count += 1
        top_ten_animes.append(item)
    return top_ten_animes


def top_users(user, user_sim_df):
    # この関数は、類似性値が最も高い上位5人のユーザーを返す
    if user not in user_sim_df.columns:
        return('No data available on user {}'.format(user))

    users = {}

    # print('Most Similar Users:\n')
    sim_values = user_sim_df.sort_values(
        by=user, ascending=False
    ).loc[:, user].tolist()[1:11]

    sim_users = user_sim_df.sort_values(
        by=user, ascending=False
    ).index[1:11]

    zipped = zip(sim_users, sim_values,)
    for user, sim in zipped:
        users[user] = sim
        # print('User #{0}, Similarity value: {1:.2f}'.format(user, sim))
    return users


def similar_user_recs(user, user_sim_df, piv_norm):
    # 類似したユーザーごとに最も評価の高いショーを含むリストのリストを作成し、
    # リストに表示される頻度とともにショーの名前を返します

    if user not in user_sim_df.columns:
        return('No data available on user {}'.format(user))

    sim_users = user_sim_df.sort_values(by=user, ascending=False).index[1:11]
    best = []
    most_common = {}

    for i in sim_users:
        max_score = piv_norm.loc[:, i].max()
        best.append(
            piv_norm[piv_norm.loc[:, i] == max_score].index.tolist()
        )

    for i in range(len(best)):
        for j in best[i]:
            if j in most_common:
                most_common[j] += 1
            else:
                most_common[j] = 1

    sorted_list = sorted(
        most_common.items(),
        key=operator.itemgetter(1),
        reverse=True
    )
    return sorted_list[:5]


def predicted_rating(anime_name, user, user_sim_df):
    # 類似ユーザーの加重平均を計算して、入力ユーザーの潜在的な評価を決定し、表示します

    sim_users = user_sim_df.sort_values(
        by=user, ascending=False
    ).index[1:1000]
    user_values = user_sim_df.sort_values(
        by=user, ascending=False
    ).loc[:, user].tolist()[1:1000]

    rating_list = []
    weight_list = []
    for j, i in enumerate(sim_users):
        rating = piv.loc[i, anime_name]
        similarity = user_values[j]
        if np.isnan(rating):
            continue
        elif not np.isnan(rating):
            rating_list.append(rating*similarity)
            weight_list.append(similarity)

    return sum(rating_list)/sum(weight_list)


# アニメとユーザーの評価データを読みこむ
anime, rating = read_data()

# 変更前は、評価データセットは「-1」を使用して欠落している評価を表します。
# 後でユーザーごとの平均評価を計算し、平均を歪めたくないので、これらのプレースホルダーをnull値に置き換えます。
rating = rating.replace(-1, np.nan)

# この分析では、TVカテゴリの推奨事項を見つけることにのみ関心がある
# TVカテゴリのアニメに絞り込み
anime_tv = anime[anime['type'] == 'TV']

# データの結合
merged = data_merge(anime_tv, rating)

# データのクリーニング作業
merged = data_cleaning(merged)
print(merged.head())

# ピボットテーブルの作成
piv = pivot_table(merged)
print(piv.shape)

# ピボットテーブルの整形作業
piv_norm = shaping_piv(piv)


# 以下の関数によって読み取られる疎行列形式である必要がある
piv_sparse = sp.sparse.csr_matrix(piv_norm.values)

# これらの行列は、ユーザー/ユーザー配列の各ペアと
# アイテム/アイテム配列のペアの間で計算されたコサイン類似値を示します。
item_similarity = cosine_similarity(piv_sparse)
user_similarity = cosine_similarity(piv_sparse.T)

# 類似性マトリックスをデータフレームオブジェクトに挿入する
item_sim_df = pd.DataFrame(
    item_similarity,
    index=piv_norm.index,
    columns=piv_norm.index
)
user_sim_df = pd.DataFrame(
    user_similarity,
    index=piv_norm.columns,
    columns=piv_norm.columns
)

# print('item_sim_df', item_sim_df)
# print('user_sim_df', user_sim_df)
# print('piv_norm.index', piv_norm.index)
# print('piv_norm.columns', piv_norm.columns)

# アニメのリコメンド処理
anime_name = 'Dragon Ball'
top_ten_animes = top_animes(anime_name, item_sim_df)
print(top_ten_animes)

# 似ているユーザーのリコメンド処理
user = 3
top_ten_users = top_users(user, user_sim_df)
print(top_ten_users)


user = 3
similar_user_recs_list = similar_user_recs(user, user_sim_df, piv_norm)
print(similar_user_recs_list)


predicted_rating_list = predicted_rating('Cowboy Bebop', 3, user_sim_df)
print(predicted_rating_list)
