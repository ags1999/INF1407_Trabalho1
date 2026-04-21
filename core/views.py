import os
import requests
from core.models import Livro
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin


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