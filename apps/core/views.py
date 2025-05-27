from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Count, F, Q, ExpressionWrapper, FloatField
from django.db.models.functions import Now, Extract
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.html import strip_tags
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Postagem, Topico, Comentario, VotoComentario, VotoPostagem
from .forms import PostagemForm, ComentarioForm


class PostagensRelevantesListView(ListView):

    template_name = 'postagens_relevantes_list.html'
    model = Postagem
    paginate_by = 10

    def get_queryset(self):
        gravidade = 2.2  # Aumenta o decaimento
        peso_votos = 2  # Reduz influência dos votos
        peso_comentarios = 1.5

        
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            # Calcula horas desde a criação corretamente
            horas_desde_criacao=ExpressionWrapper(
                Extract(Now() - F('created_at'), 'epoch') / 3600,
                output_field=FloatField()
            ),
            # Conta total de comentários associados
            total_comentarios=Count('comentarios', distinct=True),
            # Conta votos positivos e negativos
            votos_positivos=Count('votos', filter=Q(votos__valor=1), distinct=True),
            votos_negativos=Count('votos', filter=Q(votos__valor=-1), distinct=True)
        ).annotate(
            # Cálculo da relevância
            relevancia=ExpressionWrapper(
                (
                    ((F('votos_positivos') - F('votos_negativos')) * peso_votos +
                    F('total_comentarios') * peso_comentarios) 
                    /
                    ((F('horas_desde_criacao') + 2) ** gravidade)
                ),
                output_field=FloatField()
            )
        ).order_by('-relevancia')

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
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Postagem criada com sucesso!')
        return response 
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Criar nova postagem'
        return context

class PostagemUpdateView(LoginRequiredMixin,
                         UserPassesTestMixin,
                         UpdateView):
    model = Postagem
    form_class = PostagemForm
    template_name = "postagem_form.html"

    def test_func(self):
        postagem = self.get_object()
        return postagem.created_by == self.request.user

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        messages.success(self.request, 'Postagem alterada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar postagem'
        return ctx
    
    def get_success_url(self):
        return reverse('postagem_detail', args=[self.object.id])
    
class PostagemDetailView(DetailView):

    template_name = 'postagem_detail.html'
    model = Postagem

    
class TopicosListView(ListView):

    template_name = 'topicos_list.html'
    model = Topico
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            postagens_count=Count('postagens', distinct=True)
        ).order_by('-postagens_count')
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
        queryset = queryset.filter(topicos=topico).order_by('-created_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        topico = Topico.objects.get(pk=pk)
        
        context['title'] = f'Postagens sobre {topico}'
        return context
    
@login_required   
@require_http_methods(["POST"])
def responder_postagem(request, pk):
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
    
@login_required
@require_http_methods(["POST"])
def responder_comentario(request, pk, comentario_id):
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

@login_required
@require_http_methods(["POST"])
def editar_comentario(request, pk, comentario_id):
    postagem = get_object_or_404(Postagem, pk=pk)
    comentario = get_object_or_404(Comentario, pk=comentario_id)

    if comentario.created_by != request.user:
        messages.error(request, 'Você não tem permissão para editar este comentário.')
        return HttpResponseForbidden("Você não tem permissão para editar este comentário.")

    form = ComentarioForm(request.POST, instance=comentario)
    if form.is_valid():
        form.save()
        messages.success(request, 'Comentário editado com sucesso!')
        return redirect(reverse('postagem_detail', args=[postagem.id]))
    

    # Renderiza o template (pode ser um partial que retorna só o fragmento do comentário)
    return render(request, 
                  'partials/postagem_button_group.html',  # ou outro template de edição
                  {
                      'form': form,
                      'comentario': comentario,
                  })

@login_required
def deletar_comentario(request, pk, comentario_id):
    postagem = get_object_or_404(Postagem, pk=pk)
    comentario = get_object_or_404(Comentario, pk=comentario_id)

    if request.method == 'POST':
        if comentario.created_by != request.user:
            messages.error(request, 'Você não tem permissão para excluir este comentário.')
            return HttpResponseForbidden("Você não tem permissão para excluir este comentário.")
        
        comentario.delete()
        messages.success(request, 'Comentário excluído com sucesso!')
        return redirect(reverse('postagem_detail', args=[postagem.id]))
    return HttpResponseForbidden()

@login_required
def deletar_postagem(request, pk):
    postagem = get_object_or_404(Postagem, pk=pk)

    if request.method == 'POST':
        if postagem.created_by != request.user:
            messages.error(request, 'Você não tem permissão para excluir esta postagem.')
            return HttpResponseForbidden("Você não tem permissão para excluir esta postagem.")
        
        postagem.delete()
        messages.success(request, 'Postagem excluída com sucesso!')
        return redirect(reverse('postagens_recentes_list'))
    return HttpResponseForbidden()


@login_required
@require_http_methods(["GET"])  # Garante que só aceita GET
def voto_postagem(request, pk, voto):
    # Validação do valor do voto
    if voto not in ['-1', '+1']:  # Assumindo que -1 é voto negativo e 1 positivo
        messages.error(request, 'Valor de voto inválido!')
        return redirect('postagem_detail', pk=pk)
    
    # Verifica se a postagem existe
    postagem = get_object_or_404(Postagem, pk=pk)
    
    try:
        # Tenta obter o voto existente
        voto_obj, created = VotoPostagem.objects.get_or_create(
            created_by=request.user,
            postagem=postagem,
            defaults={'valor': voto}
        )
        
        if not created:
            if voto_obj.valor == int(voto):
                messages.warning(request, 'Você já votou nesta postagem com o mesmo valor!')
            else:
                voto_obj.valor = voto
                voto_obj.save()
                messages.success(request, 'Seu voto foi atualizado com sucesso!')
        else:
            messages.success(request, 'Voto registrado com sucesso!')
            
    except Exception as e:
        # Log do erro (em produção, usar logging)
        print(f"Erro ao processar voto: {e}")
        messages.error(request, 'Ocorreu um erro ao processar seu voto.')
    
    return redirect('postagem_detail', pk=postagem.pk)

@login_required
@require_http_methods(["GET"])  # Garante que só aceita GET
def voto_comentario(request, pk, comentario_id, voto):
    # Validação do valor do voto
    if voto not in ['-1', '+1']:  # Assumindo que -1 é voto negativo e 1 positivo
        messages.error(request, 'Valor de voto inválido!')
        return redirect('postagem_detail', pk=pk)
    
    # Verifica se a postagem existe
    postagem = get_object_or_404(Postagem, pk=pk)
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    
    try:
        # Tenta obter o voto existente
        voto_obj, created = VotoComentario.objects.get_or_create(
            created_by=request.user,
            comentario=comentario,
            defaults={'valor': voto}
        )
        
        if not created:
            if voto_obj.valor == int(voto):
                messages.warning(request, 'Você já votou neste comentário com o mesmo valor!')
            else:
                voto_obj.valor = voto
                voto_obj.save()
                messages.success(request, 'Seu voto foi atualizado com sucesso!')
        else:
            messages.success(request, 'Voto registrado com sucesso!')
            
    except Exception as e:
        # Log do erro (em produção, usar logging)
        print(f"Erro ao processar voto: {e}")
        messages.error(request, 'Ocorreu um erro ao processar seu voto.')
    
    return redirect('postagem_detail', pk=postagem.pk)
