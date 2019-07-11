import glob
import os
import shutil
from functools import reduce


class Outou:
    def __init__(self, file_num, file_name):
        self.outou = {}
        self.outou_label = {}
        self.outou_count = 0
        self.file_num = file_num
        self.file_name = file_name

    def read_data(self):  # 全ファイルを検索して読み込み
        file_root = '../../outouwithlabel_camui/outouwithlabel_camui/'
        file_end = '/*.morph'

        files = glob.glob(file_root + self.file_num +
                          '/' + self.file_name + file_end)
        files.sort()

        for file in files:
            self.readOutou(file)

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
                # print(word, label, begin)

                self.outou.update({begin: word})
                self.outou_label.update({begin: label})

            else:
                tmp_str += data[0]  # 文字の退避

        file.close()

    def view(self):
        # 応答数を表示
        print(self.file_name, len(self.outou))


class Pause:
    def __init__(self, file_num):
        self.pause = []
        self.file_num = file_num
        self.end_time = 0.0

    def read_data(self):
        file_root = '../../katari_info/'
        big_files = glob.glob(file_root + self.file_num +
                              '/' + self.file_num + '-*')
        for small_file in big_files:
            files = glob.glob(small_file + '/*.morph')
            files.sort()
            for file in files:
                self.readPause(file)
            self.end_time = 0.0  # 一つの01-*が終わったら終了時刻を初期化

        return self.pause

    def readPause(self, file_name):  # 語り側   [間の開始時間：間の終了時間]
        file = open(file_name)  # データ入力
        lines = file.readlines()
        print(file)

        # ファイルの最初と最後の時間を取得
        begin = lines[1]
        begin = begin.split(',')
        begin = float(begin[1])
        end = lines[len(lines)-1]
        end = end.split(',')
        end = float(end[2].rstrip('\n'))  # 改行の削除

        if self.end_time != 0.0:  # 一番最初のファイルはスルー
            if begin != self.end_time:
                print(True)

        for data in lines[0:len(lines)]:
            data = data.rstrip('\n')  # 改行の削除
            data = data.split(',')  # ','で分割
            if data[0] == 'silE' or data[0] == 'silB' or data[0] == 'sp' or data[0] == 'pause':
                start = float(data[1:3][0])
                end = float(data[1:3][1])

                if len(self.pause) != 0:  # 一番初めは比較対象がないので
                    # 今までの終わりと追加するものの始まりが等しい時
                    if self.pause[len(self.pause)-1][1] == start:
                        start = self.pause[len(self.pause)-1][0]  # 開始時間を取得
                        self.pause.pop(-1)  # 最後の要素を削除

                time = [start, end]
                print(time)
                self.pause.append(time)

        print(begin, self.end_time)
        self.end_time = end  # 終了時刻の更新
        self.pause.sort()

        file.close()


def trance_data(pause, outou):  # 情報処理
    interval = 0  # 間で開始した応答数
    dic = []      # 一致を検知する基準
    time_list = list(outou.keys())  # 応答の開始時間
    time_list.sort()

    for time in pause:
        start = float(time[0])  # 間の開始時間
        end = float(time[1])  # 間の終了じかん
        for i in time_list:
            if start < i and i < end:
                #print(start, end)
                #print(i, end="")
                # print(outou[i])
                dic.append(start)  # 間の開始時間を比較基準とする
                interval += 1
                break

    return interval, dic


def compare(*args):  # 間で開始した応答時間の一致
    comp = reduce(lambda x, y: list(
        set(x) & set(y)), args)

    return len(comp)


if __name__ == '__main__':
    ps = Pause('01')
    pause = ps.read_data()

    ot = Outou('01', 'a')
    outou, outou_label = ot.read_data()
    a_interval, a_dic = trance_data(pause, outou)

    ot = Outou('01', 'b')
    outou, outou_label = ot.read_data()
    b_interval, b_dic = trance_data(pause, outou)

    print('Aの間で開始した応答数', a_interval)
    print('Bの間で開始した応答数', b_interval)

    print('ABの一致', compare(a_dic, b_dic))
