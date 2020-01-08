import glob
import copy
import pprint
from functools import reduce

fileArray = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'
]
fileArray = ['01']
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
                continue
            elif data[0] == "silB" or data[0] == "silE":
                tmp_str = ""
                continue
            elif data[0] == "sp" or data[0] == "pause":
                continue
            elif data[0] == "(" or data[0] == ")" or data[0] == "?":
                continue
            elif data[0] == 'G' or data[0] == "D" or data[0] == "F" or data[0] == "U":
                continue
            elif data[1] == "補助記号":
                continue

            if 'label' in data[num]:
                word = data[0]  # 応答文字の取得
                word = tmp_str+word
                label = data[num].lstrip('label=')  # labelの取得
                begin = float(data[num-2])  # 開始時刻の取得
                # print(word, label, begin)

                self.outou.append({begin: word})
                self.outou_label.append({begin: label})
                tmp_str = ""
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
                self.katari = []

        return self.katari_compare

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
                        begin = last_time[0]

                time = [begin, end]
            else:
                word = data[0]
                hinshi = data[1]
                detail = hinshi + data[2]
                if hinshi == '名詞':
                    detail += data[3] + data[4]
                elif hinshi == '動詞':
                    detail += data[6]
                begin = float(data[num-1])
                end = float(data[num])
                time = [begin, end]

            if self.flag:
                if 'pause' in word:  # pause時の時間情報を保持するため必要
                    tmpBegin = time[0]
                    flag = time[1]
                    self.katari.append({'word': word, 'time': time})
                else:
                    if flag != time[0]:  # そのまま更新
                        self.katari.append(
                            {'word': word, 'time': time, 'hinshi': [hinshi], 'detail': [detail], 'flag': self.flag})
                    else:   # 時間を編集して更新
                        newTime = [tmpBegin, time[1]]
                        self.katari.pop(-1)
                        self.katari.append(
                            {'word': word, 'time': newTime, 'hinshi': [hinshi], 'detail': [detail], 'flag': self.flag})
                    self.flag = False
            else:
                if 'pause' not in hinshi:
                    self.katari.append({'word': word, 'time': newTime,
                                        'hinshi': [hinshi], 'detail': [detail], 'flag': self.flag})
        file.close()


def statistics_group(katari_data, outou_info):   # 品詞を含む
    katari_value = copy.deepcopy(katari_data)
    katari_info = {}
    for index in list(katari_value):    # 文節のみを抽出
        katari_info[index] = []
        for data in katari_value[index]:
            flag = data['flag']
            if flag:
                katari_info[index].append(data)
            else:
                hinshi = data['hinshi'][0]
                detail = data['detail'][0]
                katari_info[index][-1]['hinshi'].append(hinshi)
                katari_info[index][-1]['detail'].append(detail)

    count = 0
    data_detail = {}
    for index in list(katari_info):
        data_detail[index] = []
        for katari in katari_info[index]:
            katari_time = katari['time']
            start = katari_time[0]
            end = katari_time[1]
            popIndex = katari_info[index].index(katari) - 1
            # 応答文字列の取得
            for outou in outou_info[index]:
                outou_time = list(outou.keys())[0]
                if start <= outou_time and outou_time < end:
                    # num = katari_info[index].index(katari)
                    # num2 = outou_info[index].index(outou)
                    # 応答があった一つ前の文節が対象
                    # print(katari_info[index][popIndex], outou_info[index][num2])
                    label = katari_info[index][popIndex]['hinshi']
                    value = {'group': label}
                    value.update({'outou': outou})
                    data_detail[index].append(value)
                    count += 1

    # print('CH', count)
    return data_detail


def labelGroupConversion(targetData, outouLabelData, fileName):
    labelList = []
    allLabelList = []
    for index in list(targetData):  # ラベルリストの生成
        for data in targetData[index]:
            labelList.append(data['group'])
            allLabelList.append(
                {'group': data['group'], 'labelList': [], 'keyLabelList': []})

    for index in list(outouLabelData.keys()):   # countのためにlabelList,keyLabelListを取得
        for data in targetData[index]:
            group = data['group']   # keyとなる品詞グループ
            time = list(data['outou'].keys())[0]    # 応答側のkeyとなる時間
            value = list(filter(lambda x: time == list(
                x.keys())[0], outouLabelData[index]))[0]
            label = list(value.values())[0]  # 応答ラベル
            target = list(filter(lambda x: group == x['group'], allLabelList))[
                0]   # 変更先を取得
            num = allLabelList.index(target)    # insert時に使用するindexを取得
            target['labelList'].append(label)   # labelListを更新
            if label not in target['keyLabelList']:  # keyLabelを更新
                target['keyLabelList'].append(label)
            del allLabelList[num]
            allLabelList.insert(num, target)

    result = list(filter(lambda x: len(x['labelList']) != 0, allLabelList))

    for data in result:  # groupごとのサイズを取得
        length = len(data['labelList'])
        data.update({'size': length})
    value = sorted(result, key=lambda x: -x['size'])    # sizeでsort

    for data in value:  # 数をカウントして並べなおす
        tmp = {}
        count = {'labelCount': [], 'parce': []}
        labelList = data['labelList']
        group = data['group']   # keyとなるgroup
        size = data['size']    # groupのlength

        for label in data['keyLabelList']:
            tmp.update({label: labelList.count(label)})

        for k, v in sorted(tmp.items(), key=lambda x: -x[1]):
            count['labelCount'].append({k: v})
            count['parce'].append({k: round(v/size*100, 2)})

        del data['labelList']   # データ整形
        del data['keyLabelList']
        data.update(count)

    filePath = 'segmentSize' + fileName + '.txt'
    with open(filePath, mode='w') as f:
        f.write('')

    for data in value:
        for k, v in data.items():
            if k == 'group':
                with open(filePath, mode='a') as f:
                    f.write('文節の組み合わせ| ' + ','.join(v) + '\n')
            elif k == 'labelCount':
                with open(filePath, mode='a') as f:
                    labelListData = list(map(lambda x: list(x.keys())[0], v))
                    f.write('応答ラベルリスト| ' + ','.join(labelListData) + '\n')
                    f.write('応答ラベルの内訳| ' + str(v) + '\n')
            elif k == 'parce':
                with open(filePath, mode='a') as f:
                    f.write('ラベルパーセント| ' + str(v) + '\n')

        with open(filePath, mode='a') as f:
            f.write('\n')
    # pprint.pprint(result, width=80, compact=True)


def writeConversationData(targetData, katariData, outouData, outouLabelData):
    count = 0
    result = []
    for index in list(katariData):
        content = ''
        segmentlabelList = []
        for katari in katariData[index]:
            flag = katari['flag']
            word = katari['word']
            hinshi = katari['hinshi'][0]
            # 文節ごとの語り文字列と対応する応答文字列の取得
            if flag:
                start = katari['time'][0]
                end = katari['time'][1]
                for outou in outouData[index]:
                    outouTime = list(outou.keys())[0]
                    outouText = list(outou.values())[0]
                    if start <= outouTime and outouTime < end:
                        count += 1
                        label = list(filter(lambda x: list(x.keys())[0]
                                            == outouTime, outouLabelData[index]))[0]
                        outouLabel = list(label.values())[0]
                        data = {'content': content}
                        data.update({'clauseTime': [start, end]})
                        data.update({'group': segmentlabelList})
                        data.update({'outou': outou})
                        data.update({'outouLabel': outouLabel})
                        # print(data)
                        result.append(data)
                content = word
                segmentlabelList = [hinshi]
            else:
                content += word  # 文節の語り文字列の更新
                segmentlabelList.append(hinshi)

    # print('CH', count)
    return result


def segmentContent(conversationData, path):
    segmentLabelList = []
    labelListData = []
    filePath = 'segmentSize' + path + '.txt'
    writePath = 'sentenceContent' + path + '.txt'
    with open(writePath, mode='w') as f:
        f.write('')
    file = open(filePath)
    lines = file.readlines()

    for data in lines:
        data = data.rstrip('\n')
        data = data.split('| ')
        if data[0] == '文節の組み合わせ':
            segmentLabelList.append(data[1].split(','))
        elif data[0] == '応答ラベルリスト':
            labelListData.append(data[1].split(','))
        else:
            continue

    for group, labelList in zip(segmentLabelList, labelListData):
        with open(writePath, mode='a') as f:
            f.write('文節の品詞の組み合わせ: ' + str(group) + '\n')
        value = list(filter(lambda x: x['group'] == group, conversationData))
        for label in labelList:
            content = list(filter(lambda x: label == x['outouLabel'], value))
            with open(writePath, mode='a') as f:
                f.write('応答のラベル: ' + str(label) + '\n')
            for data in content:
                with open(writePath, mode='a') as f:
                    f.write('文節: ' + str(data['content']) + '\n')
                    f.write('応答: ' + str(data['outou']) + '\n')
            with open(writePath, mode='a') as f:
                f.write('\n')
        with open(writePath, mode='a') as f:
            f.write('\n')
    print('fileWrite at ' + writePath)


def comparison(a, b, c):
    valueA = []  # [{文節の開始時間:文節の内容}]
    valueB = []
    valueC = []
    for data in a:
        valueA.append((data['clauseTime'][0], data['content']))
    for data in b:
        valueB.append((data['clauseTime'][0], data['content']))
    for data in c:
        valueC.append((data['clauseTime'][0], data['content']))
    # print(valueA)
    # print(valueB)
    # print(valueC)

    # 対称差集合により一度しか出現しない要素を取得(不完全)
    compositeContent = list(set(valueA) ^ set(valueB) ^ set(valueC))
    # ３人ともに含まれる物を削除
    aloneContent = []   # 一度しか出現しないリスト
    for data in compositeContent:
        if not (data in valueA and data in valueB and data in valueC):
            aloneContent.append(data)

    # 複数人が応答している文節応答を抜き出す(重複してる要素も削除)
    allValue = valueA + valueB + valueC
    moreResponse = list(set(allValue) ^ set(aloneContent))  # 複数人の応答
    moreConflictConversation = {}
    moreConversation = {}

    for key in moreResponse:
        moreConflictConversation[key] = []
        moreConversation[key] = []
        if key in valueA:
            content = list(filter(
                lambda x: x['clauseTime'][0] == key[0] and x['content'] == key[1], a))
            for value in content:
                if value['outouLabel'] == 'あいづち':
                    text = 'A ' + str(value['outou'])
                    moreConflictConversation[key].append(text)
                else:
                    text = text = 'A ' + \
                        str(value['outou']) + ' ' + value['outouLabel']
                    moreConversation[key].append(text)
        if key in valueB:
            content = list(filter(
                lambda x: x['clauseTime'][0] == key[0] and x['content'] == key[1], b))
            for value in content:
                if value['outouLabel'] == 'あいづち':
                    text = 'B ' + str(value['outou'])
                    moreConflictConversation[key].append(text)
                else:
                    text = text = 'B ' + \
                        str(value['outou']) + ' ' + value['outouLabel']
                    moreConversation[key].append(text)
        if key in valueC:
            content = list(filter(
                lambda x: x['clauseTime'][0] == key[0] and x['content'] == key[1], c))
            for value in content:
                if value['outouLabel'] == 'あいづち':
                    text = 'C ' + str(value['outou'])
                    moreConflictConversation[key].append(text)
                else:
                    text = text = 'C ' + \
                        str(value['outou']) + ' ' + value['outouLabel']
                    moreConversation[key].append(text)

        if len(moreConversation[key]) == 0:
            moreConversation.pop(key)
        if len(moreConflictConversation[key]) == 0:
            moreConflictConversation.pop(key)

    # 一人しか応答していない文節応答を抜き出す
    aloneConversation = {}
    aloneConflictConversation = {}
    for key in aloneContent:
        aloneConversation[key] = []
        aloneConflictConversation[key] = []
        if key in valueA:
            content = list(filter(
                lambda x: x['clauseTime'][0] == key[0] and x['content'] == key[1], a))
            for value in content:
                # a.remove(value) # 二人以上の応答に更新
                if value['outouLabel'] == 'あいづち':
                    text = 'A ' + value['content'] + ' ' + str(value['outou'])
                    aloneConflictConversation[key].append(text)
                else:
                    text = 'A ' + value['content'] + ' ' + \
                        str(value['outou']) + ' ' + value['outouLabel']
                    aloneConversation[key].append(text)

        if key in valueB:
            content = list(filter(
                lambda x: x['clauseTime'][0] == key[0] and x['content'] == key[1], b))
            for value in content:
                # b.remove(value)
                if value['outouLabel'] == 'あいづち':
                    text = 'B ' + value['content'] + ' ' + str(value['outou'])
                    aloneConflictConversation[key].append(text)
                else:
                    text = 'B ' + value['content'] + ' ' + \
                        str(value['outou']) + ' ' + value['outouLabel']
                    aloneConversation[key].append(text)

        if key in valueC:
            content = list(filter(
                lambda x: x['clauseTime'][0] == key[0] and x['content'] == key[1], c))
            for value in content:
                # c.remove(value)
                if value['outouLabel'] == 'あいづち':
                    text = 'C ' + value['content'] + ' ' + str(value['outou'])
                    aloneConflictConversation[key].append(text)
                else:
                    text = 'C ' + value['content'] + ' ' + \
                        str(value['outou']) + ' ' + value['outouLabel']
                    aloneConversation[key].append(text)

        if len(aloneConversation[key]) == 0:
            aloneConversation.pop(key)
        if len(aloneConflictConversation[key]) == 0:
            aloneConflictConversation.pop(key)

    # ファイルの初期化
    with open('aloneConflict.txt', mode='w') as f:
        f.write('')
    with open('aloneConversation.txt', mode='w') as f:
        f.write('')
    with open('moreConflictResponse.txt', mode='w') as f:
        f.write('')
    with open('moreResponse.txt', mode='a') as f:
        f.write('')

    # ファイルに書き込む
    for key, data in aloneConflictConversation.items():
        with open('aloneConflict.txt', mode='a') as f:
            f.write(str(key) + '\n' + str(data) + '\n')
    print('fileWrite at aloneConflict.txt : ３人のうち一人だけしかしていない文節応答（あいづちのみ）')
    for key, data in aloneConversation.items():
        with open('aloneConversation.txt', mode='a') as f:
            f.write(str(key) + '\n' + str(data) + '\n')
    print('fileWrite at aloneConversation.txt : ３人のうち一人だけしかしていない文節応答（あいづち以外）')
    for key, data in moreConversation.items():
        with open('moreResponse.txt', mode='a') as f:
            f.write(str(key) + '\n')
        for value in data:
            with open('moreResponse.txt', mode='a') as f:
                f.write(str(value) + '\n')


if __name__ == '__main__':
    kt = Segment()
    katari = kt.read_data()

    ot = Outou('a')
    outou_a, outou_label_a = ot.read_data()
    ot = Outou('b')
    outou_b, outou_label_b = ot.read_data()
    ot = Outou('c')
    outou_c, outou_label_c = ot.read_data()

    group_data = statistics_group(katari, outou_a)
    labelGroupConversion(group_data, outou_label_a, 'A')
    print('fileWrite at segmentSizeA.txt : 文節の組み合わせと応答の関係')
    conversationDataA = writeConversationData(
        group_data, katari, outou_a, outou_label_a)
    # segmentContent(conversationDataA, 'A')

    group_data = statistics_group(katari, outou_b)
    labelGroupConversion(group_data, outou_label_b, 'B')
    print('fileWrite at segmentSizeB.txt : 文節の組み合わせと応答の関係')
    conversationDataB = writeConversationData(
        group_data, katari, outou_b, outou_label_b)
    # segmentContent(conversationDataB, 'B')

    group_data = statistics_group(katari, outou_c)
    labelGroupConversion(group_data, outou_label_c, 'C')
    print('fileWrite at segmentSizeC.txt : 文節の組み合わせと応答の関係')
    conversationDataC = writeConversationData(
        group_data, katari, outou_c, outou_label_c)
    # segmentContent(conversationDataC, 'C')

    comparison(conversationDataA, conversationDataB, conversationDataC)
