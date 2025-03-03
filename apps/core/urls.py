from django.urls import path
from apps.core.views import PostagensRelevantesListView, PostagensRecentesListView, TopicosListView, \
    TopicoPostagensListView, PostagemDetailView, PostagemCreateView

urlpatterns = [
    path('', PostagensRelevantesListView.as_view(), name='postagens_relevantes_list'),
    path('postagens/recentes/', PostagensRecentesListView.as_view(), name='postagens_recentes_list'),
    path('postagens/nova/', PostagemCreateView.as_view(), name='postagem_create'),
    path('postagens/<int:pk>/', PostagemDetailView.as_view(), name='postagem_detail'),
    path('topicos/', TopicosListView.as_view(), name='topicos_list'),
    path('topicos/<int:pk>/postagens/', TopicoPostagensListView.as_view(), name='topico_postagens_list'),
]