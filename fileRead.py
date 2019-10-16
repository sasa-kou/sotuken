import glob

file_num = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'
]
testData_num = ['1', '2', '3', '4', '5', '6', '7']


def read_OutouData(file_name):  # 全ファイルを検索して読み込み
    file_root = '../../outouwithlabel_camui/outouwithlabel_camui/'
    file_end = '/*.morph'

    for file_index in file_num:
        files = glob.glob(file_root + file_index + '/' + file_name + '/')
        for file in files:
            for index in testData_num:
                targetFile = glob.glob(file + index + file_end)
                targetFile.sort()
                print(targetFile)


def read_KatariData():
    file_root = '../../katari_info/'
    file_end = '/*.morph'

    for file_index in file_num:
        files = glob.glob(file_root + file_index + '/')
        for file in files:
            for index in testData_num:
                bigFiles = glob.glob(file + index + '/*')
                for bigFile in bigFiles:
                    targetFile = glob.glob(bigFile + file_end)
                    targetFile.sort()
                    print(targetFile)


if __name__ == '__main__':
    # read_OutouData('a')

    read_KatariData()
