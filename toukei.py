import glob
import sys
import os
import shutil
from functools import reduce
import pprint
path = 'toukeiResult.txt'
with open(path, mode='w') as f:
    f.write('')

fileArray = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'
]
testData_num = ['1', '2', '3', '4', '5', '6', '7']


class Outou:
    def __init__(self, file_name):
        self.outou = []
        self.outou_label = []
        self.outou_compare = {}
        self.outou_label_compare = {}
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
                self.outou_label_compare.update({num: self.outou_label})
                self.outou = []
                self.outou_label = []

        return self.outou_compare, self.outou_label_compare

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

                self.outou.append({begin: word})
                self.outou_label.append({begin: label})

            else:
                tmp_str += data[0]  # 文字の退避

        file.close()

    def count(self):
        # 応答数を表示
        count = 0
        for index in list(self.outou_compare.keys()):
            # print(index)
            # print(len(self.outou_a_compare[index]))
            count += len(self.outou_compare[index])

        return count

    def label(self):
        #pprint.pprint(self.outou_compare)
        #for i in list(self.outou_compare):
        #    print(i, len(self.outou_compare[i]))
        result = {}
        ans = []
        parce = []
        labelList = []  # 出現する単語を全て保存
        keyLabel = []  # 単語の種類を保存
        size = self.count()

        # path = 'toukeiLabel' + self.file_name + '.txt'
        # with open(path, mode='w') as f:
        #     f.write('')

        for index in list(self.outou_label_compare.keys()):
            for data in self.outou_label_compare[index]:
                label = list(data.values())[0]
                labelList.append(label)

                if label not in keyLabel:
                    keyLabel.append(label)

        for label in keyLabel:
            result.update({label: labelList.count(label)})

        for k, v in sorted(result.items(), key=lambda x: -x[1]):
            ans.append({k: v})
            parce.append({k: round(v/size*100, 2)})
            # with open(path, mode='a') as f:
            #     f.write(str(k) + ':' + str(v) + '\n')
        print(ans)
        print(parce)


class Katari:
    def __init__(self):
        self.katari = []
        self.katari_compare = {}
        self.timeArray = []
        self.time = 0
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
                    self.time = round(
                        self.time + (self.timeArray[1] - self.timeArray[0]), 2)
                    self.timeArray = []  # 時間情報の初期化
                num = file_index + '-' + index
                self.katari_compare.update({num: self.katari})
                self.hinshi_compare.update({num: self.hinshi})
                self.detail_compare.update({num: self.detail})
                self.katari = []
                self.hinshi = []
                self.detail = []

        return self.katari_compare, self.time, self.hinshi_compare, self.detail_compare

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
            elif data[0] == "silB":
                begin = float(data[num-1])  # 開始時刻の取得
                if len(self.timeArray) == 0:
                    self.timeArray.append(begin)
                else:
                    if self.timeArray[0] > begin:
                        self.timeArray[0] = begin
                continue
            elif data[0] == 'silE':
                end = float(data[num])
                if len(self.timeArray) == 1:
                    self.timeArray.append(end)
                else:
                    if self.timeArray[1] < end:
                        self.timeArray[1] = end
                continue
            elif data[0] == "sp" or data[0] == "pause":
                continue
            elif data[0] == "(" or data[0] == ")":
                continue
            elif data[1] == "補助記号":
                continue

            word = data[0]
            hinshi = data[1]
            detail = hinshi + data[2]
            end = float(data[num])
            self.katari.append({end: word})
            self.hinshi.append({end: hinshi})
            self.detail.append({end: detail})

        file.close()

    def length(self):
        num = 0
        for index in list(self.katari_compare.keys()):
            for data in self.katari_compare[index]:
                num += len(data)
        print('語りの個数', num)

    def write(self):
        count(self.katari_compare, 'katariCount.txt')
        count(self.hinshi_compare, 'hinshiCount.txt')
        count(self.detail_compare, 'detailCount.txt')


def count(data, filePath):
    with open(filePath, mode='w') as f:
        f.write('')

    wordList = []  # 出現する単語を全て保存
    keyWord = []  # 単語の種類を保存
    for index in list(data.keys()):
        for value in data[index]:
            word = list(value.values())[0]
            wordList.append(word)
            if word not in keyWord:
                keyWord.append(word)

    for word in keyWord:
        with open(filePath, mode='a') as f:
            f.write(word + ':' + str(wordList.count(word)) + '\n')


def fileWrite(katari, outou, filePath):
    time_list = []
    with open('toukeiResult' + filePath + '.txt', mode='w') as f:
        f.write('語り：')
    for index in list(katari.keys()):
        for katari_data in katari[index]:
            katari_time = list(katari_data.keys())[0]
            time_list.append(katari_time)
        for outou_data in outou[index]:
            outou_time = list(outou_data.keys())[0]
            time_list.append(outou_time)
        time_list.sort()

        for time in time_list:
            flag = list(map(lambda x: time in x, katari[index]))
            if True in flag:
                num = flag.index(True)
                word = list(katari[index][num].values())[0]
                with open('toukeiResult' + filePath + '.txt', mode='a') as f:
                    f.write(word)
            else:
                tmp = list(map(lambda x: time in x, outou[index]))
                num = tmp.index(True)
                word = list(outou[index][num].values())[0]
                with open('toukeiResult' + filePath + '.txt', mode='a') as f:
                    f.write('\n' + '応答：' + word + '\n' + '語り：')
        time_list = []


if __name__ == '__main__':
    kt = Katari()
    katari, time, hinshi, detail = kt.read_data()
    kt.length()
    print("語り総時間：", time)
    # kt.write()  # fileWrite

    print('A')
    ot = Outou('a')
    outou, outou_label = ot.read_data()
    print('応答の個数：', ot.count())
    print("１秒間あたりの応答数：", round(ot.count()/time, 2), ot.count(), '/', time)
    ot.label()
    # fileWrite(katari, outou, 'A')

    print('B')
    ot = Outou('b')
    outou, outou_label = ot.read_data()
    print('応答の個数：', ot.count())
    print("１秒間あたりの応答数：", round(ot.count()/time, 2), ot.count(), '/', time)
    ot.label()
    # fileWrite(katari, outou, 'B')

    print('C')
    ot = Outou('c')
    outou, outou_label = ot.read_data()
    print('応答の個数：', ot.count())
    print("１秒間あたりの応答数：", round(ot.count()/time, 2), ot.count(), '/', time)
    ot.label()
    # fileWrite(katari, outou, 'C')
