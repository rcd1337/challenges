from .dict import exceptionDict, hundredsDict, tensDict, unitsDict


def isValid(number):    
    try:
        number = int(number)
    except ValueError:
        return False

    if number < -99999 or number > 99999:
        return False

    return True


def isException(number):
    if number == 100 or number == 0 or 10 <= number <= 19:
        return True

    return False


def exception(number):
    if number == 0:
        return 'zero'

    return exceptionDict[number]


def getUnidade(word, value):
    units = unitsDict[int(value)]
    if units:
        word = units

    return word


def getDezena(word, value):
    if isException(int(value)):
        return exception(int(value))

    value = value[0]
    tens = tensDict[int(value)]
    if tens:
        if word:
            word = f'{tens} e {word}'
        else:
            word = tens

    return word


def getCentena(word, value):
    hundreds = hundredsDict[int(value)]
    if hundreds:
        if word:
            word = f'{hundreds} e {word}'
        else:
            word = hundreds

    return word


def getMilhar(word, value):

    if isException(int(value)):
        if word:
            word = f'{exception(int(value))} mil e {word}'
        else:
            word = f'{exception(int(value))} mil'
        return word

    digits = len(value)
    units = ''
    tens = ''
    for i in range(digits):
        if i == 0:
            units = getUnidade('', value[digits - i - 1])
        if i == 1:
            tens = getDezena('', value)
    
    if not units:
        return f'{tens} mil e {word}'

    if not tens:
        if units == 'um':
            return f'mil e {word}'
            
        return f'{units} mil e {word}'

    return f'{tens} e {units} mil e {word}'


def numToWord(strNum):
    digits = len(strNum)
    word = ''

    for i in range(digits):
        if i == 0:
            word = getUnidade(word, strNum[(digits - i - 1)])
        if i == 1:
            word = getDezena(word, strNum[(digits - i - 1):])
        if i == 2:
            word = getCentena(word, strNum[(digits - i - 1)])
        if i == 3:
            word = getMilhar(word, strNum[:(digits - i)])

    return word