from django.urls import path
from apps.core.views import PostagensRelevantesListView, PostagensRecentesListView, \
    TopicosListView, TopicoPostagensListView, PostagemDetailView, PostagemCreateView, \
    PostagemUpdateView, editar_comentario, responder_postagem, responder_comentario, voto_postagem, voto_comentario

urlpatterns = [
    path('', PostagensRelevantesListView.as_view(), name='postagens_relevantes_list'),
    path('postagens/recentes/', PostagensRecentesListView.as_view(), name='postagens_recentes_list'),
    path('postagens/nova/', PostagemCreateView.as_view(), name='postagem_create'),
    path('postagens/<int:pk>/editar/', PostagemUpdateView.as_view(), name='postagem_update'),
    path('postagens/<int:pk>/', PostagemDetailView.as_view(), name='postagem_detail'),
    path('postagens/<int:pk>/voto/<str:voto>', voto_postagem, name='voto_postagem'),
    path('postagens/<int:pk>/responder', responder_postagem, name='postagem_responder'),
    path('postagens/<int:pk>/comentarios/<int:comentario_id>/voto/<str:voto>', voto_comentario, name='voto_comentario'),
    path('postagens/<int:pk>/comentarios/<int:comentario_id>/responder', responder_comentario, name='postagem_comentario_responder'),
    path('postagens/<int:pk>/comentarios/<int:comentario_id>/editar/', editar_comentario, name='comentario_update'),
    path('topicos/', TopicosListView.as_view(), name='topicos_list'),
    path('topicos/<int:pk>/postagens/', TopicoPostagensListView.as_view(), name='topico_postagens_list'),
]