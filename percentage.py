def disagreementPercentage():
    targetPath = 'disagreementPercentage.txt'
    comparePath = 'disagreementResult.txt'
    basePath = 'katariCount.txt'
    compaerList = []
    baseList = []

    with open(targetPath, mode='w') as f:
        f.write('')
    with open(comparePath) as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip('\n')  # 改行の削除
        line = line.split(':')
        morpheme = [line[0], int(line[1])]
        compaerList.append(morpheme)

    with open(basePath) as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip('\n')  # 改行の削除
        line = line.split(':')
        morpheme = [line[0], int(line[1])]
        baseList.append(morpheme)

    # 計算
    for base in baseList:
        result = list(filter(lambda x: base[0] == x[0], compaerList))

        if len(result) != 0:
            percentage = int(round(result[0][1]/base[1], 2) * 100)
            with open(targetPath, mode='a') as f:
                f.write(result[0][0] + ':' + str(percentage) + '\n')


if __name__ == '__main__':
    disagreementPercentage()
