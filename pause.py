import glob
import sys
import os
import shutil
from functools import reduce
path = 'pauseResult.txt'
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

        return self.outou_label, self.outou_compare

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

    def count(self):
        # 応答数を表示
        count = 0
        for index in list(self.outou_compare.keys()):
            # print(index)
            # print(len(self.outou_a_compare[index]))
            count = count + len(self.outou_compare[index])

        return count


class Pause:
    def __init__(self):
        self.pause = []
        self.marge = False
        self.pauseCompare = {}

    def read_data(self):
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
                        self.readPause(targetFile)
                    self.marge = False  # ファイルを跨いだ更新は行わない
                num = file_index + '-' + index
                self.pauseCompare.update({num: self.pause})
                self.pause = []

        return self.pauseCompare

    def readPause(self, file_name):  # 語り側   [間の開始時間：間の終了時間]
        file = open(file_name)  # データ入力
        lines = file.readlines()

        for data in lines[0:len(lines)]:
            data = data.rstrip('\n')  # 改行の削除
            data = data.split(',')  # ','で分割
            if data[0] == 'silB' and self.marge:  # ファイルを跨いで間をマージ
                # ファイルを跨いだ時間のmargeのためsilBの終了時間を取得する
                end = lines[1]
                end = end.split(',')
                end = float(end[2].rstrip('\n'))  # 改行の削除
                # これまでの最終時間をstart
                start = self.pause[len(self.pause)-1][0]
                self.pause.pop(-1)  # 最後の要素を削除
                time = [start, end]
                self.pause.append(time)
            elif data[0] == 'silB' and not self.marge:  # ファイルを跨いだらそのまま
                start = float(data[1:3][0])
                end = float(data[1:3][1])
                time = [start, end]
                self.pause.append(time)
            if data[0] == 'silE' or data[0] == 'sp' or data[0] == 'pause':
                start = float(data[1:3][0])
                end = float(data[1:3][1])

                if len(self.pause) != 0:  # 一番初めは比較対象がないので
                    # 今までの終わりと追加するものの始まりが等しい時
                    if self.pause[len(self.pause)-1][1] == start:
                        start = self.pause[len(self.pause)-1][0]  # 開始時間を取得
                        self.pause.pop(-1)  # 最後の要素を削除
                time = [start, end]
                self.pause.append(time)

        if not self.marge:  # Falseの時、次からはマージする
            self.marge = True

        file.close()

    def count(self):
        count = 0
        for index in list(self.pauseCompare.keys()):
            count = count + len(self.pauseCompare[index])

        return count


def trance_data(pause, outou):
    interval = 0
    length = []  # 間の長さが200ms以上なら1
    for index in list(pause.keys()):
        # print(index)
        for time in pause[index]:
            start = float(time[0])
            end = float(time[1])
            # print(outou[index])
            for time in outou[index]:
                if start < time and time < end:
                    interval += 1
                    if round(end-start, 2) >= 0.2:
                        length.append(1)
                    else:
                        length.append(0)

                    # print(start, end)
                    # print(time, end=' ')
                    # print(outou[index][time])

    return interval, length


if __name__ == '__main__':
    ps = Pause()
    pause = ps.read_data()
    pause_num = ps.count()
    print('間の数', pause_num)

    print('A')
    ot = Outou('a')
    outou_a_label, outou_a = ot.read_data()
    num = ot.count()
    print('応答数：', num)
    interval, length = trance_data(pause, outou_a)
    print('間での応答数：', interval)
    print('そのうち200ms以上の応答数：', length.count(1))
    print('全体の応答数に対する間での応答数の割合：', round(interval/num*100, 2))
    print('全体の間に対する間での応答数の割合：', round(interval/pause_num*100, 2))

    print('B')
    ot = Outou('b')
    outou_b_label, outou_b = ot.read_data()
    num = ot.count()
    print('応答数：', num)
    interval, length = trance_data(pause, outou_b)
    print('間での応答数：', interval)
    print('そのうち200ms以上の応答数：', length.count(1))
    print('全体の応答数に対する間での応答数の割合：', round(interval/num*100, 2))
    print('全体の間に対する間での応答数の割合：', round(interval/pause_num*100, 2))
