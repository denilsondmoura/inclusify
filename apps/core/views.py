from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.html import strip_tags
from django.views.generic import (
    FormView,
    ListView, CreateView, UpdateView,
    TemplateView, DetailView, DeleteView, 
)
from .models import Postagem, Topico, Comentario
from .forms import PostagemForm


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
        queryset = super().get_queryset().order_by('-created_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recentes'
        return context

class PostagemCreateView(LoginRequiredMixin, CreateView):
    model = Postagem
    form_class = PostagemForm
    template_name = "postagem_form.html"
    success_url = reverse_lazy('postagens_recentes_list')

    def form_valid(self, form):
        # TODO: Adicionar essa validação de tags e attrs aceitos
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        return response 
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Criar nova postagem'
        return context
    
class PostagemDetailView(DetailView):

    template_name = 'postagem_detail.html'
    model = Postagem

    
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
        queryset = queryset.filter(topicos=topico)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        topico = Topico.objects.get(pk=pk)
        
        context['title'] = f'Postagens sobre {topico}'
        return context
    
@login_required   
def responder_postagem(request, pk):
    if request.method == 'POST':
        postagem_id = pk
        conteudo = request.POST.get('conteudo')
        
        # TODO: Adicionar essa validação de tags e attrs aceitos
        # Validação básica (remova tags não permitidas se necessário)
        # conteudo_seguro = strip_tags(conteudo, allowed_tags=['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'a'])
        
        Comentario.objects.create(
            created_by=request.user,
            conteudo=conteudo,
            postagem_id=postagem_id
        )
        
        messages.success(request, 'Resposta enviada com sucesso!')
        return redirect('postagem_detail', pk)
    
    return redirect('postagem_detail', pk)

@login_required
def responder_comentario(request, pk, comentario_id):
    if request.method == 'POST':
        postagem_id = pk
        parent_id = comentario_id
        conteudo = request.POST.get('conteudo')
        
        # TODO: Adicionar essa validação de tags e attrs aceitos
        # Validação básica (remova tags não permitidas se necessário)
        # conteudo_seguro = strip_tags(conteudo, allowed_tags=['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'a'])
        
        Comentario.objects.create(
            created_by=request.user,
            conteudo=conteudo,
            parent_comment_id=parent_id,
        )
        
        messages.success(request, 'Resposta enviada com sucesso!')
        return redirect('postagem_detail', pk)
    
    return redirect('postagem_detail', pk)
