import os
import requests
from core.models import Livro
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class LoginView(View):
     def get(self, request, *args, **kwargs):
          return render(request, 'core/login.html')

class HomeView(LoginRequiredMixin,View):
     def get(self, request, *args, **kwargs):
          query = request.GET.get('busca_livro')

          if query:
               # If there is a search, return the SearchView render
               return SearchView.as_view()(request, *args, **kwargs)

          livros = Livro.objects.filter(user=request.user).order_by('-date_added')
          print(request)

          context = {
               'livros': livros
          }
          return render(request, 'core/home.html', context)


class SearchView(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
          query = request.GET.get('busca_livro')
          livros_resultados = []
          error_message = None  # Initialize error message

          if query:
               api_key = os.getenv("GBOOKS_API_KEY")
               base_url = "https://www.googleapis.com/books/v1/volumes"
               params = {
                    'q': query,
                    'key': api_key,
                    'maxResults': 10
               }

               try:
                    response = requests.get(base_url, params=params)
                    response.raise_for_status()
                    data = response.json()

                    if "items" in data:
                         for item in data["items"]:
                              v_info = item.get("volumeInfo", {})
                              livro_data = {
                                   'google_volume_id': item.get('id'),
                                   'title': v_info.get('title', 'Título Desconhecido'),
                                   'author': ", ".join(v_info.get('authors', ['Autor Desconhecido'])),
                                   'cover_url': v_info.get('imageLinks', {}).get('thumbnail', '')
                              }
                              livros_resultados.append(livro_data)

               except requests.exceptions.HTTPError as e:
                    # Check specifically for 503 error
                    if e.response.status_code == 503:
                         error_message = "O serviço de busca está temporariamente indisponível (Erro 503). Por favor, tente novamente mais tarde."
                    else:
                         error_message = "Ocorreu um erro ao realizar a busca. Tente novamente."
                    print(f"Erro HTTP: {e}")
               except requests.exceptions.RequestException as e:
                    error_message = "Não foi possível conectar ao serviço de busca. Verifique sua conexão."
                    print(f"Erro na busca: {e}")

          context = {
               'livros': livros_resultados,
               'query': query,
               'error_message': error_message  # Pass the message to the context
          }
          return render(request, 'core/search.html', context)


class SaveBookView(LoginRequiredMixin, View):
     def post(self, request, *args, **kwargs):
          # Extract data from the POST request
          google_volume_id = request.POST.get('google_volume_id')
          title = request.POST.get('title')
          author = request.POST.get('author')
          cover_url = request.POST.get('cover_url')

          if google_volume_id:
               # Create the book associated with the current user
               # Use get_or_create to avoid duplicates based on the unique constraint
               livro, created = Livro.objects.get_or_create(
                    user=request.user,
                    google_volume_id=google_volume_id,
                    defaults={
                         'title': title,
                         'author': author,
                         'cover_url': cover_url
                    }
               )

               if created:
                    messages.success(request, f'"{title}" foi adicionado à sua lista!')
               else:
                    messages.info(request, f'"{title}" já está na sua lista.')

          # Redirect back to the home view or the previous search
          return redirect('core:home')


class RemoveBookView(LoginRequiredMixin, View):
     def post(self, request, pk, *args, **kwargs):
          # Get the book or return 404 if it doesn't exist
          # Filtering by user ensures a user can only delete their own books
          livro = get_object_or_404(Livro, pk=pk, user=request.user)
          title = livro.title
          livro.delete()

          messages.success(request, f'"{title}" foi removido da sua lista.')
          return redirect('core:home')

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('core:login')
    template_name = 'core/register.html'

    def form_valid(self, form):
        # Optional: Add a success message
        messages.success(self.request, "Conta criada com sucesso! Agora você pode fazer login.")
        return super().form_valid(form)