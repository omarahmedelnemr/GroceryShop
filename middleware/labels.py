
def addLabels(data,legends, nasted):
    singleDict = {}
    result = []
    if nasted:
        for i in data:
                for x  in range(len(i)):
                    singleDict[legends[x][0]] = i[x]
                result.append(singleDict)
                singleDict = {}
        return result
    else:
        for x  in range(len(data)):
            singleDict[legends[x][0]] = data[x]
        return singleDict
