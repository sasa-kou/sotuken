import glob
import sys
import os
import shutil
from functools import reduce
path = 'disagreementResult.txt'
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

    def readOutou(self, file_name):  # 応答側  {応答開始時間:言葉}
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


class KatariPause:
    def __init__(self):
        self.katari = []

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

    def readKatari(self, file_name):  # 語り手側  {{語り開始時間:語り終了時間}:言葉}
        file = open(file_name)  # データ入力
        lines = file.readlines()

        for i, data in enumerate(lines[0:len(lines)]):
            data = data.rstrip('\n')  # 改行の削除
            data = data.split(',')  # ','で分割
            num = len(data)-1  # １行の長さを取得(この先の利用を考え-1)

            # 例外処理
            if num == 0:
                continue
            elif data[0] == "sp" or data[0] == "pause" or data[0] == "silB" or data[0] == "silE":
                word = word = 'pause' + str(i)
                begin = float(data[1:3][0])
                end = float(data[1:3][1])

                if len(self.katari) != 0:
                    last_word = list(self.katari[-1].keys())
                    last_time = list(self.katari[-1].values())
                    if 'pause' in last_word[0]:
                        self.katari.pop(-1)
                        begin = last_time[0][0]

                time = [begin, end]

            elif data[0] == "(" or data[0] == ")":
                continue
            elif data[1] == "補助記号":
                continue
            else:
                word = data[0]
                begin = float(data[num-1])
                end = float(data[num])
                time = [begin, end]

            self.katari.append({word: time})

        file.close()


def statistics(katari_info, outou_info):
    # print(katari_info)
    for i, katari in enumerate(katari_info):
        katari_time = list(katari.values())
        start = katari_time[0][0]
        end = katari_time[0][1]
        for outou_time in outou_info:
            if start <= outou_time and outou_time <= end:
                popWord = list(katari_info[i-1].keys())  # pop先がpauseなのを防ぐ
                if 'pause' in popWord[0]:
                    # print('pause',katari_info[i-2])
                    katari_info.pop(i-2)
                else:
                    # print('def',katari_info[i-1])
                    katari_info.pop(i-1)
                break

    return katari_info


def count(data):
    wordList = []  # 出現する単語を全て保存
    keyWord = []  # 単語の種類を保存
    for value in data:
        word = list(value.keys())[0]

        if 'pause' in word:
            continue

        wordList.append(word)
        if word not in keyWord:
            keyWord.append(word)

    for word in keyWord:
        with open(path, mode='a') as f:
            f.write(word + ': ' + str(wordList.count(word)) + '\n')
        # print(word, wordList.count(word))


if __name__ == '__main__':
    kt = KatariPause()
    katari = kt.read_data()

    ot = Outou('a')
    outou_a, outou_label = ot.read_data()

    ot = Outou('b')
    outou_b, outou_label = ot.read_data()

    result = statistics(katari, outou_a)
    result = statistics(result, outou_b)

    # print(result)
    count(result)
