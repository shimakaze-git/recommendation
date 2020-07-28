from wordcloud import WordCloud

if __name__ == "__main__":
    path = 'wakati.txt'

    list_text = []
    with open(path, encoding="utf-8") as f:
        list_text = f.readlines()

    text = ' '.join(list_text)

    wordcloud = WordCloud(
        background_color="white",
        font_path='./NotoSansCJKjp-Regular.otf',
        width=900,
        height=500
    ).generate(text)
    wordcloud.to_file("./wordcloud_sample.png")
