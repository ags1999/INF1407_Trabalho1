
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "core"

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Página Inicial (Home)
    path('', views.HomeView.as_view(), name='home'),
    # Caminho explicito
    path('home/', views.HomeView.as_view(), name='home'),

    path('search/', views.SearchView.as_view(), name='busca'),

    path('save-book/', views.SaveBookView.as_view(), name='save_book'),

    path('remove-book/<int:pk>/', views.RemoveBookView.as_view(), name='remove_book'),

    path('register/', views.RegisterView.as_view(), name='register'),

    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),

    path('update-notes/<int:pk>/', views.UpdateNotesView.as_view(), name='update_notes'),

    path('password-reset/', views.MyPasswordResetView.as_view(), name='password_reset'),

    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('password-change/', views.MyPasswordChangeView.as_view(), name='password_change'),


]