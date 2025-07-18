from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (RandomQuoteView, AddQuoteView,
                   AddSourceView, LikeDislikeView,
                   TopQuotesView, SourceListView,
                    RegisterView)

urlpatterns = [
    path('', RandomQuoteView.as_view(), name='random_quote'),
    path('add/', AddQuoteView.as_view(), name='add_quote'),
    path('add-source/', AddSourceView.as_view(), name='add_source'),
    path('like-dislike/<int:quote_id>/<str:action>/',
         LikeDislikeView.as_view(), name='like_dislike'),
    path('top/', TopQuotesView.as_view(), name='top_quotes'),
    path('sources/', SourceListView.as_view(), name='source_list'),
    path('sources/<int:source_id>/', SourceListView.as_view(), name='source_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]