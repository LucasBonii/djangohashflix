from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Homepage(FormView):
    template_name =  "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
                return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta') + f'?email={email}'

class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme

    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.qtd_views += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context= super(Detalhesfilme, self).get_context_data(**kwargs)
        context['filmes_relacionados'] = Filme.objects.filter(categoria = self.get_object().categoria)[0:5]
        return context
    

class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo = self.request.GET.get('query')
        if termo:
            object_list = self.model.objects.filter(titulo__icontains=termo)
            return object_list
        else:
            return None
        


class Perfil(LoginRequiredMixin ,UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    fields = ['first_name', 'last_name', 'username', 'email']

    def get_success_url(self):
      return reverse('filme:homefilmes')
    

    def dispatch(self, request, *args, **kwargs):
    # Obtenha o usuário atualmente autenticado
        user = request.user
        # Obtenha o ID do usuário que está tentando editar o perfil
        profile_user_id = self.kwargs['pk']
        if user.id != profile_user_id:
            # Se não forem os mesmos, retorne uma resposta de acesso negado
            return HttpResponseForbidden("Você não tem permissão para acessar este perfil.")
        # Se forem os mesmos, prossiga com o processamento normal
        return super().dispatch(request, *args, **kwargs)
    
    

class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class =  CriarContaForm

    def get_initial(self):
        initial = super().get_initial()
        email = self.request.GET.get('email')
        if email:
            initial['email'] = email
        return initial

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('filme:login')
    