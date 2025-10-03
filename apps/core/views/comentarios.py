from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden
from ..models import Postagem, Comentario, VotoComentario, VotoPostagem
from ..forms import ComentarioForm
 
    
@login_required
@require_http_methods(["POST"])
def responder_comentario(request, pk, comentario_id):
    parent_id = comentario_id
    conteudo = request.POST.get('conteudo')
    
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
