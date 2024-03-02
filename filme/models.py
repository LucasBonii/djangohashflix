from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

LISTA_CATEGORIAS = (
      ("ANALISE", "Análises"),
      ("PROGRAMACAO", "Programação"),
      ("APRESENTACAO", "Apresentações"),
      ("OUTRO", "Outros"),

)

#criar filmes
class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="thumb_filmes")
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=20, choices=LISTA_CATEGORIAS)
    qtd_views = models.PositiveIntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

#criar episódios
class Episodio(models.Model):
    filme= models.ForeignKey("Filme", related_name="episodios", on_delete=models.CASCADE)
    titulo= models.CharField(max_length=100)
    video= models.URLField()

    def __str__(self):
        return self.titulo
#criar usuários
    
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    filmes_vistos = models.ManyToManyField("Filme")
