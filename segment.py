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

    def readKatari(self, file_name):
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
                    last_word = self.katari[-1]['word']
                    last_time = self.katari[-1]['time']
                    if 'pause' in last_word:
                        self.katari.pop(-1)
                        self.hinshi.pop(-1)
                        self.detail.pop(-1)
                        begin = last_time[0]

                time = [begin, end]
            else:
                word = data[0]
                hinshi = data[1]
                detail = hinshi + data[2]
                begin = float(data[num-1])
                end = float(data[num])
                time = [begin, end]

            if self.flag:
                if 'pause' in word:  # pause時の時間情報を保持するため必要
                    tmpBegin = time[0]
                    flag = time[1]
                    self.katari.append({'word': word, 'time': time})
                    self.hinshi.append({'word': hinshi, 'time': time})
                    self.detail.append({'word': detail, 'time': time})
                else:
                    if flag != time[0]:  # そのまま更新
                        self.katari.append(
                            {'word': word, 'time': time, 'hinshi': [hinshi]})
                        self.hinshi.append({'word': hinshi, 'time': time})
                        self.detail.append({'word': detail, 'time': time})
                    else:   # 時間を編集して更新
                        newTime = [tmpBegin, time[1]]
                        self.katari.pop(-1)
                        self.hinshi.pop(-1)
                        self.detail.pop(-1)
                        self.katari.append(
                            {'word': word, 'time': newTime, 'hinshi': [hinshi]})
                        self.hinshi.append({'word': hinshi, 'time': newTime})
                        self.detail.append({'word': detail, 'time': newTime})
                    self.flag = False
            else:
                if 'pause' not in hinshi:
                    self.katari[-1]['hinshi'].append(hinshi)
        file.close()

    def labelCount(self, target):
        result = {}
        count = 0
        data = copy.deepcopy(self.katari_compare)
        for index in list(data.keys()):
            value = list(filter(lambda x: target in x['hinshi'], data[index]))
            count += len(value)
            result[index] = value

        return result, count

    def count(self):
        count = 0
        for index in list(self.katari_compare.keys()):
            count += len(self.katari_compare[index])
        return count


def statistics_count(katari_data, outou_info):
    katari_info = copy.deepcopy(katari_data)
    data = {}
    count = 0
    for index in list(katari_info.keys()):
        data[index] = []
        for katari in katari_info[index]:
            katari_time = katari['time']
            start = katari_time[0]
            end = katari_time[1]
            for outou in outou_info[index]:
                outou_time = list(outou.keys())[0]
                if start <= outou_time and outou_time < end:
                    count += 1
                    data[index].append(outou)
                    break
    return count, data


def statistics_info(katari_data, outou_info, target):
    katari_info = copy.deepcopy(katari_data)
    count = 0
    data = {}
    for index in list(katari_info):
        data[index] = []
        for katari in katari_info[index]:
            katari_time = katari['time']
            start = katari_time[0]
            end = katari_time[1]
            for outou in outou_info[index]:
                outou_time = list(outou.keys())[0]
                if start <= outou_time and outou_time < end:
                    # num = katari_info[index].index(katari)
                    # num2 = outou_info[index].index(outou)
                    popIndex = katari_info[index].index(
                        katari) - 1  # 応答があった一つ前の文節が対象
                    # print(katari_info[index][popIndex],katari_info[index][num], outou_info[index][num2])
                    if target in katari_info[index][popIndex]['hinshi']:
                        count += 1
                        data[index].append(outou)

    return count, data

def labelConversion(targetData, outouLabelData, size):
    labelList = []  # 出現するラベルをすべて保存
    keyLabel = []   # ラベルの種類を保存
    tmp = {}
    result = []
    parce = []
    for index in list(outouLabelData.keys()):
        for data in targetData[index]:
            time = list(data.keys())[0]
            value = list(filter(lambda x: time == list(
                x.keys())[0], outouLabelData[index]))[0]
            label = list(value.values())[0]
            labelList.append(label)
            if label not in keyLabel:
                keyLabel.append(label)

    for label in keyLabel:
        tmp.update({label: labelList.count(label)})

    for k, v in sorted(tmp.items(), key=lambda x: -x[1]):
        result.append({k: v})
        parce.append({k: round(v/size*100, 2)})
    print(result)
    print(parce)

if __name__ == '__main__':
    kt = Segment()
    katari, hinshi, detail = kt.read_data()
    num = kt.count()
    print('文節の数：', num)

    meishi, length_meishi = kt.labelCount('名詞')
    doushi, length_doushi = kt.labelCount('動詞')
    print('名詞を含む文節の数', length_meishi)
    print('動詞を含む文節の数', length_doushi)

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
    print('応答数：', num_a)
    count, data = statistics_count(katari, outou_a)
    count_meishi, data_meishi = statistics_info(katari, outou_a, '名詞')
    count_doushi, data_doushi = statistics_info(katari, outou_a, '動詞')
    print('文節での応答数：', count)
    labelConversion(data, outou_label_a, count)
    print('名詞を含む文節での応答数：', count_meishi)
    labelConversion(data_meishi, outou_label_a, count_meishi)
    print('動詞を含む文節での応答数：', count_doushi)
    labelConversion(data_doushi, outou_label_a, count_doushi)
    print('全応答に対する割合：', round(count/num_a*100, 2), '% ', count, '/', num_a)
    print('全文節に対する割合：', round(count/num*100, 2), '% ', count, '/', num)
    print('名詞を含む文節に関する割合', round(count_meishi/length_meishi*100, 2),
          '% ', count_meishi, '/', length_meishi)
    print('動詞を含む文節に関する割合', round(count_doushi/length_doushi*100, 2),
          '% ', count_doushi, '/', length_doushi)

    print('B')
    print('応答数：', num_b)
    count, data = statistics_count(katari, outou_b)
    count_meishi, data_meishi = statistics_info(katari, outou_b, '名詞')
    count_doushi, data_doushi = statistics_info(katari, outou_b, '動詞')
    print('文節での応答数：', count)
    labelConversion(data, outou_label_b, count)
    print('名詞を含む文節での応答数：', count_meishi)
    labelConversion(data_meishi, outou_label_b, count_meishi)
    print('動詞を含む文節での応答数：', count_doushi)
    labelConversion(data_doushi, outou_label_b, count_doushi)
    print('全応答に対する割合：', round(count/num_a*100, 2), '% ', count, '/', num_a)
    print('全文節に対する割合：', round(count/num*100, 2), '% ', count, '/', num)
    print('名詞を含む文節に関する割合', round(count_meishi/length_meishi*100, 2),
          '% ', count_meishi, '/', length_meishi)
    print('動詞を含む文節に関する割合', round(count_doushi/length_doushi*100, 2),
          '% ', count_doushi, '/', length_doushi)

    print('C')
    print('応答数：', num_c)
    count, data = statistics_count(katari, outou_c)
    count_meishi, data_meishi = statistics_info(katari, outou_c, '名詞')
    count_doushi, data_doushi = statistics_info(katari, outou_c, '動詞')
    print('文節での応答数：', count)
    labelConversion(data, outou_label_c, count)
    print('名詞を含む文節での応答数：', count_meishi)
    labelConversion(data_meishi, outou_label_c, count_meishi)
    print('動詞を含む文節での応答数：', count_doushi)
    labelConversion(data_doushi, outou_label_c, count_doushi)
    print('全応答に対する割合：', round(count/num_a*100, 2), '% ', count, '/', num_a)
    print('全文節に対する割合：', round(count/num*100, 2), '% ', count, '/', num)
    print('名詞を含む文節に関する割合', round(count_meishi/length_meishi*100, 2),
          '% ', count_meishi, '/', length_meishi)
    print('動詞を含む文節に関する割合', round(count_doushi/length_doushi*100, 2),
          '% ', count_doushi, '/', length_doushi)

