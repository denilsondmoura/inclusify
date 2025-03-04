from django.conf import settings
from django.db import models
from .mixins import AuditMixin
        
class Topico(AuditMixin):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


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


class Comentario(AuditMixin):
    conteudo = models.TextField()
    postagem = models.ForeignKey(
        Postagem,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name="respostas",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Comentário de {self.created_by} em {self.postagem}"


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