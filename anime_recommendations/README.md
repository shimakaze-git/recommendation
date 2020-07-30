# Web

streamlit で表示

streamlit の詳細は以下を参照

- [Python のスクリプトからウェブアプリを簡単に作れる Streamlit をさわってみた](https://dev.classmethod.jp/articles/streamlit-intro/)
- [Streamlit: データサイエンティストのためのフロントエンド](https://note.com/navitime_tech/n/ned827292df6f)

```
$ streamlit run app.py
```

# Install

```
$ pipenv lock -r -d > ./src/requirements.txt
```

# Anime.csv

- anime_id – アニメを識別する myanimelist.net のユニークな ID。
- name – アニメのフルネーム。
- genre – このアニメのジャンルのカンマ区切りのリスト。
- type – 映画、テレビ、OVA など
- episodes – この番組のエピソード数 （映画の場合は 1）
- rating – このアニメの 10 の平均評価
- members – このアニメの「グループ」に含まれるコミュニティメンバーの数。

# Rating.csv

- user_id – 識別不可能なランダムに生成されたユーザー ID。
- anime_id – このユーザーが評価したアニメ。
- rating – このユーザーが割り当てた 10 のうちの評価（ユーザーがそれを見たが評価を割り当てなかった場合は-1）

# Links

- [Dataset](https://www.kaggle.com/CooperUnion/anime-recommendations-database)
- [アイテムベース協調フィルタリングでリコメンドの仕組みを作成](http://maruo51.com/2019/06/30/python-recommend/)
