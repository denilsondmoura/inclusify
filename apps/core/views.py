from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    FormView,
    ListView, CreateView, UpdateView,
    TemplateView, DetailView, DeleteView, 
)
from .models import Postagem, Topico

class PostagensRelevantesListView(ListView):

    template_name = 'postagens_relevantes_list.html'
    model = Postagem
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Relevantes'
        context['postagens'] = Postagem.objects.all()
        return context
    
class PostagensRecentesListView(ListView):

    template_name = 'postagens_recentes_list.html'
    model = Postagem
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('created_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recentes'
        return context
    
class PostagemCreateView(LoginRequiredMixin, CreateView):

    template_name = 'postagem_form.html'
    model = Postagem
    paginate_by = 10
    ordering = 'id',

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Criar Postagem'
        return context
    
class PostagemDetailView(DetailView):

    template_name = 'postagem_detail.html'
    model = Postagem
    paginate_by = 10
    ordering = 'id',

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalhes'
        return context
    
class TopicosListView(ListView):

    template_name = 'topicos_list.html'
    model = Topico
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tópicos'
        return context
    
class TopicoPostagensListView(ListView):

    template_name = 'topico_postagens_list.html'
    model = Postagem
    paginate_by = 10
    ordering = 'id',

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        topico = Topico.objects.get(pk=pk)
        # TODO: filtrar as postagens pelo topico
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        topico = Topico.objects.get(pk=pk)
        
        context['title'] = f'Postagens sobre {topico}'
        return context