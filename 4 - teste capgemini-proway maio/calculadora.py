# Número de visualizações geradas para cada real investido
views_per_Real = 30

# Número máximo de compartilhamentos por anúncio
max_shares = 4

# Número de visualizações geradas por cada novo compartilhamento
views_per_share = ((12 / 100) * (3 / 20) * 40)


def investment():
    amount = input("Investimento: R$ ")

    try:
        amount = float(amount)
    except ValueError:
        print("O valor investido deve ser um valor numérico.\n")
        return investment()

    if amount <= 0:
        print("O valor investido deve ser maior que zero.\n")
        return investment()

    return amount


def projection():
    invested = investment()
    initial_views = invested * views_per_Real
    additional_views = 0

    for i in range(max_shares):
        additional_views = additional_views + (initial_views * (views_per_share**(i + 1)))

    return round(initial_views + additional_views, 2)


print("""
INFORME O VALOR QUE DESEJA INVESTIR PARA QUE A PROJEÇÃO SEJA GERADA.

PARA SAIR, PRESSIONE "Ctrl+C".
""")

while True:
    try:
        print(f'Projeção: {projection()} visualizações.\n')
    except KeyboardInterrupt:
        exit()