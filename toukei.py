import glob
import sys
import os
import shutil
from functools import reduce
path = 'toukeiResult.txt'
with open(path, mode='w') as f:
    f.write('')

fileArray = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'
]
testData_num = ['1', '2', '3', '4', '5', '6', '7']


class Outou:
    def __init__(self, file_name):
        self.outou = {}
        self.outou_label = {}
        self.outou_count = 0
        self.file_name = file_name

    def read_data(self):  # 全ファイルを検索して読み込み
        file_root = '../../outouwithlabel_camui/outouwithlabel_camui/'
        file_end = '/*.morph'

        for file_index in fileArray:
            files = glob.glob(file_root + file_index +
                              '/' + self.file_name + '/')
            for file in files:
                for index in testData_num:
                    targetFileList = glob.glob(file + index + file_end)
                    targetFileList.sort()
                    for targetFile in targetFileList:
                        self.readOutou(targetFile)
        return self.outou, self.outou_label

    def readOutou(self, file_name):  # 語り手側  {語り終了時間:言葉}
        file = open(file_name)  # データ入力
        lines = file.readlines()
        tmp_str = ""

        for data in lines[0:len(lines)]:
            data = data.rstrip('\n')  # 改行の削除
            data = data.split(',')  # ','で分割
            num = len(data)-1  # １行の長さを取得(この先の利用を考え-1)

            # 例外処理 ＋　退避させた文字の破棄
            if num == 0:
                tmp_str = ""
                continue
            elif data[0] == "silB" or data[0] == "silE":
                tmp_str = ""
                continue
            elif data[0] == "sp" or data[0] == "pause":
                tmp_str = ""
                continue
            elif data[0] == "(" or data[0] == ")" or data[0] == "?":
                tmp_str = ""
                continue
            elif data[0] == 'G' or data[0] == "D" or data[0] == "F" or data[0] == "U":
                tmp_str = ""
                continue
            elif data[1] == "補助記号":
                tmp_str = ""
                continue

            if 'label' in data[num]:
                word = data[0]  # 応答文字の取得
                word = tmp_str+word
                label = data[num].lstrip('label=')  # labelの取得
                begin = float(data[num-2])  # 開始時刻の取得
                #print(word, label, begin)

                self.outou.update({begin: word})
                self.outou_label.update({begin: label})

            else:
                tmp_str += data[0]  # 文字の退避

        file.close()

    def view(self):
        # 応答数を表示
        print(self.file_name, len(self.outou))


class Katari:
    def __init__(self):
        self.katari = {}

    def read_data(self):  # 全ファイルを検索して読み込み(読み込み順は適当)
        file_root = '../../katari_info/'
        file_end = '/*.morph'

        for file_index in fileArray:
            files = glob.glob(file_root + file_index + '/')
            for file in files:
                for index in testData_num:
                    bigFiles = glob.glob(file + index + '/*')
                    for bigFile in bigFiles:
                        targetFileList = glob.glob(bigFile + file_end)
                        targetFileList.sort()
                        for targetFile in targetFileList:
                            self.readKatari(targetFile)

        return self.katari

    def readKatari(self, file_name):  # 語り手側  {語り終了時間:言葉}
        file = open(file_name)  # データ入力
        lines = file.readlines()

        for data in lines[0:len(lines)]:
            data = data.rstrip('\n')  # 改行の削除
            data = data.split(',')  # ','で分割
            num = len(data)-1  # １行の長さを取得(この先の利用を考え-1)

            # 例外処理
            if num == 0:
                continue
            elif data[0] == "silB" or data[0] == "silE":
                continue
            elif data[0] == "sp" or data[0] == "pause":
                continue
            elif data[0] == "(" or data[0] == ")":
                continue
            elif data[1] == "補助記号":
                continue

            word = data[0]
            end = float(data[num])
            self.katari.update({end: word})

        file.close()


def trance_data(outou, outou_label, katari):  # 語りと応答の情報を解析しやすいように処理
    dic = {}
    time_list = list(outou.keys())  # 時間情報を取得
    tmp_list = list(katari.keys())
    time_list.extend(tmp_list)  # 二つを結合しソート
    time_list.sort()

    for i in time_list:
        if i in katari:
            time = i  # 時間情報の退避
        elif i in outou:
            # 比較用
            # {'語り終了時間：{応答側：ラベル}}
            dic.update({time: {outou[i]: outou_label[i]}})
        else:
            print('エラー：' + outou[i] + outou_label[i])

    return dic


class Compare:
    def __init__(self, katari):
        self.katari = katari
        self.time = list(katari.keys())
        self.word = list(katari.values())

    def match(self, *args):
        data = []  # 個数をカウントするためにラベルを全て保存
        label = []  # 出現するラベルのリスト
        time_list = reduce(lambda x, y: list(
            set(x) & set(y)), args)  # 全てのargsに対してset()
        time_list.sort()  # 語り終了時間のリスト
        con = 0

        with open(path, mode='a') as f:
            f.write('比較結果' + '\n')

        for time in time_list:
            # argsのラベル情報の配列を作成
            tmp = list(map(lambda x: list(x[time].values()), args))
            judg = reduce(lambda x, y: list(
                set(x) & set(y)), tmp)  # ラベルの一致不一致
            if judg:
                tmp = list(args[0][time].values())[0]  # ラベル情報を取得
                data.append(tmp)
                if tmp not in label:    # ラベルの出現リストに値を追加
                    label.append(tmp)

                index = self.time.index(time) + 1
                sent = ""
                for word in self.word[con:index]:
                    sent += word
                con = index

                with open(path, mode='a') as f:
                    f.write("語り" + sent + '\n')
                    for word in args:
                        f.write(str(word[time]) + '\n')

                # print("語り", sent)
                # print(args[0][time])
                # print(args[1][time])

        print("語り終了時間が一致した応答の数:", len(time_list))
        print("そのうちラベルも一致した応答の数:", len(data))
        for word in label:
            print(word, data.count(word))


def countKatari(katari):
    filePath = 'katariCount.txt'
    with open(filePath, mode='w') as f:
        f.write('')

    wordList = []  # 出現する単語を全て保存
    keyWord = []  # 単語の種類を保存
    data = list(katari.values())
    for word in data:
        wordList.append(word)
        if word not in keyWord:
            keyWord.append(word)

    for word in keyWord:
        with open(filePath, mode='a') as f:
            f.write(word + ':' + str(wordList.count(word)) + '\n')


if __name__ == '__main__':
    kt = Katari()
    katari = kt.read_data()
    countKatari(katari)

    """
    ot = Outou('a')
    outou, outou_label = ot.read_data()
    ot.view()
    a = trance_data(outou, outou_label, katari)

    ot = Outou('b')
    outou, outou_label = ot.read_data()
    ot.view()
    b = trance_data(outou, outou_label, katari)

    ot = Outou('c')
    outou, outou_label = ot.read_data()
    ot.view()
    c = trance_data(outou, outou_label, katari)
    """

    """
    comp = Compare(katari)
    print('AB')
    comp.match(a, b)
    print('AC')
    comp.match(a, c)
    print('BC')
    comp.match(b, c)
    print('ABC')
    comp.match(a, b, c)
    """
