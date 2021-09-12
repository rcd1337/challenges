from django.db import models

# Create your models here.
class Aluno(models.Model):
    nome = models.CharField(max_length=255)
    aprovado = models.BooleanField(default=False)

class Prova(models.Model):
    aluno_fk = models.ForeignKey(Aluno, on_delete=models.PROTECT, blank=True, null=True)
    nota = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nome_prova = models.CharField(max_length=255, blank=True)

class Gabarito(models.Model):
    prova_fk = models.ForeignKey(Prova, on_delete=models.CASCADE)
    pergunta = models.TextField()
    resposta = models.TextField()

class Respostas(models.Model):
    prova_fk = models.ForeignKey(Prova, on_delete=models.CASCADE)
    pergunta = models.TextField()
    resposta = models.TextField()


