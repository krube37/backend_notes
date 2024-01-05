from django.urls import path
from . import views

urlpatterns = [
    path('auth/signup', views.signup, name='signup'),
    path('auth/login', views.login, name='login'),
    path('notes/', views.note_list, name='note-list'),
    path('notes/<int:pk>/', views.note_detail, name='note-detail'),
    path('notes/<int:pk>/share/', views.share_note, name='share-note'),
]
