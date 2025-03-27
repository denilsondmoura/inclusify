from django.conf import settings
from django.utils import timezone
from django.db import models
from .mixins import AuditMixin
import math
        
class Topico(AuditMixin):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=250)

    def __str__(self):
        return self.nome
    
    @property
    def post_count(self):
        return self.postagens.count()


class Postagem(AuditMixin):
    titulo = models.CharField(max_length=200)
    corpo = models.TextField()
    # Cada postagem pertence a um tópico
    topicos = models.ManyToManyField(
        Topico,
        related_name="postagens",
        blank=True
    )

    def __str__(self):
        return self.titulo
    
    @property
    def upvotes_count(self):
        return self.votos.filter(valor='+1').count()
    
    @property
    def downvotes_count(self):
        return self.votos.filter(valor='-1').count()
    
    @property
    def comentarios_count(self):
        count = self.comentarios.count()
        for comentario in self.comentarios.all():
            count += comentario.respostas.count()
            
        return count
    
    # def calcular_relevancia(post):
    #     upvotes = post.votos_positivos
    #     downvotes = post.votos_negativos
    #     comentarios = post.comentarios.count()
    #     horas_desde_criacao = (timezone.now() - post.data_criacao).total_seconds() / 3600
        
    #     # Fatores de ponderação (ajustáveis)
    #     peso_votos = 2.0
    #     peso_comentarios = 1.5
    #     gravidade = 1.8  # Controla o decaimento temporal
        
    #     # Cálculo dos componentes
    #     score_votos = (upvotes - downvotes) * peso_votos
    #     score_comentarios = comentarios * peso_comentarios
        
    #     # Fórmula final com decaimento temporal
    #     relevancia = (score_votos + score_comentarios) / ((horas_desde_criacao + 2) ** gravidade)
        
    #     return relevancia
    
    


class Comentario(AuditMixin):
    conteudo = models.TextField()
    postagem = models.ForeignKey(
        Postagem,
        on_delete=models.CASCADE,
        related_name="comentarios",
        null=True,
        blank=True
    )
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name="respostas",
        null=True,
        blank=True
    )

    def __str__(self):
        if self.parent_comment:
            return f"Resposta de {self.created_by} ao {self.parent_comment}"
        else: 
            return f"Comentário de {self.created_by} em {self.postagem}"
        
    @property
    def upvotes_count(self):
        return self.votos.filter(valor='+1').count()
    
    @property
    def downvotes_count(self):
        return self.votos.filter(valor='-1').count()
    
    @property
    def comentarios_count(self):
        count = self.respostas.count()
        return count
    


class VotoPostagem(AuditMixin):
    VOTE_CHOICES = (
        (1, '+1'),
        (-1, '-1'),
    )
    valor = models.SmallIntegerField(choices=VOTE_CHOICES)
    postagem = models.ForeignKey(
        Postagem,
        on_delete=models.CASCADE,
        related_name="votos"
    )

    class Meta:
        unique_together = ('created_by', 'postagem')

    def __str__(self):
        return f"Voto de {self.created_by} em {self.postagem} = {self.valor}"


class VotoComentario(AuditMixin):
    VOTE_CHOICES = (
        (1, '+1'),
        (-1, '-1'),
    )
    valor = models.SmallIntegerField(choices=VOTE_CHOICES)
    comentario = models.ForeignKey(
        Comentario,
        on_delete=models.CASCADE,
        related_name="votos"
    )

    class Meta:
        unique_together = ('created_by', 'comentario')

    def __str__(self):
        return f"Voto de {self.created_by} em {self.comentario} = {self.valor}"