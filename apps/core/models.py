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

    @property
    def postagem_origem(self):
        """
        Retorna a postagem raiz mesmo para comentários aninhados,
        percorrendo a hierarquia de respostas até encontrar a postagem original
        """
        current = self
        
        # Percorre a cadeia de comentários pais até encontrar a postagem
        while current.parent_comment is not None:
            current = current.parent_comment
            
            # Segurança contra loops infinitos (caso raro de configuração errada)
            if current == self:  # Detecta loop circular
                raise ValueError("Loop infinito detectado na hierarquia de comentários")
                
        # Retorna a postagem do comentário ancestral mais alto
        if current.postagem:
            return current.postagem
            
        # Caso extremo onde não há postagem associada (deveria ser impossível pelo modelo)
        raise ValueError("Nenhuma postagem encontrada na hierarquia de comentários")
    


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