from django.shortcuts import render
from django.views.generic import (
    FormView,
    ListView, CreateView, UpdateView,
    TemplateView, DetailView, DeleteView,
)


class HomeView(TemplateView):

    template_name = 'home.html'
    # model = AreaGeral
    paginate_by = 20
    ordering = 'identificacao', 'cadastrador',

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context