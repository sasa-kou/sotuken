import glob
from toukei import Response

path = 'pauseResult.txt'
with open(path, mode='w') as f:
    f.write('')

fileArray = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
    '20', '21', '22', '23', '24'
]
testData_num = ['1', '2', '3', '4', '5', '6', '7']


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
                file_number = file_index + '-' + index
                self.pauseCompare.update({file_number: self.pause})
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
                start = self.pause[len(self.pause) - 1][0]
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
                    if self.pause[len(self.pause) - 1][1] == start:
                        start = self.pause[len(self.pause) - 1][0]  # 開始時間を取得
                        self.pause.pop(-1)  # 最後の要素を削除
                time = [start, end]
                self.pause.append(time)

        if not self.marge:  # Falseの時、次からはマージする
            self.marge = True

        file.close()

    def count(self):
        count = 0
        orver = 0
        for index in list(self.pauseCompare.keys()):
            count = count + len(self.pauseCompare[index])
            for data in self.pauseCompare[index]:
                if round(data[1] - data[0], 2) >= 0.2:
                    orver += 1
        return count, orver


def trance_data(pause, outou):
    interval = 0  # すべての間での応答数
    overThreshold = []  # 間の長さが200ms以上なら1
    intervalData = {}
    overThresholdData = {}
    for index in list(pause.keys()):
        intervalData[index] = []
        overThresholdData[index] = []
        for time in pause[index]:
            start = float(time[0])
            end = float(time[1])
            for data in outou[index]:
                time = list(data.keys())[0]
                if start < time and time < end:
                    interval += 1
                    intervalData[index].append(data)
                    if round(end - start, 2) >= 0.2:
                        overThreshold.append(1)
                        overThresholdData[index].append(data)
                    else:
                        overThreshold.append(0)

    return interval, overThreshold, intervalData, overThresholdData


def readLabelData(file_name):  # 現状使う予定なし
    path = 'toukeiLabel' + file_name + '.txt'
    with open(path, mode='r') as f:
        data = f.read()
    data = data.split('\n')[:-1]
    return data


def labelConversion(intervalData, outouLabelData, size):
    labelList = []  # 出現するラベルをすべて保存
    keyLabel = []  # ラベルの種類を保存
    tmp = {}
    result = []
    parce = []
    for index in list(outouLabelData.keys()):
        for data in intervalData[index]:
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
        parce.append({k: round(v / size * 100, 2)})
    print(result)
    print(parce)


if __name__ == '__main__':
    ps = Pause()
    pause = ps.read_data()
    pause_num, pause_orver = ps.count()
    print('間の数', pause_num)
    print('200ms以上の間', pause_orver)

    print('A')
    ot = Response('a')
    outou_a, outou_a_label = ot.read_data()
    num = ot.count()
    print('応答数：', num)
    interval, overThreshold, intervalData, overThresholdData = trance_data(
        pause, outou_a)
    print('間での応答数：', interval)
    print('そのうち200ms以上の語りの間での応答数：', overThreshold.count(1))
    labelConversion(overThresholdData, outou_a_label, overThreshold.count(1))
    print('200ms以上の語りの間における応答割合：', round(
        overThreshold.count(1) / pause_orver * 100, 2), overThreshold.count(1), '/', pause_orver)
    print('全応答のうち200ms以上の間での応答割合：', round(overThreshold.count(
        1) / num * 100, 2), overThreshold.count(1), '/', num)

    print('B')
    ot = Response('b')
    outou_b, outou_b_label = ot.read_data()
    num = ot.count()
    print('応答数：', num)
    interval, overThreshold, intervalData, overThresholdData = trance_data(
        pause, outou_b)
    print('間での応答数：', interval)
    print('そのうち200ms以上の語りの間での応答数：', overThreshold.count(1))
    labelConversion(overThresholdData, outou_b_label, overThreshold.count(1))
    print('200ms以上の語りの間における応答割合：', round(
        overThreshold.count(1) / pause_orver * 100, 2), overThreshold.count(1), '/', pause_orver)
    print('全応答のうち200ms以上の間での応答割合：', round(overThreshold.count(
        1) / num * 100, 2), overThreshold.count(1), '/', num)

    print('C')
    ot = Response('c')
    outou_c, outou_c_label = ot.read_data()
    num = ot.count()
    print('応答数：', num)
    interval, overThreshold, intervalData, overThresholdData = trance_data(
        pause, outou_c)
    print('間での応答数：', interval)
    print('そのうち200ms以上の語りの間での応答数：', overThreshold.count(1))
    labelConversion(overThresholdData, outou_c_label, overThreshold.count(1))
    print('200ms以上の語りの間における応答割合：', round(
        overThreshold.count(1) / pause_orver * 100, 2), overThreshold.count(1), '/', pause_orver)
    print('全応答のうち200ms以上の間での応答割合：', round(overThreshold.count(
        1) / num * 100, 2), overThreshold.count(1), '/', num)
