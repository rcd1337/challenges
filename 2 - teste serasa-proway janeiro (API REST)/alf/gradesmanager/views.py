import json
from django.shortcuts import render
from django.http import JsonResponse

from .models import Aluno, Gabarito, Prova, Respostas
from .util import atualizar_nota

def gabarito(request):

    if request.method != "POST":
        return JsonResponse({"error":"POST request required."}, status=400)
    
    if request.body == b'' or request.body is None:
        return JsonResponse({"error":"No JSON body"}, status=400)

    payload = json.loads(request.body)
    prova = Prova(nome_prova=payload['prova'])
    try:
        prova.save()
    except Exception:
        return JsonResponse({"error": "Failed to add new entry"}, status=400)

    for row in payload['data']:
        pergunta = list(row.keys())[0]
        resposta = list(row.values())[0]
        entry = Gabarito(prova_fk=prova, pergunta=pergunta, resposta=resposta)
        try:
            entry.save()
        except Exception:
            return JsonResponse({"error": "Failed to add new entry"}, status=400)

    return JsonResponse({"id": entry.id}, status=201)


def aluno(request):

    if request.method != "POST":
        return JsonResponse({"error":"POST request required."}, status=400)
    
    if request.body == b'' or request is None:
        return JsonResponse({"error":"No JSON body"}, status=400)

    limit = Aluno.objects.all()
    if len(limit) > 100:
        return JsonResponse({"error":"Limit of 100 students reached"}, status=400)

    payload = json.loads(request.body)
    #@TODO retornar erro caso atributo "name" estiver vazio
    entry = Aluno(nome=payload['name'])
    try:
        entry.save()
    except Exception:
        return JsonResponse({"error": "Failed to add new entry"}, status=400)
    return JsonResponse({"id": entry.id}, status=201)


def resposta(request):
    
    if request.method != "POST":
        return JsonResponse({"error":"POST request required."}, status=400)
    
    if request.body == b'' or request.body is None:
        return JsonResponse({"error":"No JSON body"}, status=400)

    payload = json.loads(request.body)

    try:
        aluno = Aluno.objects.get(id=payload['aluno_id'])
    except Exception:
        return JsonResponse({"error": "'Aluno' not found"}, status=400)
    
    try:
        prova = Prova.objects.get(id=payload['prova_id'])
    except Exception:
        return JsonResponse({"error": "'Prova' not found"}, status=400)

    prova.aluno_fk = aluno
    prova.save()
    for row in payload['data']:
        pergunta = list(row.keys())[0]
        resposta = list(row.values())[0]
        entry = Respostas(prova_fk=prova, pergunta=pergunta, resposta=resposta)
        try:
            entry.save()
        except Exception:
            return JsonResponse({"error": "Failed to add new entry"}, status=400)

    atualizar_nota(prova)

    return JsonResponse({"id": entry.id}, status=201)

def aprovados(request):
    
    if request.method == "GET":

        alunos = Aluno.objects.all()
        for aluno in alunos:
            prova = Prova.objects.filter(aluno_fk=aluno.id)
            quantidade = len(prova)
            somatorio = 0
            nota_final = 0
            
            for row in range(quantidade):
                somatorio = somatorio + prova[row].nota
            if somatorio > 0 or quantidade > 0:
                nota_final = somatorio / quantidade
            if nota_final > 7:
                aluno.aprovado = True
            else:
                aluno.aprovado = False
            aluno.save()

        aprovados = Aluno.objects.filter(aprovado=True)
        lista_aprovados = []
        for row in range(len(aprovados)):
            lista_aprovados.append(aprovados[row].nome)
        
        aprovados = json.dumps(lista_aprovados)

    return JsonResponse({"aprovados":f"{lista_aprovados}"})
