# 卒業研究
## 収集するデータ項目
+ 語りと応答の内容 -> toukei.py Comare ->toukeiResult.txt
+ 応答の個数 -> toukei.py Outou.view()
+ 間においての応答の一致 -> pause.py -> pauseResult.txt
+ 応答の不一致 -> 一人しか返事してない箇所 -> 語りに注目し、返事をしてない語りの形態素をとりあえず全部取ってくる -> disagreement.py

これらによって
+ 適切な応答の内容
+ 応答の頻度
+ 応答のしていいタイミング、してはいけないタイミング

をそれぞれ取得

## 中間発表　概要
1. 語りと応答の内容　→　pause数えない
2. 頻度　→　応答個数　/　語り時間 →　pause数えない
3. 応答していいタイミング
    + 間での応答
        + 全体の間においての割合
        + 全体の応答においての割合
        + 間の長さ（200ms以上で長い）
    + していいタイミング
        + pauseを合算　→　応答した奴がpauseならもう一つ前まで戻る
4. してはいけないタイミング　→　してない形態素の個数

## 収集データ
+ 語りと応答の内容
toukei.py -> toukeiA.txt, toukeiB.txt, toukeiC.txt
```
子供がですね
はい
3人あの女の子ばっかしなんですけど産まれて
はい
ことですね
はあ
でさらにまー今現在ではですね
はい
孫もおりますので
はあ
そういう意味ではあの他の友達なんかに比べて
うん
非常にあの恵まれてるということで
はあ
今でも感謝しうれしくなったと思い
あ
...
```
+ 語りの形態素・品詞・品詞細分類
toukei.py -> katariCount.txt, hinshiCount.txt, detailCount.txt
```
あと:74
は:1166
あの:312
大学:43
を:878
卒業:10
し:680
て:1815
から:424
です:930
ね:542
...
```
+ 応答のラベルの数
toukei.py -> toukeiLabela.txt...
```
A
応答の個数： 7058
[{'あいづち': 5203}, {'感心': 1373}, {'同意': 123}, {'評価': 111}, {'驚き': 95}, {'納得': 60}, {'その他': 45}, {'同意しない': 23}, {'あいさつ': 19}, {'意見': 3}, {'考え始め': 2}, {'驚きといぶかり': 1}]
[{'あいづち': 73.72}, {'感心': 19.45}, {'同意': 1.74}, {'評価': 1.57}, {'驚き': 1.35}, {'納得': 0.85}, {'その他': 0.64}, {'同意しない': 0.33}, {'あいさつ': 0.27}, {'意見': 0.04}, {'考え始め': 0.03}, {'驚きといぶかり': 0.01}]
B
応答の個数： 7738
[{'あいづち': 6242}, {'感心': 828}, {'同意': 152}, {'評価': 145}, {'その他': 125}, {'驚き': 102}, {'繰り返し応答': 46}, {'納得': 43}, {'意見': 16}, {'言い換え': 14}, {'同意しない': 14}, {'あいさつ': 8}, {'補完': 2}, {'記憶を呼び起こす': 1}]
[{'あいづち': 80.67}, {'感心': 10.7}, {'同意': 1.96}, {'評価': 1.87}, {'その他': 1.62}, {'驚き': 1.32}, {'繰り返し応答': 0.59}, {'納得': 0.56}, {'意見': 0.21}, {'言い換え': 0.18}, {'同意しない': 0.18}, {'あいさつ': 0.1}, {'補完': 0.03}, {'記憶を呼び起こす': 0.01}]
C
応答の個数： 8419
[{'あいづち': 5060}, {'感心': 1612}, {'繰り返し応答': 428}, {'その他': 330}, {'評価': 255}, {'言い換え': 210}, {'同意': 184}, {'驚き': 125}, {'意見': 56}, {'納得': 48}, {'同意しない': 47}, {'補完': 43}, {'あいさつ': 12}, {'考えている最中': 7}, {'記憶を呼び起こす': 2}]
[{'あいづち': 60.1}, {'感心': 19.15}, {'繰り返し応答': 5.08}, {'その他': 3.92}, {'評価': 3.03}, {'言い換え': 2.49}, {'同意': 2.19}, {'驚き': 1.48}, {'意見': 0.67}, {'納得': 0.57}, {'同意しない': 0.56}, {'補完': 0.51}, {'あいさつ': 0.14}, {'考えている最中': 0.08}, {'記憶を呼び起こす': 0.02}]
```
+ 頻度
toukei.py
```
語りの個数 42105
語り総時間： 17990.46
A
応答の個数： 7058
１秒間あたりの応答数： 0.3923190402024184
B
応答の個数： 7738
１秒間あたりの応答数： 0.4301168508198234
C
応答の個数： 8419
１秒間あたりの応答数： 0.46797024645284224
```
+ 間での応答
pause.py
```
間の数 13867
200ms以上の間 7730
A
応答数： 7058
間での応答数： 3201
そのうち200ms以上の語りの間での応答数： 3047
[{'あいづち': 2430}, {'感心': 463}, {'同意': 44}, {'評価': 36}, {'驚き': 28}, {'納得': 23}, {'その他': 10}, {'同意しない': 9}, {'あいさつ': 3}, {'意見': 1}]
[{'あいづち': 79.75}, {'感心': 15.2}, {'同意': 1.44}, {'評価': 1.18}, {'驚き': 0.92}, {'納得': 0.75}, {'その他': 0.33}, {'同意しない': 0.3}, {'あいさつ': 0.1}, {'意見': 0.03}]
200ms以上の語りの間における応答割合： 39.42 3047 / 7730
全応答のうち200ms以上の間での応答割合： 43.17 3047 / 7058
B
応答数： 7738
間での応答数： 3318
そのうち200ms以上の語りの間での応答数： 3106
[{'あいづち': 2564}, {'感心': 297}, {'同意': 61}, {'驚き': 52}, {'評価': 47}, {'その他': 31}, {'繰り返し応答': 18}, {'納得': 15}, {'意見': 7}, {'言い換え': 6}, {'同意しない': 6}, {'あいさつ': 2}]
[{'あいづち': 82.55}, {'感心': 9.56}, {'同意': 1.96}, {'驚き': 1.67}, {'評価': 1.51}, {'その他': 1.0}, {'繰り返し応答': 0.58}, {'納得': 0.48}, {'意見': 0.23}, {'言い換え': 0.19}, {'同意しない': 0.19}, {'あいさつ': 0.06}]
200ms以上の語りの間における応答割合： 40.18 3106 / 7730
全応答のうち200ms以上の間での応答割合： 40.14 3106 / 7738
C
応答数： 8419
間での応答数： 3071
そのうち200ms以上の語りの間での応答数： 2845
[{'あいづち': 1753}, {'感心': 504}, {'繰り返し応答': 148}, {'その他': 103}, {'評価': 91}, {'同意': 72}, {'言い換え': 60}, {'驚き': 43}, {'意見': 17}, {'補完': 16}, {'同意しない': 16}, {'納得': 13}, {'考えている最中': 7}, {'記憶を呼び起こす': 1}, {'あいさつ': 1}]
[{'あいづち': 61.62}, {'感心': 17.72}, {'繰り返し応答': 5.2}, {'その他': 3.62}, {'評価': 3.2}, {'同意': 2.53}, {'言い換え': 2.11}, {'驚き': 1.51}, {'意見': 0.6}, {'補完': 0.56}, {'同意しない': 0.56}, {'納得': 0.46}, {'考えている最中': 0.25}, {'記憶を呼び起こす': 0.04}, {'あいさつ': 0.04}]
200ms以上の語りの間における応答割合： 36.8 2845 / 7730
全応答のうち200ms以上の間での応答割合： 33.79 2845 / 8419
```
+ 応答した語りの形態素、してない語りの形態素の割合
disagreement.py
```
A
[{'育てる': 100.0}, {'変わり': 100.0}, {'やれれ': 100.0}, {'来週': 100.0}, {'重ね': 100.0}, {'おこ': 100.0}, {'関西': 100.0}, {'座': 100.0}, {'使わ': 100.0}, {'回り': 100.0}]
[{'卒業': 100.0}, {'鉄鋼': 100.0}, {'メーカー': 100.0}, {'就職': 100.0}, {'まず': 100.0}, {'とっかかり': 100.0}, {'うれしく': 100.0}, {'経験': 100.0}, {'面': 100.0}, {'現在': 100.0}]

[{'助詞': 20.8}, {'助動詞': 20.03}, {'接続詞': 12.73}, {'形容詞': 10.92}, {'接頭辞': 9.15}, {'動詞': 8.41}, {'副詞': 8.2}, {'記号': 7.17}, {'接尾辞': 6.56}, {'名詞': 5.8}]
[{'代名詞': 96.41}, {'連体詞': 96.18}, {'感動詞': 96.1}, {'形状詞': 95.99}, {'名詞': 94.2}, {'接尾辞': 93.44}, {'記号': 92.83}, {'副詞': 91.8}, {'動詞': 91.59}, {'接頭辞': 90.85}]

[{'助詞終助詞': 40.16}, {'助詞接続助詞': 30.99}, {'助詞係助詞': 20.78}, {'助動詞*': 20.03}, {'記号文字': 20.0}, {'助詞副助詞': 19.44}, {'助詞格助詞': 15.29}, {'接続詞*': 12.73}, {'接尾辞形容詞的': 11.11}, {'形容詞一般': 11.05}]
[{'名詞助動詞語幹': 100.0}, {'形状詞タリ': 100.0}, {'接尾辞動詞的': 100.0}, {'形状詞助動詞語幹': 98.75}, {'名詞数詞': 97.15}, {'代名詞*': 96.41}, {'感動詞一般': 96.33}, {'連体詞*': 96.18}, {'感動詞フィラー': 95.84}, {'形状詞一般': 94.16}]

B
[{'上高地': 100.0}, {'関西': 100.0}, {'座': 100.0}, {'使わ': 100.0}, {'くだ': 100.0}, {'当たり': 100.0}, {'死ねる': 100.0}, {'一切': 100.0}, {'反面': 100.0}, {'越さ': 100.0}]
[{'大学': 100.0}, {'卒業': 100.0}, {'鉄鋼': 100.0}, {'メーカー': 100.0}, {'とっかかり': 100.0}, {'うれしく': 100.0}, {'経験': 100.0}, {'面': 100.0}, {'現在': 100.0}, {'交流': 100.0}]

[{'助詞': 22.05}, {'助動詞': 20.14}, {'接続詞': 10.55}, {'記号': 9.96}, {'形容詞': 9.03}, {'動詞': 8.63}, {'副詞': 8.06}, {'接頭辞': 7.26}, {'接尾辞': 6.43}, {'名詞': 6.39}]
[{'連体詞': 96.71}, {'代名詞': 95.98}, {'感動詞': 94.92}, {'形状詞': 93.63}, {'名詞': 93.61}, {'接尾辞': 93.57}, {'接頭辞': 92.74}, {'副詞': 91.94}, {'動詞': 91.37}, {'形容詞': 90.97}]

[{'助詞終助詞': 39.86}, {'助詞接続助詞': 29.37}, {'助詞係助詞': 23.45}, {'助動詞*': 20.14}, {'記号文字': 20.0}, {'助詞副助詞': 18.7}, {'助詞格助詞': 17.73}, {'助詞準体助詞': 13.06}, {'接尾辞形容詞的': 11.11}, {'形容詞非自立可能': 11.03}]
[{'名詞助動詞語幹': 100.0}, {'形状詞タリ': 100.0}, {'接尾辞動詞的': 100.0}, {'連体詞*': 96.71}, {'名詞数詞': 96.48}, {'接尾辞形状詞的': 96.43}, {'代名詞*': 95.98}, {'感動詞フィラー': 95.41}, {'感動詞一般': 94.5}, {'形状詞助動詞語幹': 93.75}]

C
[{'守れ': 100.0}, {'あやとり': 100.0}, {'関西': 100.0}, {'座': 100.0}, {'当たり': 100.0}, {'住宅': 100.0}, {'あくる日': 100.0}, {'痛く': 100.0}, {'集中': 100.0}, {'ソプラノ': 100.0}]
[{'卒業': 100.0}, {'当時': 100.0}, {'メーカー': 100.0}, {'とっかかり': 100.0}, {'うれしく': 100.0}, {'経験': 100.0}, {'交流': 100.0}, {'こそ': 100.0}, {'感謝': 100.0}, {'企業': 100.0}]

[{'助動詞': 21.6}, {'助詞': 21.02}, {'接続詞': 14.18}, {'動詞': 11.31}, {'形容詞': 10.41}, {'接頭辞': 8.83}, {'接尾辞': 8.61}, {'副詞': 8.06}, {'感動詞': 7.75}, {'形状詞': 7.55}]
[{'代名詞': 95.63}, {'連体詞': 94.47}, {'記号': 93.63}, {'名詞': 92.78}, {'形状詞': 92.45}, {'感動詞': 92.25}, {'副詞': 91.94}, {'接尾辞': 91.39}, {'接頭辞': 91.17}, {'形容詞': 89.59}]

[{'助詞終助詞': 39.13}, {'助詞接続助詞': 26.45}, {'助詞係助詞': 22.14}, {'助動詞*': 21.6}, {'記号文字': 20.0}, {'助詞準体助詞': 19.37}, {'助詞副助詞': 18.7}, {'助詞格助詞': 16.26}, {'形容詞非自立可能': 14.48}, {'形状詞タリ': 14.29}]
[{'名詞助動詞語幹': 100.0}, {'接尾辞形状詞的': 100.0}, {'接尾辞動詞的': 100.0}, {'名詞数詞': 96.65}, {'代名詞*': 95.63}, {'連体詞*': 94.47}, {'記号一般': 93.9}, {'形状詞一般': 93.39}, {'名詞普通名詞': 92.57}, {'感動詞フィラー': 92.42}]
```
+ ABCに共通した応答した語りの形態素・してない語りの形態素の割合
disagreement.py
```
応答した
[{'関西': 100.0}, {'座': 100.0}, {'下っ': 100.0}, {'にて': 100.0}, {'日光': 100.0}, {'与え': 100.0}, {'統計': 100.0}, {'認め合う': 100.0}, {'浴': 100.0}, {'望み': 100.0}]
[{'助詞': 7.14}, {'助動詞': 6.17}, {'形容詞': 2.26}, {'接続詞': 1.82}, {'動詞': 1.44}, {'接尾辞': 1.41}, {'名詞': 1.38}, {'接頭辞': 1.26}, {'副詞': 0.96}, {'記号': 0.8}]
[{'助詞終助詞': 18.02}, {'接尾辞形容詞的': 11.11}, {'助詞接続助詞': 10.34}, {'助詞係助詞': 6.61}, {'助動詞*': 6.17}, {'助詞副助詞': 5.86}, {'助詞格助詞': 5.35}, {'形容詞非自立可能': 3.79}, {'名詞固有名詞': 2.15}, {'動詞非自立可能': 1.94}]
応答してない
[{'卒業': 100.0}, {'メーカー': 100.0}, {'とっかかり': 100.0}, {'うれしく': 100.0}, {'経験': 100.0}, {'交流': 100.0}, {'感謝': 100.0}, {'企業': 100.0}, {'入っ': 100.0}, {'十分': 100.0}]
[{'連体詞': 89.74}, {'代名詞': 89.06}, {'形状詞': 86.79}, {'名詞': 86.59}, {'感動詞': 86.43}, {'接尾辞': 84.45}, {'記号': 82.07}, {'接頭辞': 81.39}, {'副詞': 81.37}, {'動詞': 79.18}]
[{'名詞助動詞語幹': 100.0}, {'接尾辞動詞的': 100.0}, {'接尾辞形状詞的': 92.86}, {'名詞数詞': 92.46}, {'連体詞*': 89.74}, {'代名詞*': 89.06}, {'接尾辞形容詞的': 88.89}, {'形状詞一般': 87.16}, {'感動詞一般': 86.7}, {'形状詞助動詞語幹': 86.25}]
```

+ 文節で行われた応答割合
segment.py **ちょっとデータ古いので注意**
```
文節の数： 17421
名詞を含む文節の数 7889
動詞を含む文節の数 4735
A
応答数： 7058
文節での応答数： 2197
[{'あいづち': 1686}, {'感心': 378}, {'同意': 40}, {'評価': 33}, {'驚き': 18}, {'納得': 14}, {'その他': 14}, {'同意しない': 9}, {'あいさつ': 3}, {'驚きといぶかり': 1}, {'考え始め': 1}]
[{'あいづち': 76.74}, {'感心': 17.21}, {'同意': 1.82}, {'評価': 1.5}, {'驚き': 0.82}, {'納得': 0.64}, {'その他': 0.64}, {'同意しない': 0.41}, {'あいさつ': 0.14}, {'驚きといぶかり': 0.05}, {'考え始め': 0.05}]
全応答に対する割合： 31.13 %  2197 / 7058
全文節に対する割合： 12.61 %  2197 / 17421
B
応答数： 7738
文節での応答数： 2221
[{'あいづち': 1843}, {'感心': 192}, {'その他': 43}, {'同意': 42}, {'評価': 38}, {'驚き': 25}, {'繰り返し応答': 12}, {'納得': 12}, {'意見': 4}, {'言い換え': 4}, {'あいさつ': 3}, {'同意しない': 3}]
[{'あいづち': 82.98}, {'感心': 8.64}, {'その他': 1.94}, {'同意': 1.89}, {'評価': 1.71}, {'驚き': 1.13}, {'繰り返し応答': 0.54}, {'納得': 0.54}, {'意見': 0.18}, {'言い換え': 0.18}, {'あいさつ': 0.14}, {'同意しない': 0.14}]
全応答に対する割合： 31.47 %  2221 / 7058
全文節に対する割合： 12.75 %  2221 / 17421
C
応答数： 8419
文節での応答数： 2324
[{'あいづち': 1419}, {'感心': 353}, {'繰り返し応答': 133}, {'評価': 88}, {'その他': 88}, {'言い換え': 74}, {'同意': 68}, {'驚き': 31}, {'同意しない': 20}, {'意見': 17}, {'補完': 15}, {'納得': 14}, {'あいさつ': 3}, {'記憶を呼び起こす': 1}]
[{'あいづち': 61.06}, {'感心': 15.19}, {'繰り返し応答': 5.72}, {'評価': 3.79}, {'その他': 3.79}, {'言い換え': 3.18}, {'同意': 2.93}, {'驚き': 1.33}, {'同意しない': 0.86}, {'意見': 0.73}, {'補完': 0.65}, {'納得': 0.6}, {'あいさつ': 0.13}, {'記憶を呼び起こす': 0.04}]
全応答に対する割合： 32.93 %  2324 / 7058
全文節に対する割合： 13.34 %  2324 / 17421
```
名詞を含む文節
```
文節の数： 17421
名詞を含む文節の数 7889
A
応答数： 7058
文節での応答数： 2197
名詞を含む文節での応答数： 1007
[{'あいづち': 820}, {'感心': 140}, {'同意': 17}, {'驚き': 10}, {'評価': 6}, {'納得': 5}, {'同意しない': 5}, {'その他': 4}]
[{'あいづち': 81.43}, {'感心': 13.9}, {'同意': 1.69}, {'驚き': 0.99}, {'評価': 0.6}, {'納得': 0.5}, {'同意しない': 0.5}, {'その他': 0.4}]
名詞を含む文節に関する割合 12.76 %  1007 / 7889
B
応答数： 7738
文節での応答数： 2221
名詞を含む文節での応答数： 1118
[{'あいづち': 968}, {'感心': 80}, {'その他': 18}, {'同意': 15}, {'驚き': 13}, {'評価': 11}, {'繰り返し応答': 6}, {'意見': 2}, {'納得': 2}, {'同意しない': 1}, {'言い換え': 1}, {'あいさつ': 1}]
[{'あいづち': 86.58}, {'感心': 7.16}, {'その他': 1.61}, {'同意': 1.34}, {'驚き': 1.16}, {'評価': 0.98}, {'繰り返し応答': 0.54}, {'意見': 0.18}, {'納得': 0.18}, {'同意しない': 0.09}, {'言い換え': 0.09}, {'あいさつ': 0.09}]
名詞を含む文節に関する割合 14.17 %  1118 / 7889
C
応答数： 8419
文節での応答数： 2324
名詞を含む文節での応答数： 1107
[{'あいづち': 708}, {'感心': 167}, {'繰り返し応答': 77}, {'その他': 33}, {'同意': 24}, {'評価': 23}, {'驚き': 22}, {'言い換え': 17}, {'同意しない': 11}, {'補完': 9}, {'納得': 7}, {'意見': 7}, {'記憶を呼び起こす': 1}, {'あいさつ': 1}]
[{'あいづち': 63.96}, {'感心': 15.09}, {'繰り返し応答': 6.96}, {'その他': 2.98}, {'同意': 2.17}, {'評価': 2.08}, {'驚き': 1.99}, {'言い換え': 1.54}, {'同意しない': 0.99}, {'補完': 0.81}, {'納得': 0.63}, {'意見': 0.63}, {'記憶を呼び起こす': 0.09}, {'あいさつ': 0.09}]
名詞を含む文節に関する割合 14.03 %  1107 / 7889
```
動詞を含む文節
```
文節の数： 17421
動詞を含む文節の数 4735
A
応答数： 7058
文節での応答数： 2197
動詞を含む文節での応答数： 882
[{'あいづち': 643}, {'感心': 178}, {'評価': 13}, {'同意': 13}, {'その他': 11}, {'納得': 10}, {'驚き': 7}, {'同意しない': 3}, {'あいさつ': 2}, {'驚きといぶかり': 1}, {'考え始め': 1}]
[{'あいづち': 72.9}, {'感心': 20.18}, {'評価': 1.47}, {'同意': 1.47}, {'その他': 1.25}, {'納得': 1.13}, {'驚き': 0.79}, {'同意しない': 0.34}, {'あいさつ': 0.23}, {'驚きといぶかり': 0.11}, {'考え始め': 0.11}]
動詞を含む文節に関する割合 18.63 %  882 / 4735
B
応答数： 7738
文節での応答数： 2221
動詞を含む文節での応答数： 814
[{'あいづち': 642}, {'感心': 98}, {'評価': 19}, {'その他': 16}, {'驚き': 14}, {'同意': 13}, {'繰り返し応答': 3}, {'納得': 3}, {'意見': 2}, {'あいさつ': 2}, {'同意しない': 1}, {'言い換え': 1}]
[{'あいづち': 78.87}, {'感心': 12.04}, {'評価': 2.33}, {'その他': 1.97}, {'驚き': 1.72}, {'同意': 1.6}, {'繰り返し応答': 0.37}, {'納得': 0.37}, {'意見': 0.25}, {'あいさつ': 0.25}, {'同意しない': 0.12}, {'言い換え': 0.12}]
動詞を含む文節に関する割合 17.19 %  814 / 4735
C
応答数： 8419
文節での応答数： 2324
動詞を含む文節での応答数： 869
[{'あいづち': 494}, {'感心': 151}, {'繰り返し応答': 48}, {'その他': 44}, {'評価': 43}, {'言い換え': 32}, {'同意': 30}, {'同意しない': 7}, {'驚き': 6}, {'納得': 5}, {'補完': 4}, {'あいさつ': 3}, {'意見': 2}]
[{'あいづち': 56.85}, {'感心': 17.38}, {'繰り返し応答': 5.52}, {'その他': 5.06}, {'評価': 4.95}, {'言い換え': 3.68}, {'同意': 3.45}, {'同意しない': 0.81}, {'驚き': 0.69}, {'納得': 0.58}, {'補完': 0.46}, {'あいさつ': 0.35}, {'意見': 0.23}]
動詞を含む文節に関する割合 18.35 %  869 / 4735
```
**品詞細分類を加えた詳細なデータがsegment.pyにあり**
+ 文節の品詞の組み合わせと応答の関係（個数var）
segmentCount.py -> segmentSizeA.txt 
```
文節の組み合わせ　| 名詞,助詞
その文節の応答割合| 31.14% (1111/3568)
応答のラベルリスト| あいづち,感心,驚き,同意,納得,その他,同意しない,評価
応答のラベルの内訳| [{'あいづち': 930}, {'感心': 247}, {'驚き': 21}, {'同意': 18}, {'納得': 11}, {'その他': 3}, {'同意しない': 2}, {'評価': 1}]
ラベルパーセント　| [{'あいづち': 75.43}, {'感心': 20.03}, {'驚き': 1.7}, {'同意': 1.46}, {'納得': 0.89}, {'その他': 0.24}, {'同意しない': 0.16}, {'評価': 0.08}]

文節の組み合わせ　| 名詞,助動詞
その文節の応答割合| 40.37% (109/270)
応答のラベルリスト| あいづち,感心,同意,評価,あいさつ,納得,驚き,その他,同意しない,意見
応答のラベルの内訳| [{'あいづち': 353}, {'感心': 74}, {'同意': 9}, {'評価': 7}, {'あいさつ': 7}, {'納得': 3}, {'驚き': 3}, {'その他': 3}, {'同意しない': 2}, {'意見': 1}]
ラベルパーセント　| [{'あいづち': 76.41}, {'感心': 16.02}, {'同意': 1.95}, {'評価': 1.52}, {'あいさつ': 1.52}, {'納得': 0.65}, {'驚き': 0.65}, {'その他': 0.65}, {'同意しない': 0.43}, {'意見': 0.22}]

文節の組み合わせ　| 動詞,助詞
その文節の応答割合| 36.44% (317/870)
応答のラベルリスト| あいづち,感心,評価,その他,驚き,同意,納得
応答のラベルの内訳| [{'あいづち': 289}, {'感心': 74}, {'評価': 3}, {'その他': 3}, {'驚き': 2}, {'同意': 2}, {'納得': 2}]
ラベルパーセント　| [{'あいづち': 77.07}, {'感心': 19.73}, {'評価': 0.8}, {'その他': 0.8}, {'驚き': 0.53}, {'同意': 0.53}, {'納得': 0.53}]

文節の組み合わせ　| 副詞
その文節の応答割合| 25.33% (214/845)
応答のラベルリスト| あいづち,感心,驚き,同意,その他,評価,納得,同意しない
応答のラベルの内訳| [{'あいづち': 167}, {'感心': 57}, {'驚き': 6}, {'同意': 6}, {'その他': 3}, {'評価': 2}, {'納得': 2}, {'同意しない': 2}]
ラベルパーセント　| [{'あいづち': 68.16}, {'感心': 23.27}, {'驚き': 2.45}, {'同意': 2.45}, {'その他': 1.22}, {'評価': 0.82}, {'納得': 0.82}, {'同意しない': 0.82}]

文節の組み合わせ　| 動詞,助動詞,助動詞
その文節の応答割合| 50.78% (98/193)
応答のラベルリスト| あいづち,感心,評価,納得,驚き,同意,同意しない,あいさつ,その他
応答のラベルの内訳| [{'あいづち': 163}, {'感心': 48}, {'評価': 13}, {'納得': 6}, {'驚き': 3}, {'同意': 2}, {'同意しない': 1}, {'あいさつ': 1}, {'その他': 1}]
ラベルパーセント　| [{'あいづち': 68.49}, {'感心': 20.17}, {'評価': 5.46}, {'納得': 2.52}, {'驚き': 1.26}, {'同意': 0.84}, {'同意しない': 0.42}, {'あいさつ': 0.42}, {'その他': 0.42}]

・・・
```
+ その応答の内容
segmentCount.py -> sentenceContentA.txt
```
文節の品詞の組み合わせ: ['名詞', '助詞']
応答のラベル: あいづち
文節: 交流が
応答: {139.42: 'うん'}
文節: ことで
応答: {94.46: 'はあ'}
文節: ことで
応答: {201.39: 'ええ'}
文節: ことで
応答: {201.46: 'ええ'}
文節: 新宿まで
応答: {215.75: 'うん'}
文節: 女の子は
応答: {357.81: 'ええええ'}
文節: 今は
応答: {358.1: 'ええええ'}
文節: 時から
応答: {443.22: 'ええ'}
文節: 父親が
応答: {527.39: 'ええ'}
文節: 人に
応答: {587.35: 'うん'}
文節: ことで
応答: {798.66: 'はいはい'}
・・・
```
+ 複数数人の文節応答の一致（相槌とそれ以外）
相槌のみ
```
(731.27, '流行って来た')
B {731.27: 'うん'} あいづち
C {731.33: 'ええ'} あいづち
(554.63, '生き甲斐を')
A {554.92: 'うん'} あいづち
B {554.77: 'うん'} あいづち
C {554.7: 'ええ'} あいづち
(796.29, 'なって')
A {796.54: 'え'} あいづち
B {796.48: 'はい'} あいづち
C {796.51: 'ええ'} あいづち
(1654.78, '人に')
A {1655.01: 'ええ'} あいづち
C {1655.25: 'ええ'} あいづち
・・・
```
それ以外
```
(279.21, 'で')
A {279.26: '凄いですね'} 評価
A {279.59: 'はい'} あいづち
C {279.23: '良かったです'} 評価
(172.57, 'ありがたく')
A {172.58: 'あー'} 感心
B {172.74: 'うーん'} あいづち
(263.52, '一番')
A {263.97: 'ええええ'} あいづち
B {263.85: 'うん'} あいづち
C {263.86: '感謝ですうーん'} 感心
・・・
```
+ 一人だけの文節応答(相槌とそれ以外)
相槌のみ 
```
961.52, 'いう')
B {961.73: 'はい'}
(349.2, 'いいましてね')
C {349.21: 'ええ'}
(241.05, '日本で')
C {241.25: 'ええ'}
(540.79, '中に')
A {540.88: 'ええええ'}
(256.22, '預かってるような')
B {256.24: 'うん'}
・・・
```
それ以外
```
(307.1, 'まーざっと')
B {307.15: 'そうなんですね'} 感心
(233.52, 'あのーやっぱ')
C {233.63: 'はははーはー'} その他
(272.51, '健康で')
C {272.71: 'それが一番です'} 意見
(886.27, '乗るという')
C {886.36: 'ふーん'} 感心
(314.95, 'してません')
A {315.44: 'そうなんですか'} 感心
(229.58, '初めてでしたので')
B {229.7: 'そうなんですね'} 感心
(1266.87, 'ものですけれども')
C {1266.89: 'そうですね'} 同意
・・・
```

## 今後
+ 語りと応答の内容から適切な応答内容を取得したい
+ 応答の頻度はこれでいいの？
+ 応答していいタイミング・してはいけないタイミングからシステム作成していきたい

## 山口先生へインタビュー
### 研究概要
話を聞くことを傾聴するという
相手の話を邪魔しないで、相手に話すことを促すようなうんうんなどの傾聴的応答とはどのようなものかについて研究を行う
研究結果を用いて、スマートスピーカーなどの機械が人間の話を聞きながらうんうんと言った応答をすることで今までにない、対話システムができるのでは
をテーマに研究

研究手法は一人の話者に対して、複数人が応答する形の会話データがあるので
そのデータから適切な応答を生成するのに必要な特徴を抽出して
その結果から応答モデルを作成する

山口先生へのインタビューからこんな特徴も抽出してみようや
前提が間違っていないかの確認をしたいと考えています

### 質問
+ 普段授業をされる時、生徒に授業内容を聞いてもらう必要があると思うんですが、聞いてもらうために何か意識していることはありますか
無意識的
どうかな、じゃないかななどの疑問形で話す
じゃないですかーは使わないようにしている

+ 普段人と話すときにどんな反応が返ってくると嬉しいですか
興味をもって話を聞いてくれることが嬉しい
話に興味がある人と話をしている私（の体験や考え方）に興味がある人は違う
先生は個人的に後者が好き（個人差がある）
傾聴の姿勢は大切
その人が歩んできた人生をそのまま受け取る
機械と分かっていれば別のアプローチができるのでは

+ 人と話すときに気をつけていることはありますか


+ 人が話をするとき、相手に反応を求めるためにする行動は何かあるのか
一番上の質問でしたよ

+ 機械がうんうんなどの反応をするのはどう思うか
反応を受け取った後に質問など返すの？
→まだ分析段階です
男女差など
→あり
初対面かどうか、年齢差（一般的なものをシステムに入れると）、立場、距離感、公式かプライベートな話なのか、地域
→追加を検討
今のスマートスピーカーには親しさを変更することはできない？
→できない→表情がないので音声で対応することができるのでは
「へー」は単独では使えない
→それは知りませんでしたと言った応答が入り、話の方向が決まる
方言や地方、年齢の違いによるイントネーションの違いが出る
→「へー」などの発音の仕方が変わる
**相手を飽きさせない種類豊富な応答が必要だ！**
**対面と発話だけだと違う！**


 
