from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (RandomQuoteView, AddQuoteView,
                    LikeDislikeView,
                    TopQuotesView, SourceListView,
                    RegisterView)

urlpatterns = [
    path('', RandomQuoteView.as_view(), name='random_quote'),
    path('add/', AddQuoteView.as_view(), name='add_quote'),
    path('like-dislike/<int:quote_id>/<str:action>/',
         LikeDislikeView.as_view(), name='like_dislike'),
    path('top/', TopQuotesView.as_view(), name='top_quotes'),
    path('sources/', SourceListView.as_view(), name='source_list'),
    path('sources/<int:source_id>/', SourceListView.as_view(), name='source_detail'),
    path('accounts/register/', RegisterView.as_view(template_name='register.html'), name='register'),
    path('accounts/', include('django.contrib.auth.urls'))
]

