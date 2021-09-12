dolar = 1.00
fee = 0.1

# 23 de maio, 07:30 GMT-3
currency = {
    "AUD": {'value': 1.29, 'name': "Dólar australiano"},
    "BRL": {'value': 5.37, 'name': "Real brasileiro"},
    "CAD": {'value': 1.21, 'name': "Dólar canadense"},
    "CHF": {'value': 0.90, 'name': "Franco suíço"},
    "CNY": {'value': 6.43, 'name': "Yuan chinês"},
    "EUR": {'value': 0.82, 'name': "Euro"},
    "GBP": {'value': 0.71, 'name': "Libra esterlina"},
    "HKD": {'value': 7.76, 'name': "Dólar de Hong Kong"},
    "JPY": {'value': 108.93, 'name': "Iene japonês"},
    "NZD": {'value': 1.39, 'name': "Dólar da Nova Zelândia"},
    "USD": {'value': dolar, 'name': "Dólar dos Estados Unidos"},
}

currencyCodes = ', '.join(currency)


def getSource():
    source = input(f"Moedas disponíveis: {currencyCodes}\nMoeda origem: ")

    if not source.upper() in currency:
        return getSource()

    return source.upper()


def getOutcome():
    outcome = input("Moeda destino: ")

    if not outcome.upper() in currency:
        print(f"Moedas disponíveis: {currencyCodes}")
        return getOutcome()

    return outcome.upper()


def getAmount():
    amount = input("Valor a ser convertido: ")

    try:
        amount = float(amount)
    except ValueError:
        print("Valor inválido, tente novamente.")
        return getAmount()

    return amount


def convertCurrency(source, outcome, amount):
    sourceIndex = currency[source]['value']
    outcomeIndex = currency[outcome]['value']

    result = (outcomeIndex / sourceIndex) * amount

    return result


def calc():
    source = getSource()
    outcome = getOutcome()
    amount = getAmount()
    discount = 1 - fee

    converted_currency = convertCurrency(source, outcome, amount)

    return f"""
Conversão: {round(converted_currency, 2)} {outcome}
Taxa: {round(converted_currency * fee, 2)} {outcome}
Total: {round(converted_currency * discount, 2)} {outcome}"""


print(calc())


input()