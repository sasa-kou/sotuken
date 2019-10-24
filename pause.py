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
        self.tmpOutou = {}
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
                self.outou_compare.update({num: self.tmpOutou})
                self.tmpOutou = {}

        return self.outou, self.outou_label, self.outou_compare

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
                self.tmpOutou.update({begin: word})
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
        self.length = []  # 200msより、0が短く、1が長い
        self.tmpPause = []
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
                    num = file_index + '-' + index
                    self.pauseCompare.update({num: self.tmpPause})
                    self.tmpPause = []
                    self.marge = False  # ファイルを跨いだ更新は行わない

        return self.pause, self.pauseCompare

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
                self.tmpPause.pop(-1)
                time = [start, end]
                self.pause.append(time)
                self.tmpPause.append(time)
                if round(end-start, 2) >= 0.2:
                    self.length.append(1)
                else:
                    self.length.append(0)
            elif data[0] == 'silB' and not self.marge:  # ファイルを跨いだらそのまま
                start = float(data[1:3][0])
                end = float(data[1:3][1])
                time = [start, end]
                self.pause.append(time)
                self.tmpPause.append(time)
                if round(end-start, 2) >= 0.2:
                    self.length.append(1)
                else:
                    self.length.append(0)

            if data[0] == 'silE' or data[0] == 'sp' or data[0] == 'pause':
                start = float(data[1:3][0])
                end = float(data[1:3][1])

                if len(self.pause) != 0:  # 一番初めは比較対象がないので
                    # 今までの終わりと追加するものの始まりが等しい時
                    if self.pause[len(self.pause)-1][1] == start:
                        start = self.pause[len(self.pause)-1][0]  # 開始時間を取得
                        self.pause.pop(-1)  # 最後の要素を削除
                        self.tmpPause.pop(-1)
                time = [start, end]
                self.pause.append(time)
                self.tmpPause.append(time)
                if round(end-start, 2) >= 0.2:
                    self.length.append(1)
                else:
                    self.length.append(0)

        if not self.marge:  # Falseの時、次からはマージする
            self.marge = True

        file.close()

    def countLength(self):
        print('CH', len(self.length), len(self.pause))
        print("長い：", self.length.count(1))
        print("短い：", self.length.count(0))


def trance_data(pause, outou):
    interval = 0

    for index in list(pause.keys()):
        # print(index)
        for time in pause[index]:
            start = float(time[0])
            end = float(time[1])
            # print(outou[index])
            for time in outou[index]:
                if start < time and time < end:
                    interval += 1
                    #print(start, end)
                    #print(time, end=' ')
                    #print(outou[index][time])

    return interval


def trance_dataX(pause, outou, outou_label):  # 情報処理
    interval = 0  # 間で開始した応答数
    dic = {}      # 一致を検知する基準
    time_list = list(outou.keys())  # 応答の開始時間
    time_list.sort()

    for time in pause:
        start = float(time[0])  # 間の開始時間
        end = float(time[1])  # 間の終了じかん
        for i in time_list:
            if start < i and i < end:
                # print(start, end)
                # print(i, end="")
                # print(outou[i])
                # 間の開始時間を比較基準とする
                dic.update({start: {outou[i]: outou_label[i]}})
                interval += 1
                with open(path, mode='a') as f:
                    f.write('間の開始時間：' + str(start))
                    f.write(' 間の終了時間：' + str(end) + '\n')
                    f.write(str(dic[start]) + '\n')
                break

    with open(path, mode='a') as f:
        f.write('\n')

    return interval, dic


def compare(*args):  # 間で開始した応答時間の一致
    time_list = reduce(lambda x, y: list(
        set(x) & set(y)), args)
    time_list.sort()

    return len(time_list)


if __name__ == '__main__':
    ps = Pause()
    pause, pauseCompare = ps.read_data()
    ps.countLength()

    ot = Outou('a')
    outou_a, outou_a_label, outou_a_compare = ot.read_data()
    num = ot.count()
    print('応答数：', num)
    a_interval, a_dic = trance_dataX(pause, outou_a, outou_a_label)
    interval_a = trance_data(pauseCompare, outou_a_compare)
    print(interval_a)
    print(a_interval)

    ot = Outou('b')
    outou_b, outou_b_label, outou_b_compare = ot.read_data()
    #b_interval, b_dic = trance_data(pause, outou_b, outou_b_label)
"""
    print('A')
    print('間で開始した応答数：', a_interval)
    print('全体の応答に対する間で開始した応答の割合：', a_interval/len(outou_a)*100, ' %',)

    print('B')
    print('間で開始した応答数：', b_interval)
    print('全体の応答に対する間で開始した応答の割合：', b_interval/len(outou_b)*100, ' %')

    print('ABの一致', compare(a_dic, b_dic))
"""
