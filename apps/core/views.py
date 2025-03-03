from django.shortcuts import render
from django.views.generic import (
    FormView,
    ListView, CreateView, UpdateView,
    TemplateView, DetailView, DeleteView,
)
from .models import Postagem

class PostagensRelevantesListView(TemplateView):

    template_name = 'postagens_relevantes_list.html'
    # model = Postagem
    paginate_by = 20
    ordering = 'identificacao', 'cadastrador',

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Relevantes'
        return context
    
class PostagensRecentesListView(TemplateView):

    template_name = 'postagens_recentes_list.html'
    # model = Postagem
    paginate_by = 20
    ordering = 'identificacao', 'cadastrador',

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recentes'
        return context
    
class PostagemCreateView(TemplateView):

    template_name = 'postagem_form.html'
    # model = Postagem
    paginate_by = 20
    ordering = 'identificacao', 'cadastrador',

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Criar Postagem'
        return context
    
class PostagemDetailView(TemplateView):

    template_name = 'postagem_detail.html'
    # model = Postagem
    paginate_by = 20
    ordering = 'identificacao', 'cadastrador',

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalhes'
        return context
    
class TopicosListView(TemplateView):

    template_name = 'topicos_list.html'
    # model = Postagem
    paginate_by = 20
    ordering = 'identificacao', 'cadastrador',

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tópicos'
        return context
    
class TopicoPostagensListView(TemplateView):

    template_name = 'topico_postagens_list.html'
    # model = Postagem
    paginate_by = 20
    ordering = 'identificacao', 'cadastrador',

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Postagens'
        return context