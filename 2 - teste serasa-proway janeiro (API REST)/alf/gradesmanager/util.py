from django.http import JsonResponse
from .models import Aluno, Gabarito, Prova, Respostas

def atualizar_nota(prova):
    gabarito = Gabarito.objects.filter(prova_fk_id='1')
    resposta = Gabarito.objects.filter(prova_fk_id='1')
    quantidade = len(gabarito)
    parcial = quantidade
    for row in range(quantidade):
        if not gabarito[row].resposta == resposta[row].resposta:
            parcial = parcial - 1
    nota = round(parcial * 10 / quantidade, 2)
    prova.nota = nota
    prova.save()