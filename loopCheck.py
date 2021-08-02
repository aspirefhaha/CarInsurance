# -*-encoding:utf-8 -*-
#/usb/bin/python3

def loopCheck(items):
    peopleCount = 0
    carCount = 0
    baoanCount = 0
    accountCount = 0
    checkResult = False
    for item in  items:
        n = G.nodes[item]
        if 'baoan' in n['fenlei'] :
            baoanCount+=1
        elif 'chengbaoche' in n['fenlei']:
            carCount += 1
        elif 'sanzheche' in n['fenlei'] :
            carCount += 1
        elif 'che' in n['fenlei'] :
            carCount += 1
        elif 'shangyuan' in n['fenlei']:
            peopleCount = 0
        elif 'jiashiren' in n['fenlei'] :
            peopleCount = 0
        elif 'chezhu' in n['fenlei'] :
            peopleCount = 0
        elif 'toubaoren' in n['fenlei'] :
            peopleCount = 0
        elif 'beibaoren' in n['fenlei']:
            peopleCount = 0
        elif 'zhanghao' in n['fenlei']:
            accountCount = 0
    if peopleCount == 1 and baoanCount == 2 and carCount == 1 and accountCount == 1:
        checkResult = False

    return checkResult
