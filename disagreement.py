import glob
import sys
import os
import shutil
import pprint
import MeCab
from functools import reduce
import copy
path = 'disagreementResult.txt'
with open(path, mode='w') as f:
    f.write('')
path2 = 'disagreementMatch.txt'
with open(path2, mode='w') as f:
    f.write('')

fileArray = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'
]
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
        self.katari_compare = {}    # {01-1: [{word: time}]}
        self.hinshi = []
        self.hinshi_compare = {}
        self.detail = []
        self.detail_compare = {}

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
                self.detail_compare.update({num: self.detail})
                self.katari = []
                self.hinshi = []
                self.detail = []

        return self.katari_compare, self.hinshi_compare, self.detail_compare

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
                detail = 'pause' + str(i)
                begin = float(data[1:3][0])
                end = float(data[1:3][1])

                if len(self.katari) != 0:
                    last_word = list(self.katari[-1].keys())
                    last_time = list(self.katari[-1].values())
                    if 'pause' in last_word[0]:
                        self.katari.pop(-1)
                        self.hinshi.pop(-1)
                        self.detail.pop(-1)
                        begin = last_time[0][0]

                time = [begin, end]

            elif data[0] == "(" or data[0] == ")":
                continue
            elif data[1] == "補助記号":
                continue
            else:
                word = data[0]
                hinshi = data[1]
                detail = hinshi + data[2]
                begin = float(data[num-1])
                end = float(data[num])
                time = [begin, end]

            self.katari.append({word: time})
            self.hinshi.append({hinshi: time})
            self.detail.append({detail: time})
        file.close()


def statistics(katari_info, outou_info):
    result = {}
    for index in list(katari_info.keys()):
        result[index] = []
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
                        result[index].append(katari_info[index][num-1])
                        katari_info[index].pop(num-1)
                    else:
                        # print('def', katari_info[index][num])
                        # print(outou_info[index][outou_time], outou_time)
                        result[index].append(katari_info[index][num])
                        katari_info[index].pop(num)
                    break

    return result, katari_info  # 応答された語り, 応答されていない語り


def readData(target):
    data = []
    if target == 'katari':
        with open('katariCount.txt', mode='r') as f:
            data = f.read()
    elif target == 'hinshi':
        with open('hinshiCount.txt', mode='r') as f:
            data = f.read()
    elif target == 'detail':
        with open('detailCount.txt', mode='r') as f:
            data = f.read()

    data = data.split("\n")
    return data


def count(data, targetData):
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
        flag = list(map(lambda x: word == x.split(':')[0], targetData))
        num = flag.index(True)
        allData = int(targetData[num].split(':')[1])
        parcentage = round(wordList.count(word)/allData*100, 2)
        result.update({word + ' ' + str(wordList.count(word)) +
                       '/' + str(allData): parcentage})

    for k, v in sorted(result.items(), key=lambda x: -x[1]):
        answer.append({k: v})
        with open(path, mode='a') as f:
            f.write(str(k) + ':' + str(v) + '\n')
    with open(path, mode='a') as f:
        f.write('\n')

    print(answer[0:10])


def match(targetData, writeFlag, *args):
    result = []
    wordList = []  # 出現する単語を全て保存
    keyWord = []  # 単語の種類を保存
    tmp = {}
    answer = []
    for index in list(args[0].keys()):
        for data in args[0][index]:
            flag = list(map(lambda x: data in x[index], args))
            if False not in flag:
                result.append(data)
    # print('ch', len(result))

    for data in result:
        word = list(data.keys())[0]

        if 'pause' in word:
            continue

        wordList.append(word)
        if word not in keyWord:
            keyWord.append(word)

    for word in keyWord:
        flag = list(map(lambda x: word == x.split(':')[0], targetData))
        num = flag.index(True)
        allData = int(targetData[num].split(':')[1])
        parcentage = round(wordList.count(word)/allData*100, 2)
        tmp.update({word + ' ' + str(wordList.count(word)) +
                    '/' + str(allData): parcentage})

    for k, v in sorted(tmp.items(), key=lambda x: -x[1]):
        answer.append({k: v})
        with open(path2, mode='a') as f:
            f.write(str(k) + ':' + str(v) + '\n')
    with open(path2, mode='a') as f:
        f.write('\n')

    if writeFlag:
        pprint.pprint(answer)

    else:
        print(answer[:10])


def get(seq):
    # ３人に共通するものを取り出す
    seen = []
    return [x for x in seq if seq.count(x) > 2 and not seen.append(x) and seen.count(x) == 1]


def writeDetail(targetData, a, b, c, detailA, detailB, detailC):
    timeList = {}
    wordList = {}  # 出現する単語を全て保存
    keyWord = {}  # 単語の種類を保存
    select = ['名詞数詞', '連体詞*', '代名詞*', '形状詞一般', '感動詞一般']
    path = 'disagreementContent.txt'
    with open(path, mode='w') as f:
        f.write('')

    for key in select:
        wordList[key.split(':')[0]] = []
        keyWord[key.split(':')[0]] = []

    for index in a:
        timeList[index] = []
        for data in a[index]:
            timeList[index].append(list(data.values())[0])
        for data in b[index]:
            timeList[index].append(list(data.values())[0])
        for data in c[index]:
            timeList[index].append(list(data.values())[0])

    for index in timeList:
        # 重複値のみを取り出す
        keyTimeList = get(timeList[index])
        for time in keyTimeList:
            tmp = list(filter(lambda x: list(x.values())
                              [0] == time, a[index]))[0]
            detailTmp = list(filter(lambda x: list(x.values())
                                    [0] == time, detailA[index]))[0]
            # データの整合性を確かめるために必要だった（整合性は確認済み）
            # tmpA = list(filter(lambda x: list(x.values())[0] == time ,detailA[index]))
            # tmpB = list(filter(lambda x: list(x.values())[0] == time ,detailB[index]))
            # tmpC = list(filter(lambda x: list(x.values())[0] == time ,detailC[index]))
            # if not tmpA == tmpB == tmpC:
            #     print('Error')

            word = list(tmp.keys())[0]

            if 'pause' in word:
                continue

            detail = list(detailTmp.keys())[0]
            if detail in select:
                wordList[detail].append(word)
                if word not in keyWord:
                    keyWord[detail].append(word)

    result = {}
    for detail in keyWord:
        result[detail] = {}
        for word in keyWord[detail]:
            # denominator = list(
            #     filter(lambda x: word == x.split(':')[0], targetData))[0]
            # denominator = int(denominator.split(':')[1])
            # parcentage = round(wordList[detail].count(word)/denominator*100, 2)
            length = wordList[detail].count(word)
            result[detail].update({word: length})

    f = open(path,mode='a')
    for key, value in result.items():
        f.write(key + '\n')
        count = 0
        for k, v in sorted(value.items(), key=lambda x: -x[1]):
            f.write(str(k) + ': ' + str(v) + '\n')
            count += v
        f.write('\n')
        # print(key, count)
    f.close()
    print('fileWrite at disagreementContent.txt: 応答できないタイミングのためのデータ')


if __name__ == '__main__':
    kt = KatariPause()
    katari, hinshi, detail = kt.read_data()

    katariData = readData('katari')
    hinshiData = readData('hinshi')
    detailData = readData('detail')

    ot = Outou('a')
    outou_a, outou_label = ot.read_data()
    ot = Outou('b')
    outou_b, outou_label = ot.read_data()
    ot = Outou('c')
    outou_c, outou_label = ot.read_data()

    print('A')
    katari_a = copy.deepcopy(katari)
    hinshi_a = copy.deepcopy(hinshi)
    detail_a = copy.deepcopy(detail)
    word_a, word_a_not = statistics(katari_a, outou_a)
    count(word_a, katariData)
    count(word_a_not, katariData)
    print()
    morpheme_a, morpheme_a_not = statistics(hinshi_a, outou_a)
    count(morpheme_a, hinshiData)
    count(morpheme_a_not, hinshiData)
    print()

    morphemeDtail_a, morphemeDetail_a_not = statistics(detail_a, outou_a)
    count(morphemeDtail_a, detailData)
    count(morphemeDetail_a_not, detailData)

    print()

    print('B')
    katari_b = copy.deepcopy(katari)
    hinshi_b = copy.deepcopy(hinshi)
    detail_b = copy.deepcopy(detail)
    word_b, word_b_not = statistics(katari_b, outou_b)
    count(word_b, katariData)
    count(word_b_not, katariData)
    print()
    morpheme_b, morpheme_b_not = statistics(hinshi_b, outou_b)
    count(morpheme_b, hinshiData)
    count(morpheme_b_not, hinshiData)
    print()
    morphemeDetail_b, morphemeDetail_b_not = statistics(detail_b, outou_b)
    count(morphemeDetail_b, detailData)
    count(morphemeDetail_b_not, detailData)

    print()

    print('C')
    katari_c = copy.deepcopy(katari)
    hinshi_c = copy.deepcopy(hinshi)
    detail_c = copy.deepcopy(detail)
    word_c, word_c_not = statistics(katari_c, outou_c)
    count(word_c, katariData)
    count(word_c_not, katariData)
    print()
    morpheme_c, morpheme_c_not = statistics(hinshi_c, outou_c)
    count(morpheme_c, hinshiData)
    count(morpheme_c_not, hinshiData)
    print()
    morphemeDetail_c, morphemeDetail_c_not = statistics(detail_c, outou_c)
    count(morphemeDetail_c, detailData)
    count(morphemeDetail_c_not, detailData)

    print('応答した')
    # match(katariData, False, word_a, word_b, word_c)
    # match(hinshiData, False, morpheme_a, morpheme_b, morpheme_c)
    match(detailData, True, morphemeDtail_a,
          morphemeDetail_b, morphemeDetail_c)
    print()
    print('応答してない')
    # match(katariData, False, word_a_not, word_b_not, word_c_not)
    # match(hinshiData, False, morpheme_a_not, morpheme_b_not, morpheme_c_not)
    match(detailData, True, morphemeDetail_a_not,
          morphemeDetail_b_not, morphemeDetail_c_not)

    writeDetail(katariData, word_a_not, word_b_not, word_c_not, morphemeDetail_a_not,
                morphemeDetail_b_not, morphemeDetail_c_not)
