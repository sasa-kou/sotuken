import glob
import copy
from functools import reduce

fileArray = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'
]
testData_num = ['1', '2', '3', '4', '5', '6', '7']


class Outou:
    def __init__(self, file_name):
        self.outou = []
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
                self.outou = []

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

                self.outou.append({begin: word})
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


class Segment:
    def __init__(self):
        self.katari = []
        self.katari_compare = {}    # {01-1: [{word: time}]}
        self.hinshi = []
        self.hinshi_compare = {}
        self.detail = []
        self.detail_compare = {}
        self.flag = False

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
                self.flag = True
                continue
            elif data[0] == "(" or data[0] == ")":
                continue
            elif data[1] == "補助記号":
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
            else:
                word = data[0]
                hinshi = data[1]
                detail = hinshi + data[2]
                begin = float(data[num-1])
                end = float(data[num])
                time = [begin, end]

            if self.flag:
                if 'pause' in word:
                    tmpBegin = time[0]
                    flag = time[1]
                    self.katari.append({word: time})
                    self.hinshi.append({hinshi: time})
                    self.detail.append({detail: time})
                else:
                    if flag != time[0]:  # そのまま更新
                        self.katari.append({word: time})
                        self.hinshi.append({hinshi: time})
                        self.detail.append({detail: time})
                    else:   # 時間を編集して更新
                        newTime = [tmpBegin, time[1]]
                        self.katari.pop(-1)
                        self.hinshi.pop(-1)
                        self.detail.pop(-1)
                        self.katari.append({word: newTime})
                        self.hinshi.append({hinshi: newTime})
                        self.detail.append({detail: newTime})
                    self.flag = False
        file.close()

    def count(self):
        count = 0
        for index in list(self.katari_compare.keys()):
            count += len(self.katari_compare[index])
        return count


def statistics(katari_info, outou_info):
    result = {}
    count = 0
    for index in list(katari_info.keys()):
        result[index] = []
        for katari in katari_info[index]:
            katari_time = list(katari.values())[0]
            start = katari_time[0]
            end = katari_time[1]
            for outou in outou_info[index]:
                outou_time = list(outou.keys())[0]
                if start <= outou_time and outou_time < end:
                    count += 1
                    # num = katari_info[index].index(katari)
                    # num2 = outou_info[index].index(outou)
                    # print(katari_info[index][num], outou_info[index][num2])
                    break
    return count


if __name__ == '__main__':
    kt = Segment()
    katari, hinshi, detail = kt.read_data()
    num = kt.count()
    print('文節の数：', num)

    ot = Outou('a')
    outou_a, outou_label_a = ot.read_data()
    num_a = ot.count()
    ot = Outou('b')
    outou_b, outou_label_b = ot.read_data()
    num_b = ot.count()
    ot = Outou('c')
    outou_c, outou_label_c = ot.read_data()
    num_c = ot.count()

    print('A')
    print('応答数：',num_a)
    katari_a = copy.deepcopy(katari)
    count = statistics(katari_a, outou_a)
    print('文節での応答数：', count)
    print('全応答に対する割合：',round(count/num_a*100, 2), '% ', count, '/', num_a)
    print('全文節に対する割合：', round(count/num*100, 2), '% ', count, '/', num)

    print('B')
    print('応答数：',num_b)
    katari_b = copy.deepcopy(katari)
    count = statistics(katari_b, outou_b)
    print('文節での応答数：', count)
    print('全応答に対する割合：',round(count/num_a*100, 2), '% ', count, '/', num_a)
    print('全文節に対する割合：', round(count/num*100, 2), '% ', count, '/', num)

    print('C')
    print('応答数：',num_c)
    katari_c = copy.deepcopy(katari)
    count = statistics(katari_c, outou_c)
    print('文節での応答数：', count)
    print('全応答に対する割合：',round(count/num_a*100, 2), '% ', count, '/', num_a)
    print('全文節に対する割合：', round(count/num*100, 2), '% ', count, '/', num)
