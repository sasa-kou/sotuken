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
fileArray = ['01']
testData_num = ['1', '2', '3', '4', '5', '6', '7']


class Outou:
    def __init__(self, file_name):
        self.outou = {}
        self.outou_label = {}
        self.outou_compare = {}
        self.file_name = file_name

    def read_data(self):  # 全ファイルを検索して読み込み
        file_root = '../../outouwithlabel_camui/outouwithlabel_camui/'
        file_end = '/*.morph'

        for file_index in fileArray:
            files = glob.glob(file_root + file_index +
                              '/' + self.file_name + '/')
            for index in testData_num:
                targetFileList = glob.glob(files[0] + index + file_end)
                targetFileList.sort()
                for targetFile in targetFileList:
                    self.readOutou(targetFile)

                num = file_index + '-' + index
                self.outou_compare.update({num: self.outou})
                self.outou = {}

        return self.outou_compare, self.outou_label

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
                # print(word, label, begin)

                self.outou.update({begin: word})
                self.outou_label.update({begin: label})

            else:
                tmp_str += data[0]  # 文字の退避

        file.close()


class KatariPause:
    def __init__(self):
        self.katari = []
        self.katari_compare = {}
        self.hinshi = []
        self.hinshi_compare = {}

    def read_data(self):  # 全ファイルを検索して読み込み(読み込み順は適当)
        file_root = '../../katari_info/'
        file_end = '/*.morph'

        for file_index in fileArray:
            files = glob.glob(file_root + file_index + '/')
            for index in testData_num:
                bigFiles = glob.glob(files[0] + index + '/*')
                for bigFile in bigFiles:
                    targetFileList = glob.glob(bigFile + file_end)
                    targetFileList.sort()
                    for targetFile in targetFileList:
                        self.readKatari(targetFile)
                num = file_index + '-' + index
                self.katari_compare.update({num: self.katari})
                self.hinshi_compare.update({num: self.hinshi})
                self.katari = []
                self.hinshi = []

        return self.katari_compare, self.hinshi_compare

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
                word = 'pause' + str(i)
                hinshi = 'pause' + str(i)
                begin = float(data[1:3][0])
                end = float(data[1:3][1])

                if len(self.katari) != 0:
                    last_katari_word = list(self.katari[-1].keys())
                    last_katari_time = list(self.katari[-1].values())
                    last_hinshi_word = list(self.hinshi[-1].keys())
                    last_hinshi_time = list(self.hinshi[-1].values())

                    if 'pause' in last_katari_word[0]:
                        self.katari.pop(-1)
                        begin = last_katari_time[0][0]
                    if 'pause' in last_hinshi_word[0]:
                        self.hinshi.pop(-1)
                        begin = last_hinshi_time[0][0]

                time = [begin, end]

            elif data[0] == "(" or data[0] == ")":
                continue
            elif data[1] == "補助記号":
                continue
            else:
                word = data[0]
                hinshi = data[1]
                begin = float(data[num-1])
                end = float(data[num])
                time = [begin, end]

            self.katari.append({word: time})
            self.hinshi.append({hinshi: time})
        file.close()


def statistics(katari_info, outou_info):
    for index in list(katari_info.keys()):
        for katari in katari_info[index]:
            katari_time = list(katari.values())
            start = katari_time[0][0]
            end = katari_time[0][1]
            for outou_time in outou_info[index]:
                if start <= outou_time and outou_time < end:
                    num = katari_info[index].index(katari) - 1
                    popWord = list(katari_info[index][num].keys())
                    if 'pause' in popWord[0]:    # pop先がpauseなのを防ぐ
                        # print('pause', katari_info[index][num-1])
                        # print(outou_info[index][outou_time], outou_time)
                        katari_info[index].pop(num-1)
                    else:
                        # print('def', katari_info[index][num])
                        # print(outou_info[index][outou_time], outou_time)
                        katari_info[index].pop(num)
                    break
                
    return katari_info


def count(data):
    result = {}
    answer = []
    wordList = []  # 出現する単語を全て保存
    keyWord = []  # 単語の種類を保存
    for index in list(data.keys()):
        for value in data[index]:
            word = list(value.keys())[0]

            if 'pause' in word:
                continue

            wordList.append(word)
            if word not in keyWord:
                keyWord.append(word)

    for word in keyWord:
        result.update({word: wordList.count(word)})
        with open(path, mode='a') as f:
            f.write(word + ':' + str(wordList.count(word)) + '\n')
        # print(word, wordList.count(word))

    for k, v in sorted(result.items(), key=lambda x: -x[1]):
        answer.append({k: v})

    print(answer[0:10])


if __name__ == '__main__':
    kt = KatariPause()
    katari, hinshi = kt.read_data()

    ot = Outou('a')
    outou_a, outou_label = ot.read_data()

    ot = Outou('b')
    outou_b, outou_label = ot.read_data()

    print('A')
    katari_a = katari.copy()
    hinshi_a = hinshi.copy()
    result = statistics(katari_a, outou_a)
    count(result)
    result = statistics(hinshi_a, outou_a)
    count(result)
    
    print()

    print('B')
    katari_b = katari.copy()
    hinshi_b = hinshi.copy()
    result = statistics(katari_b, outou_b)
    count(result)
    result = statistics(hinshi_b, outou_b)
    count(result)
