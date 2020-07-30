import MeCab

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont


# MeCab による単語への分割関数 (名詞のみ残す)
def split_text_only_noun(text):

    option = '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'
    tagger = MeCab.Tagger("-Ochasen " + option)
    tagger.parse('')

    # Execute class analysis
    node = tagger.parseToNode(text)

    words = []
    while node:
        word = node.surface
        # 基本形を使用する
        word = node.feature.split(',')[6]

        class_feature = node.feature.split(',')[0]
        sub_class_feature = node.feature.split(',')[1]

        # features = ['名詞', '動詞', '形容詞', '記号']
        features = ['名詞', '動詞', '形容詞']
        if class_feature in features:
            if sub_class_feature not in ['空白', '*']:
                words.append(word)
        node = node.next
    return words


def create_keyword_image(text, image_path=None):
    to_image_path = image_path
    if not image_path:
        to_image_path = 'image.png'

    # 使うフォント，サイズ，描くテキストの設定
    tt_fontname = 'NotoSansCJKjp-Regular.otf'
    fontsize = 36

    # 画像サイズ，背景色，フォントの色を設定
    canvasSize = (300, 150)
    backgroundRGB = (255, 255, 255)
    textRGB = (0, 0, 0)

    # 文字を描く画像の作成
    img = PIL.Image.new('RGB', canvasSize, backgroundRGB)
    draw = PIL.ImageDraw.Draw(img)

    # 用意した画像に文字列を描く
    font = PIL.ImageFont.truetype(tt_fontname, fontsize)
    textWidth, textHeight = draw.textsize(text, font=font)
    textTopLeft = (canvasSize[0]//6, canvasSize[1]//2-textHeight//2)
    draw.text(textTopLeft, text, fill=textRGB, font=font)

    # imgの生成
    img.save(to_image_path)

    return to_image_path


if __name__ == "__main__":
    text = '立って歩け。前へ進め。あんたには立派な足がついてるじゃないか'
    wakati = split_text_only_noun(text)
    print(wakati)
