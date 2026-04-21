from django.http import HttpResponse
from django.shortcuts import render
from core.models import Livro
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
     return HttpResponse("Hello, world. You're at the core index.")

#class HomeView(LoginRequiredMixin,View):
class HomeView(View):
     def get(self, request, *args, **kwargs):
          return render(request, 'core/home.html')

#class LoginView(View):
#     def get(self, request, *args, **kwargs):
#          return render(request, 'core/login.html')